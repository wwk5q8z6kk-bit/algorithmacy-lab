# Hackathon workflow and provenance — six-of-eight experiment

## Research objective

Demonstrate whether identical observations leave exact IIT-4.0 coordination classification underdetermined, and identify the minimum diagnostic counterfactual query.

## Recorded execution

- The study design and structural implementation were authored through a ChatGPT assistant. Six standard-library tests passed locally and one PyPhi-dependent test was skipped locally.
- The prerequisite preregistration was committed at `e25e5be1c550779f288c23b170a59621775a9832` before the new exact four-model screen.
- The ChatGPT assistant added a GitHub Actions workflow on the public fork and triggered it by a branch commit.
- **Actual exact computation:** GitHub Actions run https://github.com/wwk5q8z6kk-bit/algorithmacy-lab/actions/runs/39062046064, completed successfully.
- Environment: Python 3.12.15, PyPhi IIT-4.0 branch resolved to commit `b78d0e342d37175cbd55cf35a6d52ae035b4c50f`.
- The exact IIT instrument controls passed, **7** focused tests passed, and the named structural CI reproduction check passed.
- The exact results were copied into `results_exact.json` from the successful workflow run and interpreted in FINDINGS.md.

## Grokbot attribution

**No Grokbot execution has been recorded or claimed.** The hackathon requires actual Grokbot participation. To complete that requirement, point Grokbot at the branch and have it independently reproduce the exact output, audit the identifiability logic, optionally investigate tied major-complex membership, and document the actual invocation, actions, results, corrections and responsible human decisions.

Do not relabel ChatGPT's research and the GitHub runner's computation as Grokbot actions.

## Grokbot continuation checklist

1. Review the research precommitment and exact output independently.
2. Run the canonical controls and full exact four-model analysis in the lab environment.
3. Verify the one-intervention result (input 110) and the two-intervention full-TPM result.
4. Investigate whether equal whole-system Φ and (W,S) major-complex Φ in model (a=1,b=0) reflects ties in the lab's maximal-complex selection convention.
5. Independently reproduce the state-111 subsystem tie audit and the numeric manifest checks, run the full relevant tests, and update the study documentation from genuine receipts.
6. Record the actual Grokbot workflow, prompt, commands, changes, limitations and review outcome.
7. Prepare and submit the upstream PR to `contrib`, noting the model-only validation boundary.

Only record steps actually performed.
