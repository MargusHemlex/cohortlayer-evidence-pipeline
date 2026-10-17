# Architecture and decisions

```text
Predefined hypothesis + scenario + fixture version
  → independent synthetic adapter A and adapter B
  → strict Pydantic contracts and statistical validation
  → disclosure projection (no raw result in reporting)
  → comparison + hypothesis-direction assessment + fictional flags
  → RFC 8785 JSON, SHA-256 provenance, JSON and Markdown reports

Two saved reports → validated input → disclosure projection again
  → reference changes | cohort changes | derived-conclusion changes
```

The interface is deliberately narrow: `run_adapter`, `disclose`, `compare`,
`phenotype_flags`, `run_demo`, and `compare_reports`. The code has no model or
cloud SDK, database or production worker abstraction.

## Evidence and execution mean different things

Both adapters failing gives `failed/not_evaluable`; one failing gives
`partial/not_evaluable`. Both completing can still yield `not_evaluable` because
of disclosure restrictions or incompatible measurements. Two released comparable
intervals that include the null in either cohort yield `inconclusive`.
Intervals entirely on the same side of the null yield `concordant`; intervals on
opposite sides yield `conflicting`. Beta's null is 0, odds ratio's null is 1.
This interval rule is demonstrative, not a significance or replication protocol.

`direction_vs_hypothesis` is separate: two consistent estimates can both oppose
the expected direction. Units, trait encoding, contrasts, alleles, genome build
and analysis versions must match; no automatic flipping or liftover is done.

## Publication boundary

`disclose` removes estimates, counts, sample size and phenotype effects when a
required count is absent or below `k=10`. It is idempotent. An unavailable result
has no statistical payload. The renderer receives only disclosed results.
The diff rechecks disclosure and omits before/after values and derived conclusions
when either side is restricted. No adapter diagnostics are logged.

The CLI importer reconstructs the expected report from the selected fixed
hypothesis/scenario/version and compares its full canonical content. A valid
manifest hash alone is insufficient. Edited values, stale code exports and
inconsistent conclusions are rejected with a controlled error. This is integrity
validation of the current demo fixtures, not a digital signature or proof of an
external scientific result. This release supports comparing v1/v2 exports from
the same current code build only. The lower-level diff also recomputes conclusions
from disclosed cohort fields instead of trusting supplied labels.

This is not differential privacy. Metadata and content hashes remain available
and can support inference in adversarial settings; only synthetic fixtures are
allowed. Never use this program with confidential inputs or real cohort data.

## Reproducibility

Fixtures are fixed aggregates, with no individual-genome generator. Generator seed
is `null` with an explicit reason. Manifest hashes bind input, raw synthetic
fixture content, analysis and comparison versions, disclosure configuration,
schema version and actual Python source content. Source identity is used instead
of a Git hash to avoid the self-reference created by checked-in example reports.
The release Git commit can be recorded separately by CI.

RFC 8785 serialization and stable record ordering define the canonical bytes.
No machine paths, current timestamps, random run IDs or environment variables are
included. Identical writes are reused; differing bytes at the same path fail.

The synthetic raw-fixture digest intentionally includes pre-disclosure counts.
Those fixture values are public in the source; a low-entropy hidden count could be
recovered by enumerating candidate fixture hashes. This manifest design must not
be reused as a privacy-preserving commitment to confidential data.

## Timeout scope

The example timeout budget is 5 seconds, versioned in `config.py`. The synthetic
timeout scenario injects a deterministic unavailable result. This repository has
no external worker or production cancellation scheduler; real execution limits
would belong to the private adapter infrastructure.

## Schemas and semantic validation

Exported JSON schemas forbid unexpected fields. Pydantic validators additionally
check statistical semantics such as finite numbers, interval ordering, positive
ratio intervals, count consistency and redaction rules. JSON Schema alone cannot
express every relationship; import uses the semantic validators as well.

