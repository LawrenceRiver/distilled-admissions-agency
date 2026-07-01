#!/usr/bin/env python3
"""Advisory score helper for a program fit audit.

This is intentionally conservative. It produces a starting point for a human-
checked scorecard, not an admission probability.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_data(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on environment
        raise SystemExit(
            f"{path} looks like YAML, but PyYAML is not installed. "
            "Install pyyaml or provide JSON."
        ) from exc
    data = yaml.safe_load(text)
    return data or {}


def as_float(value: Any, default: float | None = None) -> float | None:
    if value in (None, "", "Unknown", "unknown", "Need verification"):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def nested(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def mean_known(values: list[float | None], default: float = 50.0) -> float:
    known = [v for v in values if v is not None]
    if not known:
        return default
    return sum(known) / len(known)


def score_gpa(applicant: dict[str, Any], program: dict[str, Any]) -> tuple[float, str]:
    gpa = as_float(applicant.get("gpa"))
    scale = as_float(applicant.get("gpa_scale"), 4.0) or 4.0
    min_gpa = as_float(program.get("minimum_gpa"))
    typical_low = as_float(program.get("typical_gpa_low"))
    typical_high = as_float(program.get("typical_gpa_high"))

    if gpa is None:
        return 0.0, "blocked"

    normalized = gpa / scale * 4.0
    if min_gpa is not None and normalized < min_gpa:
        return 10.0, "hard-gate"
    if typical_low is not None and normalized < typical_low:
        return 45.0, "high"
    if typical_high is not None and normalized >= typical_high:
        return 90.0, "low"
    if min_gpa is not None and normalized <= min_gpa + 0.25:
        return 55.0, "medium"
    return 72.0, "unknown"


def score_tests(applicant: dict[str, Any], program: dict[str, Any]) -> float | None:
    toefl = as_float(nested(applicant, "tests", "toefl"))
    target_toefl = as_float(nested(applicant, "tests", "target_toefl"))
    applicant_toefl = target_toefl if target_toefl is not None else toefl
    min_toefl = as_float(program.get("toefl_min"))
    if min_toefl is None:
        return None
    if applicant_toefl is None:
        return 45.0
    if applicant_toefl < min_toefl:
        return 20.0
    if applicant_toefl >= min_toefl + 10:
        return 85.0
    return 65.0


def score_list_overlap(applicant_terms: list[str], program_terms: list[str]) -> float | None:
    if not applicant_terms or not program_terms:
        return None
    a = {str(x).lower() for x in applicant_terms}
    p = {str(x).lower() for x in program_terms}
    overlap = len(a & p)
    return min(95.0, 45.0 + overlap * 12.5)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--applicant", required=True)
    parser.add_argument("--program", required=True)
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    args = parser.parse_args()

    applicant = load_data(Path(args.applicant))
    program = load_data(Path(args.program))

    gpa_score, gpa_risk = score_gpa(applicant, program)
    if gpa_risk == "blocked":
        result = {
            "band": "blocked",
            "reason": "Applicant GPA missing",
            "hard_score": 0,
            "soft_score": 0,
            "fit_score": 0,
            "gpa_risk": "unknown",
            "evidence_confidence": "blocked",
        }
    else:
        coursework_score = as_float(nested(applicant, "hard_strength", "coursework_score"))
        institution_score = as_float(
            nested(applicant, "hard_strength", "institution_context_score")
        )
        test_score = score_tests(applicant, program)
        hard_score = mean_known(
            [gpa_score, coursework_score, institution_score, test_score],
            default=gpa_score,
        )

        soft_score = mean_known(
            [
                as_float(nested(applicant, "soft_strength", "project_score")),
                as_float(nested(applicant, "soft_strength", "research_score")),
                as_float(nested(applicant, "soft_strength", "product_score")),
                as_float(nested(applicant, "soft_strength", "awards_score")),
                as_float(nested(applicant, "soft_strength", "leadership_score")),
                as_float(nested(applicant, "soft_strength", "creative_story_score")),
            ],
            default=50.0,
        )

        applicant_terms = applicant.get("fit_keywords") or []
        program_terms = program.get("curriculum_keywords") or []
        curriculum_fit = score_list_overlap(applicant_terms, program_terms)
        tolerance = min(
            20.0,
            len(program.get("holistic_review_signals") or []) * 4.0,
        )
        fit_score = mean_known([hard_score, soft_score, curriculum_fit], default=hard_score)
        fit_score = min(100.0, fit_score + tolerance * 0.5)

        if gpa_risk == "hard-gate":
            band = "not-advised"
        elif hard_score < 45:
            band = "high-reach"
        elif fit_score >= 78 and gpa_risk in {"low", "unknown"}:
            band = "main-stable"
        elif fit_score >= 65:
            band = "main"
        elif fit_score >= 55:
            band = "reach"
        else:
            band = "high-reach"

        verification = program.get("verification_status", "need-review")
        evidence_confidence = "medium" if verification in {"verified-official", "partial-official"} else "low"

        result = {
            "band": band,
            "hard_score": round(hard_score, 1),
            "soft_score": round(soft_score, 1),
            "fit_score": round(fit_score, 1),
            "gpa_risk": gpa_risk,
            "evidence_confidence": evidence_confidence,
            "notes": [
                "Advisory only; verify against official requirements and public cases.",
                "Do not present this as an admission probability.",
            ],
        }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
