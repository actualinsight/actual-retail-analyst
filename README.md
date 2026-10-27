# Actual Retail Analyst

An AI analytics system that turns executive questions into finished analysis. It runs on a demo restaurant chain, **Actual Burger Co.**, with 48 restaurants across the US, Canada and Mexico and two years of orders.

It's a free system from [Actual Insight](https://www.actualinsight.com/systems/retail-analyst). Take it apart, run it, and rebuild it on your own data (see [Using your own data](data/context.md#using-your-own-data-instead)).

## How it's built

| Part | Where | What it does |
|---|---|---|
| **Context** | [`context/`](context/context.md) | The business, the data dictionary, the metric definitions. The AI never has to guess. |
| **Process** | [`.claude/skills/`](.claude/skills/) | Three skills that follow the same method every time: [`ad-hoc-analysis`](.claude/skills/ad-hoc-analysis/SKILL.md), [`query-builder`](.claude/skills/query-builder/SKILL.md), [`dashboard-builder`](.claude/skills/dashboard-builder/SKILL.md). Plus [`project-setup`](.claude/skills/project-setup/SKILL.md), which installs everything on first run. |
| **Tools** | [`data/`](data/context.md) + `query-builder` | A local DuckDB database, and the query tool that lives in the `query-builder` skill |
| **Structure** | [`workbench/`](workbench/context.md) | Every output lands here, in a structure the analyst designs, so nothing gets lost: each analysis gets a folder with its record, queries, data and dashboard |

Agent instructions live in [AGENTS.md](AGENTS.md). [CLAUDE.md](CLAUDE.md) points Claude Code to the same file. The brand for dashboards lives in [.claude/skills/dashboard-builder/brand/](.claude/skills/dashboard-builder/brand/README.md).

## Setup

You need [Python](https://www.python.org/downloads/) 3.9 or newer and [Claude Code](https://claude.com/claude-code).

1. Clone this repo (or download it as a zip) and open the folder in Claude Code.
2. Ask a question (see below).

The first time, the agent offers to set things up: it creates the Python environment, installs two packages, and downloads the demo database (about 90 MB). It asks before each step.

### Setting up by hand

If you'd rather do it yourself, or you use a tool that won't run commands:

**Mac / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
curl -fL -o data/actual_burger.zip "https://github.com/actualinsight/actual-retail-analyst/releases/download/data-v1/actual_burger.zip"
python -m zipfile -e data/actual_burger.zip data && rm data/actual_burger.zip
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1         # if blocked: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
pip install -r requirements.txt
curl.exe -fL -o data\actual_burger.zip "https://github.com/actualinsight/actual-retail-analyst/releases/download/data-v1/actual_burger.zip"
if ($LASTEXITCODE -eq 0) { python -m zipfile -e data\actual_burger.zip data; if ($?) { Remove-Item data\actual_burger.zip } }
```

In Command Prompt, activate with `.venv\Scripts\activate.bat` instead.

## Try it

Open the folder in [Claude Code](https://claude.com/claude-code) and ask a question the way an executive would:

> How are same-store sales by market?

The agent will:
1. ask you to confirm the timeframe and markets;
2. create a folder in [`workbench/ad-hoc-analysis/`](workbench/ad-hoc-analysis/) and fill it as it works: the analysis record, SQL and CSV files;
3. walk you through what it found;
4. once you're happy, build the dashboard.

You can also type `/ad-hoc-analysis` directly, or ask for "just the SQL" (`query-builder`).

**See a finished example first:** [workbench/ad-hoc-analysis/20261026_same_store_sales_by_market/](workbench/ad-hoc-analysis/20261026_same_store_sales_by_market/). Open its `dashboard.html` in your browser, and read its `context.md` to see every decision.

## The demo data

It's fictional, and comes pre-built: the agent downloads it on first run. What's in it:

- **US:** same-store sales up ~7%, drive-thru heavy, seven new restaurants
- **Canada:** total sales flat; older restaurants are losing traffic and new ones are doing well
- **Mexico:** the smallest market and the fastest growing (~10%), delivery heavy
- **Everywhere:** the mobile app is gaining share, and delivery has the biggest check
- **Two real-world data problems:** Mexico can't separate delivery tips and fees from sales, and its item lines have no prices. Each is documented in the context with a tag, a rule for querying around it, and what to tell the executive, so the agent works around them honestly.

## Using Codex, Gemini or another tool

This repo is set up for Claude Code. The instructions in `AGENTS.md` work in most agentic coding tools; only the skills folder needs to move.

- **Codex (OpenAI):** Codex reads `AGENTS.md` and finds skills in `.agents/skills/`. Copy the skills there:
  - Mac/Linux: `mkdir -p .agents && rm -rf .agents/skills && cp -R .claude/skills .agents/skills`
  - Windows (PowerShell): `New-Item -ItemType Directory -Force .agents | Out-Null; Remove-Item -Recurse -Force .agents\skills -ErrorAction SilentlyContinue; Copy-Item -Recurse .claude\skills .agents\skills`

  Run the same command again after you edit a skill; it replaces the old copy. ([Codex skills docs](https://developers.openai.com/codex/skills))
- **Gemini CLI:** Gemini finds skills in `.gemini/skills/` or `.agents/skills/`, so the same copy works. To make it read `AGENTS.md`, create `.gemini/settings.json` with:

  ```json
  { "context": { "fileName": ["AGENTS.md", "GEMINI.md"] } }
  ```

  ([skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md), [context files](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md))
- **Any other tool:** point its instruction file at `AGENTS.md`, and tell it the skills are the `SKILL.md` files in `.claude/skills/`.
