import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from src.data_handler import StudentManager
from src.model_pipeline import predict_grade

console = Console()
manager = StudentManager()

def display_menu():
    console.print("\n[bold cyan]=== Student Management System ===[/bold cyan]")
    console.print("[1] Add Student")
    console.print("[2] View Students")
    console.print("[3] Search Student")
    console.print("[4] Update Student")
    console.print("[5] Delete Student")
    console.print("[6] Predict Grade")
    console.print("[7] Exit")
    console.print("[bold cyan]=================================[/bold cyan]")

def add_student():
    console.print("\n[bold yellow]--- Add New Student ---[/bold yellow]")
    try:
        student_id = input("Enter Student ID: ").strip()
        attendance = float(input("Enter Weekly Attendance (%): "))
        participation = float(input("Enter Class Participation (0-10): "))
        total_score = float(input("Enter Total Score: "))
        grade = input("Enter Current Grade (Optional, press Enter to skip): ").strip()
        
        manager.add_student(student_id, attendance, participation, total_score, grade)
        console.print("[bold green]Student added successfully![/bold green]")
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

def view_students():
    console.print("\n[bold yellow]--- All Students ---[/bold yellow]")
    df = manager.view_students()
    
    if df.empty:
        console.print("[italic]No students found.[/italic]")
        return
        
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Student ID")
    table.add_column("Attendance (%)")
    table.add_column("Participation")
    table.add_column("Total Score")
    table.add_column("Grade")
    
    for _, row in df.iterrows():
        table.add_row(
            str(row['student_id']),
            f"{row['attendance_percentage']:.2f}",
            f"{row['class_participation']:.2f}",
            f"{row['total_score']:.2f}",
            str(row['grade'])
        )
    console.print(table)

def search_student():
    console.print("\n[bold yellow]--- Search Student ---[/bold yellow]")
    student_id = input("Enter Student ID to search: ").strip()
    student = manager.search_student(student_id)
    
    if student:
        console.print(Panel.fit(
            f"[bold]ID:[/bold] {student['student_id']}\n"
            f"[bold]Attendance:[/bold] {student['attendance_percentage']}%\n"
            f"[bold]Participation:[/bold] {student['class_participation']}/10\n"
            f"[bold]Total Score:[/bold] {student['total_score']}\n"
            f"[bold]Grade:[/bold] {student['grade']}",
            title="[bold green]Student Found[/bold green]"
        ))
    else:
        console.print(f"[bold red]Student ID '{student_id}' not found.[/bold red]")

def update_student():
    console.print("\n[bold yellow]--- Update Student ---[/bold yellow]")
    student_id = input("Enter Student ID to update: ").strip()
    
    if not manager.search_student(student_id):
        console.print(f"[bold red]Student ID '{student_id}' not found.[/bold red]")
        return
        
    console.print("[italic]Leave blank to keep current value.[/italic]")
    updates = {}
    
    attendance = input("New Attendance (%): ").strip()
    if attendance: updates['attendance_percentage'] = attendance
        
    participation = input("New Participation (0-10): ").strip()
    if participation: updates['class_participation'] = participation
        
    total_score = input("New Total Score: ").strip()
    if total_score: updates['total_score'] = total_score
        
    grade = input("New Grade: ").strip()
    if grade: updates['grade'] = grade
        
    if not updates:
        console.print("[yellow]No updates provided.[/yellow]")
        return
        
    try:
        manager.update_student(student_id, **updates)
        console.print("[bold green]Student updated successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error updating student:[/bold red] {e}")

def delete_student():
    console.print("\n[bold yellow]--- Delete Student ---[/bold yellow]")
    student_id = input("Enter Student ID to delete: ").strip()
    
    try:
        manager.delete_student(student_id)
        console.print(f"[bold green]Student '{student_id}' deleted successfully![/bold green]")
    except KeyError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

def predict_student_grade():
    console.print("\n[bold yellow]--- Predict Grade ---[/bold yellow]")
    student_id = input("Enter Student ID (or press Enter to input manually): ").strip()
    
    attendance, participation, score = None, None, None
    
    if student_id:
        student = manager.search_student(student_id)
        if student:
            attendance = student['attendance_percentage']
            participation = student['class_participation']
            score = student['total_score']
            console.print(f"Loaded data for ID {student_id}")
        else:
            console.print(f"[bold red]Student ID '{student_id}' not found.[/bold red]")
            return
    else:
        try:
            attendance = float(input("Enter Weekly Attendance (%): "))
            participation = float(input("Enter Class Participation (0-10): "))
            score = float(input("Enter Total Score: "))
        except ValueError:
            console.print("[bold red]Invalid input! Must be numbers.[/bold red]")
            return
            
    result = predict_grade(attendance, participation, score)
    
    if result and result[0] is not None:
        grade, confidence = result
        msg = f"[bold green]Predicted Grade:[/bold green] {grade}"
        if confidence:
            msg += f" (Confidence: {confidence}%)"
        console.print(Panel.fit(msg))
        
        # Optional: Ask to save the predicted grade if ID was provided
        if student_id and input("Save this predicted grade? (y/n): ").strip().lower() == 'y':
            manager.update_student(student_id, grade=grade)
            console.print("[green]Grade saved successfully![/green]")
            
    else:
        # Error handling from pipeline
        console.print(f"[bold red]{result[1]}[/bold red]")

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-7): ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            predict_student_grade()
        elif choice == '7':
            console.print("[bold green]Exiting Student Management System. Goodbye![/bold green]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid choice. Please select 1-7.[/bold red]")

if __name__ == "__main__":
    main()
