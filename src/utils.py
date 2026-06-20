# Helper functions
def validate_student_data(attendance, participation, score):
    """Basic validation for student inputs."""
    if not (0 <= attendance <= 100):
        return False, "Attendance must be between 0 and 100."
    if not (0 <= participation <= 100):
        return False, "Participation must be between 0 and 100."
    if not (0 <= score <= 100):
        return False, "Score must be between 0 and 100."
    return True, "Valid"
