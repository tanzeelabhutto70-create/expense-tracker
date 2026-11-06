import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os
from datetime import datetime

DATA_FILE = "expenses_data.json"

PURPLE = "#5948D8"
BG = "#F1F2F7"
WHITE = "#FFFFFF"
DARK = "#252A35"


class ExpenseTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Professional Expense Tracker")
        self.root.geometry("1100x750")
        self.root.minsize(800, 550)
        self.root.configure(bg=BG)

        self.expenses = []
        self.selected_id = None

        self.load_data()
        self.setup_style()
        self.setup_scroll()
        self.create_ui()
        self.refresh_data()

    # SCROLLABLE WINDOW
    def setup_scroll(self):

        self.canvas = tk.Canvas(
            self.root,
            bg=BG,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(self.canvas, bg=BG)

        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(
                self.window_id, width=e.width
            )
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

    def mouse_scroll(self, event):
        self.canvas.yview_scroll(
            int(-event.delta / 120), "units"
        )

    # LOAD DATA
    def load_data(self):

        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    data = json.load(file)

                self.expenses = data if isinstance(data, list) else []

                for index, expense in enumerate(self.expenses, start=1):
                    expense.setdefault("id", index)
                    expense.setdefault("name", "Unknown")
                    expense.setdefault("amount", 0)
                    expense.setdefault("category", "Other")
                    expense.setdefault("date", "N/A")

                self.save_data()

            except (json.JSONDecodeError, TypeError, OSError):
                self.expenses = []
        else:
            self.expenses = []

    # SAVE DATA
    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.expenses, file, indent=4)

    # STYLE
    def setup_style(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=DARK,
            rowheight=38,
            font=("Arial", 11)
        )

        style.configure(
            "Treeview.Heading",
            background=PURPLE,
            foreground=WHITE,
            font=("Arial", 11, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#DCD7FF")]
        )

    # BUTTON
    def make_button(self, parent, text, command):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=PURPLE,
            fg=WHITE,
            activebackground="#4032B5",
            activeforeground=WHITE,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=10,
            relief="flat",
            cursor="hand2"
        )

    # USER INTERFACE
    def create_ui(self):

        tk.Label(
            self.content,
            text="💰 Expense Tracker",
            font=("Arial", 28, "bold"),
            bg=BG,
            fg=DARK
        ).pack(pady=(25, 5))

        tk.Label(
            self.content,
            text="Manage Your Daily Expenses Easily",
            font=("Arial", 13),
            bg=BG,
            fg="gray"
        ).pack(pady=(0, 20))

        # DASHBOARD
        dashboard = tk.Frame(
            self.content,
            bg=PURPLE,
            height=145
        )
        dashboard.pack(fill="x", padx=20, pady=10)
        dashboard.pack_propagate(False)

        tk.Label(
            dashboard,
            text="Total Kharcha",
            font=("Arial", 17),
            bg=PURPLE,
            fg=WHITE
        ).pack(pady=(18, 5))

        self.total_label = tk.Label(
            dashboard,
            text="₹0.00",
            font=("Arial", 34, "bold"),
            bg=PURPLE,
            fg=WHITE
        )
        self.total_label.pack()

        # ADD EXPENSE FORM
        form = tk.LabelFrame(
            self.content,
            text=" Naya Expense Add Karo ",
            font=("Arial", 14, "bold"),
            bg=WHITE,
            fg=DARK,
            padx=15,
            pady=15
        )
        form.pack(fill="x", padx=20, pady=15)

        tk.Label(
            form,
            text="Expense Name:",
            bg=WHITE,
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky="w", pady=8)

        self.name_entry = tk.Entry(
            form,
            font=("Arial", 12),
            width=35
        )
        self.name_entry.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(
            form,
            text="Amount (₹):",
            bg=WHITE,
            font=("Arial", 11)
        ).grid(row=1, column=0, sticky="w", pady=8)

        self.amount_entry = tk.Entry(
            form,
            font=("Arial", 12),
            width=35
        )
        self.amount_entry.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(
            form,
            text="Category:",
            bg=WHITE,
            font=("Arial", 11)
        ).grid(row=2, column=0, sticky="w", pady=8)

        self.category_box = ttk.Combobox(
            form,
            values=[
                "Food", "Shopping", "Transport",
                "Bills", "Education", "Health", "Other"
            ],
            state="readonly",
            width=32,
            font=("Arial", 11)
        )
        self.category_box.set("Food")
        self.category_box.grid(row=2, column=1, padx=10, pady=8)

        buttons = tk.Frame(form, bg=WHITE)
        buttons.grid(row=3, column=0, columnspan=2, pady=15)

        self.make_button(
            buttons, "＋ Add Expense",
            self.add_expense
        ).pack(side="left", padx=5)

        self.make_button(
            buttons, "✎ Update Expense",
            self.update_expense
        ).pack(side="left", padx=5)

        # SEARCH AND FILTER
        search_frame = tk.Frame(self.content, bg=BG)
        search_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            width=22
        )
        self.search_entry.pack(side="left", padx=5, ipady=8)

        self.make_button(
            search_frame, "🔍 Search",
            self.search_expense
        ).pack(side="left", padx=5)

        self.filter_box = ttk.Combobox(
            search_frame,
            values=[
                "All", "Food", "Shopping", "Transport",
                "Bills", "Education", "Health", "Other"
            ],
            state="readonly",
            width=15
        )
        self.filter_box.set("All")
        self.filter_box.pack(side="left", padx=5)

        self.make_button(
            search_frame, "Filter",
            self.filter_expense
        ).pack(side="left", padx=5)

        # HISTORY
        tk.Label(
            self.content,
            text="📋 Expense History",
            font=("Arial", 18, "bold"),
            bg=BG,
            fg=DARK
        ).pack(anchor="w", padx=20, pady=10)

        table_frame = tk.Frame(self.content, bg=WHITE)
        table_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        columns = ("ID", "Name", "Amount", "Category", "Date")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=7
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(
                col,
                anchor="center",
                width=150
            )

        table_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=table_scroll.set
        )

        self.tree.pack(side="left", fill="x", expand=True)
        table_scroll.pack(side="right", fill="y")

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_expense
        )

        # BOTTOM BUTTONS
        bottom = tk.Frame(self.content, bg=BG)
        bottom.pack(fill="x", padx=20, pady=20)

        self.make_button(
            bottom, "✎ Edit",
            self.edit_expense
        ).pack(side="left", padx=4)

        self.make_button(
            bottom, "🗑 Delete",
            self.delete_expense
        ).pack(side="left", padx=4)

        self.make_button(
            bottom, "📥 Export CSV",
            self.export_csv
        ).pack(side="left", padx=4)

        self.make_button(
            bottom, "↻ Refresh",
            self.refresh_data
        ).pack(side="left", padx=4)

        self.make_button(
            bottom, "Clear All",
            self.clear_all
        ).pack(side="left", padx=4)

        tk.Label(
            self.content,
            text="Expense Tracker | Python GUI Project",
            font=("Arial", 10),
            bg=BG,
            fg="gray"
        ).pack(pady=20)

    # ADD
    def add_expense(self):

        name = self.name_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not name or not amount:
            messagebox.showwarning(
                "Warning", "Please enter name and amount!"
            )
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Enter a valid positive amount!"
            )
            return

        new_id = max(
            (e["id"] for e in self.expenses),
            default=0
        ) + 1

        expense = {
            "id": new_id,
            "name": name,
            "amount": amount,
            "category": self.category_box.get(),
            "date": datetime.now().strftime("%d-%m-%Y %H:%M")
        }

        self.expenses.append(expense)
        self.save_data()
        self.clear_fields()
        self.refresh_data()

        messagebox.showinfo(
            "Success", "Expense Added Successfully!"
        )

    # SELECT
    def select_expense(self, event=None):

        selected = self.tree.selection()

        if selected:
            values = self.tree.item(selected[0])["values"]
            self.selected_id = int(values[0])

    # EDIT
    def edit_expense(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Warning", "Please select an expense!"
            )
            return

        expense = next(
            (e for e in self.expenses
             if e["id"] == self.selected_id),
            None
        )

        if expense:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, expense["name"])

            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, str(expense["amount"]))

            self.category_box.set(expense["category"])

    # UPDATE
    def update_expense(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Warning", "Select an expense first!"
            )
            return

        name = self.name_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not name or not amount:
            messagebox.showwarning(
                "Warning", "Fill all fields!"
            )
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Enter a valid amount!"
            )
            return

        for expense in self.expenses:
            if expense["id"] == self.selected_id:
                expense["name"] = name
                expense["amount"] = amount
                expense["category"] = self.category_box.get()
                break

        self.save_data()
        self.clear_fields()
        self.refresh_data()

        messagebox.showinfo(
            "Success", "Expense Updated Successfully!"
        )

    # DELETE
    def delete_expense(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Warning", "Select an expense first!"
            )
            return

        if messagebox.askyesno(
            "Confirm", "Delete selected expense?"
        ):
            self.expenses = [
                e for e in self.expenses
                if e["id"] != self.selected_id
            ]

            self.save_data()
            self.clear_fields()
            self.refresh_data()

            messagebox.showinfo(
                "Success", "Expense Deleted!"
            )

    # SEARCH
    def search_expense(self):

        keyword = self.search_entry.get().strip().lower()

        self.tree.delete(*self.tree.get_children())

        for expense in self.expenses:
            if keyword in expense["name"].lower():
                self.insert_row(expense)

    # FILTER
    def filter_expense(self):

        category = self.filter_box.get()

        self.tree.delete(*self.tree.get_children())

        for expense in self.expenses:
            if category == "All" or expense["category"] == category:
                self.insert_row(expense)

    # TABLE ROW
    def insert_row(self, expense):

        self.tree.insert(
            "",
            "end",
            values=(
                expense["id"],
                expense["name"],
                f"₹{expense['amount']:,.2f}",
                expense["category"],
                expense["date"]
            )
        )

    # REFRESH
    def refresh_data(self):

        self.tree.delete(*self.tree.get_children())

        for expense in self.expenses:
            self.insert_row(expense)

        total = sum(
            float(e["amount"]) for e in self.expenses
        )

        self.total_label.config(
            text=f"₹{total:,.2f}"
        )

        self.selected_id = None

    # EXPORT CSV
    def export_csv(self):

        if not self.expenses:
            messagebox.showwarning(
                "Warning", "No expenses to export!"
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        if path:
            with open(
                path, "w", newline="", encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "ID", "Name", "Amount", "Category", "Date"
                ])

                for e in self.expenses:
                    writer.writerow([
                        e["id"],
                        e["name"],
                        e["amount"],
                        e["category"],
                        e["date"]
                    ])

            messagebox.showinfo(
                "Success", "CSV Exported Successfully!"
            )

    # CLEAR ALL
    def clear_all(self):

        if not self.expenses:
            messagebox.showinfo(
                "Information", "No records to clear!"
            )
            return

        if messagebox.askyesno(
            "Confirm", "Delete ALL expense records?"
        ):
            self.expenses = []
            self.save_data()
            self.clear_fields()
            self.refresh_data()

            messagebox.showinfo(
                "Success", "All Records Cleared!"
            )

    # CLEAR INPUT
    def clear_fields(self):

        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_box.set("Food")
        self.selected_id = None


# START APPLICATION
if __name__ == "__main__":

    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()