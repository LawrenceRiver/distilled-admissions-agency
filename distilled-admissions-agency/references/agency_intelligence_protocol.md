# Agency Intelligence Protocol

Use this to study public study-abroad agencies, counselor blogs, webinars, case summaries, public videos, and marketing pages.

## Ethical Boundary

- Use only public, accessible content or user-provided materials.
- Do not scrape login-only groups, paid databases, private chats, or copyrighted long-form materials.
- Do not copy agency wording, case names, or private student details.
- Treat agencies as biased sources. They optimize for marketing, not truth.

## What To Extract

For each agency/source, extract:

- school/program selling points
- applicant archetypes shown in public cases
- GPA/test ranges when stated
- soft evidence emphasized
- hidden risks they mention
- services they sell around the school/program
- contradictions with official requirements or other public cases

## Bias Labels

Use:

- `marketing-heavy`: likely selected to impress
- `case-useful`: concrete enough to inform profile similarity
- `requirement-lead`: useful link or official reference, but not source of truth
- `strategy-signal`: useful for framing route or materials
- `low-confidence`: too vague or unverifiable

## Distillation Output

Write an agency intelligence card:

```markdown
# Agency Intelligence: <source/school/program>

## Public Claims

| Claim | Evidence | Bias Label | How We Use It |
|---|---|---|---|

## Case Archetypes

| Archetype | Hard Profile | Soft Proof | Relevance |
|---|---|---|---|

## Distilled Strategy

- What seems genuinely useful:
- What is probably marketing:
- What to verify officially:
```

## Use In Recommendations

Agency intelligence can support:

- route hypotheses
- public-case similarity
- materials strategy
- "what counselors tend to package for this program"

It cannot establish official requirements or admission probability.
