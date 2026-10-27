# About Actual Burger Co.

> Fictional company. All data in this repo is generated demo data.

## The concept

**Actual Burger Co.** is a fast-casual chain built on one idea: *burgers and tacos, done right.* It runs a short menu, cooks fast, and prices a little above fast food. It's the place you pick when you want food you'd actually sit down for, but still need to be back at your desk in 30 minutes.

## Guests

- **Weekday lunch crowd:** office workers and trades, often ordering ahead on the app.
- **Families at dinner and on weekends**, often through the drive-thru or delivery.
- **Groups and offices** ordering delivery. These are the biggest orders of the day.

## History

| Year | Milestone |
|---|---|
| 2014 | First restaurant opens on South Congress in Austin, TX |
| 2016 | First Canadian restaurant (Toronto Queen West) |
| 2019 | First Mexican restaurant (San Pedro Garza Garcia, Monterrey) |
| 2023 | Actual App relaunched with order-ahead pickup ("Mobile") |

## Footprint

| Market | Currency | Metros |
|---|---|---|
| United States | USD | Austin, Dallas–Fort Worth, Houston, San Antonio, Denver, Phoenix; new in Nashville, Atlanta, Oklahoma City |
| Canada | CAD | Toronto area, Vancouver area, Calgary, Ottawa, Edmonton |
| Mexico | MXN | Monterrey, Mexico City, Guadalajara |

**Formats:**
- **Freestanding** restaurants have a drive-thru.
- **Urban** restaurants (downtowns and dense neighbourhoods) don't.

Most US and Canadian restaurants are freestanding. Mexico is mostly urban.

Restaurant counts and opening dates are in the data: query `store_dim`.

**Hours:** every restaurant is open 10:30–22:00 local time. All restaurants close on Christmas Day.

## How guests order (channels)

| Channel | What it is |
|---|---|
| In-Store | Order at the counter, eat in or take out |
| Drive-Thru | Freestanding restaurants only |
| Mobile | Order ahead in the Actual App, pick up in store |
| Delivery | Through third-party delivery partners. The guest pays a delivery fee and usually a tip, on top of the food. |

## Menu

A short menu of burgers, tacos, burritos and chicken sandwiches, with sides and drinks, the same in every market. The items and their prices come from the data: `item_dim` for items, `order_items.unit_price` for prices.

## FY2026 priorities

The fiscal year is the calendar year.

1. **Grow the Actual App.** Make Mobile the default way regulars order.
2. **Keep building the US.** Continue opening in the Southeast and Oklahoma.
3. **Get Canada's traffic growing again.** Leadership wants to know which restaurants and channels are behind.
4. **Scale Mexico.** It's the smallest market and the one with the most room to grow.
