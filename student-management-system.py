from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import pandas as pd
from tkinter import simpledialog

# Database connection
conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    email TEXT NOT NULL
)
""")
conn.commit()

# Global variable to store the selected class name
class_name = None

def create_class():
    """ Allows the teacher to create a new class-wise student table """
    global class_name
    class_name = simpledialog.askstring("Create Class", "Enter Class Name (e.g., class_10A):")

    if class_name:
        try:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {class_name} (
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    roll_no INTEGER NOT NULL UNIQUE,
                    marks INTEGER NOT NULL
                )
            """)
            conn.commit()
            messagebox.showinfo("Success", f"Class '{class_name}' created successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to create class: {e}")

def add_student():
    """ Adds a student to the selected class """
    global class_name
    name = name_entry.get()
    age = age_entry.get()
    roll_no = roll_entry.get()
    marks = marks_entry.get()

    if not (name and age and roll_no and marks):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        cursor.execute(f"INSERT INTO {class_name} (name, age, roll_no, marks) VALUES (?, ?, ?, ?)",
                       (name, age, roll_no, marks))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        view_students()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to add student: {e}")

def view_students():
    """ Displays all students in the selected class """
    global class_name
    cursor.execute(f"SELECT * FROM {class_name}")
    rows = cursor.fetchall()
    for item in student_table.get_children():
        student_table.delete(item)
    for row in rows:
        student_table.insert("", END, values=row)

def delete_student():
    """ Deletes the selected student from the class """
    global class_name
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a student to delete!")
        return

    student_id = student_table.item(selected_item)['values'][0]
    cursor.execute(f"DELETE FROM {class_name} WHERE student_id = ?", (student_id,))
    conn.commit()
    messagebox.showinfo("Success", "Student deleted successfully!")
    view_students()

def export_data():
    """ Exports the class data to a CSV file """
    global class_name
    cursor.execute(f"SELECT * FROM {class_name}")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Name", "Age", "Roll No", "Marks"])
    df.to_csv(f"{class_name}.csv", index=False)
    messagebox.showinfo("Export Successful", f"Class data saved as {class_name}.csv")

def show_classes():
    """ Displays all class tables available in the database """
    global class_name
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != 'teachers'")
    tables = cursor.fetchall()

    if not tables:
        messagebox.showinfo("No Classes", "No classes found! Create a new class first.")
        return

    # Create a new window to select a class
    class_window = Toplevel()
    class_window.title("Select Class")
    class_window.geometry("300x200")

    Label(class_window, text="Select a class to manage:").pack(pady=10)

    for table in tables:
        class_name = table[0]
        Button(class_window, text=class_name, command=lambda cn=class_name: manage_classes(cn)).pack(pady=5)

def manage_classes(selected_class):
    """ Opens the management window for the selected class """
    global class_name, name_entry, age_entry, roll_entry, marks_entry, student_table
    class_name = selected_class

    manage = Toplevel()
    manage.title(f"Manage {class_name}")
    manage.geometry("800x600")

    Label(manage, text="Name").grid(row=0, column=0)
    name_entry = Entry(manage)
    name_entry.grid(row=0, column=1)

    Label(manage, text="Age").grid(row=1, column=0)
    age_entry = Entry(manage)
    age_entry.grid(row=1, column=1)

    Label(manage, text="Roll No").grid(row=2, column=0)
    roll_entry = Entry(manage)
    roll_entry.grid(row=2, column=1)

    Label(manage, text="Marks").grid(row=3, column=0)
    marks_entry = Entry(manage)
    marks_entry.grid(row=3, column=1)

    Button(manage, text="Add Student", command=add_student).grid(row=4, column=0, pady=5)
    Button(manage, text="View Students", command=view_students).grid(row=4, column=1, pady=5)
    Button(manage, text="Delete Student", command=delete_student).grid(row=4, column=2, pady=5)
    Button(manage, text="Export to CSV", command=export_data).grid(row=4, column=3, pady=5)

    student_table = ttk.Treeview(manage, columns=("ID", "Name", "Age", "Roll No", "Marks"), show='headings')
    for col in ("ID", "Name", "Age", "Roll No", "Marks"):
        student_table.heading(col, text=col)
    student_table.grid(row=5, column=0, columnspan=4, pady=10)

def logout():
    """ Logs out and closes the dashboard """
    dashboard.destroy()
    root.deiconify()  # Show login window again

def open_dashboard(username):
    """ Opens the Teacher Dashboard """
    root.withdraw()  # Hide login window
    global dashboard
    dashboard = Tk()
    dashboard.title("Teacher Dashboard")
    dashboard.geometry("400x300")

    Label(dashboard, text=f"Welcome, {username}", font=("Arial", 14)).pack(pady=10)

    Button(dashboard, text="Create New Class", command=create_class).pack(pady=5)
    Button(dashboard, text="Manage Existing Classes", command=show_classes).pack(pady=5)
    Button(dashboard, text="Logout", command=logout).pack(pady=5)

    dashboard.mainloop()

def login():
    """ Handles user login """
    username = entry1.get()
    password = entry2.get()

    cursor.execute("SELECT password FROM teachers WHERE username=?", (username,))
    user = cursor.fetchone()

    if user is None:
        messagebox.showinfo("User Not Found", "Username not found! Please register.")
    elif user[0] != password:
        messagebox.showerror("Error", "Incorrect password! Please try again.")
    else:
        messagebox.showinfo("Success", "Login Successful!")
        open_dashboard(username)

def register():
    """ Clears root window and creates a registration form """
    for widget in root.winfo_children():
        widget.destroy()  # Remove all existing widgets

    Label(root, text="Register", font=("Arial", 14)).grid(row=0, column=1, pady=10)

    Label(root, text="Email").grid(row=1, column=0, pady=5, padx=5)
    email_entry = Entry(root, width=30)
    email_entry.grid(row=1, column=1, pady=5)

    Label(root, text="Username").grid(row=2, column=0, pady=5, padx=5)
    username_entry = Entry(root, width=30)
    username_entry.grid(row=2, column=1, pady=5)

    Label(root, text="Password").grid(row=3, column=0, pady=5, padx=5)
    password_entry = Entry(root, width=30, show="*")
    password_entry.grid(row=3, column=1, pady=5)

    register_button = Button(root, text="Register", command=lambda: save_registration(username_entry.get(), password_entry.get(), email_entry.get()))
    register_button.grid(row=4, column=1, pady=10)

def save_registration(username, password, email):
    """ Saves the new user to the database """
    if not username or not password or not email:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        cursor.execute("INSERT INTO teachers (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        open_dashboard(username)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

# Tkinter Window
root = Tk()
root.title("Student Management System")
root.geometry("300x250")

Label(root, text="Login").grid(row=0, column=1, pady=10)

Label(root, text="Username").grid(row=1, column=0, pady=10, padx=5)
entry1 = Entry(root, width=30)
entry1.grid(row=1, column=1, pady=10)

Label(root, text="Password").grid(row=2, column=0, pady=10, padx=5)
entry2 = Entry(root, width=30, show="*")
entry2.grid(row=2, column=1, pady=10)

button1 = Button(root, text="Log in", command=login)
button1.grid(row=3, column=1, pady=10)

Label(root, text="or").grid(row=4, column=1)

button2 = Button(root, text="Register", command=register)
button2.grid(row=5, column=1)

root.mainloop()
