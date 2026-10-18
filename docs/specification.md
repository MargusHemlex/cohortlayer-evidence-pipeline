# CohortLayer Evidence Pipeline specification

Version: 1.2 · Source specification: 18 October 2026 · English edition: 19 October 2026

This English edition preserves the requirements of the [reviewed Estonian source](specification.et.md). The approved project name is **CohortLayer Evidence Pipeline**, repository `cohortlayer-evidence-pipeline`; the naming change does not change functional requirements. This is a design contract, not a claim that every planned extension is implemented. The shipped release uses synthetic fixtures only. See [architecture](architecture.md), [acceptance evidence](acceptance.md) and [release readiness](release-readiness.md) for achieved scope and subsequent publication decisions.

## 1. Purpose and positioning

Build a standalone public engineering sample demonstrating genetic-evidence provenance, versioning, separate comparison of two synthetic cohorts and change tracking. Technical recruiters, CTOs and automated code reviewers must be able to verify its claims through code and tests.

The pipeline does not biologically validate a drug target, establish causality or demonstrate independent scientific replication. It does not connect to UK Biobank, All of Us or any other real cohort. Public reference evidence and synthetic analysis are separate data layers; agreement between them is not new scientific evidence.

The public repository is `cohortlayer-evidence-pipeline`. A separate `cohortlayer-engine` repository is reserved for private product work. These design boundaries do not assert that private production capabilities already exist.

## 2. First-version scope

1. Three to five predefined example hypotheses; no free-form scientific search.
2. Two local synthetic cohort adapters, named `Cohort A` and `Cohort B`.
3. Separate cohort effect estimates and uncertainty; no pooled effect or meta-analysis.
4. A transparent, versioned illustrative concordance rule.
5. Cohort-output validation, an illustrative small-group disclosure policy and failure scenarios.
6. Two immutable evidence versions, deterministic reruns and a change report.
7. An optional small public scientific-data snapshot only after use and redistribution rights are reviewed. The synthetic baseline must work without it. No such real snapshot is shipped in the current release.
8. English README, code identifiers, CLI output and reports. The original specification was written in Estonian; this edition makes it accessible in English.

Reports retain population descriptions. The illustrative rule does not assess scientific transferability across ancestry groups. Technical comparability does not establish scientific population equivalence.

Version 1 excludes accounts, multitenancy, billing, LLMs, model training, cloud deployment, real cohort analysis, unrestricted gene queries, general genome-build conversion and automatic production monitoring. A local command demonstrates an update; a scheduled service is future work. A web UI is also optional future work.

## 3. Data and source roles

### 3.1 Synthetic baseline

Use generated data with an explicit seed and generator version, or fixed aggregate fixtures. Document each scenario's assumptions. Comparing two outputs of the same generator demonstrates software behavior, not independent replication.

Version 1 uses fixed synthetic aggregate fixtures; an individual-genome generator is outside the MVP. An optional adapter-internal test may use synthetic row-level material, but it is not baseline input or output. Only permitted aggregate fields may reach reports and normal logs. Runtime requires neither a network connection nor an API key.

### 3.2 Optional public-reference layer

| Source | Role | Prohibited inference |
|---|---|---|
| Open Targets | Gene/disease identifiers, association context and links to original evidence | A score is neither a cohort effect estimate nor evidence of causality |
| GWAS Catalog | Selected study associations, study IDs, available aggregate estimates and metadata | Studies cannot be treated as independent without provenance review |
| ClinVar | Variant/disease interpretation, review status and version | Clinical classification is neither target validation nor a cohort effect |

Open Targets may incorporate evidence from other sources. Do not count one original record as multiple independent confirmations. Preserve original-source and study/record IDs; deduplicate identical source records. Mark possible sample overlap as `known`, `possible` or `unknown`; do not claim complete overlap resolution.

Before committing any actual snapshot, document its version, URL, download date, license/terms, provenance chain, attribution requirements and redistribution basis. Unreviewed snapshots must not be published. Where redistribution is prohibited, use a download tool permitted by the terms or synthetic substitutes. Baseline execution and tests must not depend on downloading data.

Public records provide separate context; they must not silently determine a synthetic scenario's expected result. Demonstrating a real evidence update requires two actual archived versions. Invented changes must be marked as simulations.

## 4. User workflow and output

