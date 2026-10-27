# item_dim

**Purpose:** the menu: item names and categories.

**Grain:** one row per menu item.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `item_id` | INTEGER | Item key used on `order_items`. | 1 |
| `item_name` | VARCHAR | Menu name. | Burger |
| `category` | VARCHAR | `Entree`, `Side` or `Drink`. | Entree |

All rows:

| item_id | item_name | category |
|---|---|---|
| 1 | Burger | Entree |
| 2 | Chicken Sandwich | Entree |
| 3 | Burrito | Entree |
| 4 | Tacos (2) | Entree |
| 5 | Fries | Side |
| 6 | Chips | Side |
| 7 | Drink | Drink |

## Keys & joins

- `item_id` → `order_items.item_id`

## Gotchas

- **Prices aren't stored here.** They vary by market and change over time. See `order_items.unit_price` (US and Canada). Mexico has no prices in the data (`MX-NO-ITEM-PRICES`).
- **"Tacos (2)" is one unit** containing two tacos.
