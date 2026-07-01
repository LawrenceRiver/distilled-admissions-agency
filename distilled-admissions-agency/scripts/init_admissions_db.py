#!/usr/bin/env python3
"""Initialize an admissions-db workspace for the distilled-admissions-agency skill."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


TARGET_SCHOOLS_HEADER = [
    "school_slug",
    "school_name",
    "country",
    "region",
    "priority",
    "user_reason",
    "status",
    "official_catalog_url",
    "notes",
]


RECOMMENDATION_HEADER = [
    "school",
    "program",
    "degree",
    "band",
    "hard_score",
    "soft_score",
    "fit_score",
    "evidence_confidence",
    "gpa_risk",
    "soft_compensation",
    "key_sources",
    "next_action",
]

SOURCE_LOG_HEADER = [
    "date",
    "stage",
    "source_url",
    "source_type",
    "school",
    "program",
    "claim_supported",
    "reliability",
    "notes",
]

PLATFORM_REGISTRY_HEADER = [
    "platform_slug",
    "platform_name",
    "language_region",
    "source_family",
    "case_signal",
    "access_mode",
    "crawl_tier",
    "default_query_pattern",
    "reliability_default",
    "notes",
]

SOURCE_QUEUE_HEADER = [
    "queue_id",
    "date_added",
    "stage",
    "platform_slug",
    "query",
    "target_school",
    "target_program",
    "priority",
    "status",
    "next_action",
    "notes",
]

CAPTURE_INDEX_HEADER = [
    "capture_id",
    "date",
    "source_url",
    "platform_slug",
    "school",
    "program",
    "media_type",
    "local_path",
    "extracted_text_path",
    "extraction_method",
    "confidence",
    "privacy_review",
    "notes",
]

BACKEND_RUNS_HEADER = [
    "run_id",
    "date",
    "backend",
    "task",
    "input_scope",
    "command_or_tool",
    "output_path",
    "status",
    "notes",
]

WEBPAGE_ARCHIVE_HEADER = [
    "archive_id",
    "date",
    "school",
    "program",
    "source_url",
    "page_title",
    "original_pdf_path",
    "enhanced_pdf_path",
    "html_path",
    "dom_text_path",
    "pdf_text_path",
    "validation_json_path",
    "text_match_status",
    "color_mode",
    "notes",
]

PLATFORM_REGISTRY_ROWS = [
    [
        "gradcafe",
        "The GradCafe",
        "en",
        "structured-public-case",
        "admit-reject-results",
        "public-static",
        "T2",
        "{school} {program} GradCafe",
        "structured",
        "Noisy user-reported graduate results; verify exact program names.",
    ],
    [
        "yocket",
        "Yocket",
        "en/global",
        "structured-community-case",
        "profiles-admits",
        "public-dynamic",
        "T2",
        "{school} {program} Yocket admit",
        "detailed-public",
        "Public and logged-in areas vary; do not bypass account walls.",
    ],
    [
        "ymgrad-admits",
        "YMGrad / admits-style sites",
        "en/global",
        "structured-public-case",
        "admit-profile-leads",
        "probe-first",
        "T2",
        "{school} {program} admit profile GPA",
        "thin-public",
        "Use as lead source; verify exact school, program, and cycle.",
    ],
    [
        "reddit-gradadmissions",
        "Reddit r/gradadmissions",
        "en",
        "forum",
        "narrative-edge-cases",
        "public-static",
        "T3",
        "site:reddit.com/r/gradadmissions {school} {program}",
        "thin-public",
        "Use posts as anecdotes and source leads.",
    ],
    [
        "onepointthreeacres",
        "1Point3Acres",
        "zh/en",
        "forum",
        "chinese-applicant-cases",
        "public-search-snippet",
        "T3",
        "site:1point3acres.com {school} {program} 录取",
        "thin-public",
        "Respect login, points, and paywall barriers.",
    ],
    [
        "chasedream-gter",
        "ChaseDream / GTER / ApplySquare-style forums",
        "zh",
        "forum",
        "chinese-applicant-cases",
        "public-search-snippet",
        "T3",
        "{school} {program} 录取 案例 GPA",
        "thin-public",
        "Useful for Chinese applicant signals; verify access rules per site.",
    ],
    [
        "zhihu",
        "Zhihu",
        "zh",
        "social-longform",
        "experience-posts",
        "public-dynamic",
        "T3",
        "{school} {program} 知乎 申请",
        "thin-public",
        "Use public pages or user-authorized browser only.",
    ],
    [
        "college-confidential",
        "College Confidential",
        "en",
        "forum",
        "discussion-leads",
        "public-static",
        "T3",
        "site:collegeconfidential.com {school} {program} admissions",
        "thin-public",
        "Mostly anecdotal; more useful for leads than decisions.",
    ],
    [
        "student-room",
        "The Student Room",
        "en/uk",
        "forum",
        "uk-applicant-discussion",
        "public-static",
        "T3",
        "site:thestudentroom.co.uk {school} {program} postgraduate",
        "thin-public",
        "Useful for UK programs and international student context.",
    ],
    [
        "xiaohongshu",
        "小红书",
        "zh",
        "social-image-comment",
        "comments-images-informal-stats",
        "user-authorized-browser",
        "T5",
        "{school} {program} 小红书 录取",
        "unverified",
        "Image-heavy; use screenshots/OCR only for public or user-provided material.",
    ],
    [
        "bilibili-douyin",
        "Bilibili/Douyin",
        "zh",
        "video-social",
        "comments-agency-videos",
        "user-authorized-browser",
        "T5",
        "{school} {program} 录取 bilibili",
        "unverified",
        "Video/comments are deep-pass only; do not bypass platform controls.",
    ],
    [
        "linkedin-blogs",
        "LinkedIn / personal blogs / Medium",
        "multi",
        "personal-public",
        "background-outcome-leads",
        "public-search-snippet",
        "T3",
        "{school} {program} admitted profile LinkedIn Medium blog",
        "thin-public",
        "Do not store personal identifiers; use only aggregate profile signals.",
    ],
    [
        "agency-pages",
        "Public agency case pages",
        "multi",
        "agency-marketing",
        "selected-case-archetypes",
        "public-static",
        "T4",
        "{school} {program} 留学 案例",
        "agency-summary",
        "Treat as biased strategy signal, not truth.",
    ],
    [
        "openison",
        "OpenIsOn / user-named source",
        "unknown",
        "candidate-platform",
        "unknown",
        "probe-first",
        "T2",
        "{school} {program} openison",
        "unverified",
        "Probe reachability each run; record DNS or access failures.",
    ],
]


PASSPORT = """applicant_id: unknown
last_updated: YYYY-MM-DD
current_institution: Unknown
major: Unknown
year: Unknown
expected_graduation: Unknown
gpa: Unknown
gpa_scale: 4.0
rank: Unknown
citizenship_or_visa: Unknown
target_degree: masters
target_countries: []
hard_strength:
  gpa_score: Unknown
  coursework_score: Unknown
  test_score: Unknown
  institution_context_score: Unknown
