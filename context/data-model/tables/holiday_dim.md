# holiday_dim

**Purpose:** public holidays and big days in each market. Use it to explain unusual days. Holidays differ by country, so each row belongs to one market.

**Grain:** one row per holiday per market.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `date` | DATE | Holiday date. | 2024-11-28 |
| `market_iso` | INTEGER | Market the holiday applies to. | 840 |
| `holiday_name` | VARCHAR | Name. Mexico's names are in Spanish, without accents. | Thanksgiving |

## Keys & joins

- `date` + `market_iso` → `orders` (`business_date`, `market_iso`). Always join on both.

## What holidays do to sales

| Effect | Holidays |
|---|---|
| Closed, no orders | Christmas Day / Navidad (Dec 25), every market |
| Quieter | Christmas Eve / Nochebuena, New Year's Eve and Day, US Thanksgiving (much quieter), Canadian Thanksgiving, Dia de Muertos |
| Busier | US Memorial Day, Independence Day, Labor Day; Canada Day, Victoria Day, Family Day, Labour Day, Boxing Day; Mexico's Independence Day (Sep 16) and long-weekend Mondays |

## Gotchas

- **Two different Thanksgivings.** Canada's is in October and the US's in November. Always filter by `market_iso`.
- **Moving holidays.** Thanksgiving, Memorial Day and others land on different dates each year. That can shift a week's year-over-year result.
