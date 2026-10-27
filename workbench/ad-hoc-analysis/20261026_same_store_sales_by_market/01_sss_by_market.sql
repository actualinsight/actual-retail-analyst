-- Question:   How are same-store sales by market?
-- Asked:      2026-10-26 · Period: Nov 2025–Oct 2026 vs Nov 2024–Oct 2025
-- Scope:      US, Canada, Mexico + all-markets total · all channels · comp stores (standard comp rule)
-- Metric:     Same-Store Sales %, with same-store traffic % and average check % (context/data-model/metrics.md)
-- Data notes: MX-TIPS-FEES: Mexico can't separate delivery tips and fees; its net sales include them (growth barely affected)
-- Dialect:    DuckDB (other databases may need small syntax changes)
--
-- Canonical year-2-vs-year-1 SSS query, with the standard ALL rollup for the chain total.
-- Added columns: full_year_comp_stores (stores comp in all 12 months), sales_ty_usd and
-- sales_ly_usd (comp sales, so the monthly pull can be reconciled to this one).

WITH store_month AS (
    SELECT o.store_id,
           o.market_iso,
           date_trunc('month', o.business_date) AS month,
           COUNT(*) AS orders,
           -- DATA ISSUE: MX-TIPS-FEES, Mexico has no net_sales_excl_tips_fees, so its delivery orders keep tips and fees.
           SUM(coalesce(o.net_sales_excl_tips_fees, o.net_sales) * fx.usd_per_local) AS net_sales_usd
    FROM orders o
    -- Convert each order at its own month's rate (USD rows have rate 1.0).
    JOIN exchange_rates fx ON fx.curn_iso = o.curn_iso AND fx.month = date_trunc('month', o.business_date)
    GROUP BY ALL
),
comp AS (
    SELECT ty.market_iso,
           ty.store_id,
           ty.month,
           ty.net_sales_usd AS sales_ty,
           ly.net_sales_usd AS sales_ly,
           ty.orders        AS orders_ty,
           ly.orders        AS orders_ly
    FROM store_month ty
    -- Each comp store-month is compared with the same store's same month a year earlier.
    JOIN store_month ly
      ON ly.store_id = ty.store_id
     AND ly.month = ty.month - INTERVAL 12 MONTH
    JOIN store_dim s ON s.store_id = ty.store_id
    -- DECISION: latest 12 months (Nov 2025–Oct 2026) vs the prior 12, per analyst
    WHERE ty.month >= DATE '2025-11-01' AND ty.month < DATE '2026-11-01'
      -- Comp rule: open at least 13 full months before the month measured
      AND date_trunc('month', s.open_date - INTERVAL 1 DAY) + INTERVAL 14 MONTH <= ty.month
),
store_comp_months AS (
    -- How many of the 12 months each store was in the comp base
    SELECT store_id, COUNT(*) AS comp_months
    FROM comp
    GROUP BY store_id
)
-- DECISION: all three markets plus an all-markets total (labelled ALL, shown last)
SELECT coalesce(m.market_code, 'ALL')                                AS market_code,
       CASE WHEN GROUPING(m.market_code) = 1 THEN 'All markets'
            ELSE MIN(m.market_name) END                              AS market_name,
       COUNT(DISTINCT c.store_id)                                    AS comp_stores,
       COUNT(DISTINCT CASE WHEN scm.comp_months = 12 THEN c.store_id END) AS full_year_comp_stores,
       ROUND(SUM(sales_ty), 2)                                       AS sales_ty_usd,
       ROUND(SUM(sales_ly), 2)                                       AS sales_ly_usd,
       ROUND(100 * (SUM(sales_ty) / SUM(sales_ly) - 1), 4)           AS sss_pct,
       ROUND(100 * (SUM(orders_ty) / SUM(orders_ly) - 1), 4)         AS traffic_pct,
       ROUND(100 * ((SUM(sales_ty) / SUM(orders_ty))
                  / (SUM(sales_ly) / SUM(orders_ly)) - 1), 4)       AS avg_check_pct
FROM comp c
JOIN store_comp_months scm USING (store_id)
JOIN market_dim m USING (market_iso)
GROUP BY ROLLUP (m.market_code)
ORDER BY GROUPING(m.market_code), MIN(m.display_order)
