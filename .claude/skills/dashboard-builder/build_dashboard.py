"""Turn an analysis folder into one self-contained dashboard.html.

    python .claude/skills/dashboard-builder/build_dashboard.py workbench/ad-hoc-analysis/<folder>

The agent writes the page as dashboard.template.html in the analysis folder,
with three markers this script fills in:

    <!-- BRAND_HEAD -->  font link + color variables from brand/tokens.json
    <!-- LOGO -->        the logo SVG from brand/
    <!-- SCRIPTS -->     the chart library, then `const DATA = {...}` built from
                         every NN_*.csv in the folder (DATA["01_name"] = list of rows)

The result opens in any browser with no internet (only the font is fetched,
with a fallback). The agent never copies numbers into the page by hand.

To change a built dashboard, get its template back first:

    python .claude/skills/dashboard-builder/build_dashboard.py <folder> --edit

Each filled-in marker is wrapped in start/end comments, so --edit can swap it
back for the marker and recreate the exact page that was approved.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
CHART_JS = SKILL_DIR / "assets" / "chart.umd.min.js"
TEMPLATE_NAME = "dashboard.template.html"
OUTPUT_NAME = "dashboard.html"
MARKERS = ("<!-- BRAND_HEAD -->", "<!-- LOGO -->", "<!-- SCRIPTS -->")


def _wrap(marker: str) -> tuple[str, str]:
    """The comments around a filled-in marker: <!-- LOGO start --> ... <!-- LOGO end -->."""
    return marker.replace(" -->", " start -->"), marker.replace(" -->", " end -->")
# A dashboard shows summaries. Thousands of rows means the pull wasn't aggregated.
MAX_ROWS = 20_000


def _value(text: str):
    """CSV text -> number where it looks like one, None where empty."""
    if text == "":
        return None
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    return text


def load_data(folder: Path) -> dict:
    data, total = {}, 0
    for path in sorted(folder.glob("[0-9][0-9]_*.csv")):
        with open(path, newline="", encoding="utf-8") as f:
            rows = [{k: _value(v) for k, v in row.items()} for row in csv.DictReader(f)]
        data[path.stem] = rows
        total += len(rows)
    if total > MAX_ROWS:
        raise ValueError(f"The CSVs hold {total:,} rows, but a dashboard should show summaries: "
                         f"aggregate the data pulls first (limit {MAX_ROWS:,} rows).")
    return data


def _safe_json(data: dict) -> str:
    # Escape <, > and & so no value can close the <script> tag it sits in.
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def brand_head(tokens: dict) -> str:
    font = tokens["font"]
    variables = [f"--font: '{font['family']}', {font['fallback']};"]
    variables += [f"--{name.replace('_', '-')}: {value};" for name, value in tokens["colors"].items()]
    variables += [f"--series-{i}: {value};" for i, value in enumerate(tokens["series"])]
    return (f'<link rel="stylesheet" href="{font["google_fonts_url"]}">\n'
            f"<style>:root {{ {' '.join(variables)} }}</style>")


def build_dashboard(folder: Path, keep_template: bool = False) -> Path:
    folder = Path(folder)
    template_path = folder / TEMPLATE_NAME
    if not template_path.exists():
        raise FileNotFoundError(f"No {TEMPLATE_NAME} in {folder}")
    template = template_path.read_text(encoding="utf-8")
    for marker in MARKERS:
        if template.count(marker) != 1:
            raise ValueError(f"The template must contain the {marker} marker exactly once.")
    if re.search(r"<script[^>]*\bsrc=", template, flags=re.I):
        raise ValueError("The template loads an external script; everything must be inline.")

    brand = SKILL_DIR / "brand"
    tokens = json.loads((brand / "tokens.json").read_text(encoding="utf-8"))
    logo = (brand / tokens["logo"]).read_text(encoding="utf-8")
    logo = re.sub(r"<\?xml[^>]*\?>\s*", "", logo)
    data = load_data(folder)

    scripts = (f"<script>\n{CHART_JS.read_text(encoding='utf-8')}\n</script>\n"
               f"<script>const DATA = {_safe_json(data)};</script>")
    html = template
    for marker, filled in zip(MARKERS, (brand_head(tokens), logo, scripts)):
        start, end = _wrap(marker)
        html = html.replace(marker, f"{start}\n{filled}\n{end}")

    # Write to a side file and swap it in, so a failed build never leaves half a page.
    out = folder / OUTPUT_NAME
    building = folder / (OUTPUT_NAME + ".building")
    try:
        building.write_text(html, encoding="utf-8")
        os.replace(building, out)
    finally:
        if building.exists():
            building.unlink()
    if not keep_template:
        template_path.unlink()
    return out


def edit_template(folder: Path) -> Path:
    """Recreate dashboard.template.html from a built dashboard.html, so it can be changed."""
    folder = Path(folder)
    built, template_path = folder / OUTPUT_NAME, folder / TEMPLATE_NAME
    if not built.exists():
        raise FileNotFoundError(f"No {OUTPUT_NAME} in {folder}")
    if template_path.exists():
        raise ValueError(f"{TEMPLATE_NAME} already exists in {folder}: edit that one.")
    html = built.read_text(encoding="utf-8")
    for marker in MARKERS:
        start, end = _wrap(marker)
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), flags=re.S)
        if len(pattern.findall(html)) != 1:
            raise ValueError(f"Can't find the {marker} section in {OUTPUT_NAME}. It was built by an "
                             "older version of this script: rebuild it from reference-dashboard.html.")
        html = pattern.sub(lambda _: marker, html)
    template_path.write_text(html, encoding="utf-8")
    return template_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build dashboard.html for an analysis folder.")
    parser.add_argument("folder", type=Path)
    parser.add_argument("--keep-template", action="store_true",
                        help="keep dashboard.template.html for further edits")
    parser.add_argument("--edit", action="store_true",
                        help="recreate dashboard.template.html from dashboard.html, to change it")
    args = parser.parse_args(argv)
    if args.edit:
        try:
            path = edit_template(args.folder)
        except (ValueError, FileNotFoundError) as err:
            print(f"Template not recreated: {err}")
            return 1
        print(f"Wrote {path}. Change it, then build again.")
        return 0
    try:
        out = build_dashboard(args.folder, args.keep_template)
    except (ValueError, FileNotFoundError) as err:
        print(f"Dashboard not built: {err}")
        return 1
    print(f"Built {out} ({out.stat().st_size / 1000:,.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
