"""Open a built dashboard in a real (headless) browser and check it works.

    python .claude/skills/dashboard-builder/check_dashboard.py <path to dashboard.html>

Uses Chrome, Edge or Chromium if one is installed. The network is blocked, so
this also proves the page works offline. It clicks every tab and reports:
script and console errors, tabs with no charts, charts that didn't draw or have
no data, tabs that don't change anything, and sideways scrolling at laptop and
phone widths. It also prints each tab's text, so the numbers on the page can be
checked against context.md. Exit code 0 = OK, 1 = problems, 2 = no browser found.
"""
from __future__ import annotations

import html
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WIDTHS = (1280, 390)

# Injected first in <head>: catches errors, then clicks each tab and records what rendered.
PROBE = r"""<script>
window.__errors = [];
window.addEventListener('error', e => window.__errors.push(String(e.message)));
const __consoleError = console.error;
console.error = (...args) => { window.__errors.push(args.map(String).join(' ')); __consoleError(...args); };
setTimeout(() => {
  const out = { views: [] };
  const tabs = [...document.querySelectorAll('[role=tab]')];
  const snap = label => ({
    tab: label,
    charts: (window.Chart ? Object.values(Chart.instances) : []).map(c => ({
      points: c.data.datasets.reduce((n, d) => n + (d.data || []).filter(v => v !== null && v !== undefined).length, 0),
      drawn: !!(c.canvas && c.canvas.isConnected && c.canvas.offsetWidth > 0 && c.canvas.offsetHeight > 0),
      data: JSON.stringify(c.data.datasets.map(d => d.data)) })),
    text: document.body.innerText.replace(/\s+/g, ' ').trim(),
    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  });
  if (tabs.length) { tabs.forEach(t => { t.click(); out.views.push(snap(t.textContent.trim())); }); tabs[0].click(); }
  else out.views.push(snap('page'));
  out.errors = window.__errors;
  const pre = document.createElement('pre'); pre.id = '__probe'; pre.textContent = JSON.stringify(out);
  document.body.appendChild(pre);
}, 1500);
</script>"""


def find_browser() -> str | None:
    names = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "chrome", "msedge"]
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    candidates = {
        "Darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                   "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
                   "/Applications/Chromium.app/Contents/MacOS/Chromium"],
        "Windows": [os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
                    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
                    os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
                    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe")],
    }.get(platform.system(), [])
    return next((c for c in candidates if Path(c).exists()), None)


def _run(browser: str, page: Path, width: int) -> dict:
    with tempfile.TemporaryDirectory() as profile:
        result = subprocess.run(
            [browser, "--headless=new", "--disable-gpu", f"--user-data-dir={profile}",
             "--host-resolver-rules=MAP * ~NOTFOUND", f"--window-size={width},2000",
             "--virtual-time-budget=5000", "--dump-dom", page.as_uri()],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    match = re.search(r'<pre id="__probe">(.*?)</pre>', result.stdout, flags=re.S)
    if not match:
        return {"views": [], "errors": ["The page never finished loading (no probe output)."]}
    return json.loads(html.unescape(match.group(1)))


def check_dashboard(path: Path) -> dict:
    """Return {"ok": bool, "errors": [...], "problems": [...], "views": [...]}."""
    browser = find_browser()
    if browser is None:
        raise FileNotFoundError("No Chrome, Edge or Chromium found.")
    path = Path(path).resolve()
    source = path.read_text(encoding="utf-8")
    errors, problems, views = [], [], []
    with tempfile.TemporaryDirectory() as tmp:
        probe_page = Path(tmp) / "probe.html"
        probe_page.write_text(source.replace("<head>", "<head>" + PROBE, 1), encoding="utf-8")
        for width in WIDTHS:
            result = _run(browser, probe_page, width)
            errors += [e for e in result["errors"] if e not in errors]
            for view in result["views"]:
                name = view["tab"]
                if width == WIDTHS[0]:
                    views.append({"tab": name, "charts": len(view["charts"]), "text": view["text"]})
                    if not view["charts"]:
                        problems.append(f"'{name}' shows no charts")
                    for chart in view["charts"]:
                        if chart["points"] == 0:
                            problems.append(f"'{name}' has a chart with no data")
                        if not chart["drawn"]:
                            problems.append(f"'{name}' has a chart that didn't draw (missing or hidden canvas)")
                if view["overflow"]:
                    problems.append(f"'{name}' scrolls sideways at {width}px wide")
            if width == WIDTHS[0]:
                # Clicking a tab must change something: its text or its chart data.
                seen = {}
                for view in result["views"]:
                    print_ = view["text"] + "".join(c["data"] for c in view["charts"])
                    if print_ in seen:
                        problems.append(f"tabs '{seen[print_]}' and '{view['tab']}' show the same content (dead tab?)")
                    seen.setdefault(print_, view["tab"])
    return {"ok": not errors and not problems, "errors": errors, "problems": problems, "views": views}


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print(__doc__)
        return 1
    if find_browser() is None:
        print("No Chrome, Edge or Chromium found, so the page can't be checked automatically. "
              "Ask the analyst to open dashboard.html in a browser and click every tab.")
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    report = check_dashboard(Path(args[0]))
    for view in report["views"]:
        print(f"\n=== {view['tab']}: {view['charts']} chart(s). Text on the page (check numbers against context.md):")
        print(view["text"])
    print()
    for line in report["errors"]:
        print(f"SCRIPT ERROR: {line}")
    for line in report["problems"]:
        print(f"PROBLEM: {line}")
    print("OK: works offline, every tab renders." if report["ok"] else "Fix the problems above, rebuild, and check again.")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
