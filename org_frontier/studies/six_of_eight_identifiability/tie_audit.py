"""Exploratory audit of equal-max Phi subsystem candidates at state 111.

Executed after the preregistered exact four-model test. Do not conflate
whole-system Phi, selected major-complex membership, or all tied subsystem SIAs.
Run from repository root:
    python -m org_frontier.studies.six_of_eight_identifiability.tie_audit
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def run_audit():
    import pyphi
    from pyphi import new_big_phi
    from org_frontier.classifier.classifier import tpm_from_rules, cm_from_rules
    from org_frontier.studies.six_of_eight_identifiability.experiment import (
        LABELS, COMPLETIONS, name, rules,
    )

    report = {
        "scope": "exploratory posthoc subsystem SIA tie audit at state (1,1,1)",
        "method": "PyPhi IIT-4.0 new_big_phi.all_complexes, without Φ approximation",
        "models": {},
    }
    for a, b in COMPLETIONS:
        funcs = rules(a, b)
        net = pyphi.Network(
            tpm_from_rules(funcs), cm=cm_from_rules(funcs), node_labels=LABELS
        )
        state = (1, 1, 1)
        candidates = []
        for sia in new_big_phi.all_complexes(net, state):
            phi = float(sia.phi)
            if phi <= 1e-9:
                continue
            indices = tuple(sia.node_indices)
            candidates.append({
                "nodes": [LABELS[i] for i in indices],
                "phi": phi,
            })
        peak = max((item["phi"] for item in candidates), default=0.0)
        tied = [
            item for item in candidates if abs(item["phi"] - peak) <= 1e-9
        ]
        chosen = new_big_phi.maximal_complex(net, state)
        report["models"][name(a, b)] = {
            "peak_subsystem_phi": peak,
            "highest_phi_subsystems": tied,
            "selected_major_complex": [
                LABELS[i] for i in getattr(chosen, "node_indices", ())
            ],
            "all_positive_phi_subsystems": candidates,
        }
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    report = run_audit()
    result = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    print(result, end="")
    sizes = [len(report["models"][key]["highest_phi_subsystems"])
             for key in ("a0_b0", "a0_b1", "a1_b0", "a1_b1")]
    print("TIE_AUDIT_111 " + " ".join(
        "%s=%d" % (k, n)
        for k, n in zip(("a0_b0", "a0_b1", "a1_b0", "a1_b1"), sizes)
    ))


if __name__ == "__main__":
    main()
