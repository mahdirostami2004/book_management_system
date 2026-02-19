"""
Main Window Module
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.database import Database
from src.ui.store_manager import StoreManager
from src.ui.book_manager import BookManager
from src.ui.inventory_manager import InventoryManager
from src.ui.sales_manager import SalesManager
from src.ui.reports_manager import ReportsManager
from src.ui.fonts import get_persian_font


class MainWindow:
    """Main Window"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Bookstore Chain Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Database connection
        self.db = Database()
        
        # Create menu
        self.create_menu()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create notebook for tabs
        self.create_notebook()
        
        # Test connection
        self.test_connection()
    
    def create_menu(self):
        """Create main menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_toolbar(self):
        """Create toolbar"""
        toolbar_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        toolbar_frame.pack_propagate(False)
        
        # Connection button
        conn_btn = tk.Button(
            toolbar_frame,
            text="🔌 Test Connection",
            command=self.test_connection,
            bg='#3498db',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        conn_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Status label
        self.status_label = tk.Label(
            toolbar_frame,
            text="Status: Connecting...",
            bg='#2c3e50',
            fg='white',
            font=get_persian_font(10)
        )
        self.status_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def create_notebook(self):
        """Create notebook with different tabs"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[20, 10], font=get_persian_font(11))
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Store management tab
        self.store_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.store_frame, text="🏪 Store Management")
        self.store_manager = StoreManager(self.store_frame, self.db)
        
        # Book management tab
        self.book_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.book_frame, text="📚 Book Management")
        self.book_manager = BookManager(self.book_frame, self.db)
        
        # Inventory management tab
        self.inventory_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.inventory_frame, text="📦 Inventory Management")
        self.inventory_manager = InventoryManager(self.inventory_frame, self.db)
        
        # Sales tab
        self.sales_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.sales_frame, text="💰 Sales")
        self.sales_manager = SalesManager(self.sales_frame, self.db)
        
        # Reports tab
        self.reports_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.reports_frame, text="📊 Reports & Search")
        self.reports_manager = ReportsManager(self.reports_frame, self.db)
    
    def test_connection(self):
        """Test database connection"""
        if self.db.test_connection():
            self.status_label.config(text="Status: Connected ✓", fg='#2ecc71')
            messagebox.showinfo("Success", "Database connection established!")
        else:
            self.status_label.config(text="Status: Disconnected ✗", fg='#e74c3c')
            messagebox.showerror(
                "Error",
                "Database connection error!\n\n"
                "Please make sure:\n"
                "1. SQLite database is created\n"
                "2. Database file path in config.py is correct\n"
                "3. Read/write permissions exist for database file"
            )
    
    def show_about(self):
        """Show program information"""
        messagebox.showinfo(
            "About",
            "Bookstore Chain Management System\n\n"
            "Database Project\n\n"
            "Developer: MEHDI ROSTAMI"
        )
    
    def on_closing(self):
        """When closing program"""
        if self.db:
            self.db.disconnect()
        self.root.destroy()
