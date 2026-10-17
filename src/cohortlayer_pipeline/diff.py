"""Semantic differences built exclusively from releasable projections."""

from .comparison import compare, phenotype_flags
from .contracts import Change, DiffReport, Report
from .disclosure import disclose


def _index(items, key):
    indexed = {}
    for item in items:
        identity = getattr(item, key)
        if identity in indexed:
            raise ValueError("duplicate_identity")
        indexed[identity] = item
    return indexed


def _change(identity, before, after):
    if before == after:
        return None
    kind = "added" if before is None else "removed" if after is None else "changed"
    return Change(entity_id=identity, change_type=kind, before=before, after=after)


def compare_reports(before: Report, after: Report) -> DiffReport:
    """Compare one hypothesis/scenario; never expose restricted statistics."""
    if before.hypothesis != after.hypothesis or before.scenario_id != after.scenario_id:
        raise ValueError("incompatible_reports")
    cohort_maps = []
    for report in (before, after):
        cohorts = _index(report.cohorts, "cohort_id")
        flags = _index(report.flags, "cohort_id")
        if set(cohorts) != {"Cohort A", "Cohort B"} or set(flags) != set(cohorts):
            raise ValueError("invalid_cohort_identity")
        if any(c.hypothesis_id != report.hypothesis.hypothesis_id for c in cohorts.values()):
            raise ValueError("invalid_hypothesis_identity")
        cohort_maps.append({key: disclose(value) for key, value in cohorts.items()})
    evidence_maps = [_index(r.reference_evidence, "evidence_id") for r in (before, after)]
    evidence_changes = []
    for identity in sorted(set(evidence_maps[0]) | set(evidence_maps[1])):
        values = [
            m[identity].model_dump(mode="json") if identity in m else None for m in evidence_maps
        ]
        change = _change(identity, *values)
        if change is not None:
            evidence_changes.append(change)
    cohort_changes = []
    restricted = False
    for identity in sorted(cohort_maps[0]):
        pair = [m[identity] for m in cohort_maps]
        if any(
            c.execution_status != "succeeded" or c.disclosure_status != "released" for c in pair
        ):
            restricted = True
            cohort_changes.append(Change(entity_id=identity, change_type="restricted"))
            continue
        change = _change(identity, *(c.model_dump(mode="json") for c in pair))
        if change is not None:
            cohort_changes.append(change)
    if restricted:
        conclusion_changes = [Change(entity_id="conclusions", change_type="restricted")]
    else:
        conclusions = [
            {
                "comparison": compare(report.hypothesis, list(cohorts.values())).model_dump(
                    mode="json"
                ),
                "flags": [
                    f.model_dump(mode="json")
                    for f in phenotype_flags(sorted(cohorts.values(), key=lambda c: c.cohort_id))
                ],
            }
            for report, cohorts in zip((before, after), cohort_maps, strict=True)
        ]
        change = _change("conclusions", *conclusions)
        conclusion_changes = [change] if change is not None else []
    return DiffReport(
        data_kind="mixed" if "mixed" in (before.data_kind, after.data_kind) else "synthetic",
        before_manifest_id=before.manifest_id,
        after_manifest_id=after.manifest_id,
        evidence_changes=evidence_changes,
        cohort_changes=cohort_changes,
        conclusion_changes=conclusion_changes,
        limitations=[
            "Synthetic evaluation; differences are not new scientific evidence.",
            "Restricted comparisons disclose no statistics or derived conclusion details.",
            "Aggregate release is not a formal privacy guarantee.",
        ],
    )
