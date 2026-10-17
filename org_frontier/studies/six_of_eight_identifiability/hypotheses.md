# Six-of-eight observational equivalence: analysis precommitment

**Status:** prospective for the *new four-completion exact-Φ screen*; the established strict-mediation and relay verdicts, and the six-state truth-table witness, are known before this commitment. This is an in-silico study, not empirical validation of organizations.

## Research question

When deterministic three-party coordination is observed only on a transition-closed six-state support, can the lab's full-system exact-IIT-4.0 binary verdict be identified? Which counterfactual transition queries suffice to identify the verdict, as distinct from the entire transition table?

## Fixed model

State order is `(W,S,C)` with labels in that order; each bit is 0 or 1. Synchronous update and little-endian state-index conventions follow the existing classifier.

Both models obey `W'=S` and `C'=S`. The mediator rules are:
- Model A: `S'=W & C` (known strict-mediation reference).
- Model B: `S'=W` (known relay reference).

The observed support is `O={000,001,010,011,101,111}`. The two unobserved states are `100` and `110`; these state labels mean W,S,C, not conventional most-significant-bit indexing.

**Primary admissible family:** Keep `W'=S`, `C'=S`, and every observed transition fixed. Independently assign `S'(100)=a`, `S'(110)=b`, for `a,b∈{0,1}`, producing four completions. No unknown other than these two mediator output bits is permitted in the primary family.

## Hypotheses and decisions

- **H1 (known witness; structural check):** Both references agree on all six observed transitions and O is forward-invariant. Refute on any differing observed row or trajectory escaping O.
- **H2 (known lab controls):** Model A is triadic and Model B dyadic under the lab's existing `classify_rules` convention. Refute if validated current instrument returns otherwise; report that as a control failure, not a new science result.
- **H3 (primary exact result):** The admissible four-completion family has both triadic and dyadic members. Null: all four yield the same binary verdict. Compute and report all four regardless of outcome.
- **H4 (diagnostic action):** Either transition query at 100 or 110 separates reference models A and B; neither query alone identifies both missing bits in the four-completion family. Refute if partition behavior disagrees.
- **H5 (verdict identification):** Compute minimum number of distinct state interventions in {100,110} whose deterministic next-state outcomes determine the *verdict* for every member of the four-completion family. Do not assume H5's answer equals the two interventions needed to identify both unknown rule bits.

## Methods and controls

Use `org_frontier.classifier.classifier.classify_rules` and `org_frontier.probes.lib.major_complex`, without implementing a Φ proxy. Run the repository's strict-mediation and relay control validation first. Enumerate all four completions in fixed order (a,b)=(0,0),(0,1),(1,0),(1,1). Compute exact verdicts and major complexes using identical state conventions; do not cherry-pick.

Construct observation signatures from the next-state values at each queried hidden state. Enumerate all subsets of {100,110} in increasing cardinality and lexicographic order. A query subset identifies the verdict iff no two models sharing its observation signature disagree in verdict. It identifies the full TPM iff all models have distinct signatures.

**Decision rule:** classify H3 supported iff there are at least two distinct binary verdicts. H5 is the exact minimum subset cardinality by exhaustive search, with ties reported. Report errors and uncertainty without inferring an uncomputed value.

## Controls and limitations

Verify the complete truth table directly, observed-trajectory equality (from every O state), closure of O, and invariance across long horizons. Distinguish state reachability from interventionally queryable states. Do not equate the resulting logic proof with evidence from a real organization. No new human or biomedical evidence is included.

## External prior work

This small deterministic identification test complements, and does not supersede, the separate q221 draft on identifiability of pairwise cross-recurrence summaries. The difference is uncertainty about *unobserved transition-rule entries* and exact Φ, not ambiguity of recurrence statistics when complete stochastic laws exist.

## Reporting

Commit this plan before implementing and running the new exact-completion screen. Preserve the plan; any deviations must be dated and explicit. Output all four configurations, numerics from the exact library, major complexes, identified minimal intervention sets, tests, and code provenance. Record unavailable compute as unavailable rather than fabricated.
