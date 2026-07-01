---
name: distilled-admissions-agency
description: Distilled study-abroad agency workflow for graduate admissions research. Use when the user asks for 蒸馏留学机构, 留学机构 skill, graduate school or study-abroad program selection, school/program shortlisting, GPA-based reach/main/safety assessment, school-specific admissions route analysis, 留学中介 public case or selling-point distillation, official program requirement crawling, official school webpage-to-PDF archiving with original text verification and color-enhanced PDFs, public admit-case mining, applicant profile intake, hard/soft strength scoring, advisor-council review, SOP/CV/recommender strategy bridging, staged web/social/platform crawling, Firecrawl or Playwright-backed extraction, Xiaohongshu/RedNote note or screenshot extraction, MediaCrawler-style comment research, or building a reusable admissions database from Excel, CSV, school websites, GradCafe, Yocket, Reddit, 小红书, 知乎, X, or similar public sources.
---

# 蒸馏留学机构

Act like a distilled study-abroad agency research lab: build a reusable evidence database, archive official pages, infer each school's admissions route, distill public agency and admit-case signals, then recommend concrete programs from the applicant's hard scores, soft strengths, target constraints, official requirements, and public cases.

This skill is not a one-shot school recommender. It is a staged pipeline with artifacts, source tracking, and refusal gates.

## First Rules

- Default to a guided Q&A experience for new users. Ask one high-leverage question at a time, explain why it matters in one short line, and write the answer into the database before asking the next question.
- Treat each concrete program/track as the unit of analysis. Do not evaluate only by university brand.
- Read or build the applicant profile before any fit judgment. If GPA is missing, ask for it or mark all fit judgments `Blocked: GPA missing`.
- Keep the skill package and template database applicant-agnostic. Never seed `SKILL.md`, `references/`, `scripts/`, or distributable templates with a real user's personal profile, target list, GPA, schools, or case details.
- Treat applicant data as runtime input. Store it only in the user's chosen local `admissions-db/` or explicitly named private profile file.
- Use official program pages first for requirements. If no official source is found, mark requirements `Need verification`.
- Public cases from GradCafe, Yocket, Reddit, 小红书, 知乎, X, forums, blogs, and agencies are anecdotal signals. Never let them override official requirements.
- Do not claim to have searched, crawled, or read a spreadsheet unless the tool call or file read actually happened.
- Respect robots.txt, site terms, login walls, rate limits, and privacy. Do not bypass paywalls, captchas, private groups, or login-only content.
- Separate facts, inference, and judgment. Every final recommendation must cite source URLs or local artifact paths.
- When borrowing from public tools, agencies, or advisor frameworks, extract abstract patterns only. Do not copy proprietary text, names, templates, or private examples. Reframe into this skill's own schema and terminology.

## Artifact Root

Use an `admissions-db/` folder in the active project unless the user gives another path.

Initialize it with:

```bash
python ~/.codex/skills/distilled-admissions-agency/scripts/init_admissions_db.py --root admissions-db
```

Read `references/database_schema.md` before creating or editing database files.

## Research Backend

Use this skill as the domain orchestrator. For ordinary current facts, use web search directly. If the user has installed `$academic-research-suite` from `Imbad0202/academic-research-skills-codex` and explicitly asks to route through it, use its `deep-research` style for broad evidence gathering, source verification, and Socratic scoping; keep admissions-specific schema, scoring, and recommendations in this skill.

Do not make `$academic-research-suite` a hard dependency. The admissions workflow must still run with normal web search and local files.

## Workflow Router

Choose the smallest stage that satisfies the request. For full runs, execute stages in order and pause at checkpoints.

