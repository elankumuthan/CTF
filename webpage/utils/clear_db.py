import sqlite3

def clear_db():
    try:
        conn = sqlite3.connect('/app/utils/users.db')
        c = conn.cursor()

        # Get all table names in the database
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()

        # For each table, delete all rows
        for table in tables:
            table_name = table[0]
            c.execute(f"DELETE FROM {table_name};")

        conn.commit()
        print("All data cleared successfully.")
    except Exception as e:
        print(f"Error clearing database: {e}")
    finally:
        conn.close()

# Call the function to clear all data
clear_db()
