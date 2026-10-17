# Findings — six-of-eight counterfactual identifiability

## Verified structural witness

Six observed transitions are:
- 000→000
- 001→000
- 010→101
- 011→101
- 101→010
- 111→111

The observed support is forward-invariant. Four admissible deterministic completions generate the same trajectories from every observed state. The alternatives disagree only at the two missing rows (100 and 110).

For strict mediation, the counterfactual rows are 100→000 and 110→101. For relay, they are 100→010 and 110→111. Either query distinguishes these two reference models. To identify the **full transition table** among all four completions, both state interventions are necessary and sufficient.

## Exact IIT-4.0 results

NOT YET COMPUTED in this execution environment. PyPhi is not installed locally and installing it is blocked by container network restrictions. The preregistered four-model exact computation, major complexes and minimum number of queries required to identify the **verdict only** remain to be executed using the repository's PyPhi environment. No exact numeric values for the two mixed-rule completions are claimed.

## Initial tests

The corresponding pure-Python locally executed implementation passed six structural tests, with one PyPhi-gated integration test skipped. The committed branch's test module should be rerun in the supported environment. No upstream CI success is claimed.

## Limits and relationship to prior work

Constructed deterministic Boolean rules; no field data or organizational inference. The causal rules outside observable support are not established by the observational trajectories. The strict-mediation and relay verdicts were known before the preregistration. The separate q221 draft addresses a different identifiability question about pairwise recurrence profiles.
