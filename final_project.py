"""
This program is created by Thatoe Nyi
ID-6708351, Computer Science,
Year 1, Semester 2
DIT102 - Programming Fundamentals
This program is a Motorcycle Management System that allows users to manage motorcycle inventory and customer orders.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os
from PIL import Image, ImageTk
import random
from datetime import datetime

# Define data models using OOP
class Motorcycle:
    def __init__(self, id, brand, model, year, color, price, stock, image_path=""):
        self.id = id
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.stock = stock
        self.image_path = image_path

    def to_list(self):
        return [self.id, self.brand, self.model, self.year, 
                self.color, self.price, self.stock, self.image_path]

    @classmethod
    def from_list(cls, data):
        return cls(data[0], data[1], data[2], data[3], 
                  data[4], data[5], data[6], data[7] if len(data) > 7 else "")

class Order:
    def __init__(self, order_id, motorcycle_id, customer_name, phone, address, date):
        self.order_id = order_id
        self.motorcycle_id = motorcycle_id
        self.customer_name = customer_name
        self.phone = phone
        self.address = address
        self.date = date

    def to_list(self):
        return [self.order_id, self.motorcycle_id, self.customer_name, 
                self.phone, self.address, self.date]

# Data Management Classes
class InventoryManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ensure_file_exists()
        
    def ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            # Create inventory file with sample data
            with open(self.file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Brand', 'Model', 'Year', 'Color', 'Price', 'Stock', 'ImagePath'])
                
                # Generate 20 sample motorcycles
                brands = ['Honda', 'Yamaha', 'Kawasaki', 'Suzuki', 'Ducati', 'Harley-Davidson', 'BMW', 'KTM']
                models = ['Sport', 'Cruiser', 'Touring', 'Adventure', 'Naked', 'Scooter', 'Chopper', 'Dirt']
                colors = ['Red', 'Black', 'Blue', 'White', 'Silver', 'Green', 'Yellow', 'Orange']
                
                for i in range(1, 21):
                    brand = random.choice(brands)
                    model = f"{brand} {random.choice(models)} {random.randint(100, 999)}"
                    year = random.randint(2018, 2023)
                    color = random.choice(colors)
                    price = random.randint(5000, 30000)
                    stock = random.randint(1, 10)
                    
                    writer.writerow([i, brand, model, year, color, price, stock, ""])
    
    def get_all_motorcycles(self):
        motorcycles = []
        with open(self.file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                motorcycles.append(Motorcycle.from_list(row))
        return motorcycles
    
    def add_motorcycle(self, motorcycle):
        motorcycles = self.get_all_motorcycles()
        
        # Find the highest ID and increment by 1
        max_id = 0
        for m in motorcycles:
            if int(m.id) > max_id:
                max_id = int(m.id)
        
        motorcycle.id = str(max_id + 1)
        motorcycles.append(motorcycle)
        self._save_motorcycles(motorcycles)
        
    def update_motorcycle(self, motorcycle):
        motorcycles = self.get_all_motorcycles()
        for i, m in enumerate(motorcycles):
            if m.id == motorcycle.id:
                motorcycles[i] = motorcycle
                break
        self._save_motorcycles(motorcycles)
    
    def delete_motorcycle(self, motorcycle_id):
        motorcycles = self.get_all_motorcycles()
        motorcycles = [m for m in motorcycles if m.id != motorcycle_id]
        self._save_motorcycles(motorcycles)
    
    def get_motorcycle_by_id(self, motorcycle_id):
        for motorcycle in self.get_all_motorcycles():
            if motorcycle.id == motorcycle_id:
                return motorcycle
        return None
    
    def _save_motorcycles(self, motorcycles):
        with open(self.file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Brand', 'Model', 'Year', 'Color', 'Price', 'Stock', 'ImagePath'])
            for motorcycle in motorcycles:
                writer.writerow(motorcycle.to_list())

class OrderManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['OrderID', 'MotorcycleID', 'CustomerName', 'Phone', 'Address', 'Date'])
    
    def place_order(self, motorcycle_id, customer_name, phone, address):
        orders = self.get_all_orders()
        
        # Generate order ID
        order_id = f"ORD-{len(orders) + 1}"
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create new order
        new_order = Order(order_id, motorcycle_id, customer_name, phone, address, date)
        
        # Add to list and save
        with open(self.file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(new_order.to_list())
        
        # Update inventory (decrease stock)
        inventory_manager = InventoryManager("inventory.csv")
        motorcycle = inventory_manager.get_motorcycle_by_id(motorcycle_id)
        if motorcycle:
            motorcycle.stock = str(int(motorcycle.stock) - 1)
            inventory_manager.update_motorcycle(motorcycle)
    
    def get_all_orders(self):
        orders = []
        if not os.path.exists(self.file_path):
            return orders
            
        with open(self.file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 6:  # Ensure row has enough data
                    order = Order(row[0], row[1], row[2], row[3], row[4], row[5])
                    orders.append(order)
        return orders

# Authentication System
class AuthManager:
    def __init__(self):
        self.admin_username = "Thatoe"
        self.admin_password = "dit102"
    
    def validate_admin(self, username, password):
        return username == self.admin_username and password == self.admin_password

# GUI Classes
class SplashScreen:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        
        # Set the window size to be smaller (reduced by 40%)
        original_width, original_height = 500, 600
        self.parent.geometry(f"{original_width}x{original_height}")
        
        self.setup_ui()
        
    def setup_ui(self):
        self.frame = tk.Frame(self.parent, bg="black")
        self.frame.pack(fill="both", expand=True)
        
        # Try to load splash image
        try:
            img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cycle.png")
            img = Image.open(img_path)
            
            # Get window dimensions for proper sizing
            width, height = 500, 600  # Match the window size
            img = img.resize((width, height), Image.LANCZOS)
            
            self.splash_img = ImageTk.PhotoImage(img)
            
            # Create canvas to overlay text on image
            self.canvas = tk.Canvas(self.frame, width=width, height=height, bd=0, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)
            
            # Add image to canvas
            self.canvas.create_image(width//2, height//2, image=self.splash_img)
            
            # Add text overlay - adjusted for the smaller width
            self.canvas.create_text(
                width//2, height//2 + 150, 
                text="Press space to enter", 
                fill="white", font=("Arial", 24, "bold"),
                tags="text"
            )
            
            # Create blinking effect for text
            self.blink_text()
            
        except Exception as e:
            print(f"Failed to load splash image: {e}")
            # Fallback if image fails to load
            tk.Label(self.frame, text="Motorcycle Management System", 
                    font=("Arial", 24, "bold"), fg="white", bg="black").pack(pady=100)
            tk.Label(self.frame, text="Press space to enter", 
                    font=("Arial", 16), fg="white", bg="black").pack()
        
        # Bind space key to proceed
        self.parent.bind("<space>", self.on_space)
    
    def blink_text(self):
        """Create a blinking effect for the 'Press space to enter' text"""
        current_state = self.canvas.itemcget("text", "state")
        next_state = "hidden" if current_state == "normal" else "normal"
        self.canvas.itemconfigure("text", state=next_state)
        self.parent.after(500, self.blink_text)  # Toggle every 500ms
    
    def on_space(self, event):
        # Unbind space key to prevent multiple triggers
        self.parent.unbind("<space>")
        # Remove the splash screen and proceed to main app
        self.frame.destroy()
        self.callback()
    
    def destroy(self):
        # Clean up
        if hasattr(self, 'frame'):
            self.frame.destroy()


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Motorcycle Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        # Show splash screen first
        self.splash = SplashScreen(self.root, self.initialize_main_app)
    
    def initialize_main_app(self):
        # Load logo and set as icon
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rsu_logo.png")
            logo = Image.open(logo_path)
            # Create PhotoImage for window icon
            logo_icon = ImageTk.PhotoImage(logo)
            # Set window icon
            self.root.iconphoto(True, logo_icon)
            # Store the reference to prevent garbage collection
            self.logo_icon = logo_icon
        except Exception as e:
            print(f"Failed to load logo: {e}")
        
        # Create frames for different "pages"
        self.login_frame = None
        self.admin_frame = None
        self.customer_frame = None
        
        # Initialize auth manager
        self.auth_manager = AuthManager()
        
        # Show login frame initially
        self.show_login_page()
        
    def show_login_page(self):
        # Hide other frames if they exist
        if self.admin_frame:
            self.admin_frame.pack_forget()
        
        if self.customer_frame:
            self.customer_frame.pack_forget()
        
        # Create login frame if it doesn't exist
        if not self.login_frame:
            self.login_frame = LoginFrame(self.root, self.switch_to_admin, self.switch_to_customer)
        
        # Show login frame
        self.login_frame.pack(fill="both", expand=True)
        # Increased height to ensure all components are visible
        self.root.geometry("400x500")
        self.root.title("Motorcycle Sales - Login")
    
    def switch_to_admin(self, username, password):
        if self.auth_manager.validate_admin(username, password):
            # Hide login frame
            self.login_frame.pack_forget()
            
            # Clear login fields for security
            self.login_frame.clear_fields()
            
            # Create admin frame if it doesn't exist
            if not self.admin_frame:
                self.admin_frame = AdminFrame(self.root, self.show_login_page)
            
            # Show admin frame
            self.admin_frame.pack(fill="both", expand=True)
            self.root.geometry("900x600")
            self.root.title("Motorcycle Management - Admin")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def switch_to_customer(self):
        # Hide login frame
        self.login_frame.pack_forget()
        
        # Create customer frame if it doesn't exist
        if not self.customer_frame:
            self.customer_frame = CustomerFrame(self.root, self.show_login_page)
        
        # Show customer frame
        self.customer_frame.pack(fill="both", expand=True)
        self.root.geometry("900x600")
        self.root.title("Motorcycle Shop - Customer View")

class LoginFrame(tk.Frame):
    def __init__(self, parent, admin_callback, guest_callback):
        super().__init__(parent, bg="#f0f0f0", padx=20, pady=20)
        
        self.admin_callback = admin_callback
        self.guest_callback = guest_callback
        
        # Try to load and display logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rsu_logo.png")
            logo = Image.open(logo_path)
            # Resize for display
            logo = logo.resize((150, 150), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(logo)
            
            # Create logo label
            logo_label = tk.Label(self, image=self.logo_image, bg="#f0f0f0")
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Failed to load logo in login frame: {e}")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self, text="Motorcycle Management System", 
                              font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=15)
        
        # Login frame
        login_frame = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10,
                              highlightbackground="#cccccc", highlightthickness=1)
        login_frame.pack(fill="x", padx=20)
        
        # Username
        tk.Label(login_frame, text="Username:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(login_frame, width=25)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Password
        tk.Label(login_frame, text="Password:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(login_frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Login button
        login_button = tk.Button(login_frame, text="Login as Admin", 
                               command=self.login, bg="#4CAF50", fg="white", 
                               width=15, pady=5)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Guest login
        guest_button = tk.Button(self, text="Continue as Guest", 
                               command=self.guest_login, bg="#2196F3", fg="white", 
                               width=15, pady=5)
        guest_button.pack(pady=15)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.admin_callback(username, password)
    
    def guest_login(self):
        self.guest_callback()
    
    def clear_fields(self):
        """Clear the username and password fields for security"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

