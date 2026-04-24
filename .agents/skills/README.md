# Agent Skills

`.agents/skills/` is the repo-local source for workflow skills. Claude sessions may expose
these through `.claude/skills/` symlinks; Codex sessions can use the same files as local
workflow documentation.

Use `docs/runbooks/project-working-practices.md` to choose the right loop before opening a
skill.

- `sprint-packet`: turn accepted scope into a sprint-ready packet and register it.
- `sprint-resume`: resume an existing sprint item with claim checks.
- `sprint-snapshot`: render live sprint state to the committed snapshot.
- `item-done`: verify and close a finished sprint item.
- `kctl-extract`: extract and review sprint-close knowledge candidates.
- `code-change-verification`: choose and report verification for a change.
- `domain-impact-scan`: map source/evidence/lens/HLA impact for new scope.
- `pr-handoff-summary`: write a compact reviewer or handoff summary.
