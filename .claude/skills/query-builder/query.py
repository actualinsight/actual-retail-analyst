"""Run a SQL query against the project's database and print the result.

    python .claude/skills/query-builder/query.py "SELECT * FROM store_dim LIMIT 5"
    python .claude/skills/query-builder/query.py --file my_query.sql
    python .claude/skills/query-builder/query.py --csv workbench/<folder>/01_pull.csv "SELECT ..."

The database is the one .duckdb file in the project's data/ folder (pick another with --db).
It's opened read-only, so a query can never change the data. Relative --file and --csv
paths are read from the project folder, wherever you run this from.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    import duckdb
    import pandas as pd
except ImportError:
    print("Missing packages (duckdb, pandas). Use the project-setup skill to install them.")
    sys.exit(1)

# Printing millions of rows helps no one (least of all an AI agent reading them).
MAX_ROWS = 500


class DatabaseUnavailable(Exception):
    """The database file is missing or another program has it locked."""


def find_root(start: Path) -> Path:
    """The project folder: the nearest one above `start` that holds AGENTS.md.

    Walking up (rather than counting folders) keeps this working when the skills
    are copied somewhere else, such as .agents/skills/ for Codex.
    """
    for folder in (start, *start.parents):
        if (folder / "AGENTS.md").is_file():
            return folder
    raise DatabaseUnavailable(f"Can't find the project folder (no AGENTS.md above {start}).")


def find_database(root: Path) -> Path:
    """The single .duckdb file in the project's data/ folder."""
    found = sorted((root / "data").glob("*.duckdb"))
    if not found:
        raise DatabaseUnavailable("No database in data/. Use the project-setup skill to download it.")
    if len(found) > 1:
        names = ", ".join(p.name for p in found)
        raise DatabaseUnavailable(f"More than one database in data/ ({names}). Pick one with --db.")
    return found[0]


def connect_readonly(db_path: Path) -> duckdb.DuckDBPyConnection:
    if not Path(db_path).exists():
        raise DatabaseUnavailable(
            f"Database not found at {db_path}. Use the project-setup skill to download it.")
    try:
        return duckdb.connect(str(db_path), read_only=True)
    except duckdb.IOException as err:
        if "lock" not in str(err).lower():
            raise
        raise DatabaseUnavailable(
            f"The database at {db_path} is in use by another program (maybe it's open in a "
            "DuckDB window, or the database is being rebuilt). Close it and try again.") from None


def run_query(sql: str, db_path: Path) -> pd.DataFrame:
    con = connect_readonly(db_path)
    try:
        return con.execute(sql).df()
    finally:
        con.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run SQL against the project's database.")
    parser.add_argument("sql", nargs="?", help="the SQL to run (or use --file)")
    parser.add_argument("--file", type=Path, help="read the SQL from this file")
    parser.add_argument("--db", type=Path, help="database path (default: the one in data/)")
    parser.add_argument("--csv", type=Path,
                        help="save the full result to this CSV file")
    args = parser.parse_args(argv)

    if not (args.file or args.sql):
        parser.error("give a SQL string or --file")
    try:
        root = find_root(Path(__file__).resolve().parent)
        db_path = args.db or find_database(root)
    except DatabaseUnavailable as err:
        print(err)
        return 1
    sql = args.sql
    if args.file:
        sql_path = args.file if args.file.is_absolute() else root / args.file
        try:
            sql = sql_path.read_text(encoding="utf-8")
        except OSError:
            print(f"Can't read the SQL file {args.file} (looked for {sql_path}).")
            return 1
    csv_path = None
    if args.csv:
        csv_path = (args.csv if args.csv.is_absolute() else root / args.csv).resolve()
        if csv_path.suffix.lower() != ".csv":
            print("The --csv file name must end in .csv")
            return 1
    try:
        con = connect_readonly(db_path)
    except DatabaseUnavailable as err:
        print(err)
        return 1
    try:
        result = con.sql(sql)
        if csv_path and result is not None:
            # The whole result, not just the first rows shown on screen. DuckDB writes
            # the CSV itself so whole numbers stay whole (no "1397779.0").
            # Write to a side file and swap it in, so a query that fails half-way never
            # leaves a partial pull (or wipes out the previous one).
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            partial = csv_path.with_name(csv_path.name + ".partial")
            try:
                result.write_csv(str(partial))
                # fetchall, not fetchone: DuckDB 2 keeps a half-read result open and blocks the next query.
                rows = con.execute("SELECT COUNT(*) FROM read_csv_auto(?)", [str(partial)]).fetchall()[0][0]
                os.replace(partial, csv_path)
            finally:
                if partial.exists():
                    partial.unlink()
            print(f"Saved {rows:,} rows x {len(result.columns)} columns to {args.csv} "
                  f"(showing the first 10)")
            frame = result.limit(10).df()
        else:
            frame = None if result is None else result.limit(MAX_ROWS + 1).df()
    except duckdb.Error as err:
        print(f"Query failed: {err}")
        return 1
    finally:
        con.close()

    if frame is None:
        print("(done)")
    elif frame.empty:
        print(", ".join(frame.columns))
        print("(no rows)")
    else:
        with pd.option_context("display.max_rows", None, "display.max_columns", None, "display.width", 200):
            print(frame.head(MAX_ROWS).to_string(index=False, na_rep="NULL"))
        if len(frame) > MAX_ROWS:
            print(f"... showing the first {MAX_ROWS} rows. Add LIMIT or aggregate to see the rest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
