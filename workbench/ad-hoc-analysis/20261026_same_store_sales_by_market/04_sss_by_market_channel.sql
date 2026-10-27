-- Question:   How are same-store sales by market? Follow-up: "Can we see this by channel too?"
-- Asked:      2026-10-26 · Period: Nov 2025–Oct 2026 vs Nov 2024–Oct 2025
-- Scope:      US, Canada, Mexico + all-markets total · each channel (In-Store, Drive-Thru, Mobile, Delivery) · comp stores (standard comp rule)
-- Metric:     Same-Store Sales by channel: sss_pct, traffic_pct, contribution_pts (context/data-model/metrics.md),
--             plus avg_check_pct (Average Check growth, same formula as the Same-Store Sales query)
-- Data notes: MX-TIPS-FEES: Mexico can't separate delivery tips and fees, so its Delivery sales include them
--             (its Delivery growth is barely affected; its Delivery dollar levels and share are inflated)
-- Dialect:    DuckDB (other databases may need small syntax changes)
--
-- Canonical "Same-Store Sales by channel" query, with an all-markets total by channel added
-- (GROUPING SETS) and comp sales both years so channels can be reconciled to 01_sss_by_market.

WITH store_channel_month AS (
    SELECT o.store_id,
           o.channel_id,
           date_trunc('month', o.business_date) AS month,
           COUNT(*) AS orders,
           -- DATA ISSUE: MX-TIPS-FEES, Mexico has no net_sales_excl_tips_fees, so its Delivery orders keep tips and fees.
           SUM(coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local) AS net_sales_usd
    FROM orders o
    -- Convert each order at its own month's rate (USD rows have rate 1.0).
    JOIN exchange_rates fx ON fx.curn_iso = o.curn_iso AND fx.month = date_trunc('month', o.business_date)
    GROUP BY ALL
),
comp_month AS (
    -- The comp rule stays at store level: which store-months count, whatever the channel.
    SELECT s.store_id, s.market_iso, m.month
    FROM store_dim s
    CROSS JOIN (SELECT DISTINCT month FROM exchange_rates
                -- DECISION: latest 12 months (Nov 2025–Oct 2026) vs the prior 12, per analyst
                WHERE month >= DATE '2025-11-01' AND month < DATE '2026-11-01') m
    WHERE date_trunc('month', s.open_date - INTERVAL 1 DAY) + INTERVAL 14 MONTH <= m.month
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
-- DECISION: by channel within each market, plus an all-markets row per channel (market_code ALL, after the markets), per analyst follow-up
SELECT coalesce(m.market_code, 'ALL')                                       AS market_code,
       ch.channel_name,
       ROUND(SUM(sales_ty), 2)                                              AS sales_ty_usd,
       ROUND(SUM(sales_ly), 2)                                              AS sales_ly_usd,
       ROUND(100 * (SUM(sales_ty) / NULLIF(SUM(sales_ly), 0) - 1), 4)       AS sss_pct,
       ROUND(100 * (SUM(orders_ty) / NULLIF(SUM(orders_ly), 0) - 1), 4)     AS traffic_pct,
       ROUND(100 * ((SUM(sales_ty) / NULLIF(SUM(orders_ty), 0))
                  / (SUM(sales_ly) / NULLIF(SUM(orders_ly), 0)) - 1), 4)   AS avg_check_pct,
       -- Points this channel adds to its market's same-store sales; they sum to the market's sss_pct.
       ROUND(100 * (SUM(sales_ty) - SUM(sales_ly))
             / SUM(SUM(sales_ly)) OVER (PARTITION BY coalesce(m.market_code, 'ALL')), 4) AS contribution_pts
FROM comp c
JOIN market_dim m USING (market_iso)
JOIN channel_dim ch USING (channel_id)
GROUP BY GROUPING SETS ((m.market_code, ch.channel_name), (ch.channel_name))
-- Drive-Thru only exists at freestanding restaurants; rows with no sales in either year are dropped.
HAVING SUM(sales_ty) + SUM(sales_ly) > 0
ORDER BY GROUPING(m.market_code), MIN(m.display_order), MIN(ch.display_order)