The user selects a predefined hypothesis and version. The pipeline validates input, runs each adapter separately, validates outputs and applies the disclosure policy. Its report shows each cohort's permitted result, limitations and comparison rationale, with public-reference evidence in a separate section when an approved snapshot exists.

The user runs the same hypothesis against another evidence version. A comparison reports added, removed and changed permitted reference records and synthetic cohort results in separate sections. Classifier, hypothesis-direction and phenotype-flag changes appear as derived conclusions under the same disclosure boundary. A file change without relevant semantic change must not create a scientific conclusion.

Outputs are schema-validated JSON and human-readable Markdown. CLI, reports and tests constitute version 1.

## 5. Architecture and implementation

Use Python 3.12+, `pyproject.toml`, locked dependencies, Pydantic/JSON Schema, pytest and Ruff. Avoid unnecessary data-processing or orchestration frameworks. Provide one documented container-free execution path; Docker must not be required.

Responsibilities:

- `contracts`: hypothesis, reference-evidence, cohort-result, manifest and report schemas.
- `fixtures`: three to five hypotheses, scenarios and synthetic v1/v2 data.
- `adapters`: a common contract and two synthetic implementations; no real cohort access or API keys.
- Validation: input, output and comparability checks. The shipped implementation distributes these across contracts, adapters and comparison rather than requiring a separate `validation` module.
- `disclosure`: permitted aggregate projections shared by reporting, diff and user-visible errors.
- `comparison`: the illustrative cohort-concordance classifier.
- `provenance`: content hashes, versions, sources and immutable analysis records.
- `diff`: permitted semantic changes between versions.
- `reporting` and `cli`: JSON/Markdown outputs and commands.
- `tests`: unit, contract, integration and reproducibility checks.

Public JSON contracts may later serve a private engine. The public repository must neither import private packages nor require access to them.

## 6. Minimum data contracts

### Hypothesis

Include `hypothesis_id`, `gene_id`, optional `variant_id`, `trait_id`, expected effect direction, analysis-protocol version and scenario identity. Version 1 supports predefined gene–trait and variant–trait cases; it does not model drug dose or modulation effects.

Use one documented genome build, GRCh38, and EFO phenotype identifiers when linking public records. Fictional phenotypes remain in the `SYNTHETIC:` namespace. Variant/allele mismatches produce a comparability problem, never silent conversion.

### Evidence record

Include `evidence_id`, `source`, `source_record_id`, optional `study_id`, `source_version`, `retrieved_at`, original-source URL, `data_kind` (`public_reference` or `synthetic`), relevant identifiers and license reference. Missing study IDs are `null` with a reason. Synthetic records use `retrieved_at=null`, reason `generated_fixture` and a fixed `fixture_version`; do not pretend a download occurred. Source scores, clinical classifications and statistical effects remain distinct concepts.

### Cohort result

- Preserve `cohort_id`, `hypothesis_id`, `analysis_version`, `dataset_version` and `data_kind=synthetic`.
- `execution_status`: `succeeded`, `failed` or `timeout`.
- `disclosure_status`: `released`, `suppressed` or `not_applicable`. The last applies to failed/timed-out executions without assessable statistics; successful statistical results are released or suppressed.
- Every successfully released effect needs a measure, estimate and 95% confidence interval. Standard error may be additional; standard-error-only output is `invalid_output`, not an instruction to derive an interval. Retain population description and available sample/carrier counts.
- Missing values are `null` with reason codes, never zero. Failed or suppressed results contain no undisclosed statistics.
- Define direction against the phenotype and effect measure: a lower biomarker is not automatically lower disease risk.
- Variant effects retain effect/reference alleles. Synthetic gene contrasts retain contrast IDs and group ordering. Phenotype encoding and units are mandatory. Version 1 rejects incompatible orientation, units or encoding rather than normalizing them.
- Statistics must be finite; standard error nonnegative; interval lower bound no greater than upper bound; estimate inside its interval. Ratio estimates and interval bounds are positive. Counts are nonnegative integers; carrier count cannot exceed sample size. Invalid statistics never enter the classifier.

### Comparison report

Include `run_status` (`complete`, `partial`, `failed`), `comparison_status` (`concordant`, `conflicting`, `inconclusive`, `not_evaluable`), machine-readable reason codes, separate cohort results, separate reference evidence, manifest ID and limitations.

