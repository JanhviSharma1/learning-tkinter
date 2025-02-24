import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Create main window
root = tk.Tk()
root.title("Mini Office Suite")
root.geometry("600x500")

# === Functions ===
def save_file():
    text_content = text_area.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_content)
        messagebox.showinfo("File Saved", "Your file has been saved successfully!")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, file.read())

def add_task():
    task = task_entry.get()
    if task:
        task_list.insert(tk.END, task)
        task_entry.delete(0, tk.END)

def delete_task():
    try:
        selected_task = task_list.curselection()[0]
        task_list.delete(selected_task)
    except IndexError:
        messagebox.showwarning("No Selection", "Please select a task to delete.")

def show_about():
    messagebox.showinfo("About", "Mini Office Suite v1.0\nBuilt with Tkinter.")

# === Menu Bar ===
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

menu_bar.add_command(label="About", command=show_about)

# === Notebook (Tabs) ===
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# --- Text Editor Tab ---
text_frame = ttk.Frame(notebook)
notebook.add(text_frame, text="Notepad")

text_area = tk.Text(text_frame, wrap="word", font=("Arial", 12))
text_area.pack(expand=True, fill="both", padx=5, pady=5)

# --- Task Manager Tab ---
task_frame = ttk.Frame(notebook)
notebook.add(task_frame, text="To-Do List")

task_entry = tk.Entry(task_frame, width=40)
task_entry.pack(pady=5)

task_button_frame = tk.Frame(task_frame)
task_button_frame.pack()

add_button = tk.Button(task_button_frame, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(task_button_frame, text="Delete Task", command=delete_task)
delete_button.pack(side=tk.LEFT, padx=5)

task_list = tk.Listbox(task_frame, height=10, width=50)
task_list.pack(pady=5)

# --- Table View Tab ---
table_frame = ttk.Frame(notebook)
notebook.add(table_frame, text="Data Table")

columns = ("Name", "Age", "Role")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Role", text="Role")

tree.insert("", "end", values=("Alice", "25", "Engineer"))
tree.insert("", "end", values=("Bob", "30", "Manager"))

tree.pack(pady=10, expand=True, fill="both")

# === Run Application ===
root.mainloop()
