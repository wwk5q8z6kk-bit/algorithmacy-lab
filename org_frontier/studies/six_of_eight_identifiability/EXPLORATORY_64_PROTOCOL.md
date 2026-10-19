# Exploratory full-row counterfactual-completion stress test

**Status:** posthoc, motivated by the confirmed four-completion result and its global `W'=S`, `C'=S` restriction. This document is committed **before** the new 64-completion exact-Φ computation, but does **not** convert the extension into an independently preregistered confirmatory study. The original `hypotheses.md` and original results remain unchanged.

## Question

Does the primary study's one-intervention identification rule (query input 110) survive after dropping the unsupported assumption that the non-mediator outputs at unobserved inputs 100 and 110 follow known functions?

## Model family

Hold fixed all six fully observed transition rows and their forward-invariant support O. Permit each of the two **unobserved complete next-state vectors** to be *any* three-bit vector in {000,001,010,011,100,101,110,111}. Enumerate 8² = 64 full deterministic TPM completions in lexical order.

This family strictly includes the original four rule completions. Every model must preserve all six observed transitions and every trajectory beginning in O, irrespective of differences outside O. No human/organizational data are claimed.

## Method fixed before the extension

1. Verify the six observed transitions and closure of O on all 64 completions.
2. Reuse the existing lab exact PyPhi/IIT-4.0 classifier on all 64 complete TPMs (no approximations, no learned proxy).
3. For every completion, record the transition outputs at both hidden states, its whole-form Φ_MIP maximum and its dyadic/triadic verdict.
4. Report the counts of each binary verdict and the range of exact Φ across the 64 models. These counts are descriptive, not estimates of population frequency.
5. Exhaustively evaluate intervention subsets {}, {100}, {110}, {100,110}. An intervention subset *identifies the verdict* if every completion with the same outcomes at the queried states has the same verdict. Report the smallest globally sufficient subset(s). State interventions are assumed perfectly settable and their full next-state bit vector observable.
6. For each single-intervention candidate, count the number of outcome classes containing conflicting verdicts; show at least one explicit witness pair if ambiguity exists.
7. Verify whether the original four candidate completions occur with their original exact classifications; do not change those results.
8. Repeat the canonical instrument validation and file-local tests before reporting results.

## Expectations and falsifiers (exploratory, not confirmatory)

The four-model inference `110 ⇒ whole-form verdict` may be contingent on known non-mediator rules. The key outcome is whether the 64-model family retains or loses that identification. A single-query result is refuted for the expanded family if any two completions share the queried next-state outcome yet have different exact verdicts.

Whether zero, one, or both queries suffice is left open; choose by enumeration. Do not assert or write a numeric result until the exact computation has actually run.

## Interpretation

The 64 completions are deliberately broad, because the six observed transition rows do not determine unobserved outputs. Not all completions are plausible for any given organization. The goal is **logical identifiability under precisely stated assumptions** and sensitivity of the measurement claim to relaxing the originally assumed causal rules. It does not create empirical evidence or validate IIT as a social-scientific construct.
