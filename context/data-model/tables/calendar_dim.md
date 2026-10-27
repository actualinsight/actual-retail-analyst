# calendar_dim

**Purpose:** a date table for grouping by week, month, quarter or weekday, and for day-of-week-aligned comparisons.

**Grain:** one row per date, covering every date in the data.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `date` | DATE | The date. Join to `orders.business_date`. | 2025-11-28 |
| `year` | INTEGER | Calendar year. The fiscal year is the calendar year. | 2025 |
| `quarter` | INTEGER | Calendar quarter, 1–4. | 4 |
| `month` | INTEGER | Month number, 1–12. | 11 |
| `month_name` | VARCHAR | Month name. | November |
| `week_start` | DATE | The Monday that starts this date's week. | 2025-11-24 |
| `day_of_week` | INTEGER | 1 = Monday … 7 = Sunday. | 5 |
| `day_name` | VARCHAR | Weekday name. | Friday |
| `is_weekend` | BOOLEAN | Saturday or Sunday. | false |
| `same_day_last_year` | DATE | `date - 364 days`: the same weekday one year earlier. | 2024-11-29 |

## Keys & joins

- `date` → `orders.business_date`, `holiday_dim.date`

## Gotchas

- **For daily or weekly comparisons, use `same_day_last_year`** so Fridays compare to Fridays. Calendar dates shift weekday every year.
- **Holidays move.** US Thanksgiving was 2024-11-28 and 2025-11-27. Check `holiday_dim` when one day or week looks odd.
- **Year-over-year comparisons start one year after the first date in the data.** That's the first date with a full year of history before it.
