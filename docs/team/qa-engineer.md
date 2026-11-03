# QA Engineer Notes

QA checks finished work against the GitHub issue. QA does not fix the code and does not close an issue before writing a verdict.

## QA process
1. Read the issue and every acceptance criterion.
2. Run the relevant automated tests.
3. Test the feature in the running app when possible.
4. Check normal behavior and important invalid or edge cases.
5. If an app bug is found during manual use, create a separate issue with the `user-test-bug` label. Include Goal, Description, steps to reproduce, expected result, actual result, and environment.
6. Comment on the original issue with PASS or FAIL and say which commands and manual checks were run.
7. Close the issue only if the verdict is PASS.

## PASS comment format
```md
## QA: PASS

- [x] Acceptance criterion 1 — PASS
- [x] Acceptance criterion 2 — PASS

Tests: `command used`, N passed, 0 failed
Manual checks: brief description of the checked user flow
Code changes by QA: none
```

## FAIL comment format
```md
## QA: FAIL

- [x] Acceptance criterion 1 — PASS
- [ ] Acceptance criterion 2 — FAIL: what I did and what happened

Tests: `command used`, result
Manual checks: brief description and reproduction details
Code changes by QA: none
```

Do not trust a description that claims the feature works. Check the acceptance criteria against the running code.
