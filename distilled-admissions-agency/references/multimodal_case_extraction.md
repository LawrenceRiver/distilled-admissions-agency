# Multimodal Case Extraction

Use this protocol for screenshots, post images, comment images, admit cards, agency case posters, or user-provided social media captures that may contain applicant stats.

## Boundary

- Use only public images that can be accessed normally, or images/screenshots the user provides.
- Do not bypass login, captcha, anti-bot, watermark restrictions, or private groups.
- Do not store faces, handles, chat IDs, phone numbers, email addresses, exact names, or other private identifiers.
- Prefer extracted fields and short summaries over retaining screenshots.
- Label every extraction with method and confidence.

## Extraction Flow

1. Register the image in `10_platform_cache/capture_index.csv`.
2. Run OCR when available:

```bash
python ~/.codex/skills/distilled-admissions-agency/scripts/ocr_extract.py <image-path> --out-dir admissions-db/10_platform_cache/ocr
```

3. If OCR is unavailable or weak, use visual inspection only for user-provided/local images or ask the user to upload a clearer crop.
4. Review the text manually before adding rows to `cases.csv`.
5. Redact private identifiers before writing any long-term artifact.
6. Write a confidence label.

## Confidence Labels

- `ocr-high`: clear text, key fields match visible source
- `ocr-medium`: readable but some fields need review
- `ocr-low`: noisy extraction; use only as search lead
- `visual-manual`: manually read from a local/user-provided image
- `user-confirmed`: user confirmed extracted fields
- `unusable`: image does not support admissions fields

## Fields To Extract

Use this order:

- source platform and URL/path
- school and exact program
- cycle and decision
- degree level
- GPA and scale
- TOEFL/IELTS/GRE/GMAT
- undergraduate school/major only if relevant and not identifying
- internships, research, publications, competitions, projects, portfolio
- special constraints: gap year, career switch, low-GPA compensation, missing tests
- any explicit note about school tolerance, prerequisites, interview, or scholarship

## OCR Review Prompt

When reviewing OCR, ask:

```text
Which fields are directly visible, which are inferred, and which are missing?
Does any visible detail identify a private person? If yes, redact it.
Is this case exact-program, adjacent-program, or only school-level?
Should this become a cases.csv row, an agency-intel note, or only a search lead?
```

## Output

For each usable image, write:

- OCR text file in `10_platform_cache/ocr/`
- one `capture_index.csv` row
- optional `cases.csv` row if the case has enough admissions fields
- source log row with `source_type=image-ocr` or `source_type=user-screenshot`

Never use OCR-only data to make a final fit recommendation unless it is corroborated by official requirements or multiple independent public cases.
