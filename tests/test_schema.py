"""The schema's conditional rules are the specification's argument in machine-
readable form. Each test below pins one rule: if the rule is ever relaxed by
accident, a test fails rather than a disclosure silently passing.

Convention: `assert_rejected` / `assert_accepted` wrap the validator so failures
report which rule broke, not just "ValidationError".
"""

from __future__ import annotations

import pytest


def assert_rejected(validator, doc, because: str):
    errors = list(validator.iter_errors(doc))
    assert errors, f"expected rejection ({because}) but the record validated"


def assert_accepted(validator, doc, because: str):
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    assert not errors, (
        f"expected acceptance ({because}) but got: "
        + "; ".join(f"{'.'.join(str(p) for p in e.path) or '<root>'}: {e.message}" for e in errors)
    )


# --------------------------------------------------------------------------
# Baseline
# --------------------------------------------------------------------------

def test_schema_is_itself_valid(validator):
    """check_schema runs in the fixture; this pins that it stays Draft 2020-12."""
    assert validator.schema["$schema"].endswith("draft/2020-12/schema")


def test_minimal_all_unknown_record_validates(validator, doc):
    assert_accepted(validator, doc, "'unknown' throughout is the load-bearing valid case")


# --------------------------------------------------------------------------
# Structure
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "field",
    [
        "disclosure_version",
        "benchmark",
        "strata_reported",
        "elicitation_budget",
        "contamination_controls",
        "regeneration",
    ],
)
def test_every_top_level_field_is_required(validator, doc, field):
    doc.pop(field)
    assert_rejected(validator, doc, f"{field} is required")


def test_unknown_top_level_key_is_rejected(validator, doc):
    doc["contamination_status"] = "clean"
    assert_rejected(validator, doc, "additionalProperties is false at the root")


def test_unknown_nested_key_is_rejected(validator, doc):
    doc["contamination_controls"]["multimodal"] = "unknown"
    assert_rejected(validator, doc, "additionalProperties is false on contamination_controls")


def test_version_is_pinned(validator, doc):
    doc["disclosure_version"] = "1.0"
    assert_rejected(validator, doc, "v1.0 had a four-type taxonomy and is not this schema")


def test_benchmark_name_must_be_non_empty(validator, doc):
    doc["benchmark"]["name"] = ""
    assert_rejected(validator, doc, "an unnamed benchmark is not a disclosure")


@pytest.mark.parametrize(
    "doi,ok",
    [
        ("10.6084/m9.figshare.32814449", True),
        ("https://doi.org/10.6084/m9.figshare.32814449", True),
        ("", True),
        ("figshare.32814449", False),
        ("doi:10.6084/m9", False),
    ],
)
def test_doi_pattern(validator, doc, doi, ok):
    doc["benchmark"]["doi"] = doi
    (assert_accepted if ok else assert_rejected)(validator, doc, f"doi={doi!r}")


@pytest.mark.parametrize("date,ok", [("2026-08-02", True), ("", True), ("2 Aug 2026", False)])
def test_evaluation_date_pattern(validator, doc, date, ok):
    doc["evaluation_date"] = date
    (assert_accepted if ok else assert_rejected)(validator, doc, f"date={date!r}")


# --------------------------------------------------------------------------
# Field 1 — strata reported
# --------------------------------------------------------------------------

def test_reporting_strata_requires_naming_them(validator, doc):
    doc["strata_reported"] = {"reported": True}
    assert_rejected(validator, doc, "reported: true with no strata list")


def test_strata_list_must_be_non_empty(validator, doc):
    doc["strata_reported"] = {"reported": True, "strata": []}
    assert_rejected(validator, doc, "reported: true with an empty strata list")


def test_aggregate_only_contradicts_reported(validator, doc):
    doc["strata_reported"] = {"reported": True, "strata": ["a"], "aggregate_only": True}
    assert_rejected(validator, doc, "aggregate_only and reported cannot both be true")


def test_aggregate_only_with_reported_false_is_valid(validator, doc):
    doc["strata_reported"] = {"reported": False, "aggregate_only": True}
    assert_accepted(validator, doc, "an honest aggregate-only disclosure is valid, just weak")


def test_ci95_must_be_a_pair(validator, doc):
    doc["strata_reported"] = {
        "reported": True,
        "strata": ["rare"],
        "scores": {"rare": {"n": 100, "score": 0.4, "ci95": [0.3]}},
    }
    assert_rejected(validator, doc, "ci95 needs exactly two bounds")


# --------------------------------------------------------------------------
# Field 2 — elicitation budget
# --------------------------------------------------------------------------

def test_harness_and_attempts_are_required(validator, doc):
    doc["elicitation_budget"] = {"harness": "inspect-ai 0.3.0"}
    assert_rejected(validator, doc, "attempts_allowed is required")


def test_multiple_attempts_require_a_resolution_rule(validator, doc):
    doc["elicitation_budget"]["attempts_allowed"] = 3
    assert_rejected(validator, doc, "best-of-n vs majority-vote changes what the score means")


def test_multiple_attempts_cannot_resolve_as_single(validator, doc):
    doc["elicitation_budget"]["attempts_allowed"] = 3
    doc["elicitation_budget"]["attempt_resolution"] = "single"
    assert_rejected(validator, doc, "'single' is incoherent with 3 attempts")


