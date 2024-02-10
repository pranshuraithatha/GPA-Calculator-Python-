import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import json
import os
import webbrowser
import tkinter.filedialog as filedialog

class GPA_Calculator(tk.Tk):
    AUTO_BACKUP_INTERVAL = 1000  # Interval in milliseconds (1 second)
    backup_filename = None
    def __init__(self, course_count):
        super().__init__()
        self.title("GPA Calculator")
        self.configure(background='lightblue')
        messagebox.showerror("Dynamic Backup Feature", "You are going to name the backup file. The program is going to auto backup the file")

        self.course_count = course_count
        self.grades = []
        self.course_types = []
        self.credit_entries = []

        self.auto_backup()

        for i in range(course_count):
            self.create_grade_widgets(i)

        calculate_button_weighted = tk.Button(self, text="Calculate Weighted GPA", command=self.calculate_gpa_weighted)
        calculate_button_weighted.grid(row=16, column=0, padx=10, pady=5)

        calculate_button_unweighted = tk.Button(self, text="Calculate Unweighted GPA", command=self.calculate_gpa_unweighted)
        calculate_button_unweighted.grid(row=16, column=1, padx=10, pady=5)

        reset_button = tk.Button(self, text="Reset", command=self.reset)
        reset_button.grid(row=16, column=2, padx=10, pady=5)

        add_button = tk.Button(self, text="Adjust Number of Courses ", command=self.change_rows)
        add_button.grid(row=17, column=0)

        q_and_a_button = tk.Button(self, text="Q&A", command=self.q_and_a)
        q_and_a_button.grid(row=16, column=3)

        instructions_button = tk.Button(self, text="Instructions", command=self.show_instructions)
        instructions_button.grid(row=18, column=2)

        load_backup_button = tk.Button(self, text="Load Backup", command=self.load_backup)
        load_backup_button.grid(row=17, column=1)

        delete_backup_button = tk.Button(self, text="Delete Backup", command=self.delete_backup)
        delete_backup_button.grid(row=17, column=2)

        exit_button = tk.Button(self, text="Exit", command=self.destroy)
        exit_button.grid(row=17, column=3)

        backup_button = tk.Button(self, text="Backup Data", command=self.backup_data)
        backup_button.grid(row=18, column=1)

        self.gpa_label_weighted = tk.Label(self, text="Weighted GPA: ")
        self.gpa_label_weighted.grid(row=16, column=4, columnspan=6, padx=10, pady=5)

        self.gpa_label_unweighted = tk.Label(self, text="Unweighted GPA: ")
        self.gpa_label_unweighted.grid(row=17, column=4, columnspan=6, padx=10, pady=5)

        report_button = tk.Button(self, text="Generate and Save Report", command=self.generate_and_save_report)
        report_button.grid(row=18, column=0)

        auto_backup_button = tk.Button(self, text="Auto Backup", command=self.backup_data_silently)
        auto_backup_button.grid(row=17, column=1)

        new_calculation_button = tk.Button(self, text="Open New File", command=self.new_calculation)
        new_calculation_button.grid(row=18, column=3)


    def create_grade_widgets(self, i):
        grade_label = tk.Label(self, text="Grade:")
        grade_label.grid(row=i, column=0, padx=10, pady=5)
        grade_var = tk.StringVar()
        grade_dropdown = tk.OptionMenu(self, grade_var, *GRADE_VALUES.keys())
        grade_dropdown.grid(row=i, column=1, padx=10, pady=5)
        self.grades.append(grade_var)

        course_type_label = tk.Label(self, text="Course Type:")
        course_type_label.grid(row=i, column=2, padx=10, pady=5)

        course_type_var = tk.StringVar()
        course_type_dropdown = tk.OptionMenu(self, course_type_var, *COURSE_QUALITY_POINTS_WEIGHTED.keys())
        course_type_dropdown.grid(row=i, column=3, padx=10, pady=5)
        self.course_types.append(course_type_var)

        credit_label = tk.Label(self, text="Credits:")
        credit_label.grid(row=i, column=3, padx=10, pady=5)

        credit_entry = tk.Entry(self)
        credit_entry.grid(row=i, column=4, padx=10, pady=5)
        self.credit_entries.append(credit_entry)

    def schedule_auto_backup(self):
        # Perform auto backup and schedule the next one after 1000 milliseconds (1 second)
        self.backup_data_silently()
        self.after(1000, self.schedule_auto_backup)

    def calculate_gpa_weighted(self):
        gpa = self.calculate_gpa(COURSE_QUALITY_POINTS_WEIGHTED)
        self.gpa_label_weighted.config(text="Weighted GPA: {:.2f}".format(gpa))

    def calculate_gpa_unweighted(self):
        gpa = self.calculate_gpa(COURSE_QUALITY_POINTS_UNWEIGHTED)
        self.gpa_label_unweighted.config(text="Unweighted GPA: {:.2f}".format(gpa))

    def q_and_a(self):
        qa_page = QAPage(self)

    def show_instructions(self):
        instructions_page = InstructionsPage(self)

    def calculate_gpa(self, course_quality_points):
        total_quality_points = 0
        total_credits = 0
        empty_field = False

        for i in range(len(self.grades)):
            grade = self.grades[i].get()
            course_type = self.course_types[i].get()
            credits_entry = self.credit_entries[i]

            # Check if any required field is empty
            if not (grade and course_type and credits_entry.get()):
                empty_field = True
                break

            credits = credits_entry.get()

            # Check if credits can be converted to float
            try:
                credits = float(credits)
            except ValueError:
                messagebox.showerror("Error", "Oops! Please enter a numerical value for credits.")
                return 0.0

            if grade in GRADE_VALUES:
                quality_points = GRADE_VALUES[grade] + course_quality_points[course_type]
                total_quality_points += quality_points * credits
                total_credits += credits

        if empty_field:
            messagebox.showwarning("Warning", "Whoops! Looks like you forgot to fill in all the fields Check the different grades value, course type and credits .")
            return 0.0
        elif total_credits != 0:
            return total_quality_points / total_credits
        else:
            messagebox.showwarning("Warning", "Oops! Please enter at least one grade.")
            return 0.0

    def reset(self):
        # Display a warning message before resetting data
        confirm_reset = messagebox.askokcancel("Warning", "Are you sure you want to start over? This will delete all entered data.")

        if confirm_reset:
            # Reset all input fields
            for i in range(len(self.grades)):
                self.grades[i].set("")
                self.course_types[i].set("")
                self.credit_entries[i].delete(0, tk.END)

            # Clear GPA labels
            self.gpa_label_weighted.config(text="Weighted GPA: ")
            self.gpa_label_unweighted.config(text="Unweighted GPA: ")

    def change_rows(self):
        # Display a warning message before changing the number of rows
        confirm_change = messagebox.askokcancel("Warning", "Changing the number of rows will delete all entered data. Continue?")

        if confirm_change:
            # Destroy the current window and open the ChangeRowsPage
            change_rows_page = ChangeRowsPage(self)
        else:
            # User chose to go back, do nothing
            pass

    def update_course_count(self, course_count):
        self.course_count = course_count
        for widget in self.winfo_children():
            widget.destroy()
        self.grades = []
        self.course_types = []
        self.credit_entries = []

        for i in range(course_count):
            self.create_grade_widgets(i)


        calculate_button_weighted = tk.Button(self, text="Calculate Weighted GPA", command=self.calculate_gpa_weighted)
        calculate_button_weighted.grid(row=16, column=0, padx=10, pady=5)

        calculate_button_unweighted = tk.Button(self, text="Calculate Unweighted GPA", command=self.calculate_gpa_unweighted)
        calculate_button_unweighted.grid(row=16, column=1, padx=10, pady=5)

        reset_button = tk.Button(self, text="Reset", command=self.reset)
        reset_button.grid(row=16, column=2, padx=10, pady=5)

        add_button = tk.Button(self, text="Adjust Number of Courses", command=self.change_rows)
        add_button.grid(row=17, column=0)

        q_and_a_button = tk.Button(self, text="Q&A", command=self.q_and_a)
        q_and_a_button.grid(row=16, column=3)

        instructions_button = tk.Button(self, text="Instructions", command=self.show_instructions)
        instructions_button.grid(row=18, column=2)

        load_backup_button = tk.Button(self, text="Load Backup", command=self.load_backup)
        load_backup_button.grid(row=17, column=1)

        delete_backup_button = tk.Button(self, text="Delete Backup", command=self.delete_backup)
        delete_backup_button.grid(row=17, column=2)

        exit_button = tk.Button(self, text="Exit", command=self.destroy)
        exit_button.grid(row=17, column=3)

        backup_button = tk.Button(self, text="Backup Data", command=self.backup_data)
        backup_button.grid(row=18, column=1)

        self.gpa_label_weighted = tk.Label(self, text="Weighted GPA: ")
        self.gpa_label_weighted.grid(row=16, column=4, columnspan=6, padx=10, pady=5)

        self.gpa_label_unweighted = tk.Label(self, text="Unweighted GPA: ")
        self.gpa_label_unweighted.grid(row=17, column=4, columnspan=6, padx=10, pady=5)

        report_button = tk.Button(self, text="Generate and Save Report", command=self.generate_and_save_report)
        report_button.grid(row=18, column=0)

        auto_backup_button = tk.Button(self, text="Auto Backup", command=self.auto_backup)
        auto_backup_button.grid(row=18, column=1)

        new_calculation_button = tk.Button(self, text="Open New File", command=self.new_calculation)
        new_calculation_button.grid(row=18, column=3)

    def create_grade_widgets(self, i):
        grade_label = tk.Label(self, text="Grade:")
        grade_label.grid(row=i, column=0, padx=10, pady=5)
        grade_var = tk.StringVar()
        grade_dropdown = tk.OptionMenu(self, grade_var, *GRADE_VALUES.keys())
        grade_dropdown.grid(row=i, column=1, padx=10, pady=5)
        self.grades.append(grade_var)

        course_type_label = tk.Label(self, text="Course Type:")
        course_type_label.grid(row=i, column=2, padx=10, pady=5)

        course_type_var = tk.StringVar()
        course_type_dropdown = tk.OptionMenu(self, course_type_var, *COURSE_QUALITY_POINTS_WEIGHTED.keys())
        course_type_dropdown.grid(row=i, column=3, padx=10, pady=5)
        self.course_types.append(course_type_var)

        credit_label = tk.Label(self, text="Credits:")
        credit_label.grid(row=i, column=4, padx=10, pady=5)

        credit_entry = tk.Entry(self)
        credit_entry.grid(row=i, column=5, padx=10, pady=5)
        self.credit_entries.append(credit_entry)

    def calculate_gpa_weighted(self):
        gpa = self.calculate_gpa(COURSE_QUALITY_POINTS_WEIGHTED)
        self.gpa_label_weighted.config(text="Weighted GPA: {:.2f}".format(gpa))

    def calculate_gpa_unweighted(self):
        gpa = self.calculate_gpa(COURSE_QUALITY_POINTS_UNWEIGHTED)
        self.gpa_label_unweighted.config(text="Unweighted GPA: {:.2f}".format(gpa))

    def q_and_a(self):
        qa_page = QAPage(self)

    def show_instructions(self):
        instructions_page = InstructionsPage(self)

    def calculate_gpa(self, course_quality_points):
        total_quality_points = 0
        total_credits = 0
        empty_field = False

        for i in range(len(self.grades)):
            grade = self.grades[i].get()
            course_type = self.course_types[i].get()
            credits_entry = self.credit_entries[i]

            # Check if any required field is empty
            if not (grade and course_type and credits_entry.get()):
                empty_field = True
                break

            credits = credits_entry.get()

            # Check if credits can be converted to float
            try:
                credits = float(credits)
            except ValueError:
                messagebox.showerror("Error", "Oops! Please enter a numerical value for credits.")
                return 0.0

            if grade in GRADE_VALUES:
                quality_points = GRADE_VALUES[grade] + course_quality_points[course_type]
                total_quality_points += quality_points * credits
                total_credits += credits

        if empty_field:
            messagebox.showwarning("Warning", "Whoops! Looks like you forgot to fill in all the fields Check the different grades value, course type and credits .")
            return 0.0
        elif total_credits != 0:
            return total_quality_points / total_credits
        else:
            messagebox.showwarning("Warning", "Oops! Please enter at least one grade.")
            return 0.0

    def reset(self):
        # Display a warning message before resetting data
        confirm_reset = messagebox.askokcancel("Warning", "Are you sure you want to start over? This will delete all entered data.")

        if confirm_reset:
            # Reset all input fields
            for i in range(len(self.grades)):
                self.grades[i].set("")
                self.course_types[i].set("")
                self.credit_entries[i].delete(0, tk.END)

            # Clear GPA labels
            self.gpa_label_weighted.config(text="Weighted GPA: ")
            self.gpa_label_unweighted.config(text="Unweighted GPA: ")

    def change_rows(self):
        # Display a warning message before changing the number of rows
        confirm_change = messagebox.askokcancel("Warning", "Changing the number of rows will delete all entered data if not saved. Continue?")

        if confirm_change:
            # Destroy the current window and open the ChangeRowsPage
            change_rows_page = ChangeRowsPage(self)
        else:
            # User chose to go back, do nothing
            pass

    def update_course_count(self, course_count):
        self.course_count = course_count
        for widget in self.winfo_children():
            widget.destroy()

        self.grades = []
        self.course_types = []
        self.credit_entries = []

        for i in range(course_count):
            self.create_grade_widgets(i)

        calculate_button_weighted = tk.Button(self, text="Calculate Weighted GPA", command=self.calculate_gpa_weighted)
        calculate_button_weighted.grid(row=16, column=0, padx=10, pady=5)

        calculate_button_unweighted = tk.Button(self, text="Calculate Unweighted GPA", command=self.calculate_gpa_unweighted)
        calculate_button_unweighted.grid(row=16, column=1, padx=10, pady=5)

        reset_button = tk.Button(self, text="Start Over", command=self.reset)
        reset_button.grid(row=16, column=2, padx=10, pady=5)

        add_button = tk.Button(self, text="Adjust Number of Courses", command=self.change_rows)
        add_button.grid(row=17, column=0)

        q_and_a_button = tk.Button(self, text="Q&A", command=self.q_and_a)
        q_and_a_button.grid(row=16, column=3)

        instructions_button = tk.Button(self, text="Instructions", command=self.show_instructions)
        instructions_button.grid(row=18, column=2)

        load_backup_button = tk.Button(self, text="Load Backup", command=self.load_backup)
        load_backup_button.grid(row=17, column=1)

        delete_backup_button = tk.Button(self, text="Delete Backup", command=self.delete_backup)
        delete_backup_button.grid(row=17, column=2)

        exit_button = tk.Button(self, text="Exit", command=self.destroy)
        exit_button.grid(row=17, column=3)

        backup_button = tk.Button(self, text="Backup Data", command=self.backup_data)
        backup_button.grid(row=18, column=1)

        self.gpa_label_weighted = tk.Label(self, text="Weighted GPA: ")
        self.gpa_label_weighted.grid(row=16, column=4, columnspan=6, padx=10, pady=5)

        self.gpa_label_unweighted = tk.Label(self, text="Unweighted GPA: ")
        self.gpa_label_unweighted.grid(row=17, column=4, columnspan=6, padx=10, pady=5)

        report_button = tk.Button(self, text="Generate and Save Report", command=self.generate_and_save_report)
        report_button.grid(row=18, column=0)

        auto_backup_button = tk.Button(self, text="Auto Backup", command=self.auto_backup)
        auto_backup_button.grid(row=18, column=1)

        new_calculation_button = tk.Button(self, text="New Calculation", command=self.new_calculation)
        new_calculation_button.grid(row=18, column=3)

    def backup_data(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            data = self.get_input_data()
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", "Backup saved successfully.")

    def load_backup(self):
        filename = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "r") as f:
                data = json.load(f)
            self.load_input_data(data)
            messagebox.showinfo("Success", "Backup loaded successfully.")

    def delete_backup(self):
        filename = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            os.remove(filename)
            messagebox.showinfo("Success", "Backup deleted successfully.")

    def get_input_data(self):
        data = {
            "grades": [grade.get() for grade in self.grades],
            "course_types": [course_type.get() for course_type in self.course_types],
            "credits": [credit_entry.get() for credit_entry in self.credit_entries]
        }
        return data

    def load_input_data(self, data):
        for i in range(len(data["grades"])):
            self.grades[i].set(data["grades"][i])
            self.course_types[i].set(data["course_types"][i])
            self.credit_entries[i].delete(0, tk.END)
            self.credit_entries[i].insert(0, data["credits"][i])

    def generate_and_save_report(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            gpa_weighted = self.calculate_gpa(COURSE_QUALITY_POINTS_WEIGHTED)
            gpa_unweighted = self.calculate_gpa(COURSE_QUALITY_POINTS_UNWEIGHTED)

            # Get the input data (grades, course types, credits)
            input_data = self.get_input_data()

            with open(filename, "w") as f:
                f.write("Course\t\t\tGrade\t\tCredits\n")
                f.write("-" * 40 + "\n")
                for i, (grade, course_type, credits) in enumerate(zip(input_data["grades"], input_data["course_types"], input_data["credits"]), start=1):
                    f.write(f"{i}. {course_type}\t\t{grade}\t\t{credits}\n")
                f.write("\n")
                f.write(f"Weighted GPA: {gpa_weighted:.2f}\n")
                f.write(f"Unweighted GPA: {gpa_unweighted:.2f}\n")

            messagebox.showinfo("Success", "Report generated and saved successfully.")

            # Open the generated report using the webbrowser module
            webbrowser.open(filename)

    def auto_backup(self):
        self.backup_data_silently()  # Perform auto backup
        self.after(self.AUTO_BACKUP_INTERVAL, self.auto_backup)  # Schedule the next auto backup

    def backup_data_silently(self):
        if not self.backup_filename:
            # If backup_filename is not set, prompt the user to select a file for the first time
            self.backup_filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if self.backup_filename:
            data = self.get_input_data()

            try:
                with open(self.backup_filename, "w") as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                messagebox.showinfo("Error in backing up.")


    def new_calculation(self):
        # Restart the application
        self.destroy()
        WelcomePage()
