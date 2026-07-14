# Distilled Admissions Agency / 蒸馏留学机构

[中文说明](README.zh-CN.md) · [English](README.en.md) · [Promotion Kit](PROMOTION.md)

![Distilled Admissions Agency workflow](assets/admissions-workflow.svg)

**Distill the useful parts of a study-abroad agency into an evidence-backed Codex skill.**

**把留学中介最有价值的部分，蒸馏成一个可验证、可复用、可本地运行的 Codex Skill。**

Distilled Admissions Agency is a bilingual Codex skill for graduate admissions research. It guides applicant intake, archives official school webpages as verifiable PDFs, mines public admit-case signals including Xiaohongshu public comment leads, builds school-specific route hypotheses, and turns evidence into reach/main/safety planning.

蒸馏留学机构是一个中英文可用的研究生申请研究 Skill。它用问答方式建立申请者画像，抓取并归档学校官网，保存原版网页 PDF 和增强版 PDF，检索公开录取案例、小红书公开评论区线索与中介卖点，最后基于证据输出冲刺、主申、保底策略。

## Signature Promises / 记忆点

- **Archive first. Then recommend with evidence.**  
  **先存证，再判断。**
- **Official PDFs you can open, annotate, and verify.**  
  **官网 PDF 原封存证，可打开、可批注、可复核。**
- **Public comment leads become a sample library, not gossip.**  
  **小红书评论区线索进入公开样本库，不把评论当最终事实。**

## Workflow / 工作流程

The skill follows one traceable path: build the applicant passport, archive
official evidence, audit program requirements, describe each school's route,
then produce a reach/main/safety matrix with next actions.

这套 Skill 走一条可追踪的路径：建立申请画像、保存官网证据、审计项目要求、拆解学校路线，最后输出带下一步动作的冲主保矩阵。

The primary outputs are source logs, verified PDFs, route cards, and a decision
map you can inspect and revise. The older feature illustrations remain in the
repository as supporting material, but the workflow above is the main product
story.

主要产物是来源日志、可复核 PDF、学校路线卡和可以继续修改的决策地图。旧的功能插图仍保留在仓库中作为辅助素材，但上面的流程图是项目的主叙事。

## Why It Exists / 为什么做它

Most admissions consulting value comes from three things:

- a structured applicant profile
- a large, constantly refreshed evidence database
- experience reading school-specific requirements, preferences, and edge cases

多数留学机构真正值钱的地方，其实是三件事：

- 对申请者背景的结构化理解
- 大量持续更新的案例和学校资料库
- 对学校官网、项目要求、录取偏好和特殊案例的经验判断

This skill turns that workflow into local artifacts: CSV files, YAML profiles, archived PDFs, validation JSON, source logs, public sample tables, route cards, and recommendation matrices. You can inspect what was searched, what was inferred, and what still needs verification.

这个 Skill 把这些流程变成可检查的本地文件：CSV、YAML、官网 PDF 存证、校验 JSON、来源日志、公开样本表、学校路线卡和推荐矩阵。每一个判断都能回到证据，而不是只听一句“我觉得你可以冲”。

## Core Features / 核心能力

