# Same-store sales by market

<!-- The analysis record. Create it first, keep it current, never rebuild it from memory at the end.
     dashboard-builder reads these headings, so keep them exactly as written. -->

## The ask

- **Question:** "How are same-store sales by market?"
- **For:** not stated (an executive, via the analyst)
- **End goal:** not stated

## Clarifications

| Asked | Answer |
|---|---|
| Timeframe: latest 12 months (Nov 2025–Oct 2026) vs the 12 before (Nov 2024–Oct 2025)? | Yes: "Latest 12 months vs the prior 12" |
| Markets: all three (US, Canada, Mexico), plus an all-markets total? | "All three markets". Total not answered: used suggested (include an all-markets total) |
| Metric: standard Same-Store Sales %, split into same-store traffic and average check? | Not answered: used suggested (standard SSS %, with traffic and check) |
| Breakdown: one number per market for the 12 months, plus a monthly trend? | Not answered: used suggested (12-month total per market, plus monthly trend) |

Assumed and stated (not asked): all channels combined; all restaurants, with the standard comp rule deciding which store-months count.

## Query checklist

- **Timeframe:** Nov 2025–Oct 2026 (latest 12 months) vs Nov 2024–Oct 2025, calendar month vs the same month a year earlier
- **Markets:** United States, Canada, Mexico, plus an all-markets total
- **Channels:** all channels combined (pulls 01–03); split into In-Store, Drive-Thru, Mobile and Delivery in pull 04 (analyst follow-up)
- **Store set:** comp stores: a store counts for a month once it has been open at least 13 full months before that month (standard comp rule)
- **Metric definitions:** standard Same-Store Sales %, with same-store traffic % and average check % ([metrics.md](../../../context/data-model/metrics.md)); net sales in USD at each order month's rate
- **Known data issues that apply:** `MX-TIPS-FEES`: Mexico can't separate delivery tips and fees, so its net sales include them on delivery orders. Its growth rates are barely affected because both years carry the same issue ([context/data-model/context.md](../../../context/data-model/context.md#known-data-issues)).

## Data pulls

| # | Files | What it answers |
|---|---|---|
| 01 | `01_sss_by_market.sql` / `.csv` | 12-month same-store sales, traffic and check by market and for all markets, with comp-store counts and comp sales both years |
| 02 | `02_sss_by_market_month.sql` / `.csv` | The same, month by month (Nov 2025–Oct 2026), by market and for all markets |
| 03 | `03_delivery_share_check.sql` / `.csv` | Data check: delivery's share of comp-store sales in each year, by market (does the Mexico tips-and-fees issue move its growth?) |
| 04 | `04_sss_by_market_channel.sql` / `.csv` | Follow-up: 12-month same-store sales, traffic, check and contribution (points) by channel, for each market and all markets |

## Answer

Same-store sales grew +3.8% across all markets in the latest 12 months (Nov 2025–Oct 2026 vs the prior 12): Mexico +10.4% and the US +6.7% grew while Canada fell −3.7%, and in every market Mobile drove the growth while In-Store and Drive-Thru declined.

## Key findings / so what

1. **Mexico leads, and it's accelerating.** Same-store sales +10.4% (traffic +3.8%, check +6.4%). Positive every month, rising from +6.6% in Nov 2025 to +14.6% in Oct 2026; Jul–Oct ran between +11.0% and +14.9%. Most of the pick-up is check: check growth was +2.8% to +6.3% a month in Nov–Jun and +8.0% to +11.1% in Jul–Oct. By channel, Mobile (+54.5%) adds +6.5 points and Delivery (+13.7%) adds +5.6 points.
2. **The US is steady.** Same-store sales +6.7% (traffic +2.4%, check +4.2%), between +5.1% and +7.9% every month, with traffic up every month. Mobile (+45.5%) adds +6.4 of the 6.7 points.
3. **Canada is the only market going backwards, and it's guests at the counter and drive-thru.** Same-store sales −3.7%: traffic −6.9%, partly offset by check +3.4%. Traffic fell every month (−5.2% to −7.7%). In-Store (−10.9%, traffic −13.3%) and Drive-Thru (−11.3%, traffic −13.7%) together take 7.0 points off; Mobile (+28.4%) adds back +3.9 points; Delivery is −2.8%. The monthly decline narrowed in Jul–Oct (−1.4% to −3.1%, vs −3.7% to −5.5% in Nov–Jun), but that came from bigger check growth (+4.1% to +5.0% a month, vs +2.0% to +3.2%), not from guests coming back.
4. **Mobile is the growth engine everywhere; the counter and drive-thru are shrinking everywhere.** Across all markets Mobile grew +40.8% and adds +5.6 points, more than the whole +3.8%; In-Store (−1.7 points) and Drive-Thru (−1.5 points) declined in every market; Delivery adds +1.4 points.
5. **Across all markets, growth is all check, and part of that is channel mix.** All markets: traffic −0.6%, check +4.4%. Within each channel, check grew +3.6% to +3.8% across all markets, and in every market the total check grew faster than any single channel's (US +4.2% vs +3.4% to +3.6%; Canada +3.4% vs +2.8% to +2.9%; Mexico +6.4% vs +4.1% to +5.5%). So part of check growth is the shift in channel mix, not just price.

