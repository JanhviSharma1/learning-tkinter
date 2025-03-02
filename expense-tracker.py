import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize main window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("900x500")

# Database setup
def setup_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                      id INTEGER PRIMARY KEY,
                      date TEXT,
                      description TEXT,
                      amount REAL,
                      payee TEXT,
                      mode TEXT)''')
    conn.commit()
    conn.close()

setup_db()

# UI Elements
frame_left = tk.Frame(root, bg="beige", padx=10, pady=10)
frame_left.pack(side=tk.LEFT, fill=tk.Y)

frame_right = tk.Frame(root, padx=10, pady=10)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(frame_left, text="Date:").pack()
date_entry = DateEntry(frame_left)
date_entry.pack()

tk.Label(frame_left, text="Description:").pack()
desc_entry = tk.Entry(frame_left)
desc_entry.pack()

tk.Label(frame_left, text="Amount:").pack()
amount_entry = tk.Entry(frame_left)
amount_entry.pack()

tk.Label(frame_left, text="Payee:").pack()
payee_entry = tk.Entry(frame_left)
payee_entry.pack()

tk.Label(frame_left, text="Mode of Payment:").pack()
mode_entry = ttk.Combobox(frame_left, values=["Cash", "Credit Card", "UPI", "Bank Transfer"])
mode_entry.pack()

def add_expense():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, description, amount, payee, mode) VALUES (?, ?, ?, ?, ?)",
                   (date_entry.get(), desc_entry.get(), amount_entry.get(), payee_entry.get(), mode_entry.get()))
    conn.commit()
    conn.close()
    view_expenses()

tk.Button(frame_left, text="Add Expense", command=add_expense, bg="lightgreen").pack(pady=5)

def view_expenses():
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

tree = ttk.Treeview(frame_right, columns=("ID", "Date", "Description", "Amount", "Payee", "Mode"), show='headings')
for col in ("ID", "Date", "Description", "Amount", "Payee", "Mode"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill=tk.BOTH, expand=True)

def generate_chart():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT mode, SUM(amount) FROM expenses GROUP BY mode")
    data = cursor.fetchall()
    conn.close()
    
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis("equal")
    
    chart_window = tk.Toplevel(root)
    chart_window.title("Expense Statistics")
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.get_tk_widget().pack()
    canvas.draw()

tk.Button(frame_left, text="View Expense Chart", command=generate_chart, bg="lightblue").pack(pady=5)

view_expenses()
root.mainloop()
