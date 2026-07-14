# Distilled Admissions Agency

**A Codex skill that distills study-abroad agency workflows into evidence-backed admissions research.**

Distilled Admissions Agency is not a one-shot school recommender. It is a transparent admissions research pipeline: guided applicant intake, official school webpage archiving, requirement auditing, public case mining, school route hypotheses, and evidence-backed reach/main/safety planning.

![Distilled Admissions Agency workflow](assets/admissions-workflow.svg)

## Memorable Promises

- **Archive first. Then recommend with evidence.**
- **Official PDFs you can open, annotate, and verify.**
- **Xiaohongshu public comment leads become sample-library signals, not gossip.**

## Workflow

The skill follows one traceable path: build the applicant passport, archive
official evidence, audit program requirements, describe each school's route,
then produce a reach/main/safety matrix with next actions.

The primary outputs are source logs, verified PDFs, route cards, and a decision
map you can inspect and revise. The older feature illustrations remain in the
repository as supporting material, but this workflow is the main product story.

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
| Official PDF audit | Original PDF, color-enhanced PDF, HTML, DOM text, PDF text, validation JSON, note-ready evidence files |
| Requirement audit | Deadlines, GPA, language, GRE, prerequisites, portfolio, writing samples, curriculum signals |
| Public sample library | GradCafe, Yocket, Reddit, Zhihu, Xiaohongshu public comments, forums, blogs, agency pages |
| School route cards | Selection ideology, hard gates, soft-evidence tolerance, route risks |
| Fit matrix | Reach/main/safety bands, GPA risk, soft compensation, evidence confidence, next actions |
| Crawler routing | Firecrawl, Playwright, Xiaohongshu link parsing, MediaCrawler-style research |

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

## License

The original source code and documentation are released under the [MIT License](LICENSE). Existing visual assets may have separate provenance and are not automatically covered by MIT; follow the rights and terms of their respective creators.
