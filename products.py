import ttkbootstrap as ttk
from tkinter import messagebox

class ProductsTab(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.create_products_tab()

    def create_products_tab(self):
        product_form_frame = ttk.LabelFrame(self, text="Product Information")
        product_form_frame.grid(row= 0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(product_form_frame, text="Product Name:").grid(row=0, column=0)
        self.product_name_entry = ttk.Entry(product_form_frame)
        self.product_name_entry.grid(row=0, column=1)

        ttk.Label(product_form_frame, text="Price:").grid(row=1, column=0)
        self.product_price_entry = ttk.Entry(product_form_frame)
        self.product_price_entry.grid(row=1, column=1)

        self.add_product_button = ttk.Button(product_form_frame, text="Add Product", command=self.add_product)
        self.add_product_button.grid(row=2, column=0, columnspan=2)

        product_table_frame = ttk.LabelFrame(self, text="Product List")
        product_table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.product_listbox = ttk.Treeview(product_table_frame, columns=("Name", "Price"), show="headings")
        self.product_listbox.grid(row=0, column=0)
        self.product_listbox.heading("Name", text="Name")
        self.product_listbox.heading("Price", text="Price")
        self.load_products()

        self.edit_product_button = ttk.Button(product_table_frame, text="Edit Product", command=self.edit_product)
        self.edit_product_button.grid(row=1, column=0, sticky="ew")

        self.delete_product_button = ttk.Button(product_table_frame, text="Delete Product", command=self.delete_product)
        self.delete_product_button.grid(row=2, column=0, sticky="ew")

    def load_products(self):
        for row in self.product_listbox.get_children():
            self.product_listbox.delete(row)
        products = self.db.fetch_all("SELECT * FROM products")
        for product in products:
            self.product_listbox.insert("", "end", values=(product[1], product[2]))

    def add_product(self):
        name = self.product_name_entry.get()
        price = self.product_price_entry.get()
        if not name or not price:
            messagebox.showerror("Error", "Product name and price are required.")
            return
        self.db.execute_query("INSERT INTO products (name, price) VALUES (?, ?)", (name, float(price)))
        self.product_name_entry.delete(0, "end")
        self.product_price_entry.delete(0, "end")
        self.load_products()

    def edit_product(self):
        selected_item = self.product_listbox.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a product to edit.")
            return
        product_data = self.product_listbox.item(selected_item)['values']
        self.product_name_entry.delete(0, "end")
        self.product_name_entry.insert(0, product_data[0])
        self.product_price_entry.delete(0, "end")
        self.product_price_entry.insert(0, product_data[1])
        self.delete_product()  # Remove the old entry after editing

    def delete_product(self):
        selected_item = self.product_listbox.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select a product to delete.")
            return
        product_data = self.product_listbox.item(selected_item)['values']
        self.db.execute_query("DELETE FROM products WHERE name=? AND price=?", (product_data[0], product_data[1]))
        self.load_products()