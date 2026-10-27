# Data model

The Actual Burger Co. database: one DuckDB file in `data/`. Query it with the [`query-builder`](../../.claude/skills/query-builder/SKILL.md) skill's tool; the skill has the commands.

This file covers the tables, how they join, the rules for every query, and the **known data issues**. **Read it before writing any query**, then read these, in order:

| File | What's in it |
|---|---|
| [metrics.md](metrics.md) | Each standard metric's plain-English definition, its SQL, and its caveats |
| [tables/](tables/) | One doc per table: every column, its meaning and its quirks. Read the ones your query uses. |

## Tables

| Table | One row per | Use it for |
|---|---|---|
| [orders](tables/orders.md) | order | sales, transactions, average check, channel, time of day |
| [order_items](tables/order_items.md) | item line on an order | item mix, units, item sales (US and Canada; `MX-NO-ITEM-PRICES`) |
| [store_dim](tables/store_dim.md) | restaurant | market, city, format, open date (same-store rules) |
| [market_dim](tables/market_dim.md) | market (country) | market names and currencies |
| [channel_dim](tables/channel_dim.md) | channel | channel names |
| [item_dim](tables/item_dim.md) | menu item | item names and categories |
| [calendar_dim](tables/calendar_dim.md) | date | weeks, months, weekdays, same-day-last-year |
| [holiday_dim](tables/holiday_dim.md) | holiday in a market | explaining unusual days |
| [exchange_rates](tables/exchange_rates.md) | currency per month | converting local currency to USD |

## How the tables join

```
                  market_dim
                      │ market_iso
                      │
   channel_dim ── orders ── store_dim
    channel_id     │  │      store_id
                   │  │
                   │  └── exchange_rates   on curn_iso + month of business_date
                   │
              order_items ── item_dim
               order_id       item_id

   calendar_dim  on orders.business_date = calendar_dim.date
   holiday_dim   on date + market_iso
```

## Rules for every query

1. **Report sales in USD.** `orders` stores money in each market's local currency (see `market_dim`). Convert it with the exchange-rate join in [metrics.md](metrics.md).
2. **Use the standard net sales** from [metrics.md](metrics.md), never a raw sales column on its own. See data issue `MX-TIPS-FEES`.
3. **Times are local.** `pos_datetime` is the restaurant's local time, with no time zone. Compare hours across markets as local hours.
4. **Restaurants are closed on Dec 25.** There are no orders that day. That's a real closure, not missing data.
5. **`orders.market_iso` and `orders.curn_iso` repeat store facts.** They always agree with `store_dim`. Use them to skip a join.
6. **The latest period ends at the last date in the data** (`max(orders.business_date)`). In this demo dataset that's always the end of a month: treat that month as complete, even if today's date is earlier, with no need to caveat it for executives. With real data, cut every period at the last complete day and say so.

## Known data issues

Each issue has a short tag, like a ticket ID, and the same three parts: **What** is wrong in the data, **The rule** for querying around it, and **What to say** to the person asking. [metrics.md](metrics.md), the table docs and query comments cite an issue by its tag wherever it matters.

- **To add an issue:** copy this format and give it a new tag. Never reuse an old one.
- **When an issue is fixed:** delete its section, then search the project for its tag and update every place that cites it.

### Mexico item lines have quantities only `MX-NO-ITEM-PRICES`

- **What:** Mexico's `order_items.unit_price` and `line_net_sales` are **NULL**; only `quantity` is filled. Mexico's menu prices and price changes can't be seen in the data.
- **The rule:** analyze Mexico's items by units (`quantity`), not sales. Don't try to rebuild Mexico's sales from line items; use `orders`.
- **What to say:** when an item or price question includes Mexico, say that its item sales and price changes can't be measured from the data. Don't estimate them.

### Mexico can't separate delivery tips and fees `MX-TIPS-FEES`

- **What:** Mexico's POS doesn't report tips and delivery fees separately, so `orders.net_sales_excl_tips_fees` is **NULL for every Mexico order**, and its `net_sales` includes tips and fees on delivery orders. We don't know Mexico's true net sales for delivery orders.
- **The rule:** use the standard net sales in [metrics.md](metrics.md), which falls back to `net_sales` where tips and fees can't be separated. Never sum either column on its own: `net_sales` includes tips and fees, and `net_sales_excl_tips_fees` silently drops Mexico. The result is exact for every non-delivery order, because those have no tips or fees.
- **What to say** (always, when it applies):
  - **Mexico's delivery sales and delivery average check are inflated** by tips and fees, by an unknown amount. Its fee and tipping habits differ from the US and Canada, so don't correct it with their rates. If someone needs an estimate, give a range, label it as an assumption, and keep the unadjusted number alongside it. **Flag this whenever delivery sales, delivery share or average check are compared across markets.**
  - **Mexico's overall average check and delivery channel share are inflated too**, because delivery is a large share of Mexico's sales.
  - **Mexico's growth rates are barely affected**, because both years carry the same issue. Say "barely affected", not "unaffected". The exception: if delivery's share of Mexico's sales moved more than a couple of points between the periods, mention that its check growth may be slightly overstated.
