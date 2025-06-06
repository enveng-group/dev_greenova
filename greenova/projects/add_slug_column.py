import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../db.sqlite3')

ALTER_SQL = "ALTER TABLE projects_project ADD COLUMN slug varchar(255);"

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if not column_exists(cur, 'projects_project', 'slug'):
        print("Adding 'slug' column to projects_project table...")
        cur.execute(ALTER_SQL)
        conn.commit()
        print("Column added.")
    else:
        print("'slug' column already exists.")
    conn.close()

if __name__ == "__main__":
    main()
