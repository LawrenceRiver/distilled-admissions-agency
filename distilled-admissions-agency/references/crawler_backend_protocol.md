# Crawler Backend Protocol

Use this protocol when platform crawling needs an external backend such as Firecrawl, Playwright, a Xiaohongshu note parser, or MediaCrawler.

## Backend Choice

| Backend | Use for | Do not use for | Before running |
|---|---|---|---|
| normal web search | quick source discovery, official pages, public cases | bulk extraction or dynamic comments | record query and source URLs |
| Firecrawl skills/CLI | public web search, scrape, map, scoped crawl, JS-rendered public pages | login-only social feeds, private groups, app-only pages | check CLI/API availability; save to `.firecrawl/` or `10_platform_cache/external/firecrawl/` |
| Playwright / Codex browser | dynamic pages, visible comment expansion, screenshots, manual site operation | bypassing captcha/login/paywalls or hidden APIs | prefer user-visible browser; do not store auth state unless user approves |
| `xhs-crawler-to-base` | concrete `xhslink.com` or `xiaohongshu.com` note URLs, public note text/media | keyword search, comment crawling, account-scale scraping | use only user-provided/public links; redact author/handle if not needed |
| MediaCrawler | deep Chinese social platform comment research after narrowing | broad scraping, commercial use, anti-bot bypass, private data extraction | explicit user confirmation, small scope, research-only boundary |
| `taught-master-applications` | application OS, evidence map, documents, timeline, offer comparison | deep crawling or GPA/case database judgments | use as complementary workflow, not source of admission facts |

## Escalation Pattern

Follow this order:

1. `search`: find candidate sources.
2. `scrape`: extract one known public URL.
3. `map`: discover URLs inside a known site or school domain.
4. `crawl`: scoped extraction under a path with a page limit.
5. `browser`: interact with visible public pages or user-authorized sessions.
6. `social backend`: only for narrowed targets and explicit user confirmation.
7. `OCR`: when useful applicant fields are in images/screenshots.

Write every backend run to `10_platform_cache/backend_runs.csv`.

## Firecrawl Adapter

Use Firecrawl when the task is public web extraction and the CLI/API key is available.

Recommended patterns:

```bash
firecrawl search "<school> <program> GPA admit" --scrape -o .firecrawl/search.json --json
firecrawl scrape "<official-url>" --only-main-content -o .firecrawl/program.md
firecrawl map "<school-domain>" --search "graduate programs <field>" -o .firecrawl/map.txt
firecrawl crawl "<catalog-url>" --limit 50 --max-depth 2 --wait -o .firecrawl/crawl.json
```

If `firecrawl` is not installed, try `npx firecrawl`. If both fail, fall back to normal web search and browser tools. Do not make Firecrawl a hard dependency.

Operational rules:

- Keep outputs in `.firecrawl/` or `10_platform_cache/external/firecrawl/`.
- Use `--limit`, `--max-depth`, `--include-paths`, and `--delay` for scope control.
- Never crawl an entire university domain when a catalog path is enough.
- Use Firecrawl output as raw source material, then normalize into `requirements.yaml`, `catalog.csv`, `cases.csv`, or source logs.

## Playwright Adapter

Use Playwright when a page requires JavaScript rendering, scrolling, clicking visible controls, or screenshots.

Prefer existing Codex browser or Chrome control tools when available. Use `npx playwright` or a small Playwright script only when a repeatable browser action is needed.

Allowed actions:

- open a public page
- search within visible page content
- scroll and expand visible comments
- take screenshots for OCR or audit
- save page HTML or text if permitted

Not allowed:

- bypass captcha, login walls, private groups, paywalls, rate limits, or app-only restrictions
- store cookies, browser profiles, or auth state without explicit user approval
- automate bulk social crawling before the target list is narrow

## Xiaohongshu Link Adapter

Use installed `xhs-crawler-to-base` when the user provides specific public note links.

Suggested command shape:

```bash
python3 ~/.codex/skills/xhs-crawler-to-base/scripts/crawl_xhs_notes.py \
  --output-dir admissions-db/10_platform_cache/external/xhs/<batch-id> \
  --skip-media \
  "<xhslink-or-xiaohongshu-url>"
```

Use media download only when the user explicitly asks and the content rights are acceptable. Convert `records.json` into:

- `capture_index.csv` rows when media/images exist
- `cases.csv` rows only when admissions fields are concrete enough
- `source_log.csv` rows with `source_type=xhs-public-note`

Do not use this adapter for keyword search or comment crawling; escalate to user-authorized browser or MediaCrawler protocol only after narrowing.

## MediaCrawler Adapter

MediaCrawler can collect public information from Xiaohongshu, Douyin, Kuaishou, Bilibili, Weibo, Tieba, Zhihu, and similar platforms. Treat it as a high-friction research backend, not a default crawler.

Before any run, confirm:

- platform and target query/post IDs
- exact school/program scope
- maximum posts and comments
- login method and account owner
- whether comments are needed
- output format and storage path
- that the use is research/learning, non-commercial, limited, and compliant with platform rules

Run a one-query or one-post pilot before any batch. Store outputs under:

```text
admissions-db/10_platform_cache/external/mediacrawler/
```

Safety rules:

- Do not recommend proxy pools, multi-account rotation, anti-detection, or high-volume crawling for admissions research.
- Do not collect private messages, hidden content, private groups, or personal identifiers.
- Redact handles and names before moving data into long-term admissions artifacts.
- Treat MediaCrawler cases as `unverified` until reviewed and corroborated.

## Backend Run Log

`10_platform_cache/backend_runs.csv` columns:

```csv
run_id,date,backend,task,input_scope,command_or_tool,output_path,status,notes
```

Use statuses: `planned`, `done`, `failed`, `blocked-auth`, `blocked-terms`, `blocked-captcha`, `needs-user-confirmation`, `fallback-used`.

## Output Normalization

External backend output is never the final answer by itself. Normalize it into:

- `source_queue.csv` for planned searches
- `source_log.csv` for sources actually read
- `catalog.csv` for official program lists
- `requirements.yaml` for official requirements
- `cases.csv` for admit/reject/application profile cases
- `capture_index.csv` and OCR files for images
- `agency_intel/*.md` for agency selling-point signals

If backend output cannot be tied to a school, program, decision, GPA, requirement, or route signal, keep it as a search lead only.
