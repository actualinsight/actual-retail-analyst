# Brand

How dashboards look. The dashboard-builder skill's build script reads this folder and nothing else for colors, fonts and logos, so **change these files and every new dashboard changes with them.** You don't need to touch any other part of the skill or its code.

## What's here

| File | What it is |
|---|---|
| `tokens.json` | The colors, the font, and which logo to use (details below) |
| `logo-mark.svg` | The square logo shown in the dashboard's top-left corner (the file `logo` in `tokens.json` names) |

## Colors (`tokens.json` → `colors`)

The values are in `tokens.json`; change them there. How the agent uses each color in charts is in [choosing-visuals.md](../choosing-visuals.md).

| Name | Used for |
|---|---|
| `text` | Body text and headings |
| `background` | Page background |
| `card` | Card backgrounds |
| `rule` | Borders, dividers, chart gridlines |
| `accent` | Active tabs, badges, links |
| `accent_light` | Highlights on dark backgrounds |
| `positive` | Positive numbers (e.g. +6.7%) |
| `negative` | Negative numbers and caveat boxes |
| `highlight` | "Next steps" boxes |

## Chart colors (`tokens.json` → `series`)

An ordered list of colors for the things a chart compares (markets, channels...). Keep warning-style colors out of it, so `negative` is the only color that means "caution".

## Font (`tokens.json` → `font`)

The font family, its Google Fonts link, and a `fallback` the dashboard uses when there's no internet.

## Using your own brand

1. Replace `logo-mark.svg` with your logo, keeping the file name, or change `"logo"` in `tokens.json` to your file's name.
2. Change the hex color values in `tokens.json`. Keep `negative` a warning-style color.
3. To change the font: set `family` to any Google Fonts family, and paste that font's link from fonts.google.com into `google_fonts_url`.
4. Ask the agent to rebuild a dashboard to see the result.
