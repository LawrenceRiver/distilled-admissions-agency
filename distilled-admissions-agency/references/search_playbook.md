# Search Playbook

Use current web search for school and admissions facts. Dates, requirements, and deadlines change.

## Major-To-Program Map Queries

For the user's undergraduate major:

```text
"<major>" "master's" "admitted to" "GPA"
"<major>" "graduate school" "profile" "MS"
"<major>" "MSCS" "admit" "GPA"
"<major>" "HCI" "admission" "portfolio"
"<major>" site:reddit.com/r/gradadmissions
"<major>" "小红书" "申请" "硕士"
```

Search adjacent majors too. For AI applicants, include CS, data science, HCI, information science, ECE, design technology, music technology, computational media, ML systems, and product-oriented programs.

## Official Catalog Queries

```text
site:<school-domain> graduate programs master's <field>
site:<school-domain> "Master of Science" "Computer Science" admissions
site:<school-domain> "graduate admissions" "GPA" "<program>"
site:<school-domain> "<program>" "requirements" "TOEFL"
site:<school-domain> "<program>" "prerequisites"
site:<school-domain> filetype:pdf "<program>" "admission requirements"
```

Also search the school's own catalog or department navigation manually when search misses pages.

## Public Case Queries

```text
"<school>" "<program>" "GPA" "admitted"
"<school>" "<program>" "rejected" "GPA"
"<school>" "<program>" "GradCafe"
"<school>" "<program>" "Yocket"
"<school>" "<program>" site:reddit.com/r/gradadmissions
"<school>" "<program>" "小红书"
"<school>" "<program>" "知乎"
"<school>" "<program>" "一亩三分地"
"<school>" "<program>" "X" "admitted"
```

For Chinese applicants, search both English and Chinese program names when available.

## Platform-Specific Queries

Create rows in `10_platform_cache/source_queue.csv` before deep searching.

```text
"<school>" "<program>" "录取" "GPA" "小红书"
"<school>" "<program>" "bar" "录取" "小红书"
"<school>" "<program>" "三维" "录取"
"<school>" "<program>" "bg" "录取"
"<school>" "<program>" "admit" "profile"
site:reddit.com/r/gradadmissions "<school>" "<program>"
site:1point3acres.com "<school>" "<program>" "录取"
site:zhihu.com "<school>" "<program>" "申请"
site:<agency-domain> "<school>" "<program>" "案例"
```

For image-heavy platforms, first collect public page URLs and search snippets. Move to screenshots/OCR only after the target program list is narrowed.

## Extraction Checklist

For official pages, extract:

- program name and degree
- department/school
- application deadline
- GPA minimum or transcript evaluation wording
- TOEFL/IELTS minimums
- GRE/GMAT policy
- prerequisites
- portfolio/writing sample/interview requirements
- curriculum keywords
- career outcomes
- international applicant notes
- source URL and access date

For public cases, extract:

- decision and cycle
- program exactness
- GPA and scale
- test scores
- applicant origin/background
- project/research/work notes
- similarity to current applicant
- reliability label
- OCR confidence when the source is an image or screenshot

## Search Stop Rule

Stop searching a single program when:

- official requirements are verified from S1/S2 sources,
- at least 3 relevant public cases are found, or no useful cases after 6 targeted queries,
- major uncertainty is documented as `need-verification`,
- further search would require login-only or private content.
