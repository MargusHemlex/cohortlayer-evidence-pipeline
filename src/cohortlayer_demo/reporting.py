"""Readable projections of already disclosed results."""

import html
import json

from .contracts import DiffReport, Report


def _text(value: object) -> str:
    return html.escape(str(value)).replace("|", "&#124;").replace("\n", " ")


def render_report(report: Report) -> str:
    lines = [
        "# CohortLayer — synthetic evidence demo",
        "",
        "**SYNTHETIC SOFTWARE DEMONSTRATION — not scientific replication or target validation.**",
        "",
        f"Hypothesis: `{_text(report.hypothesis.hypothesis_id)}` · "
        f"Scenario: `{_text(report.scenario_id)}` · Version: `{report.manifest.dataset_version}`",
        "",
        f"Execution: **{report.comparison.run_status}** · "
        f"Cohort comparison: **{report.comparison.comparison_status}** · "
        f"Direction vs hypothesis: **{report.comparison.direction_vs_hypothesis}**",
        "",
        "| Fictional cohort | Execution | Disclosure | Estimate [95% CI] | Carriers | Cases |",
        "|---|---|---|---|---|---|",
    ]
    for cohort in sorted(report.cohorts, key=lambda item: item.cohort_id):
        effect = cohort.effect
        estimate = (
            f"{effect.estimate:g} [{effect.ci_lower:g}, {effect.ci_upper:g}] ({effect.measure})"
            if effect is not None
            else "Not released"
        )
        lines.append(
            f"| {cohort.cohort_id} | {cohort.execution_status} | {cohort.disclosure_status} "
            f"| {estimate} | {cohort.carrier_count if cohort.carrier_count is not None else '—'} "
            f"| {cohort.case_count if cohort.case_count is not None else '—'} |"
        )
    lines += ["", "## Effect meaning and population", ""]
    for cohort in sorted(report.cohorts, key=lambda item: item.cohort_id):
        lines += [f"### {cohort.cohort_id}", "", f"Population: {_text(cohort.population)}.", ""]
        effect = cohort.effect
        if effect is not None:
            lines += [
                f"Trait: `{_text(effect.trait_id)}` · Unit: `{_text(effect.unit)}` · "
                f"Encoding: `{_text(effect.phenotype_encoding)}`.",
                "",
                f"Contrast: `{_text(effect.contrast_id)}` · Build: `{_text(effect.genome_build)}`.",
                "",
            ]
            if effect.effect_allele is not None:
                lines += [
                    f"Effect allele: `{_text(effect.effect_allele)}` · "
                    f"Reference allele: `{_text(effect.reference_allele)}`.",
                    "",
                ]
        else:
            lines += ["Effect metadata and statistics not released.", ""]
    lines += ["", "## Fictional phenotype flags", ""]
    for flag in report.flags:
        lines.append(f"- {flag.cohort_id}: **{flag.status}** ({_text(flag.reason_code)}).")
    lines += [
        "",
        "A flag not firing is not evidence of clinical safety.",
        "",
        "## Reference evidence (separate from cohort estimates)",
        "",
    ]
    for record in report.reference_evidence:
        lines.append(
            f"- **{record.data_kind}** · {_text(record.source)} · "
            f"{_text(record.source_record_id)} · {_text(record.summary)} "
            f"Overlap: {_text(record.overlap_status)}."
        )
    lines += [
        "",
        "## Provenance",
        "",
        f"Manifest: `{report.manifest_id}`",
        "",
        f"Code: `{report.manifest.code_version}`",
        "",
        "## Limitations",
        "",
    ]
    lines += [f"- {_text(item)}" for item in report.limitations]
    return "\n".join(lines) + "\n"


def render_diff(diff: DiffReport) -> str:
    lines = [
        "# CohortLayer — synthetic version comparison",
        "",
        "**SYNTHETIC SOFTWARE DEMONSTRATION — changes are not new scientific evidence.**",
        "",
        f"Before: `{diff.before_manifest_id}`",
        "",
        f"After: `{diff.after_manifest_id}`",
        "",
    ]
    for title, changes in (
        ("Reference evidence", diff.evidence_changes),
        ("Fictional cohort results", diff.cohort_changes),
        ("Derived conclusions", diff.conclusion_changes),
    ):
        lines += [f"## {title}", ""]
        if not changes:
            lines += ["No semantic changes.", ""]
        for change in changes:
            lines += [f"### {_text(change.entity_id)} — {change.change_type}", ""]
            if change.change_type == "restricted":
                lines += ["Restricted comparability; no values or deltas are disclosed.", ""]
            else:
                # JSON in a fenced block; escape markup/backticks from external text.
                value = json.dumps(
                    {"before": change.before, "after": change.after}, indent=2, ensure_ascii=True
                ).replace("`", "\\u0060")
                lines += ["```json", value, "```", ""]
    lines += ["## Limitations", ""] + [f"- {_text(item)}" for item in diff.limitations]
    return "\n".join(lines) + "\n"
