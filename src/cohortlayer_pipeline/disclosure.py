"""A illustrative aggregate-release policy, not a privacy guarantee."""

from .contracts import CohortResult

POLICY_VERSION = "pipeline-disclosure-v1"
POLICY_CONFIG = {"k": 10}


def disclose(result: CohortResult) -> CohortResult:
    """Return an idempotent public projection without mutating the input."""
    if result.execution_status != "succeeded":
        return result
    if result.disclosure_status == "suppressed":
        reason = (
            "disclosure_input_missing"
            if "disclosure_input_missing" in result.reason_codes
            else "small_group"
        )
    elif result.carrier_count is None or result.case_count is None:
        reason = "disclosure_input_missing"
    elif min(result.carrier_count, result.case_count) < POLICY_CONFIG["k"]:
        reason = "small_group"
    else:
        return result
    projection = result.model_dump()
    projection.update(
        disclosure_status="suppressed",
        sample_size=None,
        carrier_count=None,
        case_count=None,
        effect=None,
        adverse_effect=None,
        reason_codes=[reason],
    )
    return CohortResult.model_validate(projection)