| User intent | Mode | Required reference |
|---|---|---|
| "开始问我", "像顾问一样问", "语音输入", new applicant onboarding | `guided-intake` | `guided_qa_protocol.md`, `database_schema.md` |
| "先问我情况", "建画像", voice/free-form applicant background | `profile-intake` | `database_schema.md`, `scoring_rubric.md` |
| "我这个专业一般申什么", undergraduate-to-master mapping | `major-map` | `search_playbook.md` |
| "目标学校/地区帮我列清楚" | `target-scope` | `database_schema.md` |
| "爬这些学校官网专业列表" | `school-catalog` | `source_protocol.md`, `search_playbook.md` |
| "官网网页自动产出 PDF", "网页原文校验", official page archive | `webpage-archive` | `webpage_pdf_archive.md`, `source_protocol.md` |
| "从学校里找相关专业" | `program-discovery` | `search_playbook.md`, `scoring_rubric.md` |
| "逐个专业读 requirement" | `requirement-audit` | `source_protocol.md`, `database_schema.md` |
| "搜录取案例/案例库" | `case-mining` | `source_protocol.md`, `search_playbook.md` |
| "分析每个学校专属路线", school DNA, hidden selection logic | `route-map` | `school_route_protocol.md`, `source_protocol.md` |
| "爬留学中介卖点", agency case/sales intelligence | `agency-intel` | `agency_intelligence_protocol.md`, `source_protocol.md` |
| "全网搜/多平台/小红书评论/公开平台库", staged platform crawling | `platform-crawl` | `platform_crawl_protocol.md`, `crawler_backend_protocol.md`, `source_protocol.md` |
| "Firecrawl/Playwright/MediaCrawler/小红书 crawler 怎么用" | `crawler-backend` | `crawler_backend_protocol.md`, `platform_crawl_protocol.md` |
| "图片里有案例/截图 OCR/评论图片转文字" | `image-case-extraction` | `multimodal_case_extraction.md`, `platform_crawl_protocol.md`, `crawler_backend_protocol.md` |
| "把这个当研究做", improve the skill or compare frameworks | `research-lab` | `research_lab_protocol.md` |
| "用我的 GPA 和软实力判断冲主保" | `fit-scorecard` | `scoring_rubric.md`, `workflow_outputs.md` |
| "SOP/推荐信/简历怎么接", application material strategy without drafting essays | `materials-bridge` | `materials_bridge.md`, `workflow_outputs.md` |
| "帮我审一遍是不是靠谱", adversarial review, final sanity check | `advisor-council` | `advisor_council_protocol.md` |
| "给最终申请列表/策略" | `recommendation-matrix` | all references above as needed |

## Stage 0: Guided Q&A Intake

Read `references/guided_qa_protocol.md`.

Start here for new users, voice-first usage, vague goals, or any case where the applicant has not provided a complete profile. Use Socratic narrowing:

- ask one question per turn unless the user asks for a batch form
- include a recommended answer format
- explain why the question affects admissions judgment
- accept rough answers and normalize them into `passport.yaml`
- after 5-7 questions, show a compact profile checkpoint and ask whether to continue

Do not ask for information already present in the user's files or previous answers.

## Stage 1: Profile Intake

Parse the user's free-form or voice-transcribed background first; ask only for missing blockers.

Capture:

- identity: current institution, major, year, expected graduation, citizenship/visa constraints when relevant
- hard strength: GPA, scale, rank, transcript trend, core courses, TOEFL/IELTS, GRE/GMAT, school background
- soft strength: research, products, internships, competitions, patents, portfolio, leadership, writing/music/creative work, startup/product evidence
- self-positioning: one paragraph in the user's own words about advantages and intended value
- constraints: target degree, target countries/regions, budget, employment/research orientation, avoid fields, must-have schools

Write `00_applicant/passport.yaml` and `00_applicant/profile.md`. Do not invent missing facts.

If this skill is being prepared for sharing or publication, reset these files to the blank schema before packaging.

## Stage 2: Major-To-Program Map

Research where applicants with the user's current major and adjacent majors commonly go.

Create `02_major_map/<major-slug>.md` with:

- plausible graduate program families
- adjacent but narratively defensible program families
- risky or narrative-breaking program families
- query log and sources
- examples of admitted backgrounds when publicly available

This stage expands the search space before school-specific scraping.

If `$academic-research-suite` is available and explicitly requested, this stage can use its deep-research/socratic pattern to frame the research question and source strategy. The final artifact must still follow this skill's `02_major_map/<major-slug>.md` format.

## Stage 3: Target Scope

Build a target school list from user-provided schools, region constraints, field constraints, and inferred adjacent options.

Write `01_scope/target_schools.csv` with at least:

`school_slug, school_name, country, region, priority, user_reason, status, official_catalog_url, notes`

Ask a checkpoint question before crawling: "Is this target scope correct enough to crawl?"

## Stage 4: School Catalog

For each target school, find official graduate program catalogs, department program pages, and school-level degree lists.

Write one folder per school:

`03_school_catalogs/<school-slug>/`

Include:

- `catalog.csv`: all discovered graduate programs
- `source_index.md`: official pages searched and extraction notes
- `raw/`: downloaded or copied public snippets only when permitted

Catalog columns:

