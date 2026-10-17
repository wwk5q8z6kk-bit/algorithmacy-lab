# Six-of-eight: results and identification boundary

## Source and execution

The exact four-completion analysis was run on GitHub Actions using the lab's existing PyPhi IIT-4.0 classifier and major-complex implementation. The canonical instrument controls passed, the focused test suite passed (7 tests), and the structural CI reproduction check passed.

- **Execution:** https://github.com/wwk5q8z6kk-bit/algorithmacy-lab/actions/runs/39062046064
- **Results artifact:** `results_exact.json`, generated from that run; not manually invented numbers.
- **Runtime:** Python 3.12.15, PyPhi IIT-4.0 branch resolved to Git commit `b78d0e342d37175cbd55cf35a6d52ae035b4c50f`.
- **Pre-registration:** commit `e25e5be1c550779f288c23b170a59621775a9832`, made before the new four-completion outcome calculation.
- **Instrument:** `org_frontier.classifier.classifier.classify_rules` and `org_frontier.probes.lib.major_complex`.
- **Scope:** in-silico Boolean models, no observed organization or field evidence.

## Identical observations

Six observed transitions form an invariant support for every completion:

| Input (WSC) | Common next state |
|---|---|
| 000 | 000 |
| 001 | 000 |
| 010 | 101 |
| 011 | 101 |
| 101 | 010 |
| 111 | 111 |

All six-state trajectories are identical for all four completions regardless of observation horizon. The only unobserved inputs are 100 and 110.

## Exact Φ screen

Under the precommitted restriction that W'=S and C'=S globally, and only the two missing mediator outputs `a=S'(100)` and `b=S'(110)` vary:

| a | b | next(100) | next(110) | Max whole-system Φ_MIP | Whole-form verdict | Reported major complex | Complex Φ |
|---:|---:|---|---|---:|---|---|---:|
| 0 | 0 | 000 | 101 | 2.0 | triadic | (W,S,C) | 2.0 |
| 0 | 1 | 000 | 111 | 0.0 | dyadic | (W,S) | 2.0 |
| 1 | 0 | 010 | 101 | 2.0 | triadic | (W,S) | 2.0 |
| 1 | 1 | 010 | 111 | 0.0 | dyadic | (W,S) | 2.0 |

All reported whole-system Φ profiles over the four states reachable after one update are 0 at 000, 010 and 101; the maximal value is at 111 for the two triadic completions.

**H1:** CONFIRMED by Boolean enumeration (known structural witness).  
**H2:** CONFIRMED by existing strict-mediation (Φ 2.0) and relay (Φ 0.0) controls.  
**H3:** SUPPORTED: observationally compatible completions have different exact whole-system verdicts.  
**H4:** CONFIRMED: both 100 and 110 distinguish the two reference models.  
**H5:** The **single** intervention at 110 identifies the *binary whole-system verdict* over the four-model family. **Both** interventions 100 and 110 are required to identify the full TPM in the same family.

### Decision rule

With W'/C' globally fixed as preregistered, querying input state 110 distinguishes `b=0` (observed next state 101, **triadic**) from `b=1` (observed next state 111, **dyadic**). Querying 100 alone cannot identify the binary verdict.

This is identification conditional on the four-completion restriction; it is **not** a general one-intervention guarantee for arbitrary three-node TPMs.

### The major-complex caveat

The exact implementation returns the major complex (W,S) with Φ 2.0 for completion (a=1,b=0), even though its maximum whole-system Φ_MIP is also 2.0 and its whole-form classification is triadic.

This distinction must be reported: whole-system irreducibility, a selected maximum across all reachable states, and state-conditional maximal-complex membership are different outputs. The **posthoc exploratory tie audit** in `results_ties_at_111.json` enumerated all positive-Φ subsystems at state 111 with `pyphi.new_big_phi.all_complexes`.

At state **111**, models (0,0) and (1,0) each have **three equal-maximum Φ=2.0 subsystem analyses**: (W,S,C), (S,C), and (W,S). On those models at state 111, `new_big_phi.maximal_complex` selected (W,S,C). Yet the lab's `org_frontier.probes.lib.major_complex` helper, which selects the first strictly greatest maximal-complex Φ encountered **across reachable states**, returned (W,S) for model (1,0). This is a **state/tie-selection dependence of the reported major complex**, not proof that C is excluded by a uniquely defined maximal core. The posthoc result must remain distinct from the preregistered primary whole-form comparison.

For both dyadic whole-form models, (W,S) was the single top-Φ subsystem at state 111, with Φ=2.0. This reinforces that a nonzero proper-subsystem Φ does not establish whole-system triadicity.

## Interpretation and limitations

These exact calculations establish a structural **non-identifiability witness** for the stipulated Boolean family. Observational equivalence is a limitation of the sampled support, not a failure of the exact computation. The most informative missing transition is selected from the specific set of admissible models, not from data about real coordination.

An operational field protocol should report which counterfactual transitions are supported by evidence, what alternative rule completions remain admissible, whether exact-Φ verdicts disagree among them, and which feasible observation/intervention would resolve the disagreement.

An intervention into input state 110 may be impossible in a real system; absent such evidence, the empirical verdict remains unidentified.

The original A/B contrast is pre-existing lab knowledge. The extension here is an executable four-completion identification procedure and a concrete distinction between identifying a verdict and reconstructing all rules. The finding does not itself validate the construct for an organization, infer intentions, or establish clinical or social implications.

## Reproduction

From repository root, with the requirements installed:

```bash
export PYPHI_WELCOME_OFF=true
python -m org_frontier.classifier.validate
python -m pytest org_frontier/studies/six_of_eight_identifiability/test_experiment.py -q
python -m org_frontier.studies.six_of_eight_identifiability.experiment --exact
python ci/reproduce.py six-of-eight-observational-witness
```

The exact per-state outputs and model comparisons are in `results_exact.json` and the corresponding GitHub Actions run.
