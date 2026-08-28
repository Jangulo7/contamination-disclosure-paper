#!/usr/bin/env python3
"""
Validate a Contamination Disclosure record against disclosure.schema.json.

    python docs/validate.py examples/*.yaml
    python docs/validate.py my-eval/disclosure.yaml

Accepts YAML or JSON. Exits non-zero on any validation failure, so it can be
dropped straight into CI.

Note: templates/disclosure.yaml is the BLANK form and is expected NOT to
validate (it has no benchmark name and no strata). That is intentional — an
empty form is not a disclosure. Validate filled forms, not the template.

Requires: pip install jsonschema pyyaml
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    sys.exit("Missing dependencies. Run: pip install jsonschema pyyaml")

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "templates" / "disclosure.schema.json"


def load(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    failed = 0
    for arg in argv:
        path = Path(arg)
        if not path.is_file():
            print(f"FAIL  {path} — not a file")
            failed += 1
            continue

        try:
            doc = load(path)
        except Exception as exc:
            print(f"FAIL  {path} — could not parse: {exc}")
            failed += 1
            continue

        errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
        if errors:
            failed += 1
            print(f"FAIL  {path} — {len(errors)} error(s)")
            for err in errors:
                where = ".".join(str(p) for p in err.path) or "<root>"
                print(f"        {where}: {err.message}")
        else:
            print(f"OK    {path}")
            warn(doc, path)

    print()
    print(f"{len(argv) - failed}/{len(argv)} valid")
    return 1 if failed else 0


def warn(doc: dict, path: Path) -> None:
    """Non-fatal notes. A valid disclosure can still be a weak one."""
    notes = []

    controls = doc.get("contamination_controls", {})
    keys = ("direct", "derivative", "temporal", "distributional", "acquired")
    unknowns = [k for k in keys if controls.get(k) == "unknown"]
    if len(unknowns) == len(keys):
        notes.append("all five contamination controls are 'unknown' — valid, but "
                     "the reader learns only that nothing was checked")

    net = controls.get("network_access_during_eval")
    reviewed = controls.get("transcripts_reviewed")
    if net in (True, "true"):
        notes.append("network access was enabled during evaluation — type 5b (acquired) "
                     "exposure is live; transcript review is the primary detection method")
        if reviewed not in (True, "true"):
            notes.append("network access enabled AND transcripts not reviewed — an "
                         "acquired-contamination claim cannot be supported from this run")
    if controls.get("acquired") == "controlled" and net in (True, "true") \
            and reviewed not in (True, "true"):
        notes.append("'acquired: controlled' is asserted with network access on and no "
                     "transcript review — this claim is not evidenced")
    boundary = controls.get("boundary_integrity_monitored")
    if controls.get("acquired") == "controlled" and boundary not in (True, "true"):
        notes.append("'acquired: controlled' is asserted without boundary-integrity "
                     "monitoring — no egress monitoring, canary or post-run boundary "
                     "check is recorded, so a level-5c failure would not have been seen")
    if controls.get("acquired") == "controlled":
        notes.append("reminder: acquired status is a property of THIS run and does not "
                     "transfer to other evaluations of the same benchmark")

    strata = doc.get("strata_reported", {})
    if strata.get("reported") is False or strata.get("aggregate_only") is True:
        notes.append("aggregate-only reporting — state why, and what it means for the reader")

    budget = doc.get("elicitation_budget", {})
    if not str(budget.get("harness", "")).strip():
        notes.append("no harness recorded — the score is not reproducible")
    if budget.get("still_rising_at_max_budget") in (True, "true"):
        notes.append("performance still rising at max budget — the score is a LOWER BOUND; "
                     "make sure the prose says so")

    if doc.get("regeneration", {}).get("artifact_only") is True:
        notes.append("artifact-only release — this benchmark should be assumed to "
                     "degrade after publication")

    for note in notes:
        print(f"      note: {note}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