soft_strength:
  project_score: Unknown
  research_score: Unknown
  product_score: Unknown
  awards_score: Unknown
  leadership_score: Unknown
  creative_story_score: Unknown
value_proposition: ""
constraints:
  regions: []
  budget: Unknown
  avoid_fields: []
  must_include_schools: []
  must_exclude_schools: []
notes: []
"""


PROFILE = """# Applicant Profile

## Basics

- Current institution:
- Major:
- Year / expected graduation:
- GPA / scale:
- Rank:
- Target degree:
- Target countries/regions:

## Hard Strength

- Coursework:
- Tests:
- Institution context:
- Prerequisites:

## Soft Strength

- Projects/products:
- Research/patents:
- Awards:
- Internships/social practice:
- Leadership:
- Creative/portfolio/story:

## Value Proposition

Write the applicant's one-paragraph self-positioning here.

## Constraints

- Must include:
- Avoid:
- Budget:
- Location:
"""


STRATEGY = """# Application Strategy

No recommendations yet. Build profile, catalog, requirements, cases, and scorecards first.
"""


SOURCE_INDEX = """# Source Index

Record official sources and public-case sources used across the recommendation matrix.
"""


DECISION_LEDGER = """# Decision Ledger

Record why schools or programs were added, removed, moved between bands, or blocked.
"""


def write_csv_if_missing(path: Path, header: list[str]) -> None:
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(header)


def write_csv_rows_if_missing(path: Path, header: list[str], rows: list[list[str]]) -> None:
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def write_text_if_missing(path: Path, text: str) -> None:
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="admissions-db", help="Database folder to create")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    dirs = [
        root / "00_applicant",
        root / "01_scope",
        root / "02_major_map",
        root / "03_school_catalogs",
        root / "04_programs",
        root / "05_recommendations",
        root / "06_school_routes",
        root / "07_agency_intel",
        root / "08_reviews",
        root / "09_research_log",
        root / "10_platform_cache",
        root / "10_platform_cache" / "captures",
        root / "10_platform_cache" / "external",
        root / "10_platform_cache" / "external" / "firecrawl",
        root / "10_platform_cache" / "external" / "playwright",
        root / "10_platform_cache" / "external" / "xhs",
        root / "10_platform_cache" / "external" / "mediacrawler",
        root / "10_platform_cache" / "ocr",
        root / "11_webpage_archive",
        root / "11_webpage_archive" / "pdf-original",
        root / "11_webpage_archive" / "pdf-enhanced",
        root / "11_webpage_archive" / "html",
        root / "11_webpage_archive" / "text",
        root / "11_webpage_archive" / "validation",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    write_text_if_missing(root / "00_applicant" / "passport.yaml", PASSPORT)
    write_text_if_missing(root / "00_applicant" / "profile.md", PROFILE)
    write_text_if_missing(
        root / "00_applicant" / "polygon.json",
        json.dumps(
            {
                "hard": {
                    "gpa": None,
                    "coursework": None,
                    "tests": None,
                    "institution_context": None,
                },
                "soft": {
                    "projects": None,
                    "research": None,
                    "product": None,
                    "awards": None,
                    "leadership": None,
                    "creative_story": None,
                },
            },
            indent=2,
        )
        + "\n",
    )
    write_csv_if_missing(root / "01_scope" / "target_schools.csv", TARGET_SCHOOLS_HEADER)
    write_csv_if_missing(
        root / "05_recommendations" / "recommendation_matrix.csv",
        RECOMMENDATION_HEADER,
    )
    write_text_if_missing(root / "05_recommendations" / "strategy.md", STRATEGY)
    write_text_if_missing(root / "05_recommendations" / "source_index.md", SOURCE_INDEX)
    write_csv_if_missing(root / "09_research_log" / "source_log.csv", SOURCE_LOG_HEADER)
    write_text_if_missing(root / "09_research_log" / "decision_ledger.md", DECISION_LEDGER)
    write_csv_rows_if_missing(
        root / "10_platform_cache" / "platform_registry.csv",
        PLATFORM_REGISTRY_HEADER,
        PLATFORM_REGISTRY_ROWS,
    )
    write_csv_if_missing(root / "10_platform_cache" / "source_queue.csv", SOURCE_QUEUE_HEADER)
    write_csv_if_missing(root / "10_platform_cache" / "capture_index.csv", CAPTURE_INDEX_HEADER)
    write_csv_if_missing(root / "10_platform_cache" / "backend_runs.csv", BACKEND_RUNS_HEADER)
    write_csv_if_missing(root / "11_webpage_archive" / "webpage_archive.csv", WEBPAGE_ARCHIVE_HEADER)

    print(f"Initialized admissions database at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
