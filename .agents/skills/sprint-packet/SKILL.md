---
name: sprint-packet
description: Use when accepted scope needs to become an implementation-ready sprint packet.
---

## Goal

Convert accepted scope into sprintctl state with clear deliverables and verification.

## Steps

1. Confirm the work is not already represented in live `sprintctl` state.
2. Draft goal, scope, out-of-scope, dependencies, deliverables, acceptance, and
   verification.
3. Load `.envrc`.
4. Register the sprint:
   `sprintctl sprint create --name "<name>" --goal "<goal>" --start <YYYY-MM-DD> --status active --kind active_sprint`.
5. Add deliverables with `sprintctl item add --sprint-id <id> --track <track> --title "<title>"`.
6. Render the shared snapshot with `make snapshot-refresh`.

## Do not

- Do not hide unresolved product questions as implementation items.
- Do not use a home-directory sprintctl DB.
