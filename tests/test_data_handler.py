import pytest
import os
import sqlite3
from src.data_handler import StudentManager

TEST_DB_PATH = "test_students.db"

@pytest.fixture
def manager():
    # Setup test DB
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    mgr = StudentManager(db_path=TEST_DB_PATH)
    yield mgr
    # Teardown test DB
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_add_student(manager):
    result = manager.add_student("S1", 90.0, 8.5, 85.0, "A")
    assert result is True
    
    student = manager.search_student("S1")
    assert student is not None
    assert student["attendance_percentage"] == 90.0
    assert student["class_participation"] == 8.5
    assert student["total_score"] == 85.0
    assert student["grade"] == "A"

def test_add_duplicate_student(manager):
    manager.add_student("S1", 90.0, 8.5, 85.0, "A")
    with pytest.raises(ValueError, match="already exists"):
        manager.add_student("S1", 80.0, 7.0, 75.0, "B")

def test_search_student_not_found(manager):
    student = manager.search_student("S999")
    assert student is None

def test_update_student(manager):
    manager.add_student("S1", 90.0, 8.5, 85.0, "A")
    result = manager.update_student("S1", total_score=95.0, grade="A+")
    assert result is True
    
    student = manager.search_student("S1")
    assert student["total_score"] == 95.0
    assert student["grade"] == "A+"

def test_update_student_not_found(manager):
    with pytest.raises(KeyError, match="not found"):
        manager.update_student("S999", total_score=95.0)

def test_delete_student(manager):
    manager.add_student("S1", 90.0, 8.5, 85.0, "A")
    result = manager.delete_student("S1")
    assert result is True
    
    student = manager.search_student("S1")
    assert student is None

def test_delete_student_not_found(manager):
    with pytest.raises(KeyError, match="not found"):
        manager.delete_student("S999")

def test_get_students_paginated(manager):
    for i in range(5):
        manager.add_student(f"S{i}", 90.0, 8.5, 85.0, "A")
        
    df, total_count = manager.get_students_paginated(limit=3, offset=0)
    assert len(df) == 3
    assert total_count == 5
    
    df, total_count = manager.get_students_paginated(limit=3, offset=3)
    assert len(df) == 2
    assert total_count == 5
