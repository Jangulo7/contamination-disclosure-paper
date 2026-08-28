"""Shared fixtures for the Contamination Disclosure test suite."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "templates" / "disclosure.schema.json"


@pytest.fixture(scope="session")
def schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def validator(schema) -> Draft202012Validator:
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


@pytest.fixture(scope="session")
def validate_module():
    """Import docs/validate.py by path — it is a script, not a package."""
    spec = importlib.util.spec_from_file_location(
        "disclosure_validate", ROOT / "docs" / "validate.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["disclosure_validate"] = module
    spec.loader.exec_module(module)
    return module


_MINIMAL = {
    "disclosure_version": "1.1",
    "benchmark": {"name": "Example Benchmark"},
    "strata_reported": {"reported": False},
    "elicitation_budget": {"harness": "inspect-ai 0.3.0", "attempts_allowed": 1},
    "contamination_controls": {
        "direct": "unknown",
        "derivative": "unknown",
        "temporal": "unknown",
        "distributional": "unknown",
        "acquired": "unknown",
    },
    "regeneration": {"procedure_published": False},
}


@pytest.fixture
def doc():
    """A minimal record that validates.

    Deliberately all-'unknown': the specification's central design claim is that
    an honest declaration of ignorance is a valid disclosure, so the baseline
    fixture is the one a reader with no corpus access could actually file.
    """
    return copy.deepcopy(_MINIMAL)