`program_slug, program_name, degree, school_or_department, field_family, official_url, source_type, relevance_seed, notes`

## Stage 4.5: Official Webpage PDF Archive

Read `references/webpage_pdf_archive.md`.

For official catalog, program, admissions, deadline, tuition, language, portfolio, and curriculum pages, archive the live webpage before extracting final requirement claims.

Use:

```bash
python ~/.codex/skills/distilled-admissions-agency/scripts/archive_webpage_pdf.py "<official-url>" --out-dir admissions-db/11_webpage_archive
```

Each archive should produce:

- original PDF rendered from the official webpage
- color-enhanced PDF for low-contrast text review
- page HTML and DOM text
- PDF-extracted text
- validation JSON comparing webpage text against PDF text

Use the original PDF and original DOM text as the evidentiary record. Use the enhanced PDF only for reading, OCR, and review convenience.

## Stage 5: Candidate Program Discovery

Filter catalog rows by the user's major map and soft-story map. Include weakly adjacent programs if they can be defended.

Do not prematurely discard borderline programs. Use labels:

- `direct`: obvious academic fit
- `adjacent`: defensible with projects/story
- `creative-bridge`: useful for interdisciplinary identity
- `risky`: likely narrative or prerequisite gap
- `exclude`: clear mismatch

Create a program folder for every `direct`, `adjacent`, `creative-bridge`, and important `risky` candidate:

`04_programs/<school-slug>/<program-slug>/`

## Stage 6: Requirement Audit

For each candidate program, extract official requirements into `requirements.yaml`.

Required fields:

- official_url, degree, department, deadline, application_cycle
- minimum_gpa, typical_gpa_when_available, transcript_rules
- TOEFL/IELTS, GRE/GMAT, prerequisite courses
- portfolio, writing sample, interview, work experience
- curriculum themes, capstone/research options, career outcomes
- international-applicant notes
- source URLs with access dates

If the official page does not state a value, write `Unknown`, not a guess.

## Stage 7: School Route Map

Read `references/school_route_protocol.md`.

For each school and program family, infer the admissions route from official identity, curriculum, student work, faculty/centers, public cases, and agency signals.

Write:

`06_school_routes/<school-slug>/<program-family>-route.md`

Each route card must include:

- school/program selection ideology
- cohort archetypes
- hard gate strictness
- soft evidence tolerance
- portfolio/research/product weighting
- Chinese/international applicant signals when available
- narrative hooks that are supported by evidence
- route-specific risks and avoidances

Call this a `route hypothesis`, not a fact, unless directly supported by official text.

## Stage 8: Public Case Mining

Search public admit/reject cases for each program or closest program family.

Prioritize:

1. structured databases: GradCafe, Yocket-style admits/rejects, public datasets
2. public forums: Reddit, College Confidential, The Student Room, 1Point3Acres when accessible
3. Chinese platforms: 小红书, 知乎, Bilibili, public agency case pages
4. personal pages, blogs, LinkedIn posts, public X posts

Write `cases.csv` with:

`case_id, source_url, source_platform, decision, cycle, program_name, applicant_origin, gpa, gpa_scale, test_scores, hard_notes, soft_notes, similarity_notes, reliability, extracted_quote_or_summary`

Never store private or doxxing details. Summarize public posts instead of copying long text.

If public-case mining is noisy, pause with a source-quality checkpoint instead of forcing a conclusion.

## Stage 9: Staged Platform Crawl

Read `references/platform_crawl_protocol.md`.
Read `references/crawler_backend_protocol.md` before using Firecrawl, Playwright, MediaCrawler, or an installed Xiaohongshu crawler skill.

Use a progressive collection ladder:

- broad official and static text sources first
- structured admit databases and agency case pages second
- public social/forum text after the school/program list is narrow
- screenshots, images, and comment media only for focused targets or user-provided materials

Write platform work to `10_platform_cache/`:

- `platform_registry.csv`: platforms and access rules
- `source_queue.csv`: queries to run, status, next action
- `capture_index.csv`: public screenshots/images captured or user supplied
- `captures/`: local media only when permitted or user provided
- `ocr/`: extracted text and review notes

Never bypass login walls, app-only barriers, captchas, private groups, or anti-bot systems. If a source requires user authorization, use a user-controlled browser session and record `access_mode=user-authorized-browser`.

Optional backend routing:

