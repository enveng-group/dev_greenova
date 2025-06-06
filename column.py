import sqlite3

def add_column():
    """Add recurring_forecasted_date column to obligations_obligation table."""
    conn = sqlite3.connect("greenova/db.sqlite3")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "ALTER TABLE obligations_obligation "
            "ADD COLUMN recurring_forecasted_date DATE"
        )
        print("Column added successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    add_column()
