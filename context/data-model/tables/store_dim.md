# store_dim

**Purpose:** the list of restaurants and their attributes. Use it for market, city, format and the open date that drives same-store rules.

**Grain:** one row per restaurant.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `store_id` | INTEGER | Restaurant ID. 1xxx US, 2xxx Canada, 3xxx Mexico. | 1001 |
| `store_name` | VARCHAR | Short name, usually city plus neighbourhood. | Austin South Congress |
| `market_iso` | INTEGER | Market (ISO country number): 840 US, 124 Canada, 484 Mexico. | 840 |
| `city` | VARCHAR | City. | Austin |
| `state_province` | VARCHAR | State or province code. | TX |
| `store_type` | VARCHAR | `Freestanding` (has a drive-thru) or `Urban` (no drive-thru). | Freestanding |
| `has_drive_thru` | BOOLEAN | True for freestanding restaurants. | true |
| `open_date` | DATE | First day of trading. | 2014-05-12 |

## Keys & joins

- `store_id` → `orders.store_id`
- `market_iso` → `market_dim.market_iso`

## Gotchas

- **Some restaurants opened during the data window** (`open_date` after the first date in the data). Comparing total sales across years mixes in these new stores. Use same-store sales for like-for-like growth. See [metrics.md](../metrics.md).
- **Drive-thru orders only come from freestanding restaurants.** Urban restaurants spread their orders across the other channels.
- **There are no closed restaurants.** Every restaurant is still trading on the last date in the data.