class AdminFrame(tk.Frame):
    def __init__(self, parent, logout_callback):
        super().__init__(parent, bg="#f0f0f0")
        
        self.logout_callback = logout_callback
        self.inventory_manager = InventoryManager("inventory.csv")
        self.order_manager = OrderManager("orders.csv")
        
        # Try to load logo for admin panel
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rsu_logo.png")
            logo = Image.open(logo_path)
            # Resize for display as a small logo
            logo = logo.resize((50, 50), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(logo)
        except Exception as e:
            print(f"Failed to load logo in admin frame: {e}")
            self.logo_image = None
            
        self.setup_ui()
        self.load_motorcycles()
    
    def setup_ui(self):
        # Create main frame with padding
        main_frame = tk.Frame(self, bg="#f0f0f0", padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)
        
        # Title and logout frame (horizontal layout)
        title_frame = tk.Frame(main_frame, bg="#f0f0f0")
        title_frame.pack(fill="x", pady=(0, 15))
        
        # Logo if available
        if hasattr(self, 'logo_image') and self.logo_image:
            logo_label = tk.Label(title_frame, image=self.logo_image, bg="#f0f0f0")
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Title
        title_label = tk.Label(title_frame, text="Motorcycle Inventory Management", 
                             font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(side=tk.LEFT, pady=(0, 15))
        
        # Logout button (right aligned)
        logout_btn = tk.Button(title_frame, text="Logout", command=self.logout,
                            bg="#f44336", fg="white", padx=10, pady=5)
        logout_btn.pack(side=tk.RIGHT, padx=10)
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = tk.Button(search_frame, text="Search", command=self.search_motorcycles,
                                bg="#2196F3", fg="white", padx=10)
        search_button.pack(side=tk.LEFT, padx=5)
        
        clear_search_button = tk.Button(search_frame, text="Clear Search", command=self.load_motorcycles,
                                     bg="#9E9E9E", fg="white", padx=10)
        clear_search_button.pack(side=tk.LEFT, padx=5)
        
        # Create frames
        control_frame = tk.Frame(main_frame, bg="#f0f0f0")
        control_frame.pack(fill="x", pady=10)
        
        # Buttons for CRUD
        add_btn = tk.Button(control_frame, text="Add Motorcycle", command=self.add_motorcycle,
                          bg="#4CAF50", fg="white", padx=10, pady=5)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = tk.Button(control_frame, text="Edit Selected", command=self.edit_motorcycle,
                           bg="#2196F3", fg="white", padx=10, pady=5)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(control_frame, text="Delete Selected", command=self.delete_motorcycle,
                             bg="#f44336", fg="white", padx=10, pady=5)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        view_orders_btn = tk.Button(control_frame, text="View Orders", command=self.view_orders,
                                  bg="#FF9800", fg="white", padx=10, pady=5)
        view_orders_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(control_frame, text="Refresh", command=self.load_motorcycles,
                              bg="#9E9E9E", fg="white", padx=10, pady=5)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Table for motorcycles
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Treeview
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Brand", "Model", "Year", "Color", "Price", "Stock"), 
                               show="headings", yscrollcommand=scrollbar.set)
        
        # Configure column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Brand", text="Brand")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Color", text="Color")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")
        
        # Configure column widths
        self.tree.column("ID", width=40)
        self.tree.column("Brand", width=120)
        self.tree.column("Model", width=180)
        self.tree.column("Year", width=70)
        self.tree.column("Color", width=80)
        self.tree.column("Price", width=100)
        self.tree.column("Stock", width=60)
        
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
    
    def logout(self):
        # Confirm logout
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.logout_callback()
    
    # ...existing methods for load_motorcycles, search_motorcycles, add_motorcycle, etc...

    def load_motorcycles(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load data
        motorcycles = self.inventory_manager.get_all_motorcycles()
        for motorcycle in motorcycles:
            self.tree.insert("", "end", values=(motorcycle.id, motorcycle.brand, motorcycle.model, 
                                              motorcycle.year, motorcycle.color, 
                                              f"${motorcycle.price}", motorcycle.stock))
    
    def add_motorcycle(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Motorcycle")
        add_window.geometry("400x350")
        add_window.configure(bg="#f0f0f0")
        add_window.grab_set()  # Modal window
        
        frame = tk.Frame(add_window, padx=20, pady=20, bg="#f0f0f0")
        frame.pack(fill="both", expand=True)
        
        # Input fields
        tk.Label(frame, text="Brand:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        brand_entry = tk.Entry(frame, width=30)
        brand_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Model:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
        model_entry = tk.Entry(frame, width=30)
        model_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Year:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
        year_entry = tk.Entry(frame, width=30)
        year_entry.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Color:", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
        color_entry = tk.Entry(frame, width=30)
        color_entry.grid(row=3, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Price ($):", bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=5)
        price_entry = tk.Entry(frame, width=30)
        price_entry.grid(row=4, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Stock:", bg="#f0f0f0").grid(row=5, column=0, sticky="w", pady=5)
        stock_entry = tk.Entry(frame, width=30)
        stock_entry.grid(row=5, column=1, pady=5, padx=10)
        
        def save_motorcycle():
            try:
                brand = brand_entry.get().strip()
                model = model_entry.get().strip()
                year = year_entry.get().strip()
                color = color_entry.get().strip()
                price = price_entry.get().strip()
                stock = stock_entry.get().strip()
                
                # Validation
                if not (brand and model and year and color and price and stock):
                    messagebox.showerror("Validation Error", "All fields are required")
                    return
                
                if not year.isdigit() or not price.isdigit() or not stock.isdigit():
                    messagebox.showerror("Validation Error", "Year, price and stock must be numbers")
                    return
                
                # Create motorcycle object
                motorcycle = Motorcycle("", brand, model, year, color, price, stock)
                self.inventory_manager.add_motorcycle(motorcycle)
                
                messagebox.showinfo("Success", "Motorcycle added successfully!")
                add_window.destroy()
                self.load_motorcycles()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        
        # Save button
        save_button = tk.Button(frame, text="Save", command=save_motorcycle,
                              bg="#4CAF50", fg="white", width=10, pady=5)
        save_button.grid(row=6, column=0, columnspan=2, pady=15)
    
    def edit_motorcycle(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a motorcycle to edit")
            return
        
        # Get selected item
        item = self.tree.item(selection[0])
        motorcycle_id = item['values'][0]
        motorcycle = self.inventory_manager.get_motorcycle_by_id(str(motorcycle_id))
        
        if not motorcycle:
            messagebox.showerror("Error", "Motorcycle not found")
            return
        
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Motorcycle")
        edit_window.geometry("400x350")
        edit_window.configure(bg="#f0f0f0")
        edit_window.grab_set()  # Modal window
        
        frame = tk.Frame(edit_window, padx=20, pady=20, bg="#f0f0f0")
        frame.pack(fill="both", expand=True)
        
        # Input fields
        tk.Label(frame, text="Brand:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        brand_entry = tk.Entry(frame, width=30)
        brand_entry.insert(0, motorcycle.brand)
        brand_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Model:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
        model_entry = tk.Entry(frame, width=30)
        model_entry.insert(0, motorcycle.model)
        model_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Year:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
        year_entry = tk.Entry(frame, width=30)
        year_entry.insert(0, motorcycle.year)
        year_entry.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Color:", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
        color_entry = tk.Entry(frame, width=30)
        color_entry.insert(0, motorcycle.color)
        color_entry.grid(row=3, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Price ($):", bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=5)
        price_entry = tk.Entry(frame, width=30)
        price_entry.insert(0, motorcycle.price)
        price_entry.grid(row=4, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Stock:", bg="#f0f0f0").grid(row=5, column=0, sticky="w", pady=5)
        stock_entry = tk.Entry(frame, width=30)
        stock_entry.insert(0, motorcycle.stock)
        stock_entry.grid(row=5, column=1, pady=5, padx=10)
        
        def save_changes():
            try:
                brand = brand_entry.get().strip()
                model = model_entry.get().strip()
                year = year_entry.get().strip()
                color = color_entry.get().strip()
                price = price_entry.get().strip()
                stock = stock_entry.get().strip()
                
                # Validation
                if not (brand and model and year and color and price and stock):
                    messagebox.showerror("Validation Error", "All fields are required")
                    return
                
                if not year.isdigit() or not price.isdigit() or not stock.isdigit():
                    messagebox.showerror("Validation Error", "Year, price and stock must be numbers")
                    return
                
                # Update motorcycle object
                motorcycle.brand = brand
                motorcycle.model = model
                motorcycle.year = year
                motorcycle.color = color
                motorcycle.price = price
                motorcycle.stock = stock
                
                self.inventory_manager.update_motorcycle(motorcycle)
                
                messagebox.showinfo("Success", "Motorcycle updated successfully!")
                edit_window.destroy()
                self.load_motorcycles()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        
        # Save button
        save_button = tk.Button(frame, text="Save Changes", command=save_changes,
                              bg="#2196F3", fg="white", width=15, pady=5)
        save_button.grid(row=6, column=0, columnspan=2, pady=15)
    
    def delete_motorcycle(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a motorcycle to delete")
            return
        
        # Get selected item
        item = self.tree.item(selection[0])
        motorcycle_id = item['values'][0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete motorcycle ID: {motorcycle_id}?")
        
        if confirm:
            try:
                self.inventory_manager.delete_motorcycle(str(motorcycle_id))
                messagebox.showinfo("Success", "Motorcycle deleted successfully!")
                self.load_motorcycles()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
    def search_motorcycles(self):
        search_term = self.search_entry.get().lower()
        if not search_term:
            return
            
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search in motorcycles
        motorcycles = self.inventory_manager.get_all_motorcycles()
        filtered_motorcycles = []
        
        for motorcycle in motorcycles:
            if (search_term in motorcycle.brand.lower() or
                search_term in motorcycle.model.lower() or
                search_term in motorcycle.year.lower() or
                search_term in motorcycle.color.lower() or
                search_term in motorcycle.price.lower() or
                search_term in motorcycle.stock.lower()):
                filtered_motorcycles.append(motorcycle)
        
        # Display filtered results
        for motorcycle in filtered_motorcycles:
            self.tree.insert("", "end", values=(motorcycle.id, motorcycle.brand, motorcycle.model, 
                                              motorcycle.year, motorcycle.color, 
                                              f"${motorcycle.price}", motorcycle.stock))
                                              
    def view_orders(self):
        orders_window = tk.Toplevel(self)
        orders_window.title("Customer Orders")
        orders_window.geometry("900x500")
        orders_window.configure(bg="#f0f0f0")
        orders_window.grab_set()  # Modal window
        
        # Main frame
        main_frame = tk.Frame(orders_window, bg="#f0f0f0", padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Customer Orders", 
                             font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=(0, 15))
        
        # Search frame for orders
        search_frame = tk.Frame(main_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="Search Orders:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        order_search_entry = tk.Entry(search_frame, width=30)
        order_search_entry.pack(side=tk.LEFT, padx=5)
        
        def search_orders():
            search_term = order_search_entry.get().lower()
            if not search_term:
                load_orders()
                return
                
            # Clear existing data
            for item in order_tree.get_children():
                order_tree.delete(item)
            
            # Get all orders
            orders = self.order_manager.get_all_orders()
            
            # Filter orders
            for order in orders:
                motorcycle = self.inventory_manager.get_motorcycle_by_id(order.motorcycle_id)
                if motorcycle:
                    motorcycle_info = f"{motorcycle.brand} {motorcycle.model}"
                else:
                    motorcycle_info = "Unknown Motorcycle"
                    
                # Search in all fields
                if (search_term in order.order_id.lower() or
                    search_term in motorcycle_info.lower() or
                    search_term in order.customer_name.lower() or
                    search_term in order.phone.lower() or
                    search_term in order.address.lower() or
                    search_term in order.date.lower()):
                    order_tree.insert("", "end", values=(
                        order.order_id, motorcycle_info, order.customer_name,
                        order.phone, order.address, order.date
                    ))
        
        search_btn = tk.Button(search_frame, text="Search", command=search_orders,
                             bg="#2196F3", fg="white", padx=10)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(search_frame, text="Clear Search", command=lambda: load_orders(),
                            bg="#9E9E9E", fg="white", padx=10)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Order table frame
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Treeview for orders
        order_tree = ttk.Treeview(
            table_frame, 
            columns=("OrderID", "Motorcycle", "CustomerName", "Phone", "Address", "Date"),
            show="headings", 
            yscrollcommand=scrollbar.set
        )
        
        # Configure column headings
        order_tree.heading("OrderID", text="Order ID")
        order_tree.heading("Motorcycle", text="Motorcycle")
        order_tree.heading("CustomerName", text="Customer Name")
        order_tree.heading("Phone", text="Phone")
        order_tree.heading("Address", text="Address")
        order_tree.heading("Date", text="Date")
        
        # Configure column widths
        order_tree.column("OrderID", width=80)
        order_tree.column("Motorcycle", width=150)
        order_tree.column("CustomerName", width=120)
        order_tree.column("Phone", width=100)
        order_tree.column("Address", width=200)
        order_tree.column("Date", width=150)
        
        order_tree.pack(fill="both", expand=True)
        scrollbar.config(command=order_tree.yview)
        
        # Function to load orders
        def load_orders():
            # Clear existing data
            for item in order_tree.get_children():
                order_tree.delete(item)
            
            # Get all orders
            orders = self.order_manager.get_all_orders()
            
            # Display orders
            for order in orders:
                motorcycle = self.inventory_manager.get_motorcycle_by_id(order.motorcycle_id)
                if motorcycle:
                    motorcycle_info = f"{motorcycle.brand} {motorcycle.model}"
                else:
                    motorcycle_info = "Unknown Motorcycle"
                    
                order_tree.insert("", "end", values=(
                    order.order_id, motorcycle_info, order.customer_name,
                    order.phone, order.address, order.date
                ))
        
        # Load orders
        load_orders()
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", 
                            command=orders_window.destroy,
                            bg="#f44336", fg="white", padx=20, pady=5)
        close_btn.pack(pady=10)

class CustomerFrame(tk.Frame):
    def __init__(self, parent, back_callback):
        super().__init__(parent, bg="#f0f0f0")
        
        self.back_callback = back_callback
        self.inventory_manager = InventoryManager("inventory.csv")
        self.order_manager = OrderManager("orders.csv")
        self.motorcycles = []
        
        # Try to set background image
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rsu_logo.png")
            logo = Image.open(logo_path)
            # Create a semi-transparent watermark image
            logo = logo.resize((200, 200), Image.LANCZOS)
            logo = logo.convert("RGBA")
            # Make it semi-transparent
            data = logo.getdata()
            new_data = []
            for item in data:
                # Change all white (also shades of whites) to transparent
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append((item[0], item[1], item[2], 100))  # 100 = semi-transparent
            logo.putdata(new_data)
            self.bg_image = ImageTk.PhotoImage(logo)
        except Exception as e:
            print(f"Failed to load background image: {e}")
            self.bg_image = None
            
        self.setup_ui()
        self.load_motorcycles()
    
    def setup_ui(self):
        # Main container
        self.main_frame = tk.Frame(self, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header frame with title and back button
        header_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        header_frame.pack(fill="x", pady=10)
        
        # If we have a background image, create a container for it
        if hasattr(self, 'bg_image') and self.bg_image:
            # Create a label with the background image in the main frame
            bg_label = tk.Label(self.main_frame, image=self.bg_image, bg="#f0f0f0")
            bg_label.place(relx=0.5, rely=0.5, anchor='center')  # Center the image
        
        # Title with logo if available
        if hasattr(self, 'bg_image') and self.bg_image:
            logo_small = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rsu_logo.png"))
            logo_small = logo_small.resize((40, 40), Image.LANCZOS)
            self.logo_small = ImageTk.PhotoImage(logo_small)
            logo_label = tk.Label(header_frame, image=self.logo_small, bg="#f0f0f0")
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Title
        title_label = tk.Label(header_frame, text="Motorcycle Shop", 
                             font=("Arial", 20, "bold"), bg="#f0f0f0")
        title_label.pack(side=tk.LEFT, pady=10)
        
        # Back button
        back_button = tk.Button(header_frame, text="Back to Login", 
                              command=self.back_to_login,
                              bg="#f44336", fg="white", padx=10, pady=5)
        back_button.pack(side=tk.RIGHT, padx=10)
        
        # Search frame
        search_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="Search:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = tk.Button(search_frame, text="Search", command=self.search_motorcycles,
                                bg="#2196F3", fg="white", padx=10)
        search_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(search_frame, text="Clear Search", command=self.load_motorcycles,
                               bg="#9E9E9E", fg="white", padx=10)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Motorcycle list
        list_frame = tk.Frame(self.main_frame, bg="white")
        list_frame.pack(fill="both", expand=True, pady=10)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(list_frame, bg="white")
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        
        self.motorcycle_frame = tk.Frame(self.canvas, bg="white")
        self.motorcycle_frame.bind("<Configure>", 
                                 lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.motorcycle_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def back_to_login(self):
        if messagebox.askyesno("Return to Login", "Are you sure you want to return to the login page?"):
            self.back_callback()
    
    # ...existing methods for load_motorcycles, search_motorcycles, etc...

    def load_motorcycles(self):
        # Clear existing items
        for widget in self.motorcycle_frame.winfo_children():
            widget.destroy()
        
        # Get motorcycles
        self.motorcycles = self.inventory_manager.get_all_motorcycles()
        
        # Display each motorcycle
        for i, motorcycle in enumerate(self.motorcycles):
            if int(motorcycle.stock) > 0:  # Only show in-stock motorcycles
                self.create_motorcycle_card(motorcycle, i)
    
    def create_motorcycle_card(self, motorcycle, index):
        # Create a card-like frame for each motorcycle
        card_frame = tk.Frame(self.motorcycle_frame, bd=1, relief="solid", bg="white")
        card_frame.grid(row=index // 2, column=index % 2, padx=10, pady=10, sticky="nsew")
        
        # Motorcycle info
        info_frame = tk.Frame(card_frame, bg="white", padx=10, pady=10)
        info_frame.pack(fill="both", expand=True)
        
        # Title (Brand & Model)
        title_label = tk.Label(info_frame, text=f"{motorcycle.brand} {motorcycle.model}", 
                             font=("Arial", 12, "bold"), bg="white")
        title_label.pack(anchor="w")
        
        # Details
        details = f"Year: {motorcycle.year}\nColor: {motorcycle.color}\nPrice: ${motorcycle.price}\nStock: {motorcycle.stock}"
        details_label = tk.Label(info_frame, text=details, justify="left", bg="white")
        details_label.pack(anchor="w", pady=5)
        
        # Order button
        order_button = tk.Button(info_frame, text="Order Now", bg="#4CAF50", fg="white",
                               command=lambda m=motorcycle: self.order_motorcycle(m))
        order_button.pack(anchor="w", pady=5)
    
    def search_motorcycles(self):
        search_term = self.search_entry.get().lower()
        
        # Clear existing items
        for widget in self.motorcycle_frame.winfo_children():
            widget.destroy()
        
        # Filter motorcycles
        filtered_motorcycles = []
        for motorcycle in self.motorcycles:
            if (search_term in motorcycle.brand.lower() or 
                search_term in motorcycle.model.lower() or 
                search_term in motorcycle.color.lower()):
                filtered_motorcycles.append(motorcycle)
        
        # Display filtered list
        for i, motorcycle in enumerate(filtered_motorcycles):
            if int(motorcycle.stock) > 0:  # Only show in-stock motorcycles
                self.create_motorcycle_card(motorcycle, i)
    
    def order_motorcycle(self, motorcycle):
        # Create order form window
        order_window = tk.Toplevel(self)
        order_window.title("Place Order")
        order_window.geometry("400x350")
        order_window.configure(bg="#f0f0f0")
        order_window.grab_set()  # Modal window
        
        frame = tk.Frame(order_window, padx=20, pady=20, bg="#f0f0f0")
        frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(frame, text=f"Order: {motorcycle.brand} {motorcycle.model}", 
                             font=("Arial", 12, "bold"), bg="#f0f0f0")
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=10)
        
        # Customer information fields
        tk.Label(frame, text="Your Name:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(frame, width=30)
        name_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Phone Number:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
        phone_entry = tk.Entry(frame, width=30)
        phone_entry.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Address:", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
        address_entry = tk.Text(frame, width=30, height=4)
        address_entry.grid(row=3, column=1, pady=5, padx=10)
        
        def place_order():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_entry.get("1.0", tk.END).strip()
            
            # Validation
            if not name:
                messagebox.showerror("Error", "Please enter your name")
                return
            
            if not phone:
                messagebox.showerror("Error", "Please enter your phone number")
                return
            
            if not address:
                messagebox.showerror("Error", "Please enter your address")
                return
            
            try:
                # Place order
                self.order_manager.place_order(motorcycle.id, name, phone, address)
                messagebox.showinfo("Success", "Your order has been placed successfully!")
                order_window.destroy()
                self.load_motorcycles()  # Refresh to update stock
            except Exception as e:
                messagebox.showerror("Error", f"Failed to place order: {e}")
        
        # Place order button
        order_button = tk.Button(frame, text="Confirm Order", command=place_order,
                               bg="#4CAF50", fg="white", width=15, pady=5)
        order_button.grid(row=4, column=0, columnspan=2, pady=15)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
