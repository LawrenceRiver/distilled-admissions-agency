# Platform Crawl Protocol

Use this protocol when the task needs broad public-source collection, platform-by-platform case mining, 小红书/知乎/forum signals, agency case pages, or a reusable crawl queue. Use `crawler_backend_protocol.md` when choosing Firecrawl, Playwright, xhs-crawler-to-base, or MediaCrawler.

## Collection Ladder

Escalate only when the previous tier cannot answer the question.

| Tier | Name | Sources | When to use | Output |
|---|---|---|---|---|
| T0 | Local intake | user files, spreadsheets, screenshots | before web search | normalized profile and source notes |
| T1 | Official/static text | program pages, catalogs, PDFs, sitemaps | always for requirements | requirements and source log |
| T2 | Structured public cases | GradCafe, Yocket, YMGrad, admits-style databases | broad admit/reject signal | cases.csv rows |
| T3 | Public forum/social text | Reddit, 1Point3Acres, Zhihu, College Confidential, The Student Room, blogs | after target programs are narrowed | anecdotal case summaries |
| T4 | Public agency pages | case pages, webinars, counselor blogs, service pages | route and sales-signal research | agency intelligence cards |
| T5 | Media and comments | public screenshots, post images, comment images, user-provided screenshots | only for focused schools/programs | OCR text plus reviewed fields |
| T6 | User-authorized browser | logged-in pages shown by the user | only with user consent and no bypassing | short summaries and source metadata |
| T7 | External backend | Firecrawl, Playwright, xhs-crawler-to-base, MediaCrawler | only when a backend clearly improves extraction | backend run log plus normalized artifacts |

Do not start T5/T6 for a broad school list. Use them after the list is narrowed to roughly 5-15 candidate programs, or when the user explicitly asks to investigate one program deeply.

## Platform Registry

Use `10_platform_cache/platform_registry.csv` to decide where to search and how. Treat it as editable local data; add new platforms when discovered.

Recommended columns:

```csv
platform_slug,platform_name,language_region,source_family,case_signal,access_mode,crawl_tier,default_query_pattern,reliability_default,notes
```

Access modes:

- `public-static`: normal web pages can be opened and summarized
- `public-search-snippet`: search results are usable, full content may be blocked
- `public-dynamic`: use browser inspection and manual scrolling when permitted
- `user-authorized-browser`: user must open or authorize access
- `probe-first`: test reachability before planning extraction
- `manual-only`: use only user-provided screenshots/files

## Seed Platform List

Keep this list as a starting queue, not a promise that every site is currently crawlable.

| Platform | Use | Access note |
|---|---|---|
| GradCafe | structured graduate admit/reject signals | public text, noisy but useful |
| Yocket | admit/profile/community signals | public and logged-in areas vary |
| YMGrad / admits.fyi-style sites | graduate admit profile leads | verify each case manually |
| Reddit r/gradadmissions and program subreddits | narrative cases and edge cases | public posts only |
| 1Point3Acres / 一亩三分地 | Chinese applicant cases and discussions | respect login/paywall barriers |
| ChaseDream / 寄托天下 / ApplySquare-style forums | Chinese applicant and business-school cases | public pages only |
| Zhihu | Chinese long-form admit experience | public pages or user-authorized browser |
| 小红书 | comments, images, informal applicant stats | usually T5/T6, avoid automated bypass |
| Douyin / Bilibili | video comments and agency content | use public metadata or user-provided captures |
| College Confidential / The Student Room | undergrad/graduate discussion leads | public pages only |
| LinkedIn / personal blogs / Medium | applicant backgrounds and outcomes | summarize, do not store identities |
| Agency case pages | biased but useful route/sales signals | label as agency-summary |
| OpenIsOn / user-named sites | possible public lead source | `probe-first`; record DNS or access failures |

## Backend Hints

| Need | Preferred backend |
|---|---|
| broad public web search with full text | Firecrawl search with scrape, or normal web search fallback |
| one official/program page | Firecrawl scrape or normal page open |
| school catalog URL discovery | Firecrawl map, sitemap, or site search |
| scoped school catalog extraction | Firecrawl crawl with strict limit/path |
| dynamic public page or visible comments | Playwright or Codex browser tools |
| specific Xiaohongshu note links | installed `xhs-crawler-to-base` |
| narrowed Xiaohongshu/Douyin/Bilibili/Zhihu comments | MediaCrawler only after explicit confirmation |

## Machine Operation Mechanism

For each school/program batch:

1. Read `01_scope/target_schools.csv` and candidate program folders.
2. Create or update `10_platform_cache/source_queue.csv` with one query per platform/program.
3. Run cheap text queries first:
   - `"<school>" "<program>" GPA admit`
   - `"<school>" "<program>" 录取 GPA`
   - `"<school>" "<program>" 小红书`
   - `site:reddit.com/r/gradadmissions "<school>" "<program>"`
4. Open public pages and record title, URL, access date, platform, and source type in `09_research_log/source_log.csv`.
5. Extract only structured admissions fields and short summaries. Do not copy long posts.
6. If the page is dynamic, use browser tools only after confirming it is public or user-authorized. Scroll, expand visible comments, and record what was visible.
7. If useful information appears inside images, save only permitted public media or use user-provided screenshots, then follow `multimodal_case_extraction.md`.
8. If an external backend is used, follow `crawler_backend_protocol.md` and write `backend_runs.csv`.
9. Mark each queue row as `done`, `blocked-login`, `blocked-captcha`, `blocked-robots`, `no-results`, `needs-user-browser`, or `needs-ocr`.

## Narrowing Triggers

Move from broad search to deep social/OCR only when at least one trigger is met:

- the applicant has a complete GPA and soft-strength profile
- the school/program is already in the top candidate set
- official requirements are verified or explicitly unavailable
- broad cases are contradictory and a deeper platform pass can resolve the uncertainty
- the user asks for one school or program to be investigated deeply

## Source Quality Rules

- Treat official requirements as stronger than every case.
- Treat public cases as evidence of possibility, not probability.
- Treat agency cases as selected marketing samples.
- Treat OCR as raw extraction until reviewed.
- Treat crawler/backend output as raw extraction until normalized into the database schema.
- Record failures. A blocked source is still useful evidence about what could not be verified.

## Output Pattern

At each crawl checkpoint, report:

```markdown
## Platform Crawl Checkpoint

- Scope:
- Platforms tried:
- Useful sources:
- Blocked sources:
- OCR/media needed:
- Fields added:
- Reliability shift:
- Next crawl tier:
```