def test_multiple_attempts_with_best_of_n_is_valid(validator, doc):
    doc["elicitation_budget"]["attempts_allowed"] = 3
    doc["elicitation_budget"]["attempt_resolution"] = "best_of_n"
    assert_accepted(validator, doc, "attempts disclosed and resolved")


def test_zero_attempts_is_rejected(validator, doc):
    doc["elicitation_budget"]["attempts_allowed"] = 0
    assert_rejected(validator, doc, "minimum is 1")


def test_token_budget_accepts_a_qualifying_string(validator, doc):
    doc["elicitation_budget"]["token_budget"] = "100k cap; 34k mean consumed"
    assert_accepted(validator, doc, "string form exists so budgets can carry a note")


# --------------------------------------------------------------------------
# Field 3 — contamination controls
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "type_name", ["direct", "derivative", "temporal", "distributional", "acquired"]
)
def test_every_contamination_type_is_required(validator, doc, type_name):
    doc["contamination_controls"].pop(type_name)
    assert_rejected(validator, doc, f"the five-way split forces an answer on {type_name}")


def test_control_status_enum_is_closed(validator, doc):
    doc["contamination_controls"]["direct"] = "probably_fine"
    assert_rejected(validator, doc, "only controlled/not_controlled/unknown/n-a")


@pytest.mark.parametrize("status", ["controlled", "not_controlled", "unknown", "n/a"])
def test_all_four_statuses_are_accepted(validator, doc, status):
    doc["contamination_controls"]["direct"] = status
    if status == "controlled":
        doc["contamination_controls"]["notes"] = "n-gram overlap run against the corpus."
    assert_accepted(validator, doc, f"{status} is a real answer")


@pytest.mark.parametrize(
    "type_name", ["direct", "derivative", "temporal", "distributional"]
)
def test_a_controlled_claim_requires_notes(validator, doc, type_name):
    doc["contamination_controls"][type_name] = "controlled"
    assert_rejected(validator, doc, "an unsubstantiated 'controlled' claim is not a control")


def test_controlled_claim_with_empty_notes_is_rejected(validator, doc):
    doc["contamination_controls"]["direct"] = "controlled"
    doc["contamination_controls"]["notes"] = ""
    assert_rejected(validator, doc, "notes must be non-empty, not merely present")


def test_acquired_controlled_requires_stating_transcript_review(validator, doc):
    """Type 5 is a property of the run. Transcript review is its evidence, so the
    schema will not accept the claim without an answer on whether it was done."""
    doc["contamination_controls"]["acquired"] = "controlled"
    doc["contamination_controls"]["notes"] = "Network disabled for the scoring run."
    assert_rejected(validator, doc, "acquired: controlled without transcripts_reviewed")


def test_acquired_controlled_requires_stating_boundary_monitoring(validator, doc):
    """Level 5c defeats network isolation itself, and the system's own transcript
    cannot establish that the boundary held. So the claim must say whether the
    boundary was watched."""
    doc["contamination_controls"].update(
        {
            "acquired": "controlled",
            "notes": "Network disabled for the scoring run.",
            "transcripts_reviewed": True,
        }
    )
    assert_rejected(validator, doc, "acquired: controlled without boundary_integrity_monitored")


def test_acquired_controlled_fully_evidenced_is_valid(validator, doc):
    doc["contamination_controls"].update(
        {
            "acquired": "controlled",
            "notes": "Network disabled; transcripts reviewed for tool calls.",
            "network_access_during_eval": False,
            "transcripts_reviewed": True,
            "boundary_integrity_monitored": True,
        }
    )
    assert_accepted(validator, doc, "the evidenced form of the claim")


@pytest.mark.parametrize("value,ok", [(True, True), (False, True), ("unknown", True),
                                      ("n/a", True), ("maybe", False), (1, False)])
def test_tristate_accepts_unknown_but_not_arbitrary_strings(validator, doc, value, ok):
    doc["contamination_controls"]["network_access_during_eval"] = value
    (assert_accepted if ok else assert_rejected)(validator, doc, f"tristate={value!r}")


# --------------------------------------------------------------------------
# Field 4 — regeneration
# --------------------------------------------------------------------------

def test_claiming_a_published_procedure_requires_a_location(validator, doc):
    doc["regeneration"] = {"procedure_published": True}
    assert_rejected(validator, doc, "'published' with nowhere to find it")


def test_published_procedure_with_empty_url_is_rejected(validator, doc):
    doc["regeneration"] = {"procedure_published": True, "procedure_url": ""}
    assert_rejected(validator, doc, "procedure_url must be non-empty")


def test_published_procedure_with_url_is_valid(validator, doc):
    doc["regeneration"] = {
        "procedure_published": True,
        "procedure_url": "https://example.org/generate",
    }
    assert_accepted(validator, doc, "regeneration properly disclosed")


def test_artifact_only_release_is_valid(validator, doc):
    doc["regeneration"] = {"procedure_published": False, "artifact_only": True}
    assert_accepted(validator, doc, "artifact-only is honest, and warned about, not invalid")
