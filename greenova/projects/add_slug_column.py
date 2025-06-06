import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "../db.sqlite3")

ALTER_SQL = "ALTER TABLE projects_project ADD COLUMN slug varchar(255);"


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if not column_exists(cur, "projects_project", "slug"):
        cur.execute(ALTER_SQL)
        conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
