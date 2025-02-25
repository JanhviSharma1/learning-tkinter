import tkinter as tk

# Functions for operations
def add():
    try:
        a = int(entry1.get())
        b = int(entry2.get())
        result_label.config(text=f"Result: {a + b}")
    except ValueError:
        result_label.config(text="Error: Enter valid numbers")

def subtract():
    try:
        a = int(entry1.get())
        b = int(entry2.get())
        result_label.config(text=f"Result: {abs(a - b)}")  # Absolute difference
    except ValueError:
        result_label.config(text="Error: Enter valid numbers")

def multiply():
    try:
        a = int(entry1.get())
        b = int(entry2.get())
        result_label.config(text=f"Result: {a * b}")
    except ValueError:
        result_label.config(text="Error: Enter valid numbers")

def divide():
    try:
        a = int(entry1.get())
        b = int(entry2.get())
        if b == 0:
            result_label.config(text="Error: Cannot divide by zero")
        else:
            result_label.config(text=f"Result: {a / b:.2f}")  # Show result up to 2 decimal places
    except ValueError:
        result_label.config(text="Error: Enter valid numbers")

# Creating main window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x300")

# Labels and Entry Fields
tk.Label(root, text="Enter first number:").grid(row=0, column=0, padx=10, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Enter second number:").grid(row=1, column=0, padx=10, pady=5)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=10, pady=5)

# Buttons for Operations
tk.Button(root, text="Add", command=add, width=10).grid(row=2, column=0, padx=5, pady=5)
tk.Button(root, text="Subtract", command=subtract, width=10).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Multiply", command=multiply, width=10).grid(row=3, column=0, padx=5, pady=5)
tk.Button(root, text="Divide", command=divide, width=10).grid(row=3, column=1, padx=5, pady=5)

# Result Label
result_label = tk.Label(root, text="Result: ", font=("Arial", 12, "bold"))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
