import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import bcrypt

# Izveido datu bāzi
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Tabulu izveide
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")
conn.commit()

# Funkcija paroles hashēšanai
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Funkcija paroles pārbaudei
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Galvenā lietotnes klase
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.current_user = None

        # Izsauc sākuma logu
        self.login_screen()

    def login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Expense Tracker Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register_screen).pack()

    def register_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Register", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Register", command=self.register).pack(pady=5)
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def main_screen(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Add Expense", command=self.add_expense_screen).pack(pady=5)
        tk.Button(self.root, text="View Expenses", command=self.view_expenses_screen).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=5)

    def add_expense_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Add Expense", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Category").pack()
        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        tk.Label(self.root, text="Amount").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        tk.Button(self.root, text="Add", command=self.add_expense).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_screen).pack()

    def view_expenses_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Your Expenses", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(self.root, columns=("Category", "Amount", "Date"), show="headings")
        tree.heading("Category", text="Category")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")
        tree.pack()

        cursor.execute("SELECT category, amount, date FROM expenses WHERE user_id = ?", (self.current_user_id,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

        tk.Button(self.root, text="Back", command=self.main_screen).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        hashed_password = hash_password(password)

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and verify_password(password, user[1]):
            self.current_user = username
            self.current_user_id = user[0]
            self.main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def add_expense(self):
        category = self.category_entry.get()
        amount = self.amount_entry.get()

        if not category or not amount:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            amount = float(amount)
            cursor.execute("INSERT INTO expenses (user_id, category, amount, date) VALUES (?, ?, ?, date('now'))",
                           (self.current_user_id, category, amount))
            conn.commit()
            messagebox.showinfo("Success", "Expense added successfully!")
            self.main_screen()
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Lietotnes palaišana
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
