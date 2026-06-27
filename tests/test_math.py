import pytest
from app.math_engine import calculate_effective_salary, calculate_discretionary_hours


def test_calculate_effective_salary_basic():
    # Base: 120,000 / 240 days = 500 per day
    # Num: 500 + 0 - 0 - 0 = 500
    # Den: 8 (contracted) + 0 (commute) + 0 (overtime) = 8
    # Effective: 500 / 8 = 62.5
    res = calculate_effective_salary(
        salary_annual=120000.0,
        working_days_annual=240.0,
        hours_contracted_daily=8.0
    )
    assert res == 62.5


def test_calculate_effective_salary_erosion():
    # Base: 120,000 / 240 = 500 per day
    # Benefits: +50 daily
    # Out of pocket: -10 travel
    # Num: 500 + 50 - 10 - 0 = 540
    # Commutes: AM = 1hr, PM = 1hr
    # Overtime: 2hrs daily
    # Den: 8 (contract) + 1 (AM) + 1 (PM) + 2 (Overtime) = 12 hours
    # Effective: 540 / 12 = 45.0
    res = calculate_effective_salary(
        salary_annual=120000.0,
        working_days_annual=240.0,
        benefits_monetary_daily=50.0,
        travel_cost_daily=10.0,
        hours_contracted_daily=8.0,
        commute_time_am_hours=1.0,
        commute_time_pm_hours=1.0,
        overtime_hours_daily=2.0
    )
    assert res == 45.0


def test_calculate_effective_salary_zero_cases():
    assert calculate_effective_salary(None) == 0.0
    assert calculate_effective_salary(100000.0, hours_contracted_daily=0.0) == 0.0


def test_calculate_discretionary_hours_basic():
    # Basic: 13.5 - (8.0 + 0 + 0 + 0 + 0.5 + 0) = 5.0 hours
    res = calculate_discretionary_hours(
        hours_contracted_daily=8.0,
        commute_time_am_hours=0.0,
        commute_time_pm_hours=0.0,
        overtime_hours_daily=0.0,
        decompress_hours=0.5
    )
    assert res == 5.0


def test_calculate_discretionary_hours_burnout():
    # Commute: AM = 1hr, PM = 1.5hr
    # Overtime: 2.0hrs
    # Contract: 8.0hrs
    # Decompress: 0.5hrs
    # Total awake hours used: 8.0 + 1.0 + 1.5 + 2.0 + 0.5 = 13.0 hrs
    # Remaining: 13.5 - 13.0 = 0.5 hrs (triggers burnout < 2.5)
    res = calculate_discretionary_hours(
        hours_contracted_daily=8.0,
        commute_time_am_hours=1.0,
        commute_time_pm_hours=1.5,
        overtime_hours_daily=2.0,
        decompress_hours=0.5
    )
    assert res == 0.5


def test_calculate_discretionary_hours_deeptech():
    # Space/DeepTech multiplies decompress_hours (0.5 * 1.5 = 0.75)
    # Total awake hours: 8.0 (contract) + 0.75 (decompress) = 8.75 hrs
    # Remaining: 13.5 - 8.75 = 4.75 hrs
    res = calculate_discretionary_hours(
        hours_contracted_daily=8.0,
        decompress_hours=0.5,
        is_space_deeptech=True
    )
    assert res == 4.75
