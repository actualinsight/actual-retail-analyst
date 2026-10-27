# <Analysis title>

<!-- The analysis record. Create it first, keep it current, never rebuild it from memory at the end.
     dashboard-builder reads these headings, so keep them exactly as written. -->

## The ask

- **Question:** "<exactly as given>"
- **For:** <who will see the answer: from the ask, or "not stated">
- **End goal:** <what decision or action this supports: from the ask, or "not stated". Only ask if it would change the analysis.>

## Clarifications

| Asked | Answer |
|---|---|
| <question asked> | <analyst's answer, or "not answered: used suggested <x>"> |

Assumed and stated (not asked): <e.g. all channels, all stores>

## Query checklist

- **Timeframe:** <period, with the actual dates, and what it's compared with>
- **Markets:** <list>
- **Channels:** <all, or which>
- **Store set:** <all stores / comp stores, rule applied>
- **Metric definitions:** <standard definition used, linked to `context/data-model/metrics.md`, or new and why>
- **Known data issues that apply:** <tags from `context/data-model/context.md`, e.g. `MX-TIPS-FEES`, or none>

## Data pulls

| # | Files | What it answers |
|---|---|---|
| 01 | `01_<name>.sql` / `.csv` | <one line> |

## Answer

<One sentence that answers the question, with the key number(s).>

## Key findings / so what

1. **<finding>.** <the numbers behind it>
2. ...

## Caveats

- <anything that limits or qualifies the answer, e.g. a known data issue: its tag and its **What to say**>

## Now what

- <recommended action or next question>

## Outputs

- `context.md`: this record
- `<each .sql / .csv>`
- `dashboard.html`

## Decision log

| When | Who | Decision |
|---|---|---|
| <YYYY-MM-DD> | <analyst / agent> | <what was decided and why: scope, definitions, follow-ups, chart choices> |
