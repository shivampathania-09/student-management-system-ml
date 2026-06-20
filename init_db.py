import sqlite3
import pandas as pd
import os

db_path = os.path.join(os.path.dirname(__file__), 'students.db')
csv_path = os.path.join(os.path.dirname(__file__), 'student_performance.csv')

def init_db():
    conn = sqlite3.connect(db_path)
    
    chunksize = 100000
    for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunksize)):
        chunk.to_sql('students', conn, if_exists='replace' if i == 0 else 'append', index=False)
        print(f"Inserted chunk {i+1}")

    conn.execute('CREATE INDEX IF NOT EXISTS idx_student_id ON students(student_id)')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
