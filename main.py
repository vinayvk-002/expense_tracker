import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date
import matplotlib.pyplot as plt

# ========== Database Setup ==========
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL,
                        category TEXT,
                        description TEXT,
                        date TEXT)''')
    conn.commit()
    conn.close()

# Insert expense into DB
def add_expense():
    amt = amount_entry.get()
    cat = category_var.get()
    desc = desc_entry.get()
    exp_date = date_entry.get()

    if not amt or not cat:
        messagebox.showerror("Error", "Amount and Category are required!")
        return
    
    try:
        amt = float(amt)
    except:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                   (amt, cat, desc, exp_date))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Expense added successfully!")
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    view_expenses()

# Fetch and display expenses
def view_expenses():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    total = 0
    for row in rows:
        tree.insert("", tk.END, values=row)
        total += row[1]
    
    total_label.config(text=f"Total Expenses: ₹{total:.2f}")

# Show Category-wise Pie Chart
def show_chart():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("Info", "No expenses to display!")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(5,5))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("Expenses by Category")
    plt.show()

# ========== GUI Setup ==========
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("750x550")
root.resizable(False, False)

# Input Frame
input_frame = tk.LabelFrame(root, text="Add Expense", padx=10, pady=10)
input_frame.pack(fill="x", padx=10, pady=5)

tk.Label(input_frame, text="Amount (₹):").grid(row=0, column=0, padx=5, pady=5)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(input_frame, textvariable=category_var,
                                 values=["Food", "Transport", "Shopping", "Bills", "Other"])
category_dropdown.grid(row=0, column=3, padx=5, pady=5)
category_dropdown.current(0)

tk.Label(input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
desc_entry = tk.Entry(input_frame)
desc_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=2, padx=5, pady=5)
date_entry = tk.Entry(input_frame)
date_entry.grid(row=1, column=3, padx=5, pady=5)
date_entry.insert(0, str(date.today()))

add_button = tk.Button(input_frame, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white")
add_button.grid(row=2, column=0, columnspan=2, pady=10)

chart_button = tk.Button(input_frame, text="Show Chart", command=show_chart, bg="#2196F3", fg="white")
chart_button.grid(row=2, column=2, columnspan=2, pady=10)

# Table Frame
table_frame = tk.LabelFrame(root, text="Expenses", padx=10, pady=10)
table_frame.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("ID", "Amount", "Category", "Description", "Date")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill="both", expand=True)

# Total Label
total_label = tk.Label(root, text="Total Expenses: ₹0.00", font=("Arial", 12, "bold"))
total_label.pack(pady=5)

# Initialize DB and Load Data
init_db()
view_expenses()

root.mainloop()
