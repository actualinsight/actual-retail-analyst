---
name: query-builder
description: Writes one commented SQL query for a business question, following the data rules and metric definitions in context/. Use when the analyst asks for a query or SQL ("give me the SQL for...", "write a query that...", "how would I pull..."), and whenever another skill needs a data pull.
---

# Query Builder

Turn a question into **one readable SQL statement** that uses the company's standard definitions, and explains every choice that changes the answer in a comment.

## Running a query

The tool is `query.py` in this skill's folder. It opens the one `.duckdb` file in `data/`, read-only, so a query can never change the data.

```
.venv/bin/python .claude/skills/query-builder/query.py "SELECT ..."                          # print the result
.venv/bin/python .claude/skills/query-builder/query.py --file <file.sql>                     # run a saved query
.venv/bin/python .claude/skills/query-builder/query.py --file <file.sql> --csv <file.csv>    # save the full result
```

Save pulls under `workbench/` so they're easy to find, unless the analyst asks for somewhere else. On Windows, use `.venv/Scripts/python.exe` in place of `.venv/bin/python`. If `.venv/` or the database is missing, use the `project-setup` skill.

For a quick factual question, this is all you need: run one query and answer. The steps below are for writing a query someone will keep.

## Before you write anything

Read `context/data-model/context.md` (the rules for every query, and the **known data issues**) and follow its reading order.

## 1. Make sure the scope is clear

An item is **set** when the analyst said it ("US", "last 12 months") or the calling skill passed it. A saved, recurring scope (like a weekly report's) counts as set. **Don't re-ask set items**: say back what you understood ("US only, latest 12 complete months") and only ask about what's missing or ambiguous.

| Item | Rule |
|---|---|
| **Timeframe** | Must be confirmed. If missing, ask, and suggest the default period from `metrics.md`. |
| **Markets** | Must be confirmed. List them from `market_dim` ("All markets: <list>?"). |
| **Metric** | Must be clear. A defined metric uses its standard definition, so say which one. If the ask is vague or the metric isn't defined, ask. |
| **Channels** | If none is named, use all of them and say so. |
| **Store set** | If none is named, use all stores and say so. Same-store metrics still apply their comp rule. |
| **Grain** | One number for the period, or broken down (by month, store, channel)? If not named, give one total and offer the breakdown. |

Ask **every** open question in **one message**, each with a suggested answer, so the analyst can reply "yes" or fix just one.

## 2. Write the SQL

- **Start from the canonical SQL** in `metrics.md`. Never invent a new version of a defined metric.
- Follow the rules in `context/data-model/context.md`: currency, net sales, known data issues.
- **For the default periods, use the `periods` building block** from `metrics.md`; don't type the dates. If the analyst gives specific dates, hard-code them with a `-- DECISION:` comment.
- **Keep the standard exchange-rate join** even when only one currency is in scope (its rate is 1.0), so every query reads the same way.
- Keep it readable:
  - CTEs with plain names (`store_month`, not `t1`);
  - one column per line in the final `SELECT`;
  - clear column names (`sss_pct`, not `x`).
- **Aggregate in SQL.** Return the summary someone needs, not raw orders.
- **Always end with an `ORDER BY`.** Without one, rows come back in a different order each run.
- **Keep 4 decimals in the query.** Round only once, when the number is displayed (to 1 decimal for percentages). Rounding twice (2 decimals, then 1) can be off by 0.1.

## 3. Comment it

Start with this header, then comment every filter or choice that changes the answer:

```sql
-- Question:   <the question, in the analyst's words>
-- Asked:      <YYYY-MM-DD> · Period: <period compared, with the actual dates when run>
-- Scope:      <markets> · <channels> · <store set>
-- Metric:     <metric name> (context/data-model/metrics.md)
-- Data notes: <tags of the known data issues this query touches, or "none">
-- Dialect:    DuckDB (other databases may need small syntax changes)
```

For a derived period, record the dates it covered, e.g. `Period: latest 12 complete months (Nov 2025–Oct 2026 when run)`, so a saved query still says what it measured after the data changes.

Inline comments use two tags, so they're easy to scan:
- `-- DECISION: ...` marks a choice made by or with the analyst. Example: `WHERE o.channel_id = 3  -- DECISION: Mobile only, per analyst`.
- `-- DATA ISSUE: <tag> ...` marks a known data problem **that can change this result**, starting with the issue's tag from `context/data-model/context.md`. Example: `coalesce(o.net_sales_excl_tips_fees, o.net_sales)  -- DATA ISSUE: MX-TIPS-FEES, Mexico's delivery sales include tips and fees`. If no known issue touches the scope, write `Data notes: none` and skip the tag.

## 4. Test it

Before handing it over, run the whole query, comments and all, with the tool (see [Running a query](#running-a-query)), so nobody ever gets SQL that errors.

If it fails, fix it and run it again. Check that the result looks sane: the expected rows, no surprise NULLs, numbers in a plausible range.

## 5. Deliver it

**When the analyst just asked for the SQL:**
- Show the full query in chat in a ```sql block, ready to copy.
- **Don't create files** unless the analyst asks. End with one offer: **"Want me to save this to a workbench folder, or pull the data?"**
- If they name a place ("put it in a `us-channels` folder"), save it there under `workbench/`, creating the folder if needed. To pull the data, save the full result with `--csv` to a `.csv` with the same name.

**When another skill called you:**
- Write the SQL to the path it gave (e.g. `NN_<name>.sql`).
- Pull the data with `--csv` to the matching `.csv`.
