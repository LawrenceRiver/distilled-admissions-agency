# Admissions Database Schema

Use this schema for the reusable `admissions-db/` folder.

## Folder Layout

```text
admissions-db/
├── 00_applicant/
│   ├── passport.yaml
│   ├── profile.md
│   └── polygon.json
├── 01_scope/
│   └── target_schools.csv
├── 02_major_map/
│   └── <major-slug>.md
├── 03_school_catalogs/
│   └── <school-slug>/
│       ├── catalog.csv
│       ├── source_index.md
│       └── raw/
├── 04_programs/
│   └── <school-slug>/
│       └── <program-slug>/
│           ├── requirements.yaml
│           ├── source_notes.md
│           ├── cases.csv
│           └── scorecard.md
└── 05_recommendations/
    ├── recommendation_matrix.csv
    ├── strategy.md
    └── source_index.md
├── 06_school_routes/
│   └── <school-slug>/
│       └── <program-family>-route.md
├── 07_agency_intel/
│   └── <school-or-agency-slug>.md
├── 08_reviews/
│   └── <date>-council-review.md
└── 09_research_log/
    ├── source_log.csv
    └── decision_ledger.md
└── 10_platform_cache/
    ├── platform_registry.csv
    ├── source_queue.csv
    ├── backend_runs.csv
    ├── capture_index.csv
    ├── captures/
    ├── external/
    └── ocr/
└── 11_webpage_archive/
    ├── webpage_archive.csv
    ├── pdf-original/
    ├── pdf-enhanced/
    ├── html/
    ├── text/
    └── validation/
```

## Applicant Passport

`00_applicant/passport.yaml`:

```yaml
applicant_id: unknown
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
```

`polygon.json` stores the same scores for visualization:

```json
{
  "hard": {
    "gpa": null,
    "coursework": null,
    "tests": null,
    "institution_context": null
  },
  "soft": {
    "projects": null,
    "research": null,
    "product": null,
    "awards": null,
    "leadership": null,
    "creative_story": null
  }
}
```

## Target Schools CSV

`01_scope/target_schools.csv` columns:

```csv
school_slug,school_name,country,region,priority,user_reason,status,official_catalog_url,notes
```

`priority` values: `must`, `high`, `medium`, `low`, `exploratory`.

`status` values: `user-provided`, `inferred`, `confirmed`, `removed`.

## School Catalog CSV

`03_school_catalogs/<school>/catalog.csv` columns:

```csv
program_slug,program_name,degree,school_or_department,field_family,official_url,source_type,relevance_seed,notes
```

`source_type` values: `official-catalog`, `official-department`, `official-pdf`, `third-party-index`, `manual-user`.

`relevance_seed` values: `direct`, `adjacent`, `creative-bridge`, `risky`, `exclude`, `unknown`.

## Program Requirements YAML

`04_programs/<school>/<program>/requirements.yaml`:

```yaml
school: Unknown
program: Unknown
degree: Unknown
department: Unknown
official_url: Unknown
application_cycle: Unknown
accessed_on: YYYY-MM-DD
deadline: Unknown
minimum_gpa: Unknown
typical_gpa_low: Unknown
typical_gpa_high: Unknown
toefl_min: Unknown
ielts_min: Unknown
gre_required: Unknown
gre_notes: Unknown
prerequisites: []
portfolio_required: Unknown
writing_sample_required: Unknown
work_experience_required: Unknown
curriculum_keywords: []
career_keywords: []
holistic_review_signals: []
international_notes: []
official_sources: []
non_official_sources: []
verification_status: need-review
```

`verification_status` values: `verified-official`, `partial-official`, `need-review`, `blocked`.

## Public Cases CSV

`cases.csv` columns:

```csv
case_id,source_url,source_platform,decision,cycle,program_name,applicant_origin,gpa,gpa_scale,test_scores,hard_notes,soft_notes,similarity_notes,reliability,extracted_quote_or_summary
```

`reliability` values:

- `structured`: database-style entry with fields
- `detailed-public`: public post with enough detail
- `thin-public`: public post with limited detail
- `agency-summary`: marketing-style agency case
- `unverified`: use only as weak signal

## Recommendation Matrix

`05_recommendations/recommendation_matrix.csv` columns:

```csv
school,program,degree,band,hard_score,soft_score,fit_score,evidence_confidence,gpa_risk,soft_compensation,key_sources,next_action
```

`band` values: `high-reach`, `reach`, `main`, `main-stable`, `safety`, `not-advised`, `blocked`.

## Research Log

`09_research_log/source_log.csv` columns:

```csv
date,stage,source_url,source_type,school,program,claim_supported,reliability,notes
```

`09_research_log/decision_ledger.md` records why programs were added, removed, or moved between bands.

## Platform Cache

`10_platform_cache/platform_registry.csv` columns:

```csv
platform_slug,platform_name,language_region,source_family,case_signal,access_mode,crawl_tier,default_query_pattern,reliability_default,notes
```

`10_platform_cache/source_queue.csv` columns:

```csv
queue_id,date_added,stage,platform_slug,query,target_school,target_program,priority,status,next_action,notes
```

`status` values: `queued`, `done`, `no-results`, `needs-user-browser`, `needs-ocr`, `blocked-login`, `blocked-captcha`, `blocked-robots`, `blocked-terms`, `failed`.

`10_platform_cache/capture_index.csv` columns:

```csv
capture_id,date,source_url,platform_slug,school,program,media_type,local_path,extracted_text_path,extraction_method,confidence,privacy_review,notes
```

`confidence` values: `ocr-high`, `ocr-medium`, `ocr-low`, `visual-manual`, `user-confirmed`, `unusable`, `unknown`.

`10_platform_cache/backend_runs.csv` columns:

```csv
run_id,date,backend,task,input_scope,command_or_tool,output_path,status,notes
```

`status` values: `planned`, `done`, `failed`, `blocked-auth`, `blocked-terms`, `blocked-captcha`, `needs-user-confirmation`, `fallback-used`.

Use `10_platform_cache/external/` for raw or semi-processed backend outputs:

```text
external/
├── firecrawl/
├── playwright/
├── xhs/
└── mediacrawler/
```

## Webpage Archive

`11_webpage_archive/webpage_archive.csv` columns:

```csv
archive_id,date,school,program,source_url,page_title,original_pdf_path,enhanced_pdf_path,html_path,dom_text_path,pdf_text_path,validation_json_path,text_match_status,color_mode,notes
```

`text_match_status` values: `ok`, `weak-text-match`, `no-pdf-text`, `archive-failed`, `manual-review`.

Use this archive for official pages whose content supports requirements, deadlines, tuition, language scores, prerequisites, curriculum, portfolio rules, or school route hypotheses.