**So what:** the business is growing like-for-like, on what guests spend and on the app, not on more guests overall. Mobile (an FY2026 priority, "Grow the Actual App") is working in every market. Canada's falling counter and drive-thru traffic is the one clear problem, and it lines up with the FY2026 priority to "get Canada's traffic growing again" (`context/company/about.md`). How much of the within-channel check growth is menu price hasn't been measured; a fixed-basket price index would answer that for the US and Canada.

## Caveats

- **Mexico's net sales include delivery tips and fees** (its POS can't separate them). Its growth rates are barely affected because both years carry the same issue. Delivery's share of Mexico's comp-store sales moved only +1.2 points (40.6% to 41.8%), so its check growth isn't materially overstated by the issue. Mexico's Delivery dollars and share are inflated, so don't compare its Delivery level with the US or Canada; its Delivery growth (+13.7%) and contribution (+5.6 points) carry the same tips and fees in both years. (`MX-TIPS-FEES`)
- **Comp-store counts:** 42 stores were in the comp base for at least one month (US 21, Canada 14, Mexico 7); 36 were comp for all 12 months (US 18, Canada 13, Mexico 5). The other 6 joined partway through the year and count only for their comp months.
- **Mexico is a small base** (5 to 7 comp stores a month), so its monthly numbers swing more than the other markets'. Its Drive-Thru is smaller still (most Mexican restaurants are urban, with no drive-thru), so its −12.3% is on a small base.
- **Channel shifts aren't guest switching.** The data has no guest IDs, so we can't tell whether the guests lost at the counter and drive-thru are the same guests now ordering on Mobile.
- **Reported in USD** at each month's exchange rate. This analysis didn't compare USD comps with local-currency comps, or check whether exchange rates contribute to Mexico's late-year check pick-up.

## Now what

- **Canada traffic:** find which restaurants are losing counter and drive-thru guests (the FY2026 priority), and whether those with the most Mobile growth lose the most at the counter.
- **Split check growth into price and mix:** a fixed-basket price index for the US and Canada. Mexico has no item prices, so its price change can't be measured and its check growth stays unsplit.
- **Explain Mexico's and Canada's check pick-up from July:** a local-currency, month-by-channel view would show whether it's exchange rates, mix or something else.

## Outputs

- `context.md`: this record
- `01_sss_by_market.sql` / `01_sss_by_market.csv`
- `02_sss_by_market_month.sql` / `02_sss_by_market_month.csv`
- `03_delivery_share_check.sql` / `03_delivery_share_check.csv`
- `04_sss_by_market_channel.sql` / `04_sss_by_market_channel.csv`
- `dashboard.html`: the dashboard (tabs: All markets, United States, Canada, Mexico); built from `dashboard.template.html`, which the build script removed

## Decision log