| Feature | English | 中文 |
|---|---|---|
| Guided intake | Ask one high-value question at a time and build an applicant passport | 一次只问一个关键问题，逐步建立申请者画像 |
| Official PDF audit | Save school webpages as original PDFs, enhanced PDFs, HTML, DOM text, validation JSON, and note-ready evidence files | 将学校官网保存为原版 PDF、增强版 PDF、HTML、网页原文、校验 JSON 和可批注证据文件 |
| Requirement audit | Extract deadlines, GPA, language, GRE, prerequisites, portfolio, writing sample, and curriculum signals | 提取截止日期、GPA、语言、GRE、先修课、作品集、writing sample 和课程信号 |
| Public sample library | Search GradCafe, Yocket, Reddit, Zhihu, Xiaohongshu public comments, forums, blogs, and agency pages as anecdotal evidence | 检索 GradCafe、Yocket、Reddit、知乎、小红书公开评论区、论坛、博客和中介案例作为弱证据 |
| Route hypothesis | Infer each school/program's selection route from official pages, curriculum, cases, and public signals | 从官网、课程、案例和公开信号推断学校或项目的录取路线 |
| Fit matrix | Convert hard scores, soft strengths, source confidence, and school tolerance into reach/main/safety bands | 把硬分数、软实力、证据强度和学校包容度转成冲刺、主申、保底矩阵 |
| Crawler routing | Route Firecrawl, Playwright, Xiaohongshu link parsing, and MediaCrawler-style research only when appropriate | 在合适阶段调用 Firecrawl、Playwright、小红书链接解析和 MediaCrawler 风格研究 |

## Install / 安装

After this repository is published, install the skill from GitHub:

仓库发布后，可以这样安装：

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <github-user-or-org>/distilled-admissions-agency \
  --path distilled-admissions-agency
```

Restart Codex after installing.

安装后重启 Codex。

## Quick Start / 快速开始

```text
Use $distilled-admissions-agency to guide intake, archive official pages as verified PDFs, build school route cards, and produce an evidence-backed application list.
```

中文也可以直接说：

```text
使用 $distilled-admissions-agency，像蒸馏留学机构一样先问我问题，建立我的申请画像，然后爬学校官网、保存 PDF 存证、分析项目路线，最后给我冲主保列表。
```

## Webpage PDF Archive / 官网 PDF 存证

Official school pages can be archived before claims are extracted:

在提取官网要求前，可以先把页面存证：

```bash
python ~/.codex/skills/distilled-admissions-agency/scripts/archive_webpage_pdf.py \
  "<official-url>" \
  --out-dir admissions-db/11_webpage_archive
```

The archive includes:

- original browser-rendered PDF
- color-enhanced PDF for low-contrast text review
- webpage HTML
- original DOM text
- PDF-extracted text
- validation JSON comparing webpage text and PDF text

存证会包含：

- 浏览器原样打印的 PDF
- 低对比文字增强版 PDF
- 网页 HTML
- 原始网页文本
- PDF 抽取文本
- 对比网页文本和 PDF 文本的校验 JSON

## Evidence Boundaries / 证据边界

- Official school pages are the source of truth for requirements, deadlines, and hard gates.
- Public cases, agency posts, forums, and social platforms are anecdotal signals, not final truth.
- The skill does not guarantee admission or calculate exact admission probability.
- It does not bypass login walls, paywalls, captchas, private groups, platform rules, or rate limits.
- Applicant data stays in the user's local `admissions-db/`, not inside the reusable skill package.

中文原则：

- 官网是申请要求、截止日期和硬门槛的最高证据。
- 公开案例、中介文章、论坛和社媒只能作为经验信号，不能替代官网。
- Skill 不保证录取，也不输出精确录取概率。
- 不绕过登录墙、付费墙、验证码、私密群组、平台规则或访问频率限制。
- 申请者个人信息只保存在用户本地 `admissions-db/`，不会写进可发布的 skill 包。

## Repository Layout / 仓库结构

```text
distilled-admissions-agency/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
└── scripts/
```

## More / 更多

- Full Chinese introduction: [README.zh-CN.md](README.zh-CN.md)
- Full English introduction: [README.en.md](README.en.md)
- GitHub description, topics, and launch copy: [PROMOTION.md](PROMOTION.md)

## License / 许可证

The original source code and documentation are released under the [MIT License](LICENSE). Existing visual assets may have separate provenance and are not automatically covered by MIT; follow the rights and terms of their respective creators.

本项目原创的源代码和文档使用 [MIT License](LICENSE)。仓库中的既有视觉素材可能有独立来源，不会因为放在仓库里就自动获得 MIT 授权；使用时请遵守相应创作者的权利和条款。
