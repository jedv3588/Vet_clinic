import os
import ttkbootstrap as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class DashboardTab(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        # Load logo and banner images from the project folder
        self.load_images()
        self.create_dashboard_tab()

        # Bind the tab selection event to refresh metrics
        parent.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
    def on_tab_changed(self, event):
        # Refresh metrics when the tab is changed
        self.load_dashboard_metrics()
        self.update_charts()
        
    def update_charts(self):
        # Update the existing charts
        self.create_service_bar_chart(self.bar_frame)
        self.create_service_line_chart(self.line_frame)
        self.create_service_gauge_meter(self.gauge_frame)

        # Update the new charts
        self.create_product_bar_chart(self.product_bar_frame)
        self.create_product_line_chart(self.product_line_frame)
        self.create_product_gauge_meter(self.product_gauge_frame)
        
    def load_images(self):
        # Get the absolute path to the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load logo
        logo_path = os.path.join(project_dir, "img", "logo-slogan.png")
        if os.path.exists(logo_path):
            self.logo_image = Image.open(logo_path).resize((250, 250))  # Resize logo
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        else:
            print(f"Warning: Logo image not found at {logo_path}")
            self.logo_photo = None  # Set to None if image is missing

        # Load banner
        banner_path = os.path.join(project_dir, "img", "banner.png")
        if os.path.exists(banner_path):
            self.banner_image = Image.open(banner_path).resize((800, 250))  # Resize banner
            self.banner_photo = ImageTk.PhotoImage(self.banner_image)
        else:
            print(f"Warning: Banner image not found at {banner_path}")
            self.banner_photo = None  # Set to None if image is missing
            
        # Load right-side image
        right_image_path = os.path.join(project_dir, "img", "female_feethands.png")
        print(f"Absolute right image path: {right_image_path}")
        if os.path.exists(right_image_path):
            self.right_image = Image.open(right_image_path).resize((350, 250))  # Resize right image
            self.right_photo = ImageTk.PhotoImage(self.right_image)
        else:
            print(f"Warning: Right image not found at {right_image_path}")
            self.right_photo = None  # Set to None if image is missing

    def create_dashboard_tab(self):
        # Create a main frame for the dashboard
        self.load_images()
        dashboard_frame = ttk.Frame(self)
        dashboard_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Create a banner frame with a custom color
        banner_frame = ttk.Frame(dashboard_frame, padding=(10, 5), bootstyle="info")
        banner_frame.pack(fill='x')

        # Load the image for the banner
        image_path = os.path.join(os.path.dirname(__file__), 'img', 'banner.png')  # Update with your image path
        banner_image = Image.open(image_path)

        # Resize the image to fit the banner frame
        banner_frame_width = 600  # Set the width of the banner frame
        banner_frame_height = 100  # Set the height of the banner frame
        banner_image = banner_image.resize((banner_frame_width, banner_frame_height), Image.LANCZOS)

        # Create a PhotoImage object
        banner_photo = ImageTk.PhotoImage(banner_image)

        # Add a label to the banner with the image
        banner_label = ttk.Label(banner_frame, image=banner_photo)
        banner_label.image = banner_photo  # Keep a reference to avoid garbage collection
        banner_label.pack(fill='both', expand=True)  # Make the label fill the entire banner frame

        # Create a frame for metrics
        metrics_frame = ttk.Frame(dashboard_frame)
        metrics_frame.pack(padx=10, pady=10, fill='x')  # Use pack instead of grid

        # Create horizontal cards for metrics with updated colors
        self.create_metric_card(metrics_frame, "Total Clients", "0", "success")
        self.create_metric_card(metrics_frame, "Total Products", "0", "info")
        self.create_metric_card(metrics_frame, "Total Services", "0", "warning")
        self.create_metric_card(metrics_frame, "Total Invoices", "0", "danger")

        # Load metrics
        self.load_dashboard_metrics()

        # Create a frame for charts
        charts_frame = ttk.LabelFrame(dashboard_frame, text="Gráficos de comportamientos", padding=(10, 10))
        charts_frame.pack(padx=10, pady=10, fill='both', expand=True)  # Use pack instead of grid

        # Create frames for the first row of charts
        self.gauge_frame = ttk.Frame(charts_frame, borderwidth=1, relief='ridge')
        self.gauge_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.bar_frame = ttk.Frame(charts_frame, borderwidth=1, relief='ridge')
        self.bar_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.line_frame = ttk.Frame(charts_frame, borderwidth=1, relief='ridge')
        self.line_frame.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # Create frames for the second row of charts
        self.product_gauge_frame = ttk.Frame(charts_frame, borderwidth=1, relief='ridge')
        self.product_gauge_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.product_bar_frame = ttk.Frame(charts_frame, borderwidth=1, relief='ridge')
        self.product_bar_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.product_line_frame = ttk.Frame(charts_frame, borderwidth=1, relief='ridge')
        self.product_line_frame.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')
        
        # Configure row and column weights for expansion
        charts_frame.grid_rowconfigure(0, weight=1)
        charts_frame.grid_rowconfigure(1, weight=1)
        charts_frame.grid_columnconfigure(0, weight=1)
        charts_frame.grid_columnconfigure(1, weight=1)
        charts_frame.grid_columnconfigure(2, weight=1)

        # Initial creation of charts
        self.create_service_gauge_meter(self.gauge_frame)
        self.create_service_bar_chart(self.bar_frame)
        self.create_service_line_chart(self.line_frame)

        # Initial creation of new product charts
        self.create_product_gauge_meter(self.product_gauge_frame)
        self.create_product_bar_chart(self.product_bar_frame)
        self.create_product_line_chart(self.product_line_frame)

    def create_metric_card(self, parent, title, value, color):
        card_frame = ttk.Frame(parent, padding=(10, 5), bootstyle=color)
        card_frame.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        card_frame['borderwidth'] = 2
        card_frame['relief'] = 'groove'

        title_label = ttk.Label(card_frame, text=title, font=("Arial", 10, "bold"))
        title_label.pack(side='top', pady=(0, 5))

        value_label = ttk.Label(card_frame, text=value, font=("Arial", 14, "bold"))
        value_label.pack(side='top')

        # Store the label for later updates
        if title == "Total Clients":
            self.total_clients_label = value_label
        elif title == "Total Products":
            self.total_products_label = value_label
        elif title == "Total Services":
            self.total_services_label = value_label
        elif title == "Total Invoices":
            self.total_invoices_label = value_label

    def load_dashboard_metrics(self):
        total_clients = self.db.fetch_all("SELECT COUNT(*) FROM clients")[0][0]
        self.total_clients_label.config(text=str(total_clients))

        total_products = self.db.fetch_all("SELECT COUNT(*) FROM products")[0][0]
        self.total_products_label.config(text=str(total_products))

        total_services = self.db.fetch_all("SELECT COUNT(*) FROM services")[0][0]
        self.total_services_label.config(text=str(total_services))

        total_invoices = self.db.fetch_all("SELECT COUNT(*) FROM invoices")[0][0]
        self.total_invoices_label.config(text=str(total_invoices))
    
    def create_service_bar_chart(self, parent):
        categories = ['Clients', 'Products', 'Services', 'Invoices']
        values = [int(self.total_clients_label.cget("text")),
                  int(self.total_products_label.cget("text")),
                  int(self.total_services_label.cget("text")),
                  int(self.total_invoices_label.cget("text"))]
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(categories, values, color='teal')
        ax.set_title('Service Income Distribution', fontsize=10, fontweight='bold')
        ax.set_ylabel('Count', fontsize=8)
        ax.set_xlabel('Categories', fontsize=8)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def create_service_line_chart(self, parent):
        # Define the x-axis labels (months)
        x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Example monthly data for each category (replace with actual data)
        total_clients_monthly = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        total_products_monthly = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115]
        total_services_monthly = [2, 12, 22, 32, 42, 52, 62, 72, 82, 92, 102, 112]
        total_invoices_monthly = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111]

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(x, total_clients_monthly, marker='o', color='darkgreen', linewidth=2, label='Clients')
        ax.plot(x, total_products_monthly, marker='o', color='steelblue', linewidth=2, label='Products')
        ax.plot(x, total_services_monthly, marker='o', color='gold', linewidth=2, label=' Services')
        ax.plot(x, total_invoices_monthly, marker='o', color='crimson', linewidth=2, label='Invoices')

        ax.set_title('Income Over Time', fontsize=10, fontweight='bold')
        ax.set_ylabel('Count', fontsize=8)
        ax.set_xlabel('Months', fontsize=8)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        ax.legend()  # Add a legend to differentiate the lines
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def create_service_gauge_meter(self, parent):
        # Get the total number of clients
        total_clients = int(self.total_clients_label.cget("text"))
        max_clients = 100  # Define the maximum capacity for the meter

        # Create the Meter widget and store it as an instance variable
        self.meter = ttk.Meter(
            master=parent,
            metersize=150,
            metertype='full',
            amounttotal=max_clients,
            amountused=80, #total_clients,  # Use the total clients as the amount used
            subtext="Client Capacity",  # Subtext for the meter
            textright='%',
            bootstyle="info", 
            stripethickness=10,
            interactive=True,  # Set to True if you want it to be interactive
        )
        self.meter.pack(pady=10, padx=10, fill='both', expand=True)

    def create_product_bar_chart(self, parent):
        categories = ['Product A', 'Product B', 'Product C', 'Product D']
        values = [int(self.total_products_label.cget("text")) // 4] * 4  # Example values
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(categories, values, color='forestgreen')
        ax.set_title('Product Distribution', fontsize=10, fontweight='bold')
        ax.set_ylabel('Count', fontsize=8)
        ax.set_xlabel('Products', fontsize=8)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def create_product_line_chart(self, parent):
        # Sample data for the product line chart
        x = ['Q1', 'Q2', 'Q3', 'Q4']
        y = [int(self.total_products_label.cget("text")) // 4] * 4  # Example values
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(x, y, marker='o', color='purple', linewidth=2)
        ax.set_title('Product Sales Over Quarters', fontsize=10, fontweight='bold')
        ax.set_ylabel('Count', fontsize=8)
        ax.set_xlabel('Quarters', fontsize=8)
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def create_product_gauge_meter(self, parent):
        # Get the total number of products
        total_products = int(self.total_products_label.cget("text"))
        max_products = 200  # Define the maximum capacity for the meter

        # Create the Meter widget for products
        self.product_meter = ttk.Meter(
            master=parent,
            metersize=150,
            metertype='full',
            amounttotal=max_products,
            amountused=60, #total_products,  # Use the total products as the amount used
            subtext="Product Capacity",  # Subtext for the meter
            textright='%',
            bootstyle="success", 
            stripethickness=10,
            interactive=True,  # Set to True if you want it to be interactive
        )
        self.product_meter.pack(pady=10, padx=10, fill='both', expand=True)