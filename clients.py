import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation
from tkinter import messagebox
import logging

class ClientsTab(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.name = ttk.StringVar(value="")
        self.phone = ttk.StringVar(value="")
        self.address = ttk.StringVar(value="")
        self.selected_client_id = None  # Track the selected client ID for editing
        self.current_page = 0
        self.records_per_page = 5
        self.total_records = 0
        self.create_clients_tab()
        self.load_data()

    def execute_db_query(self, query, params=()):
        """Helper method to execute a database query."""
        try:
            with self.db.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor
        except Exception as e:
            logging.error(f"Database error: {e}")
            messagebox.showerror("Error", f"Database operation failed: {e}")

    def insert_client(self, name, phone, address):
        """Insert a new client into the database."""
        self.execute_db_query('INSERT INTO clients (name, phone, address) VALUES (?, ?, ?)', (name, phone, address))

    def update_client(self, client_id, name, phone, address):
        """Update an existing client in the database."""
        self.execute_db_query('UPDATE clients SET name = ?, phone = ?, address = ? WHERE id = ?', (name, phone, address, client_id))

    def delete_client(self, client_id):
        """Delete a client from the database."""
        self.execute_db_query('DELETE FROM clients WHERE id = ?', (client_id,))

    def fetch_clients(self, offset=0, limit=5):
        """Fetch clients from the database with pagination."""
        try:
            with self.db.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM clients LIMIT ? OFFSET ?', (limit, offset))
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Failed to fetch clients: {e}")
            messagebox.showerror("Error", f"Failed to fetch clients: {e}")
            return []

    def count_clients(self):
        """Count the total number of clients in the database."""
        try:
            with self.db.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM clients')
                return cursor.fetchone()[0]
        except Exception as e:
            logging.error(f"Failed to count clients: {e}")
            messagebox.showerror("Error", f"Failed to count clients: {e}")
            return 0

    def create_clients_tab(self):
        """Create the clients tab UI components."""
        instruction_text = "Enter client details: " 
        instruction = ttk.Label(self, text=instruction_text, width=50)
        instruction.pack(fill=X, pady=10)

        self.create_form_entry("Name: ", self.name)
        self.create_form_entry("Phone: ", self.phone)
        self.create_form_entry("Address: ", self.address)
        self.create_buttonbox()
        self.table = self.create_table()    

    def create_form_entry(self, label, variable):
        """Create a form entry field."""
        form_field_container = ttk.Frame(self)
        form_field_container.pack(fill=X, expand=YES, pady=2)

        form_field_label = ttk.Label(master=form_field_container, text=label, width=15)
        form_field_label.pack(side=LEFT, padx=5)

        form_input = ttk.Entry(master=form_field_container, textvariable=variable)
        form_input.pack(side=LEFT, padx= 5, fill=X, expand=YES)
        
        add_regex_validation(form_input, r'^[a-zA-Z0-9_ ]*$')  # Allow spaces in names
    
        return form_input

    def create_buttonbox(self):
        """Create buttons for adding, editing, and deleting clients."""
        button_container = ttk.Frame(self)
        button_container.pack(fill=X, expand=YES, pady=(15, 10))

        delete_btn = ttk.Button(
            master=button_container,
            text="Delete",
            command=self.delete_selected_client,
            bootstyle=DANGER,
            width=8,
        )
        delete_btn.pack(side=RIGHT, padx=5)

        edit_btn = ttk.Button(
            master=button_container,
            text="Edit",
            command=self.edit_selected_client,
            bootstyle=INFO,
            width=8,
        )
        edit_btn.pack(side=RIGHT, padx=5)

        submit_btn = ttk.Button(
            master=button_container,
            text="Add",
            command=self.add_client,
            bootstyle=SUCCESS,
            width=8,
        )
        submit_btn.pack(side=RIGHT, padx=5)

    def create_table(self):
        """Create the table to display clients."""
        ttk.Label(self, text="Search Client:").pack(pady=5)
        self.search_var = ttk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_client)

        style = ttk.Style()
        style.configure("Treeview.Heading", background="#003366", foreground="white", font=("Arial", 10, "bold"))
        style.configure("Treeview", rowheight=20)

        self.table = ttk.Treeview(self, columns=("ID", "Name", "Phone", "Address"), show='headings', height=10)
        self.table.heading("ID", text="ID")
        self.table.heading("Name", text="Name")
        self.table.heading("Phone", text="Phone")
        self.table.heading("Address", text="Address")
        self.table.column("ID", width=5)
        self.table.column("Name", width=50)
        self.table.column("Phone", width=20)
        self.table.column("Address", width=100)
        self.table.pack(expand=True, fill='both', pady=10)

        self.table.tag_configure('oddrow', background='lightblue')
        self.table.tag_configure('evenrow', background='white')

        self.table.bind("<Double-1>", self.on_item_selected)

        self.pagination_frame = ttk.Frame(self)
        self.pagination_frame.pack(pady=5)

        self.prev_button = ttk.Button(self.pagination_frame, text="Previous", command=self.prev_page)
        self.prev_button.pack(side='left', padx=5)

        self.next_button = ttk.Button(self.pagination_frame, text="Next", command=self.next_page)
        self.next_button.pack(side='right', padx=5)

        self.page_info_label = ttk.Label(self.pagination_frame, text="")
        self.page_info_label.pack(side='left', padx=5)
        
        return self.table

    def load_data(self):
        """Load client data into the table."""
        for row in self.table.get_children():
            self.table.delete(row)
        clients = self.fetch_clients(self.current_page * self.records_per_page, self.records_per_page)
        for index, client in enumerate(clients):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.table.insert("", "end", values=client, tags=(tag,))
        self.update_pagination()

    def update_pagination(self):
        """Update pagination controls based on the total number of records."""
        self.total_records = self.count_clients()
        self.prev_button['state'] = 'normal' if self.current_page > 0 else 'disabled'
        self.next_button['state'] = 'normal' if (self.current_page + 1) * self.records_per_page < self.total_records else 'disabled'
        self.page_info_label.config(text=f"Page {self.current_page + 1} of {((self.total_records + self.records_per_page - 1) // self.records_per_page)} - Total Records: {self.total_records}")

    def show_message(self, message):
        """Display a toast notification."""
        toast = ToastNotification(
            title="Client Management App",
            message=message,
            duration=3000
        )
        toast.show_toast()

    def add_client(self):
        """Add a new client."""
        name = self.name.get()
        phone = self.phone.get()
        address = self.address.get()
        self.insert_client(name, phone, address)
        self.load_data()
        self.clear_entries()
        self.show_message(" Client added successfully!")

    def edit_selected_client(self):
        """Edit the selected client."""
        selected_item = self.table.selection()
        if selected_item:
            client_id = self.table.item(selected_item, 'values')[0]
            name = self.name.get()
            phone = self.phone.get()
            address = self.address.get()
            self.update_client(client_id, name, phone, address)
            self.load_data()
            self.clear_entries()
            self.show_message("Client updated successfully!")

    def delete_selected_client(self):
        """Delete the selected client."""
        selected_item = self.table.selection()
        if selected_item:
            client_id = self.table.item(selected_item, 'values')[0]
            self.delete_client(client_id)
            self.load_data()
            self.clear_entries()
            self.show_message("Client deleted successfully!")

    def on_item_selected(self, event):
        """Handle the selection of a table item."""
        selected_item = self.table.selection()
        if selected_item:
            client_id, name, phone, address = self.table.item(selected_item, 'values')
            self.name.set(name)
            self.phone.set(phone)
            self.address.set(address)

    def clear_entries(self):
        """Clear the input fields."""
        self.name.set("")
        self.phone.set("")
        self.address.set("")

    def next_page(self):
        """Navigate to the next page of clients."""
        if (self.current_page + 1) * self.records_per_page < self.total_records:
            self.current_page += 1
            self.load_data()

    def prev_page(self):
        """Navigate to the previous page of clients."""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_data()

    def search_client(self, event=None):
        """Search for clients based on the input."""
        search_term = self.search_var.get()
        try:
            with self.db.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM clients WHERE name LIKE ?', ('%' + search_term + '%',))
                rows = cursor.fetchall()
                self.table.delete(*self.table.get_children())
                for index, client in enumerate(rows):
                    tag = 'oddrow' if index % 2 == 0 else 'evenrow'
                    self.table.insert("", "end", values=client, tags=(tag,))
                self.total_records = len(rows)
                self.current_page = 0
                self.prev_button['state'] = 'disabled'
                self.next_button['state'] = 'disabled'
                self.page_info_label.config(text=f"Page 1 of 1 - Total Records: {self.total_records}")
        except Exception as e:
            logging.error(f"Failed to search clients: {e}")
            messagebox.showerror("Error", f"Failed to search clients: {e}")