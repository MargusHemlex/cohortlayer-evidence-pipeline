# CohortLayer Evidence Pipeline — synthetic example

**SYNTHETIC SOFTWARE EVALUATION — not scientific replication or target validation.**

Hypothesis: `HYP-001` · Scenario: `update` · Version: `v1`

Execution: **complete** · Cohort comparison: **concordant** · Direction vs hypothesis: **matches**

| Fictional cohort | Execution | Disclosure | Estimate [95% CI] | Carriers | Cases |
|---|---|---|---|---|---|
| Cohort A | succeeded | released | -0.4 [-0.5, -0.3] (beta) | 80 | 120 |
| Cohort B | succeeded | released | -0.3 [-0.4, -0.2] (beta) | 80 | 120 |

## Effect meaning and population

### Cohort A

Population: Fictional population; not a real cohort.

Trait: `SYNTHETIC:TRAIT_A` · Unit: `standard_deviation` · Encoding: `higher_value_means_more_trait`.

Contrast: `perturbed_vs_baseline` · Build: `GRCh38`.

### Cohort B

Population: Fictional population; not a real cohort.

Trait: `SYNTHETIC:TRAIT_A` · Unit: `standard_deviation` · Encoding: `higher_value_means_more_trait`.

Contrast: `perturbed_vs_baseline` · Build: `GRCh38`.


## Fictional phenotype flags

- Cohort A: **not_assessable** (flag_input_unavailable).
- Cohort B: **not_assessable** (flag_input_unavailable).

A flag not firing is not evidence of clinical safety.

## Reference evidence (separate from cohort estimates)

- **synthetic** · Fictional Registry A · SYNTHETIC:ORIGINAL_1 · Fictional association annotation, not a published finding. Overlap: unknown.

## Provenance

Manifest: `sha256:5938e23ba15ad1ad65711d487143d6cf4971113bf48b7d896753d6ca0c5079fb`

Code: `0.1.0@sha256:8d0340543c54bb51189bc026bb36a64c65adbb745c41f899730732ae7ff50293`

## Limitations

- SYNTHETIC SOFTWARE EVALUATION: no real cohort access or scientific validation.
- Synthetic agreement is not independent replication, causality or clinical safety.
- No pooled effect is calculated. The comparison rule is illustrative only.
- Count suppression is not a formal privacy guarantee or protection from all inference.
- Population transferability is not assessed. Reference records are fictional.
