---
name: code-change-verification
description: Use after repo-tracked code or docs change and local verification must be selected, run, or reported before review or handoff.
---

## Goal

Choose the smallest useful verification path, run it, and report exact results.

## Steps

1. Map changed files to checks.
2. Run targeted checks first.
3. Run `make verify-fast` before PR, push, or broad handoff.
4. Report commands, pass/fail result, and skipped checks.

## Do not

- Do not imply a check passed if it was not run.
- Do not skip `make verify-fast` before a CI-triggering push.
