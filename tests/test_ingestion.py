import pytest
from app.models import JobExtraction, ForensicFlag, OsintFinding


def test_job_extraction_model_defaults():
    extraction = JobExtraction()
    assert extraction.company_name is None
    assert extraction.parent_company is None
    assert extraction.salary_annual is None
    assert extraction.is_space_deeptech is False
    assert extraction.raw_skills_list == []


def test_job_extraction_model_validation():
    extraction = JobExtraction(
        company_name="Test Company",
        salary_annual=85000.0,
        salary_currency="USD",
        hours_contracted_daily=8.0,
        is_space_deeptech=True,
        raw_skills_list=["Python", "FastAPI"]
    )
    assert extraction.company_name == "Test Company"
    assert extraction.salary_annual == 85000.0
    assert extraction.is_space_deeptech is True
    assert len(extraction.raw_skills_list) == 2


def test_forensic_flag_model():
    flag = ForensicFlag(
        pattern_id="unlimited_pto",
        confidence=85,
        evidence="We offer unlimited PTO",
        triggered=True
    )
    assert flag.pattern_id == "unlimited_pto"
    assert flag.confidence == 85
    assert flag.triggered is True
