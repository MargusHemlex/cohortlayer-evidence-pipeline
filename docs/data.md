# Data inventory and reuse policy

All current inputs are repository-authored **synthetic aggregate fixtures**.
Names under `SYNTHETIC:` are fictional. They are not real Ensembl, EFO or ClinVar IDs.
GRCh38 is a compatibility label for the pipeline contract; no real variant is mapped.

| Data | Location | Origin | Terms |
|---|---|---|---|
| Three hypotheses | `fixtures.py` | Fictional, authored for this repository | MIT |
| Two cohort estimates | `adapters.py` | Fixed, fictional aggregate fixtures | MIT |
| Reference records | `fixtures.py` | Fictional registry A/B, not downloaded | MIT |
| Example reports | `examples/` | Generated from those fixtures | MIT |

The wrapper duplication scenario shares an explicit original record identifier.
It illustrates deduplication, not discovery of overlapping participants.
Population overlap remains unknown unless explicitly established; distinct source
names do not illustrate independence.

## Future public-reference layer: not shipped

- [Open Targets data sources](https://platform-docs.opentargets.org/gentropy/data-sources)
  and [evidence definitions](https://platform-docs.opentargets.org/evidence).
- [GWAS Catalog summary statistics](https://www.ebi.ac.uk/gwas/docs/summary-statistics/).
- [ClinVar access and use](https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/).

Before committing any real snapshot, record its version, acquisition URL/date,
original study/record identities, source chain, use terms, attribution requirements
and specific redistribution basis. Check the terms of upstream studies too.
Never assume a public download grants unrestricted redistribution.

The current CLI deliberately does not import arbitrary real-data files. Adding a
public adapter or downloader is a separately reviewed feature. Existing synthetic
tests, including source duplication, do not require real source records.

Public source scores, clinical classifications and cohort effect estimates are
different types of evidence. A future mixed report must label provenance per
record and per data layer, and must not pool overlapping evidence as independent
confirmation.