| When | Who | Decision |
|---|---|---|
| 2026-10-26 | analyst | Scope: latest 12 months (Nov 2025–Oct 2026) vs the prior 12 (Nov 2024–Oct 2025); all three markets. |
| 2026-10-26 | agent | Analyst didn't answer the metric, breakdown or total questions: used the suggested answers (standard SSS % with traffic and check, 12-month total plus monthly trend, all-markets total included). Will say so in the findings message. |
| 2026-10-26 | agent | Assumed all channels combined and all restaurants under the standard comp rule (stated in the clarifying message, not asked). |
| 2026-10-26 | agent | Pull plan. 01: 12-month SSS, traffic and check by market plus an all-markets row (the headline tiles), with comp-store counts (any month and all 12 months) and comp sales both years for reconciliation. 02: the same by month (the trend chart), with comp sales so its months can be reconciled to 01. 03: a data check, delivery's share of Mexico's (and every market's) comp-store sales in each year, because the Mexico tips-and-fees rule says to mention it if that share moved more than a couple of points. |
| 2026-10-26 | agent | Fixed 01 after the first run: the ALL row's market_name came back as "Canada" (MIN over the group); now labelled "All markets" with GROUPING(). Numbers unchanged. |
| 2026-10-26 | agent | Checks before presenting: the 12 monthly comp sales in 02 sum to 01's totals for every market (within a cent of rounding); markets sum to ALL every month; 03's comp sales match 01 exactly; no NULLs; 48 monthly rows (12 months x 4). Comp counts make sense: the 36 restaurants open in Nov 2024 (US 18, Canada 13, Mexico 5, per about.md) are comp all year; 6 newer ones join partway. |
| 2026-10-26 | agent | Mexico tips-and-fees rule: delivery share of Mexico's comp sales moved +1.2 points (03), under "a couple of points", so no extra warning that its check growth is overstated; standard "barely affected" caveat kept. |
| 2026-10-26 | agent | No price/mix split calculated; offered as a next step. |
| 2026-10-26 | agent | Presented preliminary findings (pulls 01–03). |
| 2026-10-26 | analyst | Follow-up: "Can we see this by channel too?" Same period, markets and comp rule. |
| 2026-10-26 | agent | Pull 04 uses the canonical "Same-Store Sales by channel" query (comp rule at store level, every comp store-month x every channel). Added: an all-markets row per channel (GROUPING SETS, contribution partitioned by market incl. ALL), avg_check_pct (the standard Average Check growth formula, as in the SSS query), and comp sales both years. 12-month grain only; no monthly channel split (offered as a next step). |
| 2026-10-26 | agent | Checks on 04: channel comp sales sum to 01's comp sales for every market and ALL (within a cent); contribution_pts sum to each market's sss_pct (Canada −3.7250 vs −3.7251, rounding); 16 rows, no NULLs (every market has sales in all four channels). |
| 2026-10-26 | agent | Replaced the earlier "part of check growth is probably mix" (not measured) with a measured statement: in every market the total check grew faster than any single channel's check (04 vs 01), so part of check growth is channel mix. |
| 2026-10-26 | analyst | "Looks good, build the dashboard." |
| 2026-10-26 | agent | Dashboard plan (per choosing-visuals.md). Tabs: All markets, United States, Canada, Mexico, because each market's channel story differs and deserves its own view. Markets own the series colors (display_order: US, CA, MX) on every tab; channels go on the axis. **All markets tab:** 4 tiles (all-markets and each market's SSS, with traffic and check under each); chart 1 grouped bars of traffic / check / SSS by market (what's driving it); chart 2 monthly SSS line per market (change over time); chart 3 (full width) contribution points by channel, grouped by market (what makes up the change). **Market tabs:** 4 tiles (SSS, traffic, check, vs all markets in points); chart 1 monthly SSS line in the market's color; chart 2 horizontal bars of each channel's contribution points, colored by sign, value in the axis label. Channels kept in display_order rather than sorted, so the four bars read the same way on every tab. Caveats only on the tabs they apply to. All numbers in tiles, charts and text computed from DATA. |
| 2026-10-26 | agent | Built `dashboard.html` with build_dashboard.py. Every tile, chart and number in the page text is computed from DATA (the four CSVs); the one comparison typed as words ("in every market the total check grew faster than any single channel's") was confirmed against 01 and 04. First check pass rendered every tab with no errors; fixed wording only ("between X to Y", "United States's"), rebuilt and re-checked: "OK: works offline, every tab renders." |
| 2026-10-26 | agent | Re-read every number in the page text from the check script's output against the CSVs and this record: all match (rounded once, half away from zero, to 1 decimal). |
| 2026-10-26 | agent | Handed over: told the analyst where the folder and dashboard are and offered to open it. Analyst: "No thanks, I'll open it myself." |
| 2026-10-27 | agent | Dashboard rebuilt after the context clean-up: the All-markets so-what now says price vs mix hasn't been measured, matching this record. Charts, tiles and tabs unchanged. Removed a caveat that quoted a measured exchange-rate figure from the table docs. |
