"""End-to-end behaviour of docs/validate.py: exit codes (so CI can gate on it)
and the non-fatal warning layer that separates a *valid* disclosure from a
*strong* one.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = sorted((ROOT / "examples").glob("*.yaml"))
BLANK_TEMPLATE = ROOT / "templates" / "disclosure.yaml"


# --------------------------------------------------------------------------
# Exit codes — CI gates on these
# --------------------------------------------------------------------------

# The worked examples are withheld during double-blind review: their benchmark
# DOIs identify the authors. They are present in the anonymised review mirror
# and are restored at camera-ready. Skip rather than fail, so that a reviewer
# cloning this repository gets a green suite -- but skip loudly, so that their
# absence at camera-ready is not mistaken for a pass.
needs_examples = pytest.mark.skipif(
    not EXAMPLES,
    reason="examples/ withheld for double-blind review; present in the anonymised mirror",
)


@needs_examples
def test_repository_ships_worked_examples():
    assert EXAMPLES, "examples/*.yaml is empty; the worked examples are part of the release"


@needs_examples
def test_shipped_examples_validate(validate_module, capsys):
    assert validate_module.main([str(p) for p in EXAMPLES]) == 0
    assert "FAIL" not in capsys.readouterr().out


def test_blank_template_is_rejected(validate_module, capsys):
    """Documented intent: an empty form is not a disclosure."""
    assert validate_module.main([str(BLANK_TEMPLATE)]) == 1
    out = capsys.readouterr().out
    assert "benchmark.name" in out and "strata_reported.strata" in out


def test_missing_file_fails_rather_than_raising(validate_module, capsys):
    assert validate_module.main([str(ROOT / "no-such-file.yaml")]) == 1
    assert "not a file" in capsys.readouterr().out


def test_unparseable_file_fails_rather_than_raising(validate_module, tmp_path, capsys):
    bad = tmp_path / "broken.yaml"
    bad.write_text("benchmark: [unclosed\n", encoding="utf-8")
    assert validate_module.main([str(bad)]) == 1
    assert "could not parse" in capsys.readouterr().out


def test_no_arguments_prints_usage(validate_module, capsys):
    assert validate_module.main([]) == 2
    assert "validate.py" in capsys.readouterr().out


def test_json_records_are_accepted_too(validate_module, tmp_path, doc, capsys):
    path = tmp_path / "disclosure.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    assert validate_module.main([str(path)]) == 0
    assert "OK" in capsys.readouterr().out


# --------------------------------------------------------------------------
# The warning layer — valid, but weak
# --------------------------------------------------------------------------

def notes_for(validate_module, capsys, doc) -> str:
    validate_module.warn(doc, Path("in-memory"))
    return capsys.readouterr().out


def test_all_unknown_is_valid_but_warned(validate_module, capsys, doc):
    assert "nothing was checked" in notes_for(validate_module, capsys, doc)


def test_network_access_alone_warns(validate_module, capsys, doc):
    doc["contamination_controls"]["network_access_during_eval"] = True
    doc["contamination_controls"]["transcripts_reviewed"] = True
    out = notes_for(validate_module, capsys, doc)
    assert "type 5b" in out
    assert "cannot be supported" not in out


def test_network_on_and_transcripts_unreviewed_warns_hardest(validate_module, capsys, doc):
    """The combination the paper singles out by name."""
    doc["contamination_controls"]["network_access_during_eval"] = True
    doc["contamination_controls"]["transcripts_reviewed"] = False
    assert "cannot be supported" in notes_for(validate_module, capsys, doc)


def test_unevidenced_acquired_claim_is_called_out(validate_module, capsys, doc):
    doc["contamination_controls"].update(
        {
            "acquired": "controlled",
            "notes": "Assumed clean.",
            "network_access_during_eval": True,
            "transcripts_reviewed": False,
        }
    )
    assert "not evidenced" in notes_for(validate_module, capsys, doc)


def test_unmonitored_boundary_is_flagged_on_a_controlled_claim(validate_module, capsys, doc):
    doc["contamination_controls"].update(
        {
            "acquired": "controlled",
            "notes": "Network disabled.",
            "transcripts_reviewed": True,
            "boundary_integrity_monitored": False,
        }
    )
    assert "level-5c failure would not have been seen" in notes_for(validate_module, capsys, doc)


def test_monitored_boundary_clears_the_flag(validate_module, capsys, doc):
    doc["contamination_controls"].update(
        {
            "acquired": "controlled",
            "notes": "Network disabled; egress monitored; canary in the answer key.",
            "transcripts_reviewed": True,
            "boundary_integrity_monitored": True,
        }
    )
    assert "level-5c failure" not in notes_for(validate_module, capsys, doc)


def test_acquired_controlled_always_carries_the_per_run_reminder(validate_module, capsys, doc):
    """Type 5 does not transfer between runs; the reminder fires even when the
    claim is fully evidenced."""
    doc["contamination_controls"].update(
        {
            "acquired": "controlled",
            "notes": "Network disabled; transcripts reviewed.",
            "network_access_during_eval": False,
            "transcripts_reviewed": True,
            "boundary_integrity_monitored": True,
        }
    )
    out = notes_for(validate_module, capsys, doc)
    assert "does not transfer" in out
    assert "not evidenced" not in out


def test_aggregate_only_warns(validate_module, capsys, doc):
    doc["strata_reported"] = {"reported": False, "aggregate_only": True}
    assert "aggregate-only" in notes_for(validate_module, capsys, doc)


def test_empty_harness_warns(validate_module, capsys, doc):
    doc["elicitation_budget"]["harness"] = "   "
    assert "not reproducible" in notes_for(validate_module, capsys, doc)


def test_still_rising_budget_flags_the_score_as_a_lower_bound(validate_module, capsys, doc):
    doc["elicitation_budget"]["still_rising_at_max_budget"] = True
    assert "LOWER BOUND" in notes_for(validate_module, capsys, doc)


def test_artifact_only_warns(validate_module, capsys, doc):
    doc["regeneration"]["artifact_only"] = True
    assert "degrade after publication" in notes_for(validate_module, capsys, doc)


def test_a_strong_disclosure_produces_no_notes(validate_module, capsys, doc):
    doc["strata_reported"] = {"reported": True, "strata": ["rare", "common"]}
    doc["contamination_controls"].update(
        {
            "direct": "controlled",
            "derivative": "not_controlled",
            "notes": "Canary string embedded; source provenance published.",
            "network_access_during_eval": False,
            "transcripts_reviewed": True,
            "boundary_integrity_monitored": True,
        }
    )
    doc["regeneration"] = {
        "procedure_published": True,
        "procedure_url": "https://example.org/generate",
    }
    assert notes_for(validate_module, capsys, doc).strip() == ""


@pytest.mark.parametrize("truthy", [True, "true"])
def test_warnings_accept_both_boolean_and_string_tristates(validate_module, capsys, doc, truthy):
    """YAML gives a bool; a hand-written JSON record may give the string form.
    The tristate definition permits both, so the warning layer must read both."""
    doc["contamination_controls"]["network_access_during_eval"] = truthy
    assert "type 5b" in notes_for(validate_module, capsys, doc)
