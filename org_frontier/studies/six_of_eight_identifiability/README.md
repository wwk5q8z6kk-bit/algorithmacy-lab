# Six-of-eight counterfactual identifiability

## Research question

Can six exactly observed transitions identify the causal IIT-4.0 whole-form classification of a three-party system? What is the minimum counterfactual-state intervention needed to identify the verdict, as distinguished from the full rules?

This is a small deterministic transition-rule identification test, complementary to q221's pairwise-recurrence identifiability work. The strict-mediation and relay control verdicts are existing lab findings; their recreation is not claimed as novel.

## How to run

Use Python >=3.10, install the root requirements as described in AGENTS.md, and run these commands **from the repository root**:

    python -m org_frontier.studies.six_of_eight_identifiability.experiment --structural --output org_frontier/studies/six_of_eight_identifiability/results_structural.json
    python -m pytest org_frontier/studies/six_of_eight_identifiability/test_experiment.py -q
    python -m org_frontier.classifier.validate
    python -m org_frontier.studies.six_of_eight_identifiability.experiment --exact --output org_frontier/studies/six_of_eight_identifiability/results_exact.json

The structural witness uses only the standard library. The exact mode uses the existing PyPhi/IIT-4.0 implementation and fails if that dependency is missing; it does not substitute an approximate formula.

## Models and observation protocol

The nodes W, S and C are Boolean. Both canonical models use W'=S and C'=S. The strict-mediation model has S'=W&C; the relay model has S'=W.

Those complete models agree on six input states: 000, 001, 010, 011, 101 and 111. These observed states are forward-invariant, meaning even unlimited trajectories initialized there cannot identify which reference model generated them.

The two missing rows are 100 and 110 (labels are W,S,C, not ordinary binary integers). The preregistered family keeps both W' and C' fixed globally and allows only S'(100)=a and S'(110)=b to vary. Exactly four deterministic completions fit the stipulated observational evidence.

The experiment exhaustively enumerates each completion, uses the existing exact-Φ classifier, reads the major complex, and searches all subsets of {100,110} for the minimum number of interventions that distinguish classification labels. It separately reports full-rule identification.

## Interpretation boundaries

A computational result is evidence about these Boolean models. It does not show the causal rules of a real organization. Counterfactual input states can be absent from all naturally observed trajectories, yet can affect the IIT result through the modeled causal dependencies. Setting those states by intervention may not be feasible outside simulation.

The hypothesis precommitment is in a separate earlier commit. Any exact-computation result should be committed only after actually running it. The original references' A/B outcomes are known controls, not blind confirmatory discoveries.

## Verified exact results (2026-10-17)

The fork's dedicated GitHub Actions run [39062046064](https://github.com/wwk5q8z6kk-bit/algorithmacy-lab/actions/runs/39062046064) completed the canonical validation, all 7 focused tests and all four exact IIT-4.0 computations. The four whole-system verdicts, in (a,b) order (00,01,10,11), are **triadic Φ=2.0; dyadic Φ=0.0; triadic Φ=2.0; dyadic Φ=0.0**. The single transition query at state 110 identifies the binary verdict for this family; both 100 and 110 are needed to identify every missing rule bit.

The model (a=1,b=0) returns (W,S) from the cross-state `major_complex` helper despite whole-system Φ=2.0. The completed exploratory audit shows that **three subsystems tie at Φ=2.0 at state 111**, including the full (W,S,C) system; see `results_ties_at_111.json`. The selected complex depends on state and tie selection, so it does not prove any excluded node is a spectator.

Reproduce all exact values using `python ci/reproduce.py six-of-eight-exact-verdicts` in the supported environment. Machine-readable results are committed in `results_exact.json`. The study remains in-silico. No Grokbot execution has been claimed.

See FINDINGS.md and GROKBOT_WORKFLOW.md for full interpretation, limits and authenticated attribution.

## Posthoc 64-completion stress test

The exploratory full-row analysis drops the assumed global W'/C' rules at the two unobserved inputs, allowing all eight possible next-state vectors for each missing row. All **64** completions remain observationally identical from the same six-state support.

Their exact-Φ outcomes are **48 triadic, 16 dyadic**; the full-range exact Φ is **0–2**. Crucially, **one intervention no longer identifies the verdict universally**. Both inputs 100 and 110 are required in the worst case. Querying 110 first resolves the verdict after one query in 48 of 64 model completions; the remaining cases require a second query at 100. This is a posthoc model-sensitivity finding, not evidence about real coordination.

Reproduce with:
```bash
python -m org_frontier.studies.six_of_eight_identifiability.exploratory_full_rows --exact
```
See [EXPLORATORY_64_PROTOCOL.md](EXPLORATORY_64_PROTOCOL.md), [results_exploratory_64.json](results_exploratory_64.json), and [FINDINGS.md](FINDINGS.md).

