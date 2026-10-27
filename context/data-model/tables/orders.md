# orders

**Purpose:** every order placed at an Actual Burger Co. restaurant. This is the main table for sales, transactions (traffic), average check and channel mix.

**Grain:** one row per order. Millions of rows, so always aggregate in SQL.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `order_id` | BIGINT | Unique order ID. The first digits are the store_id (`store_id × 10,000,000 + sequence`). | 10010000014 |
| `market_iso` | INTEGER | Market (ISO country number): 840 US, 124 Canada, 484 Mexico. Same as the store's. | 840 |
| `curn_iso` | INTEGER | Currency the money columns are in (ISO currency number): 840 USD, 124 CAD, 484 MXN. | 840 |
| `store_id` | INTEGER | Restaurant. Joins to `store_dim`. | 1001 |
| `channel_id` | INTEGER | How the order was placed. Joins to `channel_dim` (1 In-Store, 2 Drive-Thru, 3 Mobile, 4 Delivery). | 4 |
| `business_date` | DATE | The day the order counts toward. Use this for all date logic. | 2024-11-01 |
| `pos_datetime` | TIMESTAMP | When the order was placed, **restaurant local time**. Use for hour-of-day analysis. | 2024-11-01 11:12:46 |
| `items` | INTEGER | Total item quantity on the order (sum of `order_items.quantity`). | 2 |
| `net_sales` | DECIMAL(10,2) | Order total in local currency. **Includes delivery tips and fees** on delivery orders. | 15.72 |
| `net_sales_excl_tips_fees` | DECIMAL(10,2) | Order total excluding delivery tips and fees. Equals `net_sales` for non-delivery orders. **NULL for every Mexico order** (`MX-TIPS-FEES`). | 10.48 |

## Keys & joins

- `store_id` → `store_dim.store_id`
- `channel_id` → `channel_dim.channel_id`
- `market_iso` → `market_dim.market_iso`
- `order_id` → `order_items.order_id` (one order, many lines)
- `curn_iso` + `date_trunc('month', business_date)` → `exchange_rates` (`curn_iso`, `month`)
- `business_date` → `calendar_dim.date`

## Gotchas

- **Money is in local currency.** Convert to USD before adding up across markets.
- **Net sales:** use the standard net sales in [metrics.md](../metrics.md), never a raw sales column on its own. Mexico's delivery numbers include tips and fees: see data issue `MX-TIPS-FEES` in [context.md](../context.md).
- **No rows on Dec 25.** Restaurants are closed.
- **New restaurants have no rows before their `open_date`.** Same-store comparisons need the comp rule in [metrics.md](../metrics.md).
