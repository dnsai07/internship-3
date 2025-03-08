import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def setup_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_expense():
    date = date_entry.get()
    category = category_combobox.get()
    amount = amount_entry.get()
    description = description_entry.get()
    
    if not date or not category or not amount:
        messagebox.showerror("Error", "Please fill all required fields!")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, amount, description))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Expense added successfully!")
    display_expenses()

def display_expenses():
    for row in expense_tree.get_children():
        expense_tree.delete(row)
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    
    for expense in expenses:
        expense_tree.insert("", tk.END, values=expense)

def delete_expense():
    selected_item = expense_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to delete!")
        return
    
    expense_id = expense_tree.item(selected_item, "values")[0]
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Expense deleted successfully!")
    display_expenses()

# Setup Database
setup_database()

# GUI Setup
root = tk.Tk()
root.title("Expense Tracker")

# Input Fields
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1)

tk.Label(root, text="Category:").grid(row=1, column=0)
category_combobox = ttk.Combobox(root, values=["Food", "Transport", "Entertainment", "Others"])
category_combobox.grid(row=1, column=1)

tk.Label(root, text="Amount:").grid(row=2, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1)

tk.Label(root, text="Description:").grid(row=3, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="Delete Expense", command=delete_expense).grid(row=5, column=0, columnspan=2)

# Expense List
expense_tree = ttk.Treeview(root, columns=("ID", "Date", "Category", "Amount", "Description"), show="headings")
for col in ("ID", "Date", "Category", "Amount", "Description"):
    expense_tree.heading(col, text=col)
expense_tree.grid(row=6, column=0, columnspan=2)

display_expenses()

root.mainloop()
