# CohortLayer Evidence Pipeline

Compare evidence from two cohorts without losing the meaning of their results, disclosure restrictions or provenance. When an input version changes, explain which records and conclusions changed.

This standalone Python pipeline demonstrates that engineering problem using fictional gene–trait hypotheses and fixed aggregate fixtures. It keeps each cohort's estimate separate, rejects incompatible measurements, filters restricted statistics before reporting and produces reproducible JSON/Markdown outputs with content-addressed manifests.

**This is software engineering evidence, not drug-target validation.** Cohort A and
Cohort B are fictional. No UK Biobank, All of Us or other managed cohort is queried.
Agreement between synthetic fixtures is not independent scientific replication.
There are no patient data, credentials, model calls or paid services.

## Review in five minutes

1. Inspect the [example report](examples/report.md) and [version comparison](examples/diff.md): what the user receives.
2. Read the [architecture](docs/architecture.md): validation → disclosure → comparison → provenance and reporting.
3. Run the example below, then inspect [acceptance criteria and test coverage](docs/acceptance.md). The [English specification](docs/specification.md) defines the scope; the architecture explains implemented limits.

## Run locally

Requirements: Python 3.12–3.15 and [uv](https://docs.astral.sh/uv/).
Initial dependency installation needs a network connection. Runtime needs none.

```sh
git clone https://github.com/MargusHemlex/cohortlayer-evidence-pipeline.git
cd cohortlayer-evidence-pipeline
uv sync --frozen
uv run --no-sync cohortlayer-pipeline run --hypothesis HYP-001 --scenario update --version v1 --output pipeline-output/v1
uv run --no-sync cohortlayer-pipeline run --hypothesis HYP-001 --scenario update --version v2 --output pipeline-output/v2
uv run --no-sync cohortlayer-pipeline diff pipeline-output/v1/report.json pipeline-output/v2/report.json --output pipeline-output/diff
uv run --no-sync cohortlayer-pipeline list
```

Expected output from the two `run` commands and the `diff` command:

```text
complete: concordant (synthetic)
complete: conflicting (synthetic)
version_comparison_exported (synthetic evaluation)
```

In v1, both fictional cohort intervals lie below the null effect. In v2, Cohort B's interval moves above it, while Cohort A's stays below. The comparison therefore changes from `concordant` to `conflicting`, and hypothesis direction changes from `matches` to `mixed`. The diff separates the changed cohort statistics, fictional reference annotation and derived conclusions. This is an intentionally constructed update, not a new scientific finding.

Open `pipeline-output/v1/report.md`, `pipeline-output/v2/report.md` and `pipeline-output/diff/diff.md` to inspect the results. The checked-in examples above show the v1 report and the v1/v2 comparison before installation.

The run writes a strict JSON report, a readable Markdown report and a manifest
addressed by its SHA-256 content hash. An identical rerun reuses identical files;
it never silently overwrites different results. Use a new output directory for a
different run. Exit codes: `0` completed computation (including inconclusive or
suppressed evidence), `2` invalid invocation or input, `3` partial/failed cohort
execution, `4` output-integrity conflict.

## Scope

Three predefined gene–trait hypotheses and fixed aggregate fixtures exercise
concordance, conflicting directions, uncertainty, a result opposing the hypothesis,
small groups, missing counts, malformed results, incompatible measurements,
timeouts, partial runs and evidence updates. A fictional adverse phenotype has a
transparent flag rule; a flag not firing is **not** evidence of clinical safety.

Each cohort retains its own estimate and 95% confidence interval. There is no
pooled effect or meta-analysis. Execution status, disclosure status, cohort
agreement and agreement with the expected hypothesis direction are separate fields.

## Public evidence and synthetic data

This initial release includes **synthetic fixtures only**, including fictional
reference-evidence records used to test source overlap. It does not redistribute
Open Targets, GWAS Catalog or ClinVar records. A future public-reference layer
requires version-specific terms, attribution and redistribution review before
snapshots are committed. Public database records are context, not a second cohort.

Open Targets can incorporate evidence from other databases. Multiple appearances
of one original record must not be counted as independent confirmation. See
[the data policy](docs/data.md).

## Verify

```sh
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pytest
uv run --no-sync python scripts/check_secrets.py
uv run --no-sync cohortlayer-pipeline schemas --output pipeline-output/schemas
```

GitHub Actions runs the same quality checks and an offline-runtime integration
test. No service secrets are required.

## Supporting records

- [Data provenance and reuse policy](docs/data.md) and [public/private boundary](docs/public-private.md).
- [Implementation review and verification](docs/review.md) and [release-readiness record](docs/release-readiness.md): dated review scope and publication history.
- [English specification](docs/specification.md), with the [reviewed Estonian source](docs/specification.et.md) retained for provenance.

## Attribution and limitations

Designed and maintained by MargusHemlex, with AI-assisted implementation and
review by Codex agents, Claude Code and Kimi K3. Review records distinguish
specification review from code review; no claim of independent human scientific
review is made.

The pipeline's `k=10` count rule is illustrative. Count suppression is not differential
privacy or a guarantee against inference across repeated queries. Even suppressed
reports retain run identity and metadata; use no sensitive inputs in this pipeline.
The comparison rule is not a validated scientific protocol and does not establish
causality, clinical utility or generalization across populations.

The pipeline is standalone. Real cohort access, confidential customer hypotheses,
production configuration and proprietary methods belong in a separate private
engine and are not dependencies of this repository.

Code and synthetic fixtures: MIT license. No third-party scientific snapshots are
included; their licenses would remain separate from this repository's code license.

