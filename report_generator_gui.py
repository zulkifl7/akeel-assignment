"""
Student Marks Management System - Report Generator GUI
Program 3: Report Generator Window

This program allows users to:
- Read student_data.txt
- Calculate and display comprehensive reports including:
  * Total & average marks per student
  * Ranking (place) based on total marks
  * Maximum marks per subject
  * Average marks per subject
  * Best performer in each subject
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os


class ReportGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Marks Management - Report Generator")
        self.root.geometry("900x600")
        
        # Data storage
        self.subjects = []
        self.students_data = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Student Marks Report Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Generate report button
        generate_button = ttk.Button(main_frame, text="Generate Report", 
                                   command=self.generate_report,
                                   style="Accent.TButton")
        generate_button.grid(row=1, column=0, pady=(0, 10))
        
        # Report display frame
        display_frame = ttk.LabelFrame(main_frame, text="Generated Report", padding="5")
        display_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbars for displaying report
        self.report_display = scrolledtext.ScrolledText(
            display_frame, 
            wrap=tk.NONE,  # No text wrapping to preserve alignment
            font=("Courier New", 10),  # Monospace font for proper alignment
            state=tk.DISABLED,  # Read-only initially
            width=80,
            height=25
        )
        self.report_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to generate report", 
                                     foreground="blue")
        self.status_label.grid(row=3, column=0, pady=(10, 0))
    
    def load_data(self):
        """Load data from student_data.txt"""
        try:
            # Check if file exists
            if not os.path.exists("student_data.txt"):
                raise FileNotFoundError("student_data.txt not found")
            
            # Read and parse the file
            with open("student_data.txt", "r") as file:
                lines = file.readlines()
            
            if not lines:
                raise ValueError("File is empty")
            
            # Parse header (subjects)
            header = lines[0].strip().split()
            self.subjects = header[1:]  # Skip "Name" column
            
            # Parse student data
            self.students_data = []
            for line in lines[1:]:
                if line.strip():  # Skip empty lines
                    parts = line.strip().split()
                    if len(parts) >= len(self.subjects) + 1:
                        name = parts[0]
                        marks = [int(mark) for mark in parts[1:len(self.subjects)+1]]
                        self.students_data.append((name, marks))
            
            if not self.students_data:
                raise ValueError("No student data found")
            
            return True
            
        except FileNotFoundError:
            messagebox.showerror("Error", 
                               "student_data.txt not found!\n\n"
                               "Please run the Data Entry program first to create the file.")
            return False
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid data format: {str(e)}")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
            return False
    
    def calculate_student_stats(self):
        """Calculate total, average, and ranking for each student"""
        student_stats = []
        
        for name, marks in self.students_data:
            total = sum(marks)
            average = total / len(marks) if marks else 0
            student_stats.append((name, marks, total, average))
        
        # Sort by total marks (descending) for ranking
        student_stats.sort(key=lambda x: x[2], reverse=True)
        
        # Add ranking
        ranked_students = []
        for i, (name, marks, total, average) in enumerate(student_stats):
            place = i + 1
            ranked_students.append((name, marks, total, average, place))
        
        return ranked_students
    
    def calculate_subject_stats(self):
        """Calculate maximum, average, and best performer for each subject"""
        subject_stats = []
        
        for i, subject in enumerate(self.subjects):
            marks_in_subject = [marks[i] for _, marks in self.students_data]
            max_mark = max(marks_in_subject)
            avg_mark = sum(marks_in_subject) / len(marks_in_subject)
            
            # Find best performer(s)
            best_performers = [name for name, marks in self.students_data if marks[i] == max_mark]
            best_performer = best_performers[0]  # Take first if multiple
            
            subject_stats.append((subject, max_mark, avg_mark, best_performer))
        
        return subject_stats
    
    def generate_report(self):
        """Generate and display the comprehensive report"""
        try:
            # Load data
            if not self.load_data():
                self.status_label.config(text="Failed to load data", foreground="red")
                return
            
            # Calculate statistics
            student_stats = self.calculate_student_stats()
            subject_stats = self.calculate_subject_stats()
            
            # Generate report text
            report = self.format_report(student_stats, subject_stats)
            
            # Display report
            self.display_report(report)
            self.status_label.config(text="Report generated successfully", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
            self.status_label.config(text="Error generating report", foreground="red")
    
    def format_report(self, student_stats, subject_stats):
        """Format the report as specified in requirements"""
        report_lines = []
        
        # Header separator
        report_lines.append("-" * 80)
        
        # Table header
        header = f"{'Name':<15}"
        for subject in self.subjects:
            header += f"{subject:<12}"
        header += f"{'Total':<8}{'Avg':<8}{'Place':<6}"
        report_lines.append(header)
        
        # Student data
        for name, marks, total, average, place in student_stats:
            line = f"{name:<15}"
            for mark in marks:
                line += f"{mark:<12}"
            line += f"{total:<8}{average:<8.1f}{place:<6}"
            report_lines.append(line)
        
        # Empty line
        report_lines.append("")
        
        # Subject statistics
        # Maximum marks per subject
        max_line = f"{'Subject Max':<15}"
        for _, max_mark, _, _ in subject_stats:
            max_line += f"{max_mark:<12}"
        report_lines.append(max_line)
        
        # Average marks per subject
        avg_line = f"{'Subject Avg':<15}"
        for _, _, avg_mark, _ in subject_stats:
            avg_line += f"{avg_mark:<12.1f}"
        report_lines.append(avg_line)
        
        # Best performer per subject
        best_line = f"{'Best Person':<15}"
        for _, _, _, best_performer in subject_stats:
            best_line += f"{best_performer:<12}"
        report_lines.append(best_line)
        
        # Footer separator
        report_lines.append("-" * 80)
        
        return "\n".join(report_lines)
    
    def display_report(self, report):
        """Display the report in the text widget"""
        # Enable text widget for editing
        self.report_display.config(state=tk.NORMAL)
        
        # Clear existing content
        self.report_display.delete(1.0, tk.END)
        
        # Insert the report
        self.report_display.insert(1.0, report)
        
        # Disable text widget to make it read-only
        self.report_display.config(state=tk.DISABLED)
        
        # Move cursor to the beginning
        self.report_display.see(1.0)
    
    def save_report(self):
        """Save the current report to a file"""
        try:
            report_content = self.report_display.get(1.0, tk.END)
            if not report_content.strip():
                messagebox.showwarning("Warning", "No report to save. Generate a report first.")
                return
            
            with open("student_report.txt", "w") as file:
                file.write(report_content)
            
            messagebox.showinfo("Success", "Report saved to student_report.txt")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving report: {str(e)}")


def main():
    """Main function to run the Report Generator GUI"""
    root = tk.Tk()
    app = ReportGeneratorGUI(root)
    
    # Add menu bar for additional functionality
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Generate Report", command=app.generate_report)
    file_menu.add_command(label="Save Report", command=app.save_report)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    root.mainloop()


if __name__ == "__main__":
    main()