| Validated adapter outcomes | `run_status` | `comparison_status` |
|---|---|---|
| Both failed/timed out | `failed` | `not_evaluable` |
| Exactly one succeeded | `partial` | `not_evaluable` |
| Both succeeded; either suppressed or pair incomparable | `complete` | `not_evaluable` |
| Both succeeded, released and comparable | `complete` | Apply interval rule below |

First check execution, disclosure and comparability. For a comparable released pair, either 95% interval including the null yields `inconclusive`, including an endpoint equal to the null. Otherwise, intervals entirely on the same side yield `concordant`; opposite sides yield `conflicting`. Beta's null is 0; a ratio's null is 1. Do not compare heterogeneous phenotypes or measures. This is an illustrative rule, not a validated scientific protocol.

A partial run still applies disclosure to its successful cohort and displays permitted fields. Completed computation may be suppressed or inconclusive; `complete` is not supporting scientific evidence.

`concordant` describes agreement between cohorts, which may oppose the hypothesis. Report `direction_vs_hypothesis` separately: both distinguishable effects in the expected direction give `matches`, both opposite give `opposes`, opposite to each other give `mixed`; otherwise use `not_assessable`.

Set final statuses only after schema and semantic validation. Invalid adapter output becomes `failed` with controlled reason `invalid_output`; do not publish the raw response. Version the timeout budget in configuration (implemented default: five seconds). Scenario tests inject deterministic timeout results rather than depending on network latency or wall-clock timing. This is not production cancellation enforcement.

The `pipeline-flag-v1` rule evaluates only the fictional `SYNTHETIC:ADVERSE_EVENT` odds ratio, separately per cohort. A validated, released interval with lower bound strictly above 1 gives `triggered`; other assessable cases give `not_triggered`. Missing, suppressed, invalid or failed input gives `not_assessable`. Test all three outcomes and the boundary at 1. This is a technical flag, not clinical safety evidence.

### Manifest

Bind input hash, dataset/analysis/rule versions and hashes, disclosure-policy version/configuration hash, generator seed/version, code version, schema version and source identifiers. Cohort analysis/dataset versions must match manifest versions. Fixed aggregates use seed `null` with reason `fixed_aggregate_fixture`; fixture version is always present.

Keep changing timestamps and local paths outside canonical result identity. Identical input, versions and code produce identical canonical JSON and hash. Use RFC 8785 serialization and SHA-256. Reject NaN/infinity; order unstable record collections by stable IDs before serialization. Lock dependencies and make reproducibility independent of local timezone.

Store manifests by content hash. Identical repeated writes reuse unchanged files. Different content at an existing identity is an integrity error; new versions receive new hashes. Provide no overwrite flag.

The implemented code identity hashes package source bytes rather than its enclosing Git commit, avoiding self-reference through checked-in examples. The raw synthetic-fixture digest includes pre-disclosure counts; these public fixture values are enumerable. This must not be reused as a privacy-preserving commitment to confidential data.

Report origin is `synthetic` or, for a future approved mixed layer, `mixed`, with origin identified for each layer. Never relabel public facts as synthetic or synthetic results as measurements. Preserve origin in every independently exported output.

The current CLI importer accepts only v1/v2 fixed-fixture exports from the same current code build. It reconstructs the expected report and compares full canonical content, not just the manifest hash. This is integrity validation, not a digital signature or authentication of arbitrary scientific reports. The lower-level diff recomputes derived conclusions from disclosed fields.

## 7. Disclosure policy and limits

Document and version `k=10`: fewer than ten carriers or cases suppresses associated statistics. Missing required counts yield suppression with `disclosure_input_missing`; never invent counts. This is an illustrative policy, not a real cohort's policy or formal privacy guarantee. Remove estimates and derivable fields with restricted counts. Never copy raw adapter responses into errors, logs, reports or diffs.

Diff only permitted projections. If either version is restricted, do not emit hidden counts, effects, exact deltas or explanations that facilitate reconstruction. State changes may produce only a generic restricted-comparability entry. Test transitions across the threshold. Do not claim protection against all inference through repeated queries or external information. Metadata and hashes remain observable; only synthetic inputs are allowed.

## 8. Required scenarios

