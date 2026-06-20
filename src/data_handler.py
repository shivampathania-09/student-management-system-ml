import sqlite3
import pandas as pd
import os

class StudentManager:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = os.path.join(os.path.dirname(__file__), '..', 'students.db')
        else:
            self.db_path = db_path
            
        self.columns = ['student_id', 'weekly_self_study_hours', 'attendance_percentage', 'class_participation', 'total_score', 'grade']
        self._initialize_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        conn = self._get_connection()
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                weekly_self_study_hours REAL,
                attendance_percentage REAL,
                class_participation REAL,
                total_score REAL,
                grade TEXT
            )
        ''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_student_id ON students(student_id)')
        conn.commit()
        conn.close()

    def add_student(self, student_id, attendance, participation, total_score, grade, weekly_study_hours=0.0):
        conn = self._get_connection()
        c = conn.cursor()
        
        c.execute("SELECT student_id FROM students WHERE student_id = ?", (str(student_id),))
        if c.fetchone():
            conn.close()
            raise ValueError(f"Student ID '{student_id}' already exists.")
            
        try:
            c.execute("""
                INSERT INTO students (student_id, weekly_self_study_hours, attendance_percentage, class_participation, total_score, grade)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (str(student_id), float(weekly_study_hours), float(attendance), float(participation), float(total_score), str(grade).upper()))
            conn.commit()
        except ValueError as e:
            conn.close()
            raise ValueError(f"Invalid input data type: {e}")
        conn.close()
        return True

    def view_students(self):
        """Returns all student records."""
        conn = self._get_connection()
        df = pd.read_sql_query("SELECT * FROM students LIMIT 1000", conn)
        conn.close()
        return df

    def get_students_paginated(self, limit=50, offset=0, search_query=None):
        """Returns a paginated list of students, optionally filtered by ID."""
        conn = self._get_connection()
        
        query = "SELECT * FROM students"
        params = []
        
        if search_query:
            query += " WHERE student_id LIKE ?"
            params.append(f"%{search_query}%")
            
        c = conn.cursor()
        count_query = f"SELECT COUNT(*) FROM ({query})"
        c.execute(count_query, params)
        total_count = c.fetchone()[0]
        
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df, total_count

    def search_student(self, student_id):
        """Searches for a student by ID."""
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id = ?", (str(student_id),))
        row = c.fetchone()
        
        if not row:
            conn.close()
            return None
            
        # Get column names
        cols = [description[0] for description in c.description]
        result = dict(zip(cols, row))
        conn.close()
        return result

    def update_student(self, student_id, **kwargs):
        """Updates an existing student's record."""
        conn = self._get_connection()
        c = conn.cursor()
        
        c.execute("SELECT student_id FROM students WHERE student_id = ?", (str(student_id),))
        if not c.fetchone():
            conn.close()
            raise KeyError(f"Student ID '{student_id}' not found.")
            
        set_clauses = []
        params = []
        for key, value in kwargs.items():
            if key in self.columns and key != 'student_id':
                try:
                    if key in ['attendance_percentage', 'class_participation', 'total_score', 'weekly_self_study_hours']:
                        val = float(value)
                    else:
                        val = str(value).upper()
                    set_clauses.append(f"{key} = ?")
                    params.append(val)
                except ValueError:
                    conn.close()
                    raise ValueError(f"Invalid value provided for {key}: {value}")
                    
        if set_clauses:
            params.append(str(student_id))
            query = f"UPDATE students SET {', '.join(set_clauses)} WHERE student_id = ?"
            c.execute(query, params)
            conn.commit()
            
        conn.close()
        return True

    def delete_student(self, student_id):
        """Deletes a student record by ID."""
        conn = self._get_connection()
        c = conn.cursor()
        
        c.execute("SELECT student_id FROM students WHERE student_id = ?", (str(student_id),))
        if not c.fetchone():
            conn.close()
            raise KeyError(f"Student ID '{student_id}' not found.")
            
        c.execute("DELETE FROM students WHERE student_id = ?", (str(student_id),))
        conn.commit()
        conn.close()
        return True
