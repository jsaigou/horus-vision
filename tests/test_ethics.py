import pytest
from app.agents.ethics import check_ethical_violations


def test_ethical_violations_pass():
    status, category, matched = check_ethical_violations("Healthy Corp", None)
    assert status == "PASS"
    assert category is None
    assert matched is None


def test_ethical_violations_lockout_exact():
    status, category, matched = check_ethical_violations("Anduril", None)
    assert status == "LOCKOUT"
    assert category == "autonomous_weapons"
    assert matched == "Anduril"


def test_ethical_violations_lockout_fuzzy():
    # Fuzzy matching should catch slight spelling errors or variations
    status, category, matched = check_ethical_violations("Anduril Industries", None)
    assert status == "LOCKOUT"
    assert category == "autonomous_weapons"
    assert matched == "Anduril"


def test_ethical_violations_lockout_parent():
    # Check parent matching works
    status, category, matched = check_ethical_violations("Unknown Subsidiary Ltd", "Palantir")
    assert status == "LOCKOUT"
    assert category == "autonomous_weapons"
    assert matched == "Palantir"


def test_ethical_violations_warning():
    # Partial ratio matching for things like "McKinsey (pharma division)" vs "McKinsey Corp"
    status, category, matched = check_ethical_violations("Philip Morris International", None)
    # Philip Morris is in tobacco, should match "Philip Morris" with high confidence -> LOCKOUT or WARNING
    assert status in ["LOCKOUT", "WARNING"]
    assert category == "tobacco"
    assert matched == "Philip Morris"