1. Same-direction distinguishable estimates: `concordant`.
2. Opposite-direction distinguishable estimates: `conflicting`.
3. Either interval includes the null: `inconclusive`; width alone does not decide the class.
4. Small group: restricted fields suppressed; pair `not_evaluable`.
5. Cohort B fails/times out: `partial`, not successful replication or absence of evidence.
6. Invalid schema or mismatched allele/build/phenotype/measure: safe rejection or incomparability.
7. v1 → v2 added/removed/changed permitted records: precise semantic diff and new content hash.
8. Repeating the same version: identical canonical result.
9. One original record represented twice: mark overlap without adding independent confirmation. Use fictional source IDs; no real snapshot is required.
10. Fictional phenotype flag: explain the exact rule; an untriggered flag does not mean safe.

All ten scenarios must run on synthetic fixtures alone. Three to five hypotheses may supply multiple scenarios; ten separate biological examples are unnecessary.

## 9. Public/private boundary

| Public pipeline | Separate private engine scope |
|---|---|
| JSON schemas and adapter contract | Real cohort adapters, queries and processing configuration |
| Synthetic fixtures/generator and A/B adapters | Credentials, accounts and environment configuration |
| Fully readable simplified comparison rule | Proprietary production statistics, scoring and harmonization |
| Illustrative disclosure filter and its limitations | Confidential cohort-specific controls and operations |
| Versioning, provenance, diff and reporting | Customer hypotheses, contracts, results and query history |
| Rights-reviewed public snapshots and attribution, if later added | Restricted or non-redistributable data |
| Tests, example reports, CI, decisions and limitations | Production infrastructure, monitoring, audit records and deployment |

This boundary does not imply all future components exist. Clearly identify substituted components. No private submodules, dependencies or bundles generated from private files are permitted. Snapshots, fixtures and Git history are subject to the same publication review.

## 10. Acceptance criteria

- **AC01:** One README path works in a clean supported environment without an API key or runtime network; document initial dependency installation.
- **AC02:** At least three predefined hypotheses; automated coverage of all required scenarios.
- **AC03:** Inputs and exported JSON validate against closed schemas; unexpected fields cannot enter reports.
- **AC04:** No pooled effect; incompatible measure/allele/build/trait combinations cannot claim concordance.
- **AC05:** Failure, uncertainty and suppression are distinct machine-readable states. Missing counts never become zero. Test every status-table branch, orientation, concordance opposing the hypothesis and all three flag outcomes.
- **AC06:** Every standalone report retains data-layer origins and synthetic labels.
- **AC07:** Repeated versions produce identical canonical JSON/hash regardless of location or time.
- **AC08:** Explain v1/v2 changes through records and versions; never disclose hidden values or deltas.
- **AC09:** Test disclosure across logs, errors, reports and diffs; failures expose controlled error codes only.
- **AC10:** Add real public snapshots only after documenting version-specific rights. Without that review, ship the synthetic baseline only.
- **AC11:** CI runs lint/format, schema, unit, integration, reproducibility and secret checks without cohort or paid-service keys.
- **AC12:** README states purpose, actual author contribution, architecture, execution example, example report, provenance, public/private boundary and scientific limitations.
- **AC13:** No private-engine dependency, customer material, secrets or unlicensed data. Distinguish code and data licenses.

## 11. Work sequence and completion

1. Schemas, status semantics, three to five synthetic hypotheses and public/private boundary.
2. Adapters, disclosure and comparability checks with tests.
3. Report, manifest and deterministic execution.
4. Second evidence version and disclosure-aware diff.
5. Rights review and optional permitted public-reference layer; this must not block the synthetic baseline.
6. README, example outputs and CI; acceptance review before publication.

Completion means AC01–AC13 are met and limitations accurately documented. The original specification task delivered a plan, not repository creation or publication authorization. Implementation and public release were later separately authorized; see [release readiness](release-readiness.md). Translating this document does not authorize new production work or data disclosure.

## 12. Original reference sources

These references are preserved from the source specification, not revalidated licensing decisions for any snapshot:

- [CohortLayer product description](https://cohortlayer.com/)
- [Open Targets data sources](https://platform-docs.opentargets.org/gentropy/data-sources)
- [Open Targets evidence](https://platform-docs.opentargets.org/evidence)
- [Open Targets downloads](https://platform.opentargets.org/downloads/data)
- [GWAS Catalog summary statistics](https://www.ebi.ac.uk/gwas/docs/summary-statistics/)
- [ClinVar data use](https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/)

A source list does not replace snapshot-specific rights review. Reviewer assessments are specification quality checks, not scientific or legal certification.
