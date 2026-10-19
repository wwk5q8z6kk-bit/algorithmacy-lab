"""Exploratory 64-completion extension of the six-of-eight identifiability study.

A separate, posthoc stress test that drops the assumption that unobserved
W' and C' follow globally known rules. It keeps all six observed rows fixed,
and exhaustively enumerates 8 x 8 assignments to the two unobserved rows.

Use the lab's exact PyPhi IIT-4.0 classifier, never a proxy.

Run from the root:
    python -m org_frontier.studies.six_of_eight_identifiability.exploratory_full_rows --structural
    python -m org_frontier.studies.six_of_eight_identifiability.exploratory_full_rows --exact
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path

from .experiment import ALL_STATES, LABELS, OBSERVED, UNOBSERVED, bits, label, observed_witness, rules


def model_id(out100: str, out110: str) -> str:
    return out100 + "_" + out110


def enumerate_completions() -> dict[str, dict[str, str]]:
    """64 distinct full transition maps, all consistent with six observed rows."""
    observed = observed_witness()
    models = {}
    for next100, next110 in product(ALL_STATES, repeat=2):
        transitions = dict(observed)
        transitions.update({"100": next100, "110": next110})
        assert set(transitions) == set(ALL_STATES)
        assert {transitions[s] for s in OBSERVED} <= set(OBSERVED)
        models[model_id(next100, next110)] = transitions
    assert len(models) == 64
    return models


def rule_functions(transitions: dict[str, str]):
    """Map full WSC transition table to the lab's per-node Boolean functions."""
    if set(transitions) != set(ALL_STATES):
        raise ValueError("A complete eight-row transition table is required")
    if any(value not in ALL_STATES for value in transitions.values()):
        raise ValueError("Invalid next-state vector")

    def make(j: int):
        def next_bit(state):
            return bits(transitions[label(state)])[j]
        return next_bit

    return tuple(make(j) for j in range(3))


def query_analysis(models: dict[str, dict[str, str]], verdicts: dict[str, str]):
    """Find global fixed query subsets identifying verdicts across all completions."""
    if set(models) != set(verdicts):
        raise ValueError("Each candidate requires an observed exact verdict")
    by_subset = []
    for k in range(len(UNOBSERVED) + 1):
        for subset in combinations(UNOBSERVED, k):
            grouped = defaultdict(list)
            for ident, transitions in models.items():
                signature = tuple(transitions[s] for s in subset)
                grouped[signature].append(ident)
            conflicting = []
            for sig, group in sorted(grouped.items()):
                labels = {verdicts[ident] for ident in group}
                if len(labels) > 1:
                    conflicting.append({
                        "outcome": list(sig),
                        "n_models": len(group),
                        "example_pair": [
                            next(i for i in group if verdicts[i] == "dyadic"),
                            next(i for i in group if verdicts[i] == "triadic"),
                        ],
                    })
            by_subset.append({
                "states": list(subset),
                "is_sufficient": not conflicting,
                "distinct_outcome_groups": len(grouped),
                "ambiguous_outcome_groups": len(conflicting),
                "models_in_ambiguous_groups": sum(item["n_models"] for item in conflicting),
                "ambiguity_witnesses": conflicting,
            })
    sufficient = [entry for entry in by_subset if entry["is_sufficient"]]
    if not sufficient:
        raise AssertionError("Both hidden-row queries must identify the model")
    min_k = min(len(entry["states"]) for entry in sufficient)
    return {
        "minimum_global_queries": min_k,
        "sufficient_minimal_query_sets": [
            entry["states"] for entry in sufficient if len(entry["states"]) == min_k
        ],
        "candidate_subsets": by_subset,
        "full_transition_table_requires_queries": 2,
    }


def structural():
    models = enumerate_completions()
    return {
        "analysis_type": "posthoc exploratory extension",
        "num_completions": len(models),
        "observed_support": list(OBSERVED),
        "unobserved_rows": list(UNOBSERVED),
        "unique_transition_tables": len({
            tuple(transitions[s] for s in ALL_STATES)
            for transitions in models.values()
        }),
        "reference_witnesses": {
            "strict_mediation": model_id("000", "101"),
            "relay": model_id("010", "111"),
        },
        "observed_rows": observed_witness(),
    }


def exact():
    try:
        from org_frontier.classifier.classifier import classify_rules
    except ImportError as e:
        raise RuntimeError("Lab PyPhi IIT-4.0 dependency unavailable") from e

    precheck_a = classify_rules(rules(0, 0), LABELS)
    precheck_b = classify_rules(rules(1, 1), LABELS)
    if precheck_a.structure != "triadic" or abs(precheck_a.max_phi - 2.0) > 1e-6:
        raise RuntimeError("Strict-mediation instrument control failed")
    if precheck_b.structure != "dyadic" or abs(precheck_b.max_phi) > 1e-9:
        raise RuntimeError("Relay instrument control failed")

    report = structural()
    models = enumerate_completions()
    verdicts = {}
    results = {}
    for ident, table in models.items():
        v = classify_rules(rule_functions(table), LABELS)
        verdicts[ident] = v.structure
        results[ident] = {
            "next_state_100": table["100"],
            "next_state_110": table["110"],
            "whole_system_phi": float(v.max_phi),
            "whole_system_verdict": v.structure,
            "n_reachable_states_scored": len(v.phi_profile),
        }
    controls = {
        model_id("000", "101"): ("triadic", 2.0),
        model_id("000", "111"): ("dyadic", 0.0),
        model_id("010", "101"): ("triadic", 2.0),
        model_id("010", "111"): ("dyadic", 0.0),
    }
    for ident, (cls, phi) in controls.items():
        value = results[ident]
        if value["whole_system_verdict"] != cls or abs(value["whole_system_phi"] - phi) > 1e-6:
            raise AssertionError(f"Original four-completion result changed: {ident}")
    counts = Counter(verdicts.values())
    if sum(counts.values()) != 64:
        raise AssertionError("Missing an exact outcome")

    diagnostics = query_analysis(models, verdicts)
    report["exact_iit_4"] = {
        "instrument": "lab classify_rules + PyPhi IIT-4.0",
        "verdict_counts": {"triadic": counts.get("triadic", 0), "dyadic": counts.get("dyadic", 0)},
        "phi_min": min(r["whole_system_phi"] for r in results.values()),
        "phi_max": max(r["whole_system_phi"] for r in results.values()),
        "models": results,
        "query_analysis": diagnostics,
    }
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    opts = ap.add_mutually_exclusive_group()
    opts.add_argument("--exact", action="store_true")
    opts.add_argument("--structural", action="store_true")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    report = exact() if args.exact else structural()
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")
    if args.exact:
        e = report["exact_iit_4"]
        q = e["query_analysis"]
        subsets = "+".join("/".join(s) for s in q["sufficient_minimal_query_sets"])
        print(
            "EXPLORATORY_64 total=64 triadic=%d dyadic=%d min_verdict_queries=%d:%s phi_min=%.6f phi_max=%.6f"
            % (e["verdict_counts"]["triadic"], e["verdict_counts"]["dyadic"],
               q["minimum_global_queries"], subsets, e["phi_min"], e["phi_max"])
        )
    else:
        print("EXPLORATORY_64_STRUCTURE total=64 unique=64 observed=6 hidden=2")


if __name__ == "__main__":
    main()
