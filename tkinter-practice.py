import sqlite3
from tkinter import *
from tkinter import messagebox

# Database Setup
conn = sqlite3.connect("users.db")  # Create or connect to the database
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")
conn.commit()

# Function to sign up a new user
def sign_up():
    username = entry_signup_username.get()
    password = entry_signup_password.get()

    if username and password:
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Sign-up successful! Please log in.")
            signup_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
    else:
        messagebox.showerror("Error", "Please enter a username and password!")

# Function to log in an existing user
def log_in():
    username = entry_login_username.get()
    password = entry_login_password.get()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", f"Welcome, {username}!")
        login_window.destroy()
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# Creating Tkinter GUI
root = Tk()
root.title("User Authentication")
root.geometry("300x300")

# Login Window
login_window = Frame(root)
login_window.pack(pady=20)

Label(login_window, text="Login", font=("Arial", 14)).grid(row=0, column=1)

Label(login_window, text="Username:").grid(row=1, column=0)
entry_login_username = Entry(login_window, width=25)
entry_login_username.grid(row=1, column=1)

Label(login_window, text="Password:").grid(row=2, column=0)
entry_login_password = Entry(login_window, width=25, show="*")
entry_login_password.grid(row=2, column=1)

Button(login_window, text="Login", command=log_in).grid(row=3, column=1)

# Sign-up Window
signup_window = Frame(root)
signup_window.pack(pady=20)

Label(signup_window, text="Sign Up", font=("Arial", 14)).grid(row=0, column=1)

Label(signup_window, text="Username:").grid(row=1, column=0)
entry_signup_username = Entry(signup_window, width=25)
entry_signup_username.grid(row=1, column=1)

Label(signup_window, text="Password:").grid(row=2, column=0)
entry_signup_password = Entry(signup_window, width=25, show="*")
entry_signup_password.grid(row=2, column=1)

Button(signup_window, text="Sign Up", command=sign_up).grid(row=3, column=1)

root.mainloop()

# Closing the database connection
conn.close()
