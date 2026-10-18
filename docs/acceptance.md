# Acceptance criteria and verification

The authoritative scope is [specification version 1.2 (English)](specification.md), with the
[reviewed Estonian source](specification.et.md) retained for provenance.
This table maps its acceptance criteria to runnable evidence.

| Criterion | Implementation / verification |
|---|---|
| AC01: offline runtime | `tests/test_offline.py`, README workflow |
| AC02: hypotheses and required scenarios | `test_pipeline.py` cross-product; adapter/comparison tests |
| AC03: closed schemas | `contracts.py`, schema-export test, Pydantic semantic validation |
| AC04: separate effects and compatibility | `comparison.py`, mismatch and null-boundary tests |
| AC05: distinct statuses and flag semantics | comparison/adapter tests, partial CLI test |
| AC06: synthetic provenance survives export | all report round trips, example reports |
| AC07: deterministic identity | repeated-run test, RFC 8785, source/config digests, idempotent writes, full fixture-export import verification |
| AC08: version changes and safe diff | `test_diff.py`, CLI v1/v2 integration |
| AC09: output boundary | disclosure/diff sentinel tests and sanitized CLI error test |
| AC10: reuse rights | no real snapshots shipped; `docs/data.md` inventory and future gate |
| AC11: CI and secret checks | `.github/workflows/quality.yml`, frozen `uv.lock`, history scan |
| AC12: truthful portfolio docs | README, architecture, AI attribution, checked-in example freshness test |
| AC13: independent public/private boundary | minimal dependency list, `docs/public-private.md`, history review |

The handcrafted secret checker is intentionally limited to common credential
patterns and prohibited tracked file names. It does not certify absence of all
secrets. It scans tracked content and reachable Git history when requested; the
human publication checklist still includes legal rights and confidential material.

## CLI behavior

`run`, `diff`, `list` and `schemas` are documented by `--help`.
Exit `0` means the software completed its requested computation; it does not mean
that evidence supports a hypothesis. `3` denotes partial or failed cohort execution
but still emits the permitted report. `2` is a controlled invocation/input error;
`4` is an existing-output integrity conflict. Unexpected programming errors are
not mislabeled as successful scientific results.

