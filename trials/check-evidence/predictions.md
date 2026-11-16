# Predictions (written before DEV started)

Feature loop step "Predict". Compared with results in the retro.

- P1. DEV passes its own unit tests on the first PR: likely.
- P2. Holdouts on the first DEV attempt: 7 or 8 of 9. The likeliest misses
  are H4 (a `###` heading wrongly ending the section) and H5 (a duplicate
  also reported as `no proof`, or unstable sort order).
- P3. The TEST verifier finds at least one AC it can only mark UNPROVEN
  (most likely AC10's "Python 3.10+", since only 3.13 is installed here).
- P4. Wall time PRETEST to VERDICT: under 30 minutes.

Holdouts were checked against a throwaway reference implementation
(9/9) so a holdout failure points at the build, not the holdout.
