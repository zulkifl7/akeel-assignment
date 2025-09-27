"""
Student Marks Management System - File Reader GUI
Program 2: File Reader Window

This program allows users to:
- Load data from student_data.txt
- Display the contents in a Tkinter Text widget with preserved alignment
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os


class FileReaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Marks Management - File Reader")
        self.root.geometry("700x500")
        
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
        title_label = ttk.Label(main_frame, text="Student Marks File Reader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Load button
        load_button = ttk.Button(main_frame, text="Load Data", command=self.load_data,
                                style="Accent.TButton")
        load_button.grid(row=1, column=0, pady=(0, 10))
        
        # Data display frame
        display_frame = ttk.LabelFrame(main_frame, text="Student Data", padding="5")
        display_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbars for displaying data
        self.text_display = scrolledtext.ScrolledText(
            display_frame, 
            wrap=tk.NONE,  # No text wrapping to preserve alignment
            font=("Courier New", 10),  # Monospace font for proper alignment
            state=tk.DISABLED,  # Read-only initially
            width=70,
            height=20
        )
        self.text_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to load data", 
                                     foreground="blue")
        self.status_label.grid(row=3, column=0, pady=(10, 0))
    
    def load_data(self):
        """Load and display data from student_data.txt"""
        try:
            # Check if file exists
            if not os.path.exists("student_data.txt"):
                messagebox.showerror("Error", 
                                   "student_data.txt not found!\n\n"
                                   "Please run the Data Entry program first to create the file.")
                self.status_label.config(text="File not found", foreground="red")
                return
            
            # Read the file
            with open("student_data.txt", "r") as file:
                content = file.read()
            
            # Check if file is empty
            if not content.strip():
                messagebox.showwarning("Warning", "The student_data.txt file is empty.")
                self.status_label.config(text="File is empty", foreground="orange")
                return
            
            # Display the content
            self.display_content(content)
            self.status_label.config(text="Data loaded successfully", foreground="green")
            
        except PermissionError:
            messagebox.showerror("Error", "Permission denied. Cannot read student_data.txt")
            self.status_label.config(text="Permission denied", foreground="red")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the file:\n{str(e)}")
            self.status_label.config(text="Error loading file", foreground="red")
    
    def display_content(self, content):
        """Display the file content in the text widget with preserved formatting"""
        # Enable text widget for editing
        self.text_display.config(state=tk.NORMAL)
        
        # Clear existing content
        self.text_display.delete(1.0, tk.END)
        
        # Insert the file content
        self.text_display.insert(1.0, content)
        
        # Disable text widget to make it read-only
        self.text_display.config(state=tk.DISABLED)
        
        # Move cursor to the beginning
        self.text_display.see(1.0)
    
    def refresh_data(self):
        """Refresh the displayed data by reloading the file"""
        self.load_data()


def main():
    """Main function to run the File Reader GUI"""
    root = tk.Tk()
    app = FileReaderGUI(root)
    
    # Add menu bar for additional functionality
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Load Data", command=app.load_data)
    file_menu.add_command(label="Refresh", command=app.refresh_data)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    root.mainloop()


if __name__ == "__main__":
    main()