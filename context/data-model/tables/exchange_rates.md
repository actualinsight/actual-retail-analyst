# exchange_rates

**Purpose:** monthly average exchange rates for converting local-currency sales to USD. Every sales metric is reported in USD.

**Grain:** one row per currency per month, covering every month in the data.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `month` | DATE | First day of the month. | 2025-11-01 |
| `curn_iso` | INTEGER | Currency (ISO number): 840 USD, 124 CAD, 484 MXN. | 124 |
| `currency_code` | VARCHAR | Currency code. | CAD |
| `usd_per_local` | DECIMAL(12,6) | US dollars per 1 unit of local currency. **Multiply** local amounts by this. | 0.725423 |

## Keys & joins

```sql
JOIN exchange_rates fx
  ON fx.curn_iso = o.curn_iso
 AND fx.month = date_trunc('month', o.business_date)
```

## Gotchas

- **USD has rows too**, with rate 1.0, so the same join works for every order.
- **Multiply, don't divide:** `local × usd_per_local = USD`.
- **Rates move over time,** so USD growth rates can differ from local-currency growth rates. What to do about it is in the Same-Store Sales % caveats in [metrics.md](../metrics.md).
- **Convert each order at its own month's rate** before adding up. Don't convert a yearly total at one average rate.
