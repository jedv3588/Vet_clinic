import ttkbootstrap as ttk
from tkinter import messagebox

class InvoicesTab(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.create_invoices_tab()

    def create_invoices_tab(self):
        invoice_form_frame = ttk.LabelFrame(self, text="Invoice Information")
        invoice_form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(invoice_form_frame, text="Client ID:").grid(row=0, column=0)
        self.invoice_client_id_entry = ttk.Entry(invoice_form_frame)
        self.invoice_client_id_entry.grid(row=0, column=1)

        ttk.Label(invoice_form_frame, text="Total Amount:").grid(row=1, column=0)
        self.invoice_total_entry = ttk.Entry(invoice_form_frame)
        self.invoice_total_entry.grid(row=1, column=1)

        self.add_invoice_button = ttk.Button(invoice_form_frame, text="Create Invoice", command=self.add_invoice)
        self.add_invoice_button.grid(row=2, column=0, columnspan=2)

        invoice_table_frame = ttk.LabelFrame(self, text="Invoice List")
        invoice_table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.invoice_listbox = ttk.Treeview(invoice_table_frame, columns=("Client", "Total Amount", "Date"), show="headings")
        self.invoice_listbox.grid(row=0, column=0)
        self.invoice_listbox.heading("Client", text="Client")
        self.invoice_listbox.heading("Total Amount", text="Total Amount")
        self.invoice_listbox.heading("Date", text="Date")
        self.load_invoices()

        self.edit_invoice_button = ttk.Button(invoice_table_frame, text="Edit Invoice", command=self.edit_invoice)
        self.edit_invoice_button.grid(row=1, column=0, sticky="ew")

        self.delete_invoice_button = ttk.Button(invoice_table_frame, text="Delete Invoice", command=self.delete_invoice)
        self.delete_invoice_button.grid(row=2, column=0, sticky="ew")

    def load_invoices(self):
        for row in self.invoice_listbox.get_children():
            self.invoice_listbox.delete(row)
        invoices = self.db.fetch_all("SELECT invoices.id, clients.name, invoices.total_amount, invoices.date FROM invoices JOIN clients ON invoices.client_id = clients.id")
        for invoice in invoices:
            self.invoice_listbox.insert("", "end", values=(invoice[1], invoice[2], invoice[3]))

    def add_invoice(self):
        client_id = self.invoice_client_id_entry.get()
        total_amount = self.invoice_total_entry.get()
        if not client_id or not total_amount:
            messagebox.showerror("Error", "Client ID and total amount are required.")
            return
        self.db.execute_query('''
            INSERT INTO invoices (client_id, date, total_amount) 
            VALUES (?, date('now'), ?)
        ''', (client_id, float(total_amount)))
        self.invoice_client_id_entry.delete(0, "end")
        self.invoice_total_entry.delete(0, "end")
        self.load_invoices()

    def edit_invoice(self):
        selected_item = self.invoice_listbox.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an invoice to edit.")
            return
        invoice_data = self.invoice_listbox.item(selected_item)['values']
        self.invoice_client_id_entry.delete(0, "end")
        self.invoice_client_id_entry.insert(0, invoice_data[0])  # Assuming client ID is stored
        self.invoice_total_entry.delete(0, "end")
        self.invoice_total_entry.insert(0, invoice_data[1])
        self.delete_invoice()  # Remove the old entry after editing

    def delete_invoice(self):
        selected_item = self.invoice_listbox.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an invoice to delete.")
            return
        invoice_data = self.invoice_listbox.item(selected_item)['values']
        self.db.execute_query("DELETE FROM invoices WHERE client_id=? AND total_amount=?", (invoice_data[0], invoice_data[1]))
        self.load_invoices()