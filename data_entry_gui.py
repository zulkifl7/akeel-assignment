"""
Student Marks Management System - Data Entry GUI
Program 1: Data Entry Window

This program allows users to:
- Enter number of subjects and dynamically generate subject name fields
- Enter number of students and dynamically generate student name + marks entry fields
- Save data to student_data.txt in aligned columns
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os


class DataEntryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Marks Management - Data Entry")
        self.root.geometry("600x500")
        
        # Variables to store data
        self.subjects = []
        self.students = []
        self.subject_entries = []
        self.student_entries = []
        self.marks_entries = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Student Marks Data Entry", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Subject section
        ttk.Label(main_frame, text="Number of Subjects:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.subjects_count_var = tk.StringVar()
        subjects_entry = ttk.Entry(main_frame, textvariable=self.subjects_count_var, width=10)
        subjects_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(main_frame, text="Generate Subject Fields", 
                  command=self.generate_subject_fields).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Subject names frame
        self.subjects_frame = ttk.LabelFrame(main_frame, text="Subject Names", padding="5")
        self.subjects_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.subjects_frame.columnconfigure(1, weight=1)
        
        # Student section
        ttk.Label(main_frame, text="Number of Students:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.students_count_var = tk.StringVar()
        students_entry = ttk.Entry(main_frame, textvariable=self.students_count_var, width=10)
        students_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(main_frame, text="Generate Student Fields", 
                  command=self.generate_student_fields).grid(row=5, column=0, columnspan=2, pady=5)
        
        # Students frame with scrollbar
        self.students_canvas_frame = ttk.Frame(main_frame)
        self.students_canvas_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.students_canvas_frame.columnconfigure(0, weight=1)
        self.students_canvas_frame.rowconfigure(0, weight=1)
        
        # Canvas and scrollbar for students
        self.canvas = tk.Canvas(self.students_canvas_frame, height=200)
        scrollbar = ttk.Scrollbar(self.students_canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Save button
        ttk.Button(main_frame, text="Save Data", command=self.save_data, 
                  style="Accent.TButton").grid(row=7, column=0, columnspan=2, pady=20)
        
        # Configure main frame grid weights
        main_frame.rowconfigure(6, weight=1)
    
    def generate_subject_fields(self):
        """Generate input fields for subject names"""
        try:
            num_subjects = int(self.subjects_count_var.get())
            if num_subjects <= 0:
                raise ValueError("Number must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for subjects")
            return
        
        # Clear existing subject entries
        for widget in self.subjects_frame.winfo_children():
            widget.destroy()
        self.subject_entries.clear()
        
        # Create new subject entry fields
        for i in range(num_subjects):
            ttk.Label(self.subjects_frame, text=f"Subject {i+1}:").grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(self.subjects_frame, width=20)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
            self.subject_entries.append(entry)
    
    def generate_student_fields(self):
        """Generate input fields for student names and marks"""
        if not self.subject_entries:
            messagebox.showerror("Error", "Please generate subject fields first")
            return
        
        try:
            num_students = int(self.students_count_var.get())
            if num_students <= 0:
                raise ValueError("Number must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for students")
            return
        
        # Clear existing student entries
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.student_entries.clear()
        self.marks_entries.clear()
        
        # Create header
        ttk.Label(self.scrollable_frame, text="Student Name", font=("Arial", 10, "bold")).grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        for i, entry in enumerate(self.subject_entries):
            subject_name = entry.get().strip()
            if not subject_name:
                subject_name = f"Subject {i+1}"
            ttk.Label(self.scrollable_frame, text=subject_name, font=("Arial", 10, "bold")).grid(
                row=0, column=i+1, padx=5, pady=5)
        
        # Create student entry fields
        for i in range(num_students):
            # Student name entry
            name_entry = ttk.Entry(self.scrollable_frame, width=15)
            name_entry.grid(row=i+1, column=0, padx=5, pady=2)
            self.student_entries.append(name_entry)
            
            # Marks entries for each subject
            student_marks = []
            for j in range(len(self.subject_entries)):
                marks_entry = ttk.Entry(self.scrollable_frame, width=10)
                marks_entry.grid(row=i+1, column=j+1, padx=5, pady=2)
                student_marks.append(marks_entry)
            self.marks_entries.append(student_marks)
    
    def save_data(self):
        """Save the entered data to student_data.txt"""
        if not self.subject_entries or not self.student_entries:
            messagebox.showerror("Error", "Please generate and fill all fields before saving")
            return
        
        try:
            # Collect subject names
            subjects = []
            for entry in self.subject_entries:
                subject = entry.get().strip()
                if not subject:
                    messagebox.showerror("Error", "All subject names must be filled")
                    return
                subjects.append(subject)
            
            # Collect student data
            students_data = []
            for i, name_entry in enumerate(self.student_entries):
                name = name_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", f"Student {i+1} name cannot be empty")
                    return
                
                marks = []
                for j, marks_entry in enumerate(self.marks_entries[i]):
                    try:
                        mark = int(marks_entry.get().strip())
                        if mark < 0:
                            raise ValueError("Negative marks not allowed")
                        marks.append(mark)
                    except ValueError:
                        messagebox.showerror("Error", 
                                           f"Invalid mark for {name} in {subjects[j]}. Please enter a valid non-negative integer.")
                        return
                
                students_data.append((name, marks))
            
            # Write to file with proper alignment
            self.write_to_file(subjects, students_data)
            messagebox.showinfo("Success", "Data saved successfully to student_data.txt")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")
    
    def write_to_file(self, subjects, students_data):
        """Write data to student_data.txt with proper column alignment"""
        # Calculate column widths for alignment
        name_width = max(len("Name"), max(len(student[0]) for student in students_data))
        subject_widths = []
        
        for i, subject in enumerate(subjects):
            max_width = len(subject)
            for student_name, marks in students_data:
                max_width = max(max_width, len(str(marks[i])))
            subject_widths.append(max_width)
        
        # Write to file
        with open("student_data.txt", "w") as file:
            # Write header
            header = f"{'Name':<{name_width}}"
            for i, subject in enumerate(subjects):
                header += f"  {subject:<{subject_widths[i]}}"
            file.write(header + "\n")
            
            # Write student data
            for student_name, marks in students_data:
                line = f"{student_name:<{name_width}}"
                for i, mark in enumerate(marks):
                    line += f"  {mark:<{subject_widths[i]}}"
                file.write(line + "\n")


def main():
    """Main function to run the Data Entry GUI"""
    root = tk.Tk()
    app = DataEntryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()