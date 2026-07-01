# Webpage PDF Archive

Use this protocol when an official school webpage supports requirements, deadlines, tuition, language scores, prerequisites, curriculum, portfolio rules, or route hypotheses.

## Purpose

Archive the official webpage before relying on it:

- `original PDF`: browser-rendered webpage as the evidentiary record
- `enhanced PDF`: same page after light print-color enhancement for readability/OCR
- `DOM text`: original webpage text extracted before color enhancement
- `PDF text`: text extracted from the original PDF
- `validation JSON`: text-length and overlap checks between DOM text and PDF text

The original PDF and DOM text are the source of record. The enhanced PDF is only for review convenience.

## Command

```bash
python ~/.codex/skills/distilled-admissions-agency/scripts/archive_webpage_pdf.py "<official-url>" \
  --out-dir admissions-db/11_webpage_archive \
  --school "<school-slug>" \
  --program "<program-slug>"
```

If Chrome or the DevTools websocket dependency is unavailable, record `archive-failed` and fall back to Firecrawl/browser/manual source notes.

## When To Archive

Archive:

- program overview pages
- admissions requirement pages
- application deadline pages
- tuition and fees pages
- language test policy pages
- portfolio or writing sample requirement pages
- official PDF landing pages only when the HTML page contains meaningful context

Do not archive private portals, login-only pages, payment pages, captchas, or pages that disallow automated access.

## Color Enhancement

Use color enhancement only as a secondary artifact. The script injects print-only CSS that darkens text and removes text shadows so faint gray/white text can be read or OCRed.

Rules:

- keep the original PDF unchanged
- label enhanced PDF as `color-enhanced`
- do not cite enhanced color as evidence of original design or emphasis
- if enhancement changes layout too much, mark `manual-review`

## Validation

Use `validation.json` to decide whether the archive is reliable:

- `ok`: PDF text overlaps enough with DOM text for routine extraction
- `weak-text-match`: PDF may be missing hidden/tabbed/JS text; review DOM text and page manually
- `no-pdf-text`: PDF is image-like or extraction failed; use visual review/OCR
- `archive-failed`: browser or page failed

When validation is weak, do not finalize requirement claims until the page is manually reviewed or corroborated by another official source.

## Database Row

Append a row to `11_webpage_archive/webpage_archive.csv`:

```csv
archive_id,date,school,program,source_url,page_title,original_pdf_path,enhanced_pdf_path,html_path,dom_text_path,pdf_text_path,validation_json_path,text_match_status,color_mode,notes
```

Use relative paths from the `admissions-db/` root where practical.
