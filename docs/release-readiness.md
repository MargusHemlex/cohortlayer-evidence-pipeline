# Repository contents and release readiness

This repository contains the standalone **CohortLayer Evidence Pipeline**.
The owner approved public release on **18 October 2026**, after the final
four-agent review of `a7758b585fe00b371b5b064ae4aaf50866919019`.
The separate product repository remains private; its deployment is unchanged.

## Included

- README with clone/install/run instructions, scope, limitations and attribution.
- MIT code license and a separate synthetic-data inventory.
- Python package, CLI, locked dependency manifest and JSON schemas.
- Synthetic aggregate fixtures, example reports and version comparisons.
- Tests and a read-only GitHub Actions workflow with pinned action commits.
- Architecture, acceptance criteria, reviewed specification and implementation
  review records. These describe only the published pipeline's scope and clearly
  identify the private production-engine components as future work.

## Excluded

No real cohort adapters, managed-cohort queries, patient records, customer
hypotheses/results, production credentials, private package dependencies,
restricted scientific snapshots or production configuration are included.
No proprietary production engine has been copied into this repository.

The data inventory is exhaustive for this release: the hypotheses, cohort
aggregates and reference annotations are authored synthetic fixtures. The
pipeline neither downloads scientific data nor calls a model provider at runtime.

Local virtual environments, caches and generated run directories are ignored and
are not tracked source. Historical review logs and provider authentication are
stored outside the repository and are not release assets.

## Verification scope

The tracked file inventory, package dependencies, documentation and data origin
were checked against the public/private boundary. Common credential-pattern and
prohibited-file checks cover tracked content and reachable Git history. Runtime
tests exercise offline execution, output filtering, report integrity and version
comparison. Generated examples and schemas are refreshed with naming changes.

Automated credential-pattern checks are limited detectors, not a guarantee of
absence of every possible secret. Future source or data additions need their own
rights and confidentiality review. The presence of synthetic data does not
establish scientific validity or a formal privacy guarantee.

The current implementation uses `run_pipeline`, `pipeline-*` rule versions and
the `SYNTHETIC:` identifier namespace. These names do not alter the fictional
origin of the data or broaden the pipeline's scientific claims.
