import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db import Database
from dashboard import DashboardTab
from clients import ClientsTab
from products import ProductsTab
from services import ServicesTab
from invoices import InvoicesTab
from income import IncomeTab
from hematology_report import HematReportTab

class Animalium(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera")
        self.title("Animalium - Consultorio Veterinario")
        self.state('zoomed')
        logo_path = os.path.join(os.path.dirname(__file__), 'img', 'logo.ico')
        self.iconbitmap(logo_path)

        # Initialize the database
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error initializing database: {e}")
            self.destroy()  # Close the application if the database fails to initialize


        # Create tabs
        self.tab_control = ttk.Notebook(self)
        self.dashboard_tab = DashboardTab(self.tab_control, self.db)
        self.clients_tab = ClientsTab(self.tab_control, self.db)
        self.products_tab = ProductsTab(self.tab_control, self.db)
        self.services_tab = ServicesTab(self.tab_control, self.db)
        self.invoices_tab = InvoicesTab(self.tab_control, self.db)
        self.income_tab = IncomeTab(self.tab_control, self.db)
        self.ih_tab = HematReportTab(self.tab_control, self.db)

        self.tab_control.add(self.dashboard_tab, text="Dashboard")
        self.tab_control.add(self.clients_tab, text="Clientes")
        self.tab_control.add(self.products_tab, text="Productos")
        self.tab_control.add(self.services_tab, text="Servicios")
        self.tab_control.add(self.invoices_tab, text="Facturas")
        self.tab_control.add(self.income_tab, text="Ingresos")
        self.tab_control.add(self.income_tab, text="Informe Hematológico")

        self.tab_control.pack(expand=1, fill=BOTH)

if __name__ == "__main__":
    app = Animalium()
    app.mainloop()