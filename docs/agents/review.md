# Review Mode

## Purpose

Review stable work for bugs, regressions, missing tests, and architecture drift.

## Required inputs

- The diff or changed file list.
- The relevant architecture and specification docs.
- The expected behavior and failure modes.

## Review focus

- Evidence lineage is preserved before interpretation.
- Confidence and comparability are not collapsed into behavioral scores.
- Lens outputs reuse the shared scorecard vocabulary.
- HLA publications stay behind the optional integration boundary.
- Tests cover any repository contract or schema change.

## Output

Lead with findings ordered by severity. Include open questions, then a short summary.
Say clearly when no issues were found and name any residual verification gap.
