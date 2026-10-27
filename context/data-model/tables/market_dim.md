# market_dim

**Purpose:** the markets (countries) and their currencies.

**Grain:** one row per market.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `market_iso` | INTEGER | ISO 3166 numeric country code. The key used across the database. | 840 |
| `market_code` | VARCHAR | Short code: US, CA, MX. Use it in output. | US |
| `market_name` | VARCHAR | Full name. | United States |
| `curn_iso` | INTEGER | ISO 4217 numeric currency code of the market. | 840 |
| `currency_code` | VARCHAR | Currency: USD, CAD, MXN. | USD |
| `display_order` | INTEGER | The order markets appear in reports and charts (and so which chart color each gets). Always `ORDER BY display_order`. | 1 |

All rows:

| market_iso | market_code | market_name | curn_iso | currency_code | display_order |
|---|---|---|---|---|---|
| 840 | US | United States | 840 | USD | 1 |
| 124 | CA | Canada | 124 | CAD | 2 |
| 484 | MX | Mexico | 484 | MXN | 3 |

## Keys & joins

- `market_iso` → `orders.market_iso`, `store_dim.market_iso`, `holiday_dim.market_iso`
- `curn_iso` → `exchange_rates.curn_iso`

## Gotchas

- **For the current markets, the country number and the currency number happen to be the same** (840, 124, 484). Still join currency on `curn_iso` and market on `market_iso`. A copy of this template with other countries won't be so lucky.
