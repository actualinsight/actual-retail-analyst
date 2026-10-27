# Choosing the right visual

Pick visuals that answer **this** question. Don't fill a fixed template. Start from what the reader needs to see first.

## Question → visual

| The question is about... | Use | Example |
|---|---|---|
| A few headline numbers | **KPI tiles**: big number, short context line | Growth by group, with traffic and check under each |
| Change over time | **Line chart**, one line per group | Monthly growth by group |
| Comparing groups on one or more measures | **Grouped bars**: groups as colors, measures on the axis | Traffic vs. check vs. sales growth, by group |
| What makes up a change (parts of growth) | **Grouped or stacked bars** of the parts | Traffic and check contributions to growth |
| Ranking (best/worst, top/bottom N) | **Horizontal bars, sorted**, with the value labelled | Which stores lost the most traffic |
| Share or mix | **100% stacked bars**, one bar per group or period | Channel mix by group, this year vs. last |
| Exact values someone will look up | **A small table** (≤ 12 rows) | Store list with its numbers |

**Avoid:**
- pie or donut charts (use bars);
- 3D;
- two y-axes;
- more than about 6 lines on one chart.

## How many

- **Tiles:** 3–5.
- **Charts:** usually two, side by side; never more than four on one view.
- **Each chart answers one question.** Its title says what the reader should see, not just what it is ("Fewer guests is the drag", not "Traffic by month").

## Tabs

Use tabs only when **a deep dive into each group** (each market, region...) helps the analysis.
- **Each tab gets its own:** tiles, one-sentence answer, findings, and **charts**. A group's view can use different charts from the overview, if another visual tells that group's story better.
- **Caveats** appear only on the tabs they apply to.
- **No tabs** when the analysis is one view.

## Color

Colors come from `brand/tokens.json`, via the CSS variables the build script adds.
- **Series colors belong to one kind of group per page**, usually the groups the question compares (e.g. markets). They're taken in a fixed order (`--series-0`, `--series-1`, ...), following the group's `display_order` in its lookup table (sort the rows by it; never rely on the order a query happens to return). **The same group gets the same color on every chart and tab.**
- **A second kind of group** (e.g. channels, when markets have the colors) goes on the axis or into tabs. Don't give it series colors too.
- **Ranking and other one-bar-per-item charts** (stores, items) use one color, `--accent`, or are colored by sign: `--positive` for gains, `--negative` for declines. Don't give each bar its own color, and never color more than 6 groups.
- **Measures are never colored like groups.** When bars show measures, group them by measure and color them by group (as in the reference).
- **`--negative` (orange) only for negative numbers and caveats.** Never use it as a series color.
- Positive numbers use `--positive`. Counts and other values with no direction (e.g. "14 of 14") use the normal text color.
- A page or tab about **one** group uses that group's own color (from its `display_order`), so it matches the overview. A page with no groups at all uses `--series-0`.

## Labels

- Percent changes are signed, with one decimal: `+6.7%`, `−3.7%` (a real minus sign). **Round once, for display only**: queries keep 4 decimals, and the reference's `round` helper rounds half away from zero, so the page and `context.md` agree.
- Differences between two percentages are **points**, not percent: "+3.0 pts" (the reference's `pts` helper).
- Ranking bars: put the value in the axis label ("Store name  −5.2%") so it's readable without hovering.
- Money: currency symbol and sensible rounding ($13.12; $1.6M).
- Say the period and the comparison in the header badge.
- Axis gridlines are light (`--rule`). No chart borders.
