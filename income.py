import ttkbootstrap as ttk
from tkinter import messagebox

class IncomeTab(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.create_income_tab()

    def create_income_tab(self):
        income_frame = ttk.Frame(self)
        income_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Date Range Selection
        ttk.Label(income_frame, text="Start Date:").grid(row=0, column=0, padx=10, pady=10)
        self.start_date_entry = ttk.Entry(income_frame)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(income_frame, text="End Date:").grid(row=1, column=0, padx=10, pady=10)
        self.end_date_entry = ttk.Entry(income_frame)
        self.end_date_entry.grid(row=1, column=1, padx=10, pady=10)

        self.calculate_income_button = ttk.Button(income_frame, text="Calculate Income", command=self.calculate_income)
        self.calculate_income_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Income List
        self.income_listbox = ttk.Treeview(income_frame, columns=("Client", "Total Amount", "Date"), show="headings")
        self.income_listbox.grid(row=3, column=0, columnspan=2, pady=10)
        self.income_listbox.heading("Client", text="Client")
        self.income_listbox.heading("Total Amount", text="Total Amount")
        self.income_listbox.heading("Date", text="Date")

    def calculate_income(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if not start_date or not end_date:
            messagebox.showerror("Error", "Please enter both start and end dates.")
            return 
        for row in self.income_listbox.get_children():
            self.income_listbox.delete(row)

        income_data = self.db.fetch_all('''
            SELECT clients.name, SUM(invoices.total_amount), invoices.date
            FROM invoices
            JOIN clients ON invoices.client_id = clients.id
            WHERE invoices.date BETWEEN ? AND ?
            GROUP BY clients.name
        ''', (start_date, end_date))
        for income in income_data:
            self.income_listbox.insert("", "end", values=(income[0], income[1], income[2]))