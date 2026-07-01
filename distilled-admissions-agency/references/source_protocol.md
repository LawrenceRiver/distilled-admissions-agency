# Source Protocol

## Source Tiers

| Tier | Source | Use |
|---|---|---|
| S1 | Official program/admissions pages, official PDFs, department pages | Requirements, deadlines, prerequisites, official claims |
| S2 | Official university catalogs, graduate school policies | Cross-check requirements and general rules |
| S3 | Structured public admissions datasets such as GradCafe-style records | Admit/reject signal, GPA/test distribution, timing |
| S4 | Public personal posts, Reddit, 小红书, 知乎, X, blogs | Anecdotal fit signals and special cases |
| S5 | Agency marketing pages, rankings, third-party summaries | Search leads only unless independently verified |
| S6 | Public screenshots, user-provided images, OCR text | Search leads and case-field extraction after review |
| S7 | Archived official webpage PDFs plus verified DOM/PDF text | Evidence preservation and requirement audit support |

Final requirement claims require S1 or S2. S3-S5 can support tolerance and case-similarity judgments only.

## Browsing And Crawling Rules

- Prefer official APIs, static HTML, RSS, sitemaps, and public catalog pages.
- Use normal browsing first; use scripted scraping only when a repeated extraction task is clear.
- Check `robots.txt` or site terms for automated crawls when using scripts.
- Do not bypass login, paywalls, captchas, private groups, app-only content, or anti-bot systems.
- Use polite delays and narrow scope. Do not crawl entire university domains.
- Store only extracted fields, source URLs, access dates, and short summaries. Avoid copying long copyrighted text.
- Use `platform_crawl_protocol.md` for staged platform crawling and `multimodal_case_extraction.md` for screenshots or image comments.
- Use `crawler_backend_protocol.md` before running Firecrawl, Playwright, xhs-crawler-to-base, MediaCrawler, or any external crawler backend.
- Use `webpage_pdf_archive.md` before finalizing official requirement claims from school pages.

## Evidence Labels

Use these labels in notes and scorecards:

- `official-verified`: supported by official source
- `official-partial`: official source exists but field is incomplete
- `case-supported`: supported by public cases, not official policy
- `anecdotal`: weak public signal
- `inferred`: reasoned from curriculum, cohort, or admissions language
- `need-verification`: not enough evidence
- `ocr-unreviewed`: extracted from image text but not yet manually checked
- `backend-raw`: extracted by a crawler/backend but not yet normalized or reviewed
- `archived-official`: official page saved as PDF and text archive
- `archive-weak-match`: archived PDF text does not strongly match DOM text; manual review needed

## Claim Discipline

For every recommendation claim, keep a source trail:

```text
Claim: Program is GPA-risky for the applicant's GPA.
Evidence: official minimum GPA is 3.0; no typical GPA published; public cases show several admits around 3.7-3.9; one 3.5 admit had strong research.
Verdict: inferred, case-supported, not official.
Sources: [URLs or local paths]
```

If the source does not support the claim, downgrade or remove the claim.

## Public Case Privacy

Do not store names, handles, exact screenshots, or private details unless the user explicitly provided their own data. For public posts, store source URL, short summary, and extracted admissions fields.
