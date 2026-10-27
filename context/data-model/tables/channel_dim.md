# channel_dim

**Purpose:** names for the ways guests order.

**Grain:** one row per channel.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `channel_id` | INTEGER | Channel key used on `orders`. | 3 |
| `channel_name` | VARCHAR | Display name. | Mobile |
| `display_order` | INTEGER | The order channels appear in reports and charts. Always `ORDER BY display_order`. | 3 |

All rows:

| channel_id | channel_name | What it is |
|---|---|---|
| 1 | In-Store | Ordered at the counter |
| 2 | Drive-Thru | Freestanding restaurants only |
| 3 | Mobile | Ordered ahead in the Actual App, picked up in store |
| 4 | Delivery | Third-party delivery. Only this channel has tips and fees. |

## Keys & joins

- `channel_id` → `orders.channel_id`

## Gotchas

- **"Digital" isn't a channel here.** See Channel Mix % in [metrics.md](../metrics.md) for how to handle it.