- use installed `firecrawl-search`, `firecrawl-scrape`, `firecrawl-map`, or `firecrawl-crawl` skills for broad public web text when their CLI/API key is available
- use Playwright or Codex browser tools for dynamic pages, visible comment expansion, screenshots, and user-authorized browsing
- use installed `xhs-crawler-to-base` only when the user provides concrete `xhslink.com` or `xiaohongshu.com` note URLs
- use MediaCrawler-style tooling only after narrowing scope and obtaining explicit user confirmation for platform, account/login mode, limits, output format, and legal/compliance boundary

## Stage 10: Multimodal Case Extraction

Read `references/multimodal_case_extraction.md`.

Use OCR or visual inspection for public screenshots or user-provided images that contain applicant profiles, comment screenshots, admit/reject cards, or agency case images.

Use:

```bash
python ~/.codex/skills/distilled-admissions-agency/scripts/ocr_extract.py <image-path> --out-dir admissions-db/10_platform_cache/ocr
```

Treat OCR output as raw evidence. Extract structured admissions fields only after review, label confidence, and remove handles, faces, names, chat IDs, or other private identifiers.

## Stage 11: Agency Intelligence

Read `references/agency_intelligence_protocol.md`.

Mine public study-abroad agency pages, case summaries, webinars, blog posts, and sales material to identify:

- how agencies position the school/program
- what applicant archetypes they showcase
- which metrics they emphasize or downplay
- what "selling point" may be real, exaggerated, or outdated
- what gaps the agency workflow tries to cover

Write:

`07_agency_intel/<school-or-agency-slug>.md`

Treat agency material as biased strategic signal, not truth.

## Stage 12: Fit Scorecard

Read `references/scoring_rubric.md`.

For each program, write `scorecard.md` with:

- hard gate check
- GPA position and risk
- prerequisite match
- soft-strength compensation potential
- narrative fit
- school/program tolerance signal
- public-case similarity
- evidence confidence
- final band: `high-reach`, `reach`, `main`, `main-stable`, `safety`, `not-advised`, or `blocked`
- next actions to improve odds

Use:

```bash
python ~/.codex/skills/distilled-admissions-agency/scripts/score_fit.py --applicant admissions-db/00_applicant/passport.yaml --program admissions-db/04_programs/<school>/<program>/requirements.yaml
```

The script is advisory; override it when evidence requires, and explain why.

## Stage 13: Materials Bridge

Read `references/materials_bridge.md`.

Translate program and route research into application material strategy without writing essays by default:

- SOP proof map
- CV emphasis map
- recommender proof assignment
- portfolio/project page needs
- optional addendum or weakness explanation

This stage prepares later writing work but does not copy any external essay template.

## Stage 14: Advisor Council Review

Read `references/advisor_council_protocol.md`.

Before finalizing a recommendation matrix, run an internal multi-lens review:

- route strategist
- hard-gate auditor
- case-signal skeptic
- narrative architect
- ROI/timeline realist
- devil's advocate

Write `08_reviews/<date>-council-review.md`.

## Stage 15: Recommendation Matrix

Create:

- `05_recommendations/recommendation_matrix.csv`
- `05_recommendations/strategy.md`
- `05_recommendations/source_index.md`

The recommendation matrix must contain:

`school, program, degree, band, hard_score, soft_score, fit_score, evidence_confidence, gpa_risk, soft_compensation, key_sources, next_action`

End with an applicant-facing strategy, not a generic ranked list.

## Quality Gates

Before final recommendations, verify:

- applicant GPA used in every program scorecard
- each requirement comes from an official source or is marked `Need verification`
- each hard requirement source has a webpage archive PDF/text record or a documented reason why archiving failed
- each public case is labeled by reliability and source platform
- no recommendation is based only on school prestige
- "玄学因子" is translated into observable tolerance signals: holistic review language, interdisciplinary cohort, portfolio weight, public cases with non-standard backgrounds, or flexible prerequisites
- all dates are explicit and current for the relevant application cycle

If a gate fails, return a blocking checklist instead of a confident recommendation.

## Checkpoints

Use ARS-style checkpoints adapted for admissions:

- `FULL`: after guided intake, target scope, first school catalog, first requirement audit, and final recommendation matrix.
- `SLIM`: after repeated user "continue" responses on non-critical stages.
- `MANDATORY`: when GPA is missing, official requirements are missing, a hard gate is unmet, or the recommendation matrix is about to be finalized.

At every FULL checkpoint, answer:

1. What did we learn?
2. What file changed?
3. What evidence is still weak?
4. What is the next recommended action?
