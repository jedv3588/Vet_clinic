import ttkbootstrap as ttk
from tkinter import messagebox

class ServicesTab(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.create_services_tab()

    def create_services_tab(self):
        service_form_frame = ttk.LabelFrame(self, text="Service Information")
        service_form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(service_form_frame, text="Service Name:").grid(row=0, column=0)
        self.service_name_entry = ttk.Entry(service_form_frame)
        self.service_name_entry.grid(row=0, column=1)

        ttk.Label(service_form_frame, text="Price:").grid(row=1, column=0)
        self.service_price_entry = ttk.Entry(service_form_frame)
        self.service_price_entry.grid(row=1, column=1)

        self.add_service_button = ttk.Button(service_form_frame, text="Add Service", command=self.add_service)
        self.add_service_button.grid(row=2, column=0, columnspan=2)

        service_table_frame = ttk.LabelFrame(self, text="Service List")
        service_table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.service_listbox = ttk.Treeview(service_table_frame, columns=("Name", "Price"), show="headings")
        self.service_listbox.grid(row=0, column=0)
        self.service_listbox.heading("Name", text="Name")
        self.service_listbox.heading("Price", text="Price")
        self.load_services()

        self.edit_service_button = ttk.Button(service_table_frame, text="Edit Service", command=self.edit_service)
        self.edit_service_button.grid(row=1, column=0, sticky="ew")

        self.delete_service_button = ttk.Button(service_table_frame, text="Delete Service", command=self.delete_service)
        self.delete_service_button.grid(row=2, column=0, sticky="ew")

    def load_services(self):
        for row in self.service_listbox.get_children():
            self.service_listbox.delete(row)
        services = self.db.fetch_all("SELECT * FROM services")
        for service in services:
            self.service_listbox.insert("", "end", values=(service[1], service[2]))

    def add_service(self):
        name = self.service_name_entry.get()
        price = self.service_price_entry.get()
        if not name or not price:
            messagebox.showerror("Error", "Service name and price are required.")
            return
        self.db.execute_query("INSERT INTO services (name, price) VALUES (?, ?)", (name, float(price)))
        self.service_name_entry.delete(0, "end")
        self.service_price_entry.delete(0, "end")
        self.load_services()

    def edit_service(self):
        selected_item = self.service_listbox.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a service to edit.")
            return
        service_data = self.service_listbox.item(selected_item)['values']
        self.service_name_entry.delete(0, "end")
        self.service_name_entry.insert(0, service_data[0])
        self.service_price_entry.delete(0, "end")
        self.service_price_entry.insert(0, service_data[1])
        self.delete_service()  # Remove the old entry after editing

    def delete_service(self):
        selected_item = self.service_listbox.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a service to delete.")
            return
        service_data = self.service_listbox.item(selected_item)['values']
        self.db.execute_query("DELETE FROM services WHERE name=? AND price=?", (service_data[0], service_data[1]))
        self.load_services()