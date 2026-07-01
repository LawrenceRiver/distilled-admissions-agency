# Guided Q&A Protocol

Use this protocol when the user is new, using voice input, unsure what to provide, or asking to be guided like a study-abroad counselor.

## Experience Rules

- Ask one question at a time by default.
- Keep the question short enough for voice answers.
- Add a one-sentence reason: "Why this matters".
- Provide a recommended answer format, not a multiple-choice trap.
- After the user answers, normalize the answer into the database and briefly confirm what changed.
- Do not ask for information already present in `passport.yaml`, uploaded files, spreadsheets, or previous turns.
- If a user gives a long messy answer, extract structured fields first, then ask the next missing blocker.

## Question Order

### Blocker Layer

Ask these first because recommendations cannot work without them:

1. Degree and cycle: target degree, application year/term.
2. Academic identity: current institution, major, year.
3. GPA: value, scale, rank, transcript trend.
4. Target geography: countries/regions and hard constraints.
5. Current must-have schools or programs.

### Hard Strength Layer

6. Core coursework and prerequisites.
7. TOEFL/IELTS and GRE/GMAT current/target scores.
8. Undergraduate institution context and grading notes.

### Soft Strength Layer

9. Best 2-3 projects or research experiences.
10. Awards, patents, publications, products, internships.
11. Leadership, communication, community, creative or portfolio evidence.
12. Recommenders and what each can prove.

### Value Proposition Layer

13. Ask the user to summarize their value in one rough paragraph.
14. Reflect it back as 2-3 possible application identities.
15. Ask which identity feels most true.

### Target Scope Layer

16. Ask what schools/programs are must-include, maybe, or already excluded.
17. Ask whether to infer additional schools from region, field, ranking, budget, or career goal.
18. Confirm target scope before crawling.

## Question Template

```markdown
Question [n]: <one concise question>

Why this matters: <one sentence connecting answer to admissions judgment>

Recommended answer format: <example with placeholders>
```

## After Each Answer

Write or update:

- `00_applicant/passport.yaml` for structured facts
- `00_applicant/profile.md` for human-readable profile
- `00_applicant/polygon.json` for hard/soft score estimates when enough evidence exists

Then respond:

```markdown
Recorded: <field updated>
Current blocker status: <none or missing fields>
Next question: ...
```

## Checkpoint After 5-7 Questions

Show:

```markdown
Profile checkpoint
- Hard profile known:
- Soft profile known:
- Target scope known:
- Still missing:
- Suggested next step:
```

Ask whether to continue intake, upload files, or start school/program research.

## Scoring Caution

Do not assign hard/soft scores until there is enough evidence. Use `Unknown` rather than false precision. Initial scores must be labeled `initial estimate`.

## Failure Modes To Avoid

- Asking 10 questions in one turn.
- Moving to school recommendations before GPA and target degree are known.
- Repeating questions answered in uploaded files.
- Turning the user's rough self-description into polished marketing copy too early.
- Treating soft strength as a magic override for hard gates.
