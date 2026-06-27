def calculate_effective_salary(
    salary_annual: float | None,
    working_days_annual: float | None = None,
    benefits_monetary_daily: float | None = None,
    travel_cost_daily: float | None = None,
    medical_cost_daily: float | None = None,
    hours_contracted_daily: float | None = None,
    commute_time_am_hours: float | None = None,
    commute_time_pm_hours: float | None = None,
    overtime_hours_daily: float | None = None,
    medical_hours_daily: float | None = None,
) -> float:
    if not salary_annual:
        return 0.0

    days = working_days_annual if (working_days_annual and working_days_annual > 0) else 240.0
    s_base = salary_annual / days

    b_monetary = benefits_monetary_daily or 0.0
    c_travel = travel_cost_daily or 0.0
    c_medical = medical_cost_daily or 0.0

    h_contract = hours_contracted_daily if hours_contracted_daily is not None else 8.0
    t_am = commute_time_am_hours or 0.0
    t_pm = commute_time_pm_hours or 0.0
    h_overtime = overtime_hours_daily or 0.0
    t_medical = medical_hours_daily or 0.0

    numerator = s_base + b_monetary - c_travel - c_medical
    denominator = h_contract + t_am + t_pm + h_overtime + t_medical

    if denominator <= 0:
        return 0.0

    return round(numerator / denominator, 2)


def calculate_discretionary_hours(
    hours_contracted_daily: float | None,
    commute_time_am_hours: float | None = None,
    commute_time_pm_hours: float | None = None,
    overtime_hours_daily: float | None = None,
    decompress_hours: float | None = None,
    medical_hours_daily: float | None = None,
    is_space_deeptech: bool = False,
) -> float:
    h_contract = hours_contracted_daily if hours_contracted_daily is not None else 8.0
    t_am = commute_time_am_hours or 0.0
    t_pm = commute_time_pm_hours or 0.0
    h_overtime = overtime_hours_daily or 0.0
    t_medical = medical_hours_daily or 0.0

    t_decompress = decompress_hours if decompress_hours is not None else 0.5
    if is_space_deeptech:
        t_decompress *= 1.5

    life_discretionary = 13.5 - (h_contract + t_am + t_pm + h_overtime + t_decompress + t_medical)
    return round(life_discretionary, 2)
