import json
from rapidfuzz import fuzz
from typing import Tuple, Optional


def check_ethical_violations(company_name: Optional[str], parent_company: Optional[str]) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Checks company_name and parent_company against the ethical violations list.
    Returns:
        (status, category_flagged, matched_entity)
        where status is 'LOCKOUT' (strong fuzzy match >= 90), 'WARNING' (partial fuzzy match 70-89), or 'PASS'.
    """
    if not company_name:
        return "PASS", None, None

    # Load ethical violations
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(BASE_DIR, "data", "ethical_violations.json")
    with open(json_path, "r", encoding="utf-8") as f:
        violations = json.load(f)

    highest_score = 0
    matched_category = None
    matched_entity = None

    candidates = []
    if company_name:
        candidates.append(company_name)
    if parent_company:
        candidates.append(parent_company)

    for category, companies in violations.items():
        for unethical_company in companies:
            for candidate in candidates:
                # Use rapidfuzz ratio
                score = fuzz.ratio(candidate.lower(), unethical_company.lower())
                # Also partial ratio for cases like "McKinsey (pharma division)" vs "McKinsey"
                partial_score = fuzz.partial_ratio(candidate.lower(), unethical_company.lower())
                best_score = max(score, partial_score)

                if best_score > highest_score:
                    highest_score = best_score
                    matched_category = category
                    matched_entity = unethical_company

    if highest_score >= 90.0:
        return "LOCKOUT", matched_category, matched_entity
    elif highest_score >= 70.0:
        return "WARNING", matched_category, matched_entity

    return "PASS", None, None
