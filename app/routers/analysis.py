import os
import re
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from app.agents.extractor import extract_job_data
from app.agents.forensic import analyze_forensic_patterns
from app.agents.ethics import check_ethical_violations
from app.agents.osint import run_osint_grounding, search_market_salary
from app.agents.decoder import decode_corporate_speak
from app.agents.synthesizer import synthesize_report
from app.math_engine import calculate_effective_salary, calculate_discretionary_hours
from app.models import JobExtraction


router = APIRouter()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


def secure_filename(filename: str) -> str:
    # Replace any character that is not alphanumeric, dot, hyphen, or underscore with underscore
    name = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return name


@router.post("/analyze", response_class=HTMLResponse)
async def analyze_job(
    request: Request,
    job_text: Optional[str] = Form(None),
    job_file: Optional[UploadFile] = File(None)
):
    file_bytes = None
    mime_type = None
    
    # 1. Validation & File Ingestion
    if job_file and job_file.filename:
        # Secure filename
        safe_name = secure_filename(job_file.filename)
        
        # MIME Type check (basic validation)
        content_type = job_file.content_type or ""
        allowed_mimes = ["application/pdf", "image/png", "image/jpeg", "image/jpg", "text/plain"]
        if content_type not in allowed_mimes:
            # We can also check by file extension for simple cases
            ext = os.path.splitext(safe_name)[1].lower()
            if ext not in [".pdf", ".png", ".jpg", ".jpeg", ".txt"]:
                return templates.TemplateResponse(
                    request=request,
                    name="error.html",
                    context={"error_msg": "Unsupported file format. Supported formats: PDF, PNG, JPG, JPEG, TXT."}
                )

        # 5MB Limit check
        file_bytes = await job_file.read()
        if len(file_bytes) > 5 * 1024 * 1024:
            return templates.TemplateResponse(
                request=request,
                name="error.html",
                context={"error_msg": "File size exceeds the 5MB limit."}
            )
        
        mime_type = content_type

    if not file_bytes and (not job_text or not job_text.strip()):
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error_msg": "Please paste job text or upload a job file."}
        )

    # 2. Stage 1: Ingestion & Extraction (Gemini 3.5 Flash)
    try:
        extracted = await extract_job_data(
            job_text=job_text,
            file_bytes=file_bytes,
            mime_type=mime_type
        )
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error_msg": f"Extraction failed. Please check your inputs or GEMINI_API_KEY. Details: {e}"}
        )

    # Check for missing salary:
    # If salary_annual is null after extraction, search online to determine the market rate.
    if not extracted.salary_annual:
        market_res = await search_market_salary(extracted.company_name, extracted.role_title)
        if market_res and market_res.get("salary_annual"):
            extracted.salary_annual = market_res["salary_annual"]
            extracted.salary_currency = market_res.get("salary_currency", "USD")
            extracted.salary_is_market_rate = True
        else:
            return templates.TemplateResponse(
                request=request,
                name="missing_salary.html",
                context={
                    "extracted_data": extracted,
                    "job_text": job_text
                }
            )

    # 3. Stage 3: Ethical Gate Check (static list + rapidfuzz)
    ethical_status, eth_category, eth_entity = check_ethical_violations(
        extracted.company_name,
        extracted.parent_company
    )

    if ethical_status == "LOCKOUT":
        # HALT. Return red lockout response. Pipeline stops here.
        return templates.TemplateResponse(
            request=request,
            name="lockout.html",
            context={
                "company_name": extracted.company_name or "Unknown Company",
                "parent_company": extracted.parent_company,
                "category": eth_category,
                "unethical_match": eth_entity
            }
        )

    # 4. Stage 2: Forensic Text Analyzer (pattern matching + Gemini 3.5 Flash)
    forensic_flags = await analyze_forensic_patterns(extracted)
    triggered_flags = [f for f in forensic_flags if f.triggered]

    # 5. Stage 4: OSINT Grounding (Gemini Managed Agent / Web Search Grounding)
    osint_findings = await run_osint_grounding(
        company_name=extracted.company_name or "Unknown Company",
        parent_company=extracted.parent_company
    )

    # 6. Stage 5: Math Engine (Pure Python)
    effective_wage = calculate_effective_salary(
        salary_annual=extracted.salary_annual,
        working_days_annual=extracted.working_days_annual,
        benefits_monetary_daily=extracted.benefits_monetary_daily,
        travel_cost_daily=extracted.travel_cost_daily,
        medical_cost_daily=extracted.travel_cost_daily, # amortized medical maintenance
        hours_contracted_daily=extracted.hours_contracted_daily,
        commute_time_am_hours=extracted.commute_time_am_hours,
        commute_time_pm_hours=extracted.commute_time_pm_hours,
        overtime_hours_daily=extracted.overtime_hours_daily,
        medical_hours_daily=0.0 # default medical time cost
    )

    discretionary_hours = calculate_discretionary_hours(
        hours_contracted_daily=extracted.hours_contracted_daily,
        commute_time_am_hours=extracted.commute_time_am_hours,
        commute_time_pm_hours=extracted.commute_time_pm_hours,
        overtime_hours_daily=extracted.overtime_hours_daily,
        decompress_hours=0.5, # standard decompression time
        medical_hours_daily=0.0,
        is_space_deeptech=extracted.is_space_deeptech
    )

    burnout_triggered = discretionary_hours < 2.5

    # 7. Corporate Speak Decoder Matches (P3)
    text_to_decode = job_text or (extracted.company_name or "") + " " + (extracted.role_title or "")
    corp_matches = await decode_corporate_speak(text_to_decode)

    # 8. Report Synthesis (Stage 6 - P4 Synthesis)
    pipeline_output_dict = {
        "company_name": extracted.company_name,
        "role_title": extracted.role_title,
        "salary_stated_annual": extracted.salary_annual,
        "salary_currency": extracted.salary_currency or "USD",
        "salary_is_market_rate": extracted.salary_is_market_rate,
        "salary_effective_hourly": effective_wage,
        "life_discretionary_hours": discretionary_hours,
        "burnout_triggered": burnout_triggered,
        "ethical_status": ethical_status,
        "math_inputs": {
            "hours_contracted_daily": extracted.hours_contracted_daily or 8.0,
            "overtime_hours_daily": extracted.overtime_hours_daily or 0.0,
            "commute_am_hours": extracted.commute_time_am_hours or 0.0,
            "commute_pm_hours": extracted.commute_time_pm_hours or 0.0,
            "decompress_hours": 0.5,
            "medical_hours_daily": 0.0,
            "travel_cost_daily": extracted.travel_cost_daily or 0.0,
            "medical_cost_daily": 0.0,
            "benefits_daily": extracted.benefits_monetary_daily or 0.0
        },
        "forensic_flags": [f.model_dump() for f in triggered_flags],
        "corporate_speak_matches": [m.model_dump() for m in corp_matches],
        "osint_findings": [f.model_dump() for f in osint_findings]
    }

    synthesis_report = await synthesize_report(pipeline_output_dict)

    # Render final report panel
    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "pipeline_data": pipeline_output_dict,
            "report": synthesis_report,
            "ethical_status": ethical_status,
            "eth_category": eth_category,
            "eth_entity": eth_entity,
            "extracted_raw": extracted
        }
    )


