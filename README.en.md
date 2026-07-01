# Distilled Admissions Agency

**A Codex skill that distills study-abroad agency workflows into evidence-backed admissions research.**

Distilled Admissions Agency is not a one-shot school recommender. It is a transparent admissions research pipeline: guided applicant intake, official school webpage archiving, requirement auditing, public case mining, school route hypotheses, and evidence-backed reach/main/safety planning.

## Who It Is For

- Applicants preparing graduate school or study-abroad applications
- Users who want GPA-aware school and program positioning
- People who want source trails instead of vague admissions advice
- Builders who want a local, reusable alternative to opaque agency workflows
- Researchers who need official requirements, public cases, and school-specific route analysis in one workflow

## What It Does

Most admissions consulting value comes from structured intake, a large evidence base, and experience reading school-specific requirements. This skill turns that workflow into local artifacts that can be inspected, rerun, and improved.

## Core Features

| Module | Output |
|---|---|
| Guided intake | Applicant passport, profile, hard/soft strength map |
| Target scope | Regions, schools, fields, constraints, target school CSV |
| Official cataloging | School catalogs, program lists, official source index |
| Webpage PDF archive | Original PDF, color-enhanced PDF, HTML, DOM text, PDF text, validation JSON |
| Requirement audit | Deadlines, GPA, language, GRE, prerequisites, portfolio, writing samples, curriculum signals |
| Public case mining | GradCafe, Yocket, Reddit, Zhihu, Xiaohongshu, forums, blogs, agency pages |
| School route cards | Selection ideology, hard gates, soft-evidence tolerance, route risks |
| Fit matrix | Reach/main/safety bands, GPA risk, soft compensation, evidence confidence, next actions |
| Crawler/OCR routing | Firecrawl, Playwright, Xiaohongshu link parsing, MediaCrawler-style research, OCR |

## Official Webpage Archive

Archive an official school page before extracting requirement claims:

```bash
python ~/.codex/skills/distilled-admissions-agency/scripts/archive_webpage_pdf.py \
  "<official-url>" \
  --out-dir admissions-db/11_webpage_archive \
  --school "<school-slug>" \
  --program "<program-slug>"
```

The archive creates:

- `pdf-original/`: browser-rendered original PDF
- `pdf-enhanced/`: color-enhanced PDF for low-contrast text review
- `html/`: saved webpage HTML
- `text/`: original DOM text and PDF-extracted text
- `validation/`: JSON comparing webpage text and PDF text

The original PDF and DOM text are the evidence record. The enhanced PDF is only a readability and OCR helper.

## Install

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <github-user-or-org>/distilled-admissions-agency \
  --path distilled-admissions-agency
```

Restart Codex after installing.

## Example Prompts

```text
Use $distilled-admissions-agency to guide intake, archive official pages as verified PDFs, build school route cards, and produce an evidence-backed reach/main/safety matrix.
```

```text
Use $distilled-admissions-agency to archive these official program pages as PDFs and verify that the PDF text matches the webpage text.
```

```text
Use $distilled-admissions-agency to analyze GPA risk and soft-strength compensation for these target programs.
```

## Evidence Boundaries

- Official school pages are the source of truth for requirements and deadlines.
- Public cases are anecdotal signals, not probability estimates.
- Agency cases are biased samples and must be labeled.
- Social posts and OCR-derived evidence must be redacted and reviewed.
- The skill does not bypass login walls, paywalls, captchas, private groups, platform rules, or rate limits.
- Applicant data stays in the user's local `admissions-db/`, not inside the reusable skill package.

## Suggested GitHub Description

```text
A Codex skill that distills study-abroad agency workflows into evidence-backed admissions research, official webpage PDF archiving, public case mining, and reach/main/safety planning.
```

