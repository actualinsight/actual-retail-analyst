-- Question:   Data check for "How are same-store sales by market?": did delivery's share of
--             comp-store sales move between the two years? (Mexico tips-and-fees rule)
-- Asked:      2026-10-26 · Period: Nov 2025–Oct 2026 vs Nov 2024–Oct 2025
-- Scope:      US, Canada, Mexico · Delivery vs all channels · comp store-months (standard comp rule)
-- Metric:     Channel Mix % (share of Net Sales USD), on the same comp store-months as Same-Store Sales %
--             (context/data-model/metrics.md)
-- Data notes: MX-TIPS-FEES: Mexico can't separate delivery tips and fees, so its delivery share is inflated;
--             the point here is whether it MOVED, which decides whether its check growth may be overstated
-- Dialect:    DuckDB (other databases may need small syntax changes)

WITH store_channel_month AS (
    SELECT o.store_id,
           o.channel_id,
           date_trunc('month', o.business_date) AS month,
           -- DATA ISSUE: MX-TIPS-FEES, Mexico has no net_sales_excl_tips_fees, so its delivery orders keep tips and fees.
           SUM(coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local) AS net_sales_usd
    FROM orders o
    JOIN exchange_rates fx ON fx.curn_iso = o.curn_iso AND fx.month = date_trunc('month', o.business_date)
    GROUP BY ALL
),
comp_month AS (
    -- Same comp store-months as the Same-Store Sales query (comp rule at store level).
    SELECT s.store_id, s.market_iso, m.month
    FROM store_dim s
    CROSS JOIN (SELECT DISTINCT month FROM exchange_rates
                -- DECISION: latest 12 months (Nov 2025–Oct 2026) vs the prior 12, per analyst
                WHERE month >= DATE '2025-11-01' AND month < DATE '2026-11-01') m
    WHERE date_trunc('month', s.open_date - INTERVAL 1 DAY) + INTERVAL 14 MONTH <= m.month
),
comp AS (
    SELECT c.market_iso,
           ty.channel_id,
           ty.net_sales_usd AS sales_ty,
           0                AS sales_ly
    FROM comp_month c
    JOIN store_channel_month ty ON ty.store_id = c.store_id AND ty.month = c.month
    UNION ALL
    SELECT c.market_iso,
           ly.channel_id,
           0,
           ly.net_sales_usd
    FROM comp_month c
    -- The year-ago month of each comp store-month
    JOIN store_channel_month ly ON ly.store_id = c.store_id AND ly.month = c.month - INTERVAL 12 MONTH
)
SELECT m.market_code,
       -- Comp sales, all channels: should match 01_sss_by_market
       ROUND(SUM(sales_ty), 2)                                                              AS sales_ty_usd,
       ROUND(SUM(sales_ly), 2)                                                              AS sales_ly_usd,
       ROUND(100 * SUM(CASE WHEN channel_id = 4 THEN sales_ly ELSE 0 END) / SUM(sales_ly), 4) AS delivery_share_ly_pct,
       ROUND(100 * SUM(CASE WHEN channel_id = 4 THEN sales_ty ELSE 0 END) / SUM(sales_ty), 4) AS delivery_share_ty_pct,
       ROUND(100 * SUM(CASE WHEN channel_id = 4 THEN sales_ty ELSE 0 END) / SUM(sales_ty)
           - 100 * SUM(CASE WHEN channel_id = 4 THEN sales_ly ELSE 0 END) / SUM(sales_ly), 4) AS delivery_share_change_pts
FROM comp c
JOIN market_dim m USING (market_iso)
GROUP BY m.market_code, m.display_order
ORDER BY m.display_order