@router.post("/analyze-manual-salary", response_class=HTMLResponse)
async def analyze_manual_salary(
    request: Request,
    job_text: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    role_title: Optional[str] = Form(None),
    salary_annual: float = Form(...),
    salary_currency: str = Form("USD"),
    hours_contracted_daily: float = Form(8.0),
    is_space_deeptech: bool = Form(False)
):
    # This handles the fallback when a salary is not found in the initial document extraction
    # We construct a mock JobExtraction and proceed with manual inputs
    extracted = JobExtraction(
        company_name=company_name,
        role_title=role_title,
        salary_annual=salary_annual,
        salary_currency=salary_currency,
        hours_contracted_daily=hours_contracted_daily,
        is_space_deeptech=is_space_deeptech,
        raw_skills_list=[]
    )
    
    # Run full analysis
    return await analyze_job_with_extracted(request, extracted, job_text or "")


async def analyze_job_with_extracted(request: Request, extracted: JobExtraction, job_text: str):
    # Reusable method for manual salary entry
    ethical_status, eth_category, eth_entity = check_ethical_violations(
        extracted.company_name,
        extracted.parent_company
    )

    if ethical_status == "LOCKOUT":
        return templates.TemplateResponse(
            request=request,
            name="lockout.html",
            context={
                "company_name": extracted.company_name or "Unknown Company",
                "parent_company": extracted.parent_company,
                "category": eth_category,
                "unethical_match": eth_entity
            }
        )

    forensic_flags = await analyze_forensic_patterns(extracted)
    triggered_flags = [f for f in forensic_flags if f.triggered]

    osint_findings = await run_osint_grounding(
        company_name=extracted.company_name or "Unknown Company",
        parent_company=extracted.parent_company
    )

    effective_wage = calculate_effective_salary(
        salary_annual=extracted.salary_annual,
        working_days_annual=extracted.working_days_annual,
        benefits_monetary_daily=extracted.benefits_monetary_daily,
        travel_cost_daily=extracted.travel_cost_daily,
        medical_cost_daily=0.0,
        hours_contracted_daily=extracted.hours_contracted_daily,
        commute_time_am_hours=extracted.commute_time_am_hours,
        commute_time_pm_hours=extracted.commute_time_pm_hours,
        overtime_hours_daily=extracted.overtime_hours_daily,
        medical_hours_daily=0.0
    )

    discretionary_hours = calculate_discretionary_hours(
        hours_contracted_daily=extracted.hours_contracted_daily,
        commute_time_am_hours=extracted.commute_time_am_hours,
        commute_time_pm_hours=extracted.commute_time_pm_hours,
        overtime_hours_daily=extracted.overtime_hours_daily,
        decompress_hours=0.5,
        medical_hours_daily=0.0,
        is_space_deeptech=extracted.is_space_deeptech
    )

    burnout_triggered = discretionary_hours < 2.5
    corp_matches = await decode_corporate_speak(job_text or (extracted.company_name or "") + " " + (extracted.role_title or ""))

    pipeline_output_dict = {
        "company_name": extracted.company_name,
        "role_title": extracted.role_title,
        "salary_stated_annual": extracted.salary_annual,
        "salary_currency": extracted.salary_currency or "USD",
        "salary_is_market_rate": extracted.salary_is_market_rate,
        "salary_effective_hourly": effective_wage,
        "life_discretionary_hours": discretionary_hours,
        "burnout_triggered": burnout_triggered,
        "ethical_status": ethical_status,
        "math_inputs": {
            "hours_contracted_daily": extracted.hours_contracted_daily or 8.0,
            "overtime_hours_daily": extracted.overtime_hours_daily or 0.0,
            "commute_am_hours": extracted.commute_time_am_hours or 0.0,
            "commute_pm_hours": extracted.commute_time_pm_hours or 0.0,
            "decompress_hours": 0.5,
            "medical_hours_daily": 0.0,
            "travel_cost_daily": extracted.travel_cost_daily or 0.0,
            "medical_cost_daily": 0.0,
            "benefits_daily": extracted.benefits_monetary_daily or 0.0
        },
        "forensic_flags": [f.model_dump() for f in triggered_flags],
        "corporate_speak_matches": [m.model_dump() for m in corp_matches],
        "osint_findings": [f.model_dump() for f in osint_findings]
    }

    synthesis_report = await synthesize_report(pipeline_output_dict)

    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "pipeline_data": pipeline_output_dict,
            "report": synthesis_report,
            "ethical_status": ethical_status,
            "eth_category": eth_category,
            "eth_entity": eth_entity,
            "extracted_raw": extracted
        }
    )
