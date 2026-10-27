# order_items

**Purpose:** what was on each order. Use it for item mix, units sold, and item sales (US and Canada only: data issue `MX-NO-ITEM-PRICES`).

**Grain:** one row per item per order (a line item). Millions of rows, so always aggregate in SQL. An order with 3 burgers and a drink has 2 lines.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `order_id` | BIGINT | The order. Joins to `orders.order_id`. | 10010000001 |
| `line_number` | INTEGER | Line position within the order, starting at 1. | 1 |
| `item_id` | INTEGER | Menu item. Joins to `item_dim`. | 1 |
| `quantity` | INTEGER | Units of this item on the order. | 3 |
| `unit_price` | DECIMAL(10,2) | Menu price per unit, in local currency, on that day. **NULL for Mexico** (`MX-NO-ITEM-PRICES`). | 7.49 |
| `line_net_sales` | DECIMAL(10,2) | `quantity × unit_price`. **NULL for Mexico** (`MX-NO-ITEM-PRICES`). | 22.47 |

## Keys & joins

- `order_id` → `orders.order_id`. Join to `orders` for store, market, channel, date and currency.
- `item_id` → `item_dim.item_id`

## Gotchas

- **Mexico has quantities only.** Analyze Mexico items by units. See data issue `MX-NO-ITEM-PRICES` in [context.md](../context.md).
- **For the US and Canada, an order's `line_net_sales` sum to `orders.net_sales_excl_tips_fees`.** Tips and fees are never line items. Mexico has no line sales (`MX-NO-ITEM-PRICES`).
- **No currency or date here.** Join to `orders` and convert with `exchange_rates` before comparing item sales across markets.
- **`unit_price` shows menu price increases** (US and Canada; `MX-NO-ITEM-PRICES`), so it's the cleanest way to measure pure price change. See Traffic vs. Average Check in [metrics.md](../metrics.md).
