# Data

Where the database lives.

| File | What it is |
|---|---|
| `actual_burger.duckdb` | The Actual Burger Co. database: a single DuckDB file. **Not stored in git**: the [`project-setup`](../.claude/skills/project-setup/SKILL.md) skill downloads it from this project's GitHub releases on first run. The tables are described in [context/data-model/](../context/data-model/context.md). |

**How it's queried:** with the [`query-builder`](../.claude/skills/query-builder/SKILL.md) skill's tool; the skill has the commands.

The data is fictional: orders for a made-up restaurant chain.

## Using your own data instead

This folder is the "Tools" part of the system: it's how the agent reaches the data. Here that's a local DuckDB file, but the data can live anywhere the agent can query, such as a warehouse like BigQuery or Snowflake.

To switch, change three things:
- **The connection:** how the `query-builder` skill runs a query, whether that's a database driver or a connector.
- **This file:** where your data lives and how to get access.
- **`context/data-model/`:** your tables, rules and metric definitions, with the SQL in your database's dialect.
