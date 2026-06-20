import pandas as pd
import sqlite3
import os
import time

def csv_to_sqlite():
    csv_file = 'student_performance.csv'
    db_file = 'student.db'
    table_name = 'students'

    if not os.path.exists(csv_file):
        print(f"Error: Could not find '{csv_file}' in the current directory.")
        return

    print(f"Connecting to database '{db_file}'...")
    conn = sqlite3.connect(db_file)

    try:
        print(f"Reading '{csv_file}' and inserting into table '{table_name}'...")
        start_time = time.time()
        
        # Using an iterator to read the large CSV in chunks to prevent memory overload
        chunksize = 100000
        total_rows = 0
        
        for chunk in pd.read_csv(csv_file, chunksize=chunksize):
            # 'if_exists' logic: 'replace' for the first chunk to create the table, 'append' for the rest
            action = 'replace' if total_rows == 0 else 'append'
            
            chunk.to_sql(table_name, conn, if_exists=action, index=False)
            total_rows += len(chunk)
            print(f"Inserted {total_rows:,} records so far...")
            
        end_time = time.time()
        
        # Create an index on student_id to ensure fast queries later
        print("Creating index on 'student_id' for performance optimization...")
        cursor = conn.cursor()
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_student_id ON {table_name}(student_id);")
        conn.commit()

        print(f"Successfully inserted a total of {total_rows:,} records into '{db_file}' in {end_time - start_time:.2f} seconds.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    csv_to_sqlite()
