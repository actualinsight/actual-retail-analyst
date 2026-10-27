# Metric definitions

The standard way Actual Burger Co. measures its business, so the same question always gets the same number. Use these definitions unless the person asking says otherwise. If you change one, write down what you changed and why.

**If a question needs a metric that isn't defined here:**
1. Say so.
2. Propose a definition built from the existing ones.
3. Record that it's new in the analysis's decision log.

Don't quietly invent one.

**Every metric uses the building blocks and default periods below.** Same-store metrics also use the comp rule in [Same-Store Sales %](#same-store-sales--sss-comps).

| Metric | Answers | Builds on |
|---|---|---|
| [Net Sales](#net-sales) | How much did we sell? | Building blocks |
| [Transactions (Traffic)](#transactions-traffic) | How many orders? | In growth questions, same-store traffic |
| [Average Check](#average-check) | How much does each order spend? | Net Sales, Transactions |
| [Items per Order](#items-per-order) | How many items are in each order? | |
| [Channel Mix %](#channel-mix-) | What share of sales comes from each channel? | Net Sales |
| [Sales per Store](#sales-per-store) | How productive is each restaurant? | Net Sales |
| [Year-over-Year (YoY) Growth](#year-over-year-yoy-growth) | How does a period compare with a year earlier? | Any metric |
| [Same-Store Sales %](#same-store-sales--sss-comps) | Like-for-like growth, without new restaurants | Net Sales, the comp rule |
| [Same-Store Sales by channel (or by store)](#same-store-sales-by-channel-or-by-store) | Which channels or stores drive same-store sales? | Same-Store Sales % |
| [Share of a change](#share-of-a-change) | How much of a change does one group account for? | Any change |
| [Traffic vs. Average Check](#traffic-vs-average-check-whats-driving-growth) | Is growth from more orders or bigger checks? | Same-Store Sales % |

All SQL uses DuckDB syntax, with `orders` aliased as `o` and `exchange_rates` as `fx`. Table details are in [context.md](context.md).

**Building blocks.** Almost every metric uses these. Use them as written, so every number is calculated the same way.

```sql
-- Net sales in local currency: exclude delivery tips and fees where we can.
-- Mexico can't report them separately, so its net sales still include them (data issue MX-TIPS-FEES).
coalesce(o.net_sales_excl_tips_fees, o.net_sales)

-- Convert to USD at the order month's rate. Every sales metric is reported in USD.
JOIN exchange_rates fx ON fx.curn_iso = o.curn_iso AND fx.month = date_trunc('month', o.business_date)
coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local
```

**Default periods.** Worked out from the data, so they move forward when new data arrives:
- **Year 2** = the latest 12 complete months.
- **Year 1** = the 12 months before that.

```sql
-- Default periods. y2_end is the first day after the last complete month in the data.
periods AS (
    SELECT date_trunc('month', max(business_date) + INTERVAL 1 DAY)::DATE                      AS y2_end,
           (date_trunc('month', max(business_date) + INTERVAL 1 DAY) - INTERVAL 12 MONTH)::DATE AS y2_start,
           (date_trunc('month', max(business_date) + INTERVAL 1 DAY) - INTERVAL 24 MONTH)::DATE AS y1_start
    FROM orders
)
```

Make it the first CTE and filter with `p.y2_start` and `p.y2_end`, as the queries below do. To see the current dates, select from it on its own.

"This year vs last year" with no dates means year 2 vs year 1, the latest 12 complete months against the 12 before.
- If someone says **"fiscal year", "FY" or "year to date"**, use calendar years instead (the fiscal year is the calendar year). Year to date = January through the last complete month, against the same months a year earlier.
- When it's ambiguous, ask. If you can't ask, use the latest 12 months and say so.

---

## Net Sales

**Definition:** money from food and drink, excluding delivery tips and delivery fees, reported in USD.

```sql
SELECT SUM(coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local) AS net_sales_usd
FROM orders o
JOIN exchange_rates fx ON fx.curn_iso = o.curn_iso AND fx.month = date_trunc('month', o.business_date)
```

**Caveats:**
- Mexico's net sales include tips and fees on delivery orders. See data issue [`MX-TIPS-FEES`](context.md#known-data-issues).
- If someone asks for local currency, use the same expression without `* fx.usd_per_local`, and label the currency.

## Transactions (Traffic)

**Definition:** the number of orders. "Traffic" and "transactions" mean the same thing.

```sql
SELECT COUNT(*) AS transactions FROM orders o
```

**Caveats:**
- A group order of ten burgers is still one transaction.
- **In a growth question, "traffic" means same-store traffic**: the `traffic_pct` column of the Same-Store Sales query. Total transactions include new restaurants. If new stores change the picture, show total traffic alongside and say which is which.

## Average Check

**Definition:** Net Sales ÷ Transactions, in USD.

```sql
SELECT SUM(coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local) / COUNT(*) AS avg_check_usd
FROM orders o
JOIN exchange_rates fx ON fx.curn_iso = o.curn_iso AND fx.month = date_trunc('month', o.business_date)
```

**Average check by channel, store or month:** use the same formula grouped by that column.

**Caveats:**
- Channels have very different checks (delivery includes group orders), so a shift in channel mix moves the overall check even when no channel's check changes.
- Across markets, USD check levels reflect each market's menu prices as well as guest behaviour. Compare rankings and growth rates across markets, not dollar levels.
- **Mexico's delivery check and overall check are inflated by tips and fees.** Flag this whenever checks are compared across markets (data issue `MX-TIPS-FEES`).
- Within one market, a local-currency check is fine (Canadian checks in CAD, for example) as long as you label it.

## Items per Order

**Definition:** total units ÷ transactions.

```sql
SELECT SUM(o.items) * 1.0 / COUNT(*) AS items_per_order FROM orders o
```

## Channel Mix %

**Definition:** each channel's share of Net Sales (USD) within the group being analyzed, usually a market.

```sql
SELECT o.market_iso, c.channel_name,
       SUM(coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local)
         / SUM(SUM(coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local))
           OVER (PARTITION BY o.market_iso) AS sales_mix
FROM orders o
JOIN exchange_rates fx ON fx.curn_iso = o.curn_iso AND fx.month = date_trunc('month', o.business_date)
JOIN channel_dim c USING (channel_id)
GROUP BY o.market_iso, c.channel_name
```

**Caveats:**
- Mix of *sales* is the default. Mix of *transactions* (`COUNT(*)` share) is a different number; say which one you used.
- **"Digital" isn't a standard channel.** If someone asks for digital sales, ask whether they mean Mobile, or Mobile + Delivery, and note the definition you used.
- Mexico's delivery share is inflated by tips and fees (data issue `MX-TIPS-FEES`).

## Sales per Store

**Definition:** Net Sales (USD) ÷ store-days. A store-day is a day a store was open and had orders. This is the fair way to compare restaurant productivity when stores opened at different times.

```sql
SELECT o.market_iso,
       SUM(coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local)
         / COUNT(DISTINCT (o.store_id, o.business_date)) AS sales_per_store_day_usd
FROM orders o
JOIN exchange_rates fx ON fx.curn_iso = o.curn_iso AND fx.month = date_trunc('month', o.business_date)
GROUP BY 1
```

**Caveats:**
- Multiply by 365 for a rough annual figure (average unit volume, AUV).
- New stores ramp up over their first 8 weeks, so exclude those weeks when judging a new store.

## Year-over-Year (YoY) Growth

**Definition:** (this period ÷ the same period last year) − 1. Uses calendar months: a month against the same month a year earlier.

**Caveats:**
- **Total-sales YoY includes new restaurants.** Use Same-Store Sales for like-for-like growth, and always say which one you're showing.
- For daily or weekly YoY, compare against `calendar_dim.same_day_last_year`, so weekdays line up.

## Same-Store Sales % (SSS, "comps")

**Definition:** Net Sales (USD) growth at restaurants that were open in both periods.

**The comp rule:** a store counts for a month once it has been open **at least 13 full months before that month**. The partial opening month doesn't count, unless the store opened on the 1st.

Worked example: a store that opened on 2025-01-15.
- January 2025 is a partial month, so its first full month is February 2025.
- Thirteen full months (Feb 2025–Feb 2026) are complete by March 2026, so it's comp from **March 2026**.
- Its March 2026 is compared with its March 2025. The 13-month rule means the year-ago month is always a full month of trading. It can still fall in the store's first 8 weeks of ramp-up, which slightly understates the base. That's accepted as a small effect.

```sql
-- s = store_dim, <month> = the first day of the month being measured
date_trunc('month', s.open_date - INTERVAL 1 DAY) + INTERVAL 14 MONTH <= <month>
```

Each comp store's month is compared with the same store's same month a year earlier. This query is the canonical year-2-vs-year-1 version, with traffic and check alongside:

```sql
WITH periods AS (
    SELECT date_trunc('month', max(business_date) + INTERVAL 1 DAY)::DATE                      AS y2_end,
           (date_trunc('month', max(business_date) + INTERVAL 1 DAY) - INTERVAL 12 MONTH)::DATE AS y2_start
    FROM orders
),
store_month AS (
    SELECT o.store_id,
           o.market_iso,
           date_trunc('month', o.business_date) AS month,
           COUNT(*) AS orders,
           SUM(coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local) AS net_sales_usd
    FROM orders o
    JOIN exchange_rates fx ON fx.curn_iso = o.curn_iso AND fx.month = date_trunc('month', o.business_date)
    GROUP BY ALL
),
comp AS (
    SELECT ty.market_iso,
           ty.store_id,
           ty.net_sales_usd AS sales_ty,
           ly.net_sales_usd AS sales_ly,
           ty.orders        AS orders_ty,
           ly.orders        AS orders_ly
    FROM store_month ty
    JOIN store_month ly
      ON ly.store_id = ty.store_id
     AND ly.month = ty.month - INTERVAL 12 MONTH
    JOIN store_dim s ON s.store_id = ty.store_id
    CROSS JOIN periods p
    WHERE ty.month >= p.y2_start AND ty.month < p.y2_end
      AND date_trunc('month', s.open_date - INTERVAL 1 DAY) + INTERVAL 14 MONTH <= ty.month
)
SELECT m.market_code,
       COUNT(DISTINCT c.store_id)                                    AS comp_stores,
       ROUND(100 * (SUM(sales_ty) / SUM(sales_ly) - 1), 4)           AS sss_pct,
       ROUND(100 * (SUM(orders_ty) / SUM(orders_ly) - 1), 4)         AS traffic_pct,
       ROUND(100 * ((SUM(sales_ty) / SUM(orders_ty))
                  / (SUM(sales_ly) / SUM(orders_ly)) - 1), 4)       AS avg_check_pct
FROM comp c
JOIN market_dim m USING (market_iso)
GROUP BY m.market_code, m.display_order
ORDER BY m.display_order
```

**Caveats:**
- To measure a different period, replace `p.y2_start` and `p.y2_end` with that period's dates. The period needs a full year of data before it to compare against.
- For a chain total, select `coalesce(m.market_code, 'ALL') AS market_code` and end with `GROUP BY ROLLUP (m.market_code) ORDER BY GROUPING(m.market_code), MIN(m.display_order)`. The total row is labelled `ALL` and comes last; show it as "All markets".
- `comp_stores` counts every store that was in the comp base for **at least one month**. Stores that joined partway through the year are included only for their comp months. When you report a store count, say so, or also count the stores that were comp for all 12 months.
- Exchange-rate moves make USD comps differ from local-currency comps. If rates moved noticeably over the period, show the local-currency version too: drop `* fx.usd_per_local`.

## Same-Store Sales by channel (or by store)

**Definition:** the same comp rule, broken down further. **The comp rule stays at store level:** a store-month either counts or it doesn't, whatever the channel. Every comp store-month is paired with every channel, so a channel with sales in only one of the two years still counts.

`contribution_pts` is how many points each channel adds to its market's same-store sales. They sum to the market's `sss_pct`.

```sql
WITH periods AS (
    SELECT date_trunc('month', max(business_date) + INTERVAL 1 DAY)::DATE                      AS y2_end,
           (date_trunc('month', max(business_date) + INTERVAL 1 DAY) - INTERVAL 12 MONTH)::DATE AS y2_start
    FROM orders
),
store_channel_month AS (
    SELECT o.store_id,
           o.channel_id,
           date_trunc('month', o.business_date) AS month,
           COUNT(*) AS orders,
           SUM(coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local) AS net_sales_usd
    FROM orders o
    JOIN exchange_rates fx ON fx.curn_iso = o.curn_iso AND fx.month = date_trunc('month', o.business_date)
    GROUP BY ALL
),
comp_month AS (
    -- The comp rule stays at store level: which store-months count, whatever the channel.
    SELECT s.store_id, s.market_iso, m.month
    FROM store_dim s
    CROSS JOIN (SELECT DISTINCT month FROM exchange_rates) m
    CROSS JOIN periods p
    WHERE m.month >= p.y2_start AND m.month < p.y2_end
      AND date_trunc('month', s.open_date - INTERVAL 1 DAY) + INTERVAL 14 MONTH <= m.month
),
comp AS (
    -- Every comp store-month x every channel, so a channel with sales in only one year still counts.
    SELECT c.market_iso,
           ch.channel_id,
           coalesce(ty.net_sales_usd, 0) AS sales_ty,
           coalesce(ly.net_sales_usd, 0) AS sales_ly,
           coalesce(ty.orders, 0)        AS orders_ty,
           coalesce(ly.orders, 0)        AS orders_ly
    FROM comp_month c
    CROSS JOIN channel_dim ch
    LEFT JOIN store_channel_month ty
      ON ty.store_id = c.store_id AND ty.channel_id = ch.channel_id AND ty.month = c.month
    LEFT JOIN store_channel_month ly
      ON ly.store_id = c.store_id AND ly.channel_id = ch.channel_id AND ly.month = c.month - INTERVAL 12 MONTH
)
SELECT m.market_code,
       ch.channel_name,
       ROUND(100 * (SUM(sales_ty) / NULLIF(SUM(sales_ly), 0) - 1), 4)     AS sss_pct,
       ROUND(100 * (SUM(orders_ty) / NULLIF(SUM(orders_ly), 0) - 1), 4)   AS traffic_pct,
       -- Points this channel adds to its market's same-store sales; they sum to the market's sss_pct.
       ROUND(100 * (SUM(sales_ty) - SUM(sales_ly))
             / SUM(SUM(sales_ly)) OVER (PARTITION BY m.market_code), 4)  AS contribution_pts
FROM comp c
JOIN market_dim m USING (market_iso)
JOIN channel_dim ch USING (channel_id)
GROUP BY m.market_code, m.display_order, ch.channel_name, ch.display_order
HAVING SUM(sales_ty) + SUM(sales_ly) > 0
ORDER BY m.display_order, ch.display_order
```

**Caveats:**
- To break down by store instead, swap `channel_id` for `store_id` in `comp` and the final `GROUP BY`. The CTE `store_channel_month` already has both.
- Drive-thru only exists at freestanding restaurants. Rows with no sales in either year are dropped by the `HAVING`.

## Share of a change

**Definition:** how much of a total change one group accounts for: (the group's change) ÷ (the total change), as a %. Use it for "what's driving the decline?" questions. It's only meaningful when the group changes point the same way as the total. Say so if some groups moved the other way.

```sql
-- given one row per group with value_ty and value_ly:
(value_ty - value_ly) / SUM(value_ty - value_ly) OVER () AS share_of_change
```

## Traffic vs. Average Check (what's driving growth)

**Definition:** sales growth splits into how many orders (traffic) and how much each order spends (check):

```
(1 + sales growth) = (1 + traffic growth) × (1 + average check growth)
```

Use the `traffic_pct` and `avg_check_pct` columns from the Same-Store Sales query. That way both halves use the same comp stores.

**Caveats:**
- **Check growth = menu price increases + mix.** Mix means things like guests shifting to bigger-check channels (mobile, delivery) or buying more items.
- **US and Canada: measuring pure price** (Mexico has no line prices: data issue `MX-NO-ITEM-PRICES`). Use a fixed-basket price index over the same comp stores and periods: price last year's units at this year's average `unit_price`, compared with last year's prices. The difference between check growth and price growth is mix. To find when prices changed, look for the dates `unit_price` steps up in `order_items`. If you split mix further (channel vs. items per order), the pieces multiply rather than add; say that.

  ```sql
  -- Fixed-basket menu price change, year 2 vs year 1, by market.
  -- Only lines with a price count, which leaves Mexico out (data issue MX-NO-ITEM-PRICES).
  WITH periods AS (
      SELECT date_trunc('month', max(business_date) + INTERVAL 1 DAY)::DATE                      AS y2_end,
             (date_trunc('month', max(business_date) + INTERVAL 1 DAY) - INTERVAL 12 MONTH)::DATE AS y2_start,
             (date_trunc('month', max(business_date) + INTERVAL 1 DAY) - INTERVAL 24 MONTH)::DATE AS y1_start
      FROM orders
  ),
  item_year AS (
      SELECT o.market_iso, i.item_id,
             CASE WHEN o.business_date >= p.y2_start THEN 'y2' ELSE 'y1' END AS yr,
             SUM(i.quantity) AS units,
             SUM(i.line_net_sales) / SUM(i.quantity) AS avg_price
      FROM order_items i
      JOIN orders o USING (order_id)
      CROSS JOIN periods p
      WHERE i.unit_price IS NOT NULL
        AND o.business_date >= p.y1_start AND o.business_date < p.y2_end
      GROUP BY ALL
  )
  SELECT y1.market_iso,
         ROUND(100 * (SUM(y1.units * y2.avg_price) / SUM(y1.units * y1.avg_price) - 1), 4) AS price_change_pct
  FROM item_year y1
  JOIN item_year y2 ON y2.market_iso = y1.market_iso AND y2.item_id = y1.item_id AND y2.yr = 'y2'
  WHERE y1.yr = 'y1'
  GROUP BY y1.market_iso
  ORDER BY y1.market_iso
  ```
- **Mexico:** there are no line prices, so price can't be measured from data. Say so, and report Mexico's check growth without a price/mix split (data issue `MX-NO-ITEM-PRICES`).
