"""Six-of-eight Boolean counterfactual-identifiability experiment.

Run from the repository root:
 python -m org_frontier.studies.six_of_eight_identifiability.experiment --structural
 python -m org_frontier.studies.six_of_eight_identifiability.experiment --exact

Structural mode is standard-library-only; exact mode uses the existing IIT-4.0
classifier. It deliberately never substitutes a proxy for exact Phi.
"""
from __future__ import annotations

import argparse
from itertools import product, combinations
from pathlib import Path
import json

LABELS = ("W", "S", "C")
OBSERVED = ("000", "001", "010", "011", "101", "111")
UNOBSERVED = ("100", "110")
ALL_STATES = tuple("".join(p) for p in product("01", repeat=3))
COMPLETIONS = tuple(product((0, 1), repeat=2))


def bits(s):
    if len(s) != 3 or any(x not in "01" for x in s):
        raise ValueError("Invalid WSC state: " + repr(s))
    return tuple(map(int, s))


def label(s):
    v = tuple(s)
    if len(v) != 3 or any(x not in (0, 1) for x in v):
        raise ValueError("Not three Boolean bits")
    return "".join(map(str, v))


def mediator(x, a, b):
    w, s, c = x
    return (a if s == 0 else b) if w == 1 and c == 0 else (w & c)


def rules(a, b):
    if a not in (0, 1) or b not in (0, 1):
        raise ValueError("The two missing outputs must be Boolean")
    return (
        lambda x: int(x[1]),
        lambda x: mediator(x, a, b),
        lambda x: int(x[1]),
    )


def step(s, a, b):
    x = bits(s)
    return label(f(x) for f in rules(a, b))


def trajectory(s, a, b, horizon=25):
    if horizon < 0:
        raise ValueError("Negative horizon")
    run = [s]
    for _ in range(horizon):
        run.append(step(run[-1], a, b))
    return tuple(run)


def name(a, b):
    return "a%d_b%d" % (a, b)


def observed_witness():
    rows = {s: step(s, 0, 0) for s in OBSERVED}
    assert len(rows) == 6
    assert set(rows.values()) <= set(OBSERVED)
    for a, b in COMPLETIONS:
        for s in OBSERVED:
            assert step(s, a, b) == rows[s]
            assert trajectory(s, a, b, 50) == trajectory(s, 0, 0, 50)
    return rows


def signatures(queries):
    queries = tuple(queries)
    if len(set(queries)) != len(queries) or any(q not in UNOBSERVED for q in queries):
        raise ValueError("Queries must be distinct unobserved states")
    return {name(a, b): tuple(step(q, a, b) for q in queries) for a, b in COMPLETIONS}


def minimum_queries(classes):
    names = {name(a, b) for a, b in COMPLETIONS}
    if set(classes) != names:
        raise ValueError("All four completion labels are required")
    for k in range(len(UNOBSERVED) + 1):
        winners = []
        for qs in combinations(UNOBSERVED, k):
            seen = {}
            valid = True
            for model, signature in signatures(qs).items():
                if signature in seen and seen[signature] != classes[model]:
                    valid = False
                    break
                seen[signature] = classes[model]
            if valid:
                winners.append(list(qs))
        if winners:
            return {"minimum_queries": k, "query_sets": winners}
    raise AssertionError("Complete intervention panel did not identify labels")


def structural():
    rows = observed_witness()
    completions = {
        name(a, b): {
            "at_100": step("100", a, b),
            "at_110": step("110", a, b),
            "reachable_states": sorted({step(s, a, b) for s in ALL_STATES}),
        }
        for a, b in COMPLETIONS
    }
    for s in UNOBSERVED:
        assert step(s, 0, 0) != step(s, 1, 1)
    return {
        "basis": "synthetic deterministic Boolean rules, no field observations",
        "state_order": "WSC (classifier bit index W=0,S=1,C=2)",
        "observed_rows": rows,
        "unobserved_states": list(UNOBSERVED),
        "four_completions": completions,
        "full_rule_identification": minimum_queries({k: k for k in completions}),
        "A_B_distinguishing_interventions": [s for s in UNOBSERVED if step(s, 0, 0) != step(s, 1, 1)],
    }


def exact():
    try:
        from org_frontier.classifier.classifier import classify_rules
        from org_frontier.probes.lib import major_complex
    except ImportError as exc:
        raise RuntimeError("Exact Phi unavailable: run with the lab's IIT-4.0 dependencies") from exc
    report = structural()
    control_a = classify_rules(rules(0, 0), LABELS)
    control_b = classify_rules(rules(1, 1), LABELS)
    if control_a.structure != "triadic" or abs(control_a.max_phi - 2.0) > 1e-6:
        raise RuntimeError("Strict-mediation instrument control failed: " + str(control_a))
    if control_b.structure != "dyadic" or abs(control_b.max_phi) > 1e-9:
        raise RuntimeError("Relay instrument control failed: " + str(control_b))
    outcomes = {}
    classes = {}
    for a, b in COMPLETIONS:
        k = name(a, b)
        result = classify_rules(rules(a, b), LABELS)
        nodes, complex_phi = major_complex(rules(a, b), LABELS)
        classes[k] = result.structure
        outcomes[k] = {
            "verdict": result.structure,
            "max_phi": float(result.max_phi),
            "max_phi_state": list(result.mip_state) if result.mip_state else None,
            "mip_partition": result.mip_partition,
            "phi_profile": [{"state": list(s), "phi": float(p)} for s, p in result.phi_profile],
            "major_complex": list(nodes) if nodes else [],
            "major_complex_phi": float(complex_phi) if nodes else None,
        }
    report["exact_iit_4"] = {
        "instrument": "org_frontier.classifier.classifier.classify_rules; PyPhi IIT 4.0",
        "models": outcomes,
        "verdict_identified_by_observation_alone": len(set(classes.values())) == 1,
        "minimum_queries_to_identify_verdict": minimum_queries(classes),
        "known_A_control_phi": float(control_a.max_phi),
        "known_B_control_phi": float(control_b.max_phi),
    }
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    opts = p.add_mutually_exclusive_group()
    opts.add_argument("--structural", action="store_true")
    opts.add_argument("--exact", action="store_true")
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    report = exact() if args.exact else structural()
    result = json.dumps(report, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    print("SIX_OF_EIGHT_OBSERVED=6 HIDDEN=2 COMPLETIONS=4 SUPPORT_INVARIANT=TRUE")
    print(result, end="")


if __name__ == "__main__":
    main()
