import json
from google import genai
from google.genai import types
from app.models import SynthesisReport
from app.agents.extractor import get_client, get_model


async def synthesize_report(pipeline_data_dict: dict) -> SynthesisReport:
    client = get_client()

    system_prompt = (
        "You are assembling a final job analysis report. You will receive pre-computed data "
        "from multiple upstream pipeline stages. Your job is to write the narrative sections only — "
        "do not recalculate numbers, do not modify flagged anti-patterns, do not add ethical "
        "judgments beyond what the ethical gate has already returned.\n\n"
        "Write in plain, direct language. No corporate tone. No hedging. No bullet spam. "
        "If something is bad, say it is bad and why. If data is missing, say so explicitly "
        "rather than omitting it.\n\n"
        "Sections to produce:\n"
        "1. 'summary': 2–3 sentence plain-language summary of the overall offer quality\n"
        "2. 'wage_narrative': 1–2 sentences contextualizing the effective hourly wage vs. stated salary\n"
        "3. 'life_narrative': 1–2 sentences contextualizing the discretionary hours figure\n"
        "4. 'osint_summary': plain-language synthesis of OSINT findings, 2–4 sentences\n\n"
        "Do not reproduce raw JSON. Do not add sections not listed above.\n\n"
        "Return strictly valid JSON with keys: summary, wage_narrative, life_narrative, osint_summary."
    )

    # Sanitize potentially unsafe fields derived from user input before injecting into the prompt
    sanitized_data = dict(pipeline_data_dict)
    if "company_name" in sanitized_data and sanitized_data["company_name"]:
        sanitized_data["company_name"] = sanitized_data["company_name"].replace("<", "").replace(">", "").strip()
    if "role_title" in sanitized_data and sanitized_data["role_title"]:
        sanitized_data["role_title"] = sanitized_data["role_title"].replace("<", "").replace(">", "").strip()

    pipeline_output_json = json.dumps(sanitized_data, ensure_ascii=False)
    user_content = f"Input data (trusted — pre-processed by upstream pipeline stages):\n{pipeline_output_json}"

    # Temperature 0.3 as specified for creative variation
    response = client.models.generate_content(
        model=get_model(),
        contents=user_content,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3,
            response_mime_type="application/json",
            response_schema=SynthesisReport,
        )
    )

    text = response.text
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    report_dict = json.loads(text)
    report = SynthesisReport(**report_dict)

    # Post-processing: Burnout validation
    # If burnout_triggered is True, the life_narrative must reference it explicitly
    if pipeline_data_dict.get("burnout_triggered", False):
        narrative_lower = report.life_narrative.lower()
        if "burnout" not in narrative_lower and "critical threshold" not in narrative_lower:
            report.life_narrative += " This falls below the critical 2.5-hour daily burnout threshold, creating a high burnout vector."

    # Post-processing: Stated salary is market rate
    if pipeline_data_dict.get("salary_is_market_rate", False):
        if "no salary" not in report.wage_narrative.lower():
            report.wage_narrative += " Note: No salary information was provided in the original job description. Stated salary is an online-searched market rate estimation."

    # Post-processing: Ethical lockout validation
    if pipeline_data_dict.get("ethical_status") == "LOCKOUT":
        summary_lower = report.summary.lower()
        if "ethical" not in summary_lower and "lockout" not in summary_lower and "objection" not in summary_lower:
            report.summary += " This role is flagged with an Ethical Compliance Lockout due to association with restricted sectors/activities."

    # Post-processing: OSINT uncertainty validation
    # If all findings are LOW confidence, ensure narrative mentions data was insufficient
    findings = pipeline_data_dict.get("osint_findings", [])
    if findings and all(f.get("uncertainty_rating") == "LOW" for f in findings):
        report.osint_summary = (
            "Available public registries and financial datasets provided sparse info on this company, "
            "indicating low confidence or insufficient public footprint."
        )

    return report
