from pydantic import BaseModel, Field
from typing import List, Optional


class JobExtraction(BaseModel):
    company_name: Optional[str] = Field(default=None, description="The name of the company offering the job")
    parent_company: Optional[str] = Field(default=None, description="The parent company of the offering company, if known")
    role_title: Optional[str] = Field(default=None, description="The title of the job role")
    salary_annual: Optional[float] = Field(default=None, description="Stated annual gross base salary in local currency. If a range is provided, this represents the minimum of the range.")
    salary_annual_max: Optional[float] = Field(default=None, description="The maximum stated annual gross base salary in local currency if a range is provided; null otherwise.")
    salary_currency: Optional[str] = Field(default=None, description="ISO 4217 currency code e.g., 'JPY', 'USD'")
    salary_is_market_rate: bool = Field(default=False, description="Whether the salary is an online-searched market rate")
    benefits_monetary_daily: Optional[float] = Field(default=None, description="Sum of quantifiable daily benefit values (e.g. housing, meal allowance)")
    hours_contracted_daily: Optional[float] = Field(default=None, description="Contracted hours per day")
    overtime_hours_daily: Optional[float] = Field(default=None, description="Expected daily overtime hours if stated; null otherwise")
    commute_time_am_hours: Optional[float] = Field(default=None, description="Door-to-door commute time in AM hours")
    commute_time_pm_hours: Optional[float] = Field(default=None, description="Door-to-door commute time in PM hours")
    travel_cost_daily: Optional[float] = Field(default=None, description="Daily travel/commute out-of-pocket costs")
    industry_sector: Optional[str] = Field(default=None, description="Industry sector of the company")
    is_space_deeptech: bool = Field(default=False, description="Whether the industry/role is in Aerospace or Deep-Tech")
    raw_skills_list: List[str] = Field(default_factory=list, description="Verbatim list of all required skills or tools")
    raw_pto_description: Optional[str] = Field(default=None, description="Exact quoted PTO/time-off language from the text")
    raw_overtime_language: Optional[str] = Field(default=None, description="Exact quoted overtime language from the text")
    raw_hardware_language: Optional[str] = Field(default=None, description="Exact quoted equipment/hardware language from the text")
    working_days_annual: Optional[float] = Field(default=None, description="Stated or standard working days per year for the jurisdiction")


class ForensicFlag(BaseModel):
    pattern_id: str
    confidence: int = Field(..., ge=0, le=100)
    evidence: Optional[str] = None
    triggered: bool


class CorporateSpeakMatch(BaseModel):
    pattern: str
    matched_text: str
    risk: str


class OsintFinding(BaseModel):
    query_id: str
    finding: str
    source_url: Optional[str] = None
    uncertainty_rating: str = Field(..., description="'HIGH' or 'MEDIUM' or 'LOW'")
    flag: Optional[str] = Field(default=None, description="'UNPROFITABILITY_TRAP' or 'LAW_ENFORCEMENT_COLLUSION' or 'ZERO_SUM_MARKET' or null")


class SynthesisReport(BaseModel):
    summary: str
    wage_narrative: str
    life_narrative: str
    osint_summary: str


class ForensicFlagsWrapper(BaseModel):
    flags: List[ForensicFlag]


class CorporateSpeakMatchesWrapper(BaseModel):
    matches: List[CorporateSpeakMatch]


class OsintFindingsWrapper(BaseModel):
    findings: List[OsintFinding]


class MarketSalaryResult(BaseModel):
    salary_annual: Optional[float] = Field(default=None, description="Average annual gross base salary determined from online search")
    salary_currency: str = Field(default="USD", description="3-letter ISO currency code of the determined salary")


