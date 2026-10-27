---
name: dashboard-builder
description: Turns an analysis folder in workbench/ (its context.md record and numbered CSV data pulls) into a self-contained dashboard.html in the company brand that works offline and can be emailed. Use when an analysis is ready for a dashboard, or when the analyst asks to build, rebuild or update one.
---

# Dashboard Builder

Make the dashboard: the polished thing the analyst forwards to an executive. **One HTML file**, with the data and charts inside it, in the company brand.

**Never run queries here.** You work from what's already in the folder. If a good visual needs data that isn't there, say so and let the analyst decide whether to add a pull (through `ad-hoc-analysis` and `query-builder`).

## Inputs

- **`context.md`** in the analysis folder. Use its **Answer**, **Key findings / so what**, **Caveats**, **Now what** and **Query checklist** (period and scope).
- **The CSVs** (`NN_<name>.csv`). In the page, each one is available as `DATA["NN_<name>"]`, a list of rows.
- **The brand** (colors, font and logo) is added by the build script; you don't need to read `brand/README.md`. To change the brand, edit the files in `brand/`.

## Steps

### 1. Read the guides
- [choosing-visuals.md](choosing-visuals.md): which visual for which question.
- [reference-dashboard.html](reference-dashboard.html): the approved look and structure.

### 2. Plan the page
Decide:
- the tiles (3–5);
- the charts (usually two);
- whether tabs help.

Follow `choosing-visuals.md`. Write the plan, and why, in the **decision log**.

### 3. Write the page
Write `dashboard.template.html` in the analysis folder, starting from `reference-dashboard.html`.
- **Keep:** its styling, page structure and helper functions, and the three markers exactly as written: `<!-- BRAND_HEAD -->`, `<!-- LOGO -->` and `<!-- SCRIPTS -->`. Your own script goes **after** `<!-- SCRIPTS -->`, **inside the reference's `(() => { ... })();` wrapper.** A top-level `const top` (or `name`, `status`...) clashes with browser built-ins and blanks the page.
- **Layout:** charts sit two per row, and a third or fourth wraps. Add class `wide` to a chart card for full width (use it for a chart left alone on its row), and class `tall` to its `chartbox` for long rankings.
- **Change:** the title, the period badge, the subtitle, and the tiles, charts and tabs to fit this analysis.
- **Tiles and charts read their numbers from `DATA`.** Never type a number into a tile or chart.
- **The answer, findings, caveats and next steps** come from `context.md`. Where you can, compute the numbers in that text from `DATA` (as the reference does) rather than typing them; otherwise confirm each one against the CSVs.
- **The footer** lists the folder's `.sql` / `.csv` files, `context.md` and `metrics.md` as plain labels, not links, so the page still makes sense when emailed.
- **No status badges** (the period badge is fine). No external scripts or images.

### 4. Build it
```
.venv/bin/python .claude/skills/dashboard-builder/build_dashboard.py <analysis folder>
```

The script:
- adds the brand, logo, chart library and data;
- writes `dashboard.html`;
- removes the template. Add `--keep-template` while you're still iterating.

If it reports an error (for example a missing marker, or too many rows), fix the cause and build again.

### 5. Check it
- **In a real browser:**

  ```
  .venv/bin/python .claude/skills/dashboard-builder/check_dashboard.py <analysis folder>/dashboard.html
  ```

  It opens the page in headless Chrome or Edge, offline, and clicks every tab. It reports script errors, tabs without charts, empty charts and sideways scrolling on a phone. Fix everything it reports, rebuild, and check again. Testing the script some other way (e.g. in Node) isn't enough. If it says no browser was found, ask the analyst to open the page and click every tab.
- **Numbers:** confirm every number in the tab text `check_dashboard.py` prints against the CSVs.
- **Record:** add the dashboard and your chart choices to `context.md` (**Outputs**, **Decision log**).

### 6. Hand it over
Tell the analyst it's ready, and offer to open it:
- macOS: `open <file>`
- Windows: `start <file>`
- Linux: `xdg-open <file>`

If your session has browser tools, you can open it there instead.

## Changing a built dashboard

When the analyst asks for a change ("make this a bar chart", "add a note under the Canada chart"):
1. **Get the template back:**

   ```
   .venv/bin/python .claude/skills/dashboard-builder/build_dashboard.py <analysis folder> --edit
   ```

   It recreates the exact page that was approved, as `dashboard.template.html`.
2. **Change only what was asked.** Leave everything else as it is.
3. **Build and check it again** (steps 4 and 5).
4. **Log the change** in the decision log.

If the request goes against `choosing-visuals.md` (a pie chart, say), say why once and suggest the alternative. If the analyst still wants it, do it and log it: what to show is their call.
