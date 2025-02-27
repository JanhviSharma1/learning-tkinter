from tkinter import *
import sqlite3
from tkinter import messagebox

# Database connection
conn = sqlite3.connect("students.db")
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

def open_dashboard(username):
    """ Opens the Teacher Dashboard """
    root.destroy()  # Close login window
    dashboard = Tk()
    dashboard.title("Teacher Dashboard")
    dashboard.geometry("400x300")

    Label(dashboard, text=f"Welcome, {username}", font=("Arial", 14)).pack(pady=10)

    Button(dashboard, text="Create New Class").pack(pady=5)
    Button(dashboard, text="Manage Existing Classes").pack(pady=5)
    Button(dashboard, text="Logout").pack(pady=5)

    dashboard.mainloop()

def login():
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
        root.destroy()  # Close after registration
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
