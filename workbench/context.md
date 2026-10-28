# Workbench

**Every output from an analysis or query lands here, in a structure the analyst designs:** analyses, queries, data pulls, dashboards. Each skill files its work in its own folder, and the analyst adds folders for anything else, so every output has a known home and nothing gets lost.

## Layout

```
workbench/
  ad-hoc-analysis/
    YYYYMMDD_<topic>/          one folder per analysis, e.g. 20261026_same_store_sales_by_market/
  <your own folders>/          analysts can create any folder they like here
```

- **Analysis folders** are named and created by the [`ad-hoc-analysis`](../.claude/skills/ad-hoc-analysis/SKILL.md) skill. For a worked example, see [20261026_same_store_sales_by_market/](ad-hoc-analysis/20261026_same_store_sales_by_market/).
- **Your own folders:** ask the agent ("make a `us-channels` folder and put the query there") or create them yourself.
- **Your work stays on your machine.** Git ignores everything here except this file and the worked example, so new analyses and folders aren't committed by accident. To publish one, add it as an exception in `.gitignore`.

## Inside an analysis folder

| File | What it is |
|---|---|
| `context.md` | The analysis record: the ask, what was clarified, the answer, findings, caveats, next steps, and a log of every decision. Created first, kept up to date. |
| `NN_<name>.sql` / `NN_<name>.csv` | Each data pull: the query (with comments on every decision and data issue) and its result. Numbered `01`, `02`, ... in the order they were pulled. |
| `dashboard.html` | The finished dashboard. One file that opens in any browser and can be emailed. |
| `dashboard.template.html` | Only while a dashboard is being worked on: the page before the build step adds the brand and data. The build removes it. |

To see how an analysis was done, start with its `context.md`.
