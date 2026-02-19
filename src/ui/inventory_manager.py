"""
Inventory Management Module
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.database import Database
from src.ui.fonts import get_persian_font


class InventoryManager:
    """Inventory Management"""
    
    def __init__(self, parent: tk.Frame, db: Database):
        self.parent = parent
        self.db = db
        
        self.create_widgets()
        self.load_inventory()
    
    def create_widgets(self):
        """Create widgets"""
        # Top frame - filter and buttons
        top_frame = tk.Frame(self.parent, bg='#f0f0f0')
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Store filter
        tk.Label(top_frame, text="Store:", bg='#f0f0f0', font=get_persian_font(10)).pack(side=tk.LEFT, padx=5)
        self.store_combo = ttk.Combobox(top_frame, width=20, font=get_persian_font(10))
        self.store_combo.pack(side=tk.LEFT, padx=5)
        self.store_combo.bind('<<ComboboxSelected>>', lambda e: self.load_inventory())
        
        # Load stores list
        self.load_stores()
        
        btn_increase = tk.Button(
            top_frame,
            text="➕ Increase Inventory",
            command=self.increase_inventory,
            bg='#27ae60',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_increase.pack(side=tk.LEFT, padx=5)
        
        btn_decrease = tk.Button(
            top_frame,
            text="➖ Decrease Inventory",
            command=self.decrease_inventory,
            bg='#e67e22',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_decrease.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(
            top_frame,
            text="🔄 Refresh",
            command=self.load_inventory,
            bg='#95a5a6',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_refresh.pack(side=tk.LEFT, padx=5)
        
        # Middle frame - table
        table_frame = tk.Frame(self.parent, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Treeview
        columns = ('store_id', 'isbn', 'title', 'quantity', 'min_stock')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('store_id', text='Store ID')
        self.tree.heading('isbn', text='ISBN')
        self.tree.heading('title', text='Book Title')
        self.tree.heading('quantity', text='Quantity')
        self.tree.heading('min_stock', text='Min Stock')
        
        self.tree.column('store_id', width=120, anchor=tk.CENTER)
        self.tree.column('isbn', width=120, anchor=tk.CENTER)
        self.tree.column('title', width=300, anchor=tk.CENTER)
        self.tree.column('quantity', width=120, anchor=tk.CENTER)
        self.tree.column('min_stock', width=120, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_stores(self):
        """Load stores list"""
        query = "SELECT id, name FROM stores ORDER BY id"
        results = self.db.execute_query(query)
        
        store_list = ["All Stores"]
        for row in results:
            store_list.append(f"{row.get('id')} - {row.get('name')}")
        
        self.store_combo['values'] = store_list
        if store_list:
            self.store_combo.current(0)
    
    def load_inventory(self):
        """Load inventory"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        selected_store = self.store_combo.get()
        store_code = None
        if selected_store and selected_store != "All Stores":
            store_code = int(selected_store.split(' - ')[0])
        
        if store_code:
            query = """
                SELECT i.store_id, i.isbn, b.title, i.quantity, i.min_stock
                FROM inventory i
                INNER JOIN books b ON i.isbn = b.isbn
                WHERE i.store_id = ?
                ORDER BY b.title
            """
            results = self.db.execute_query(query, (store_code,))
        else:
            query = """
                SELECT i.store_id, i.isbn, b.title, i.quantity, i.min_stock
                FROM inventory i
                INNER JOIN books b ON i.isbn = b.isbn
                ORDER BY i.store_id, b.title
            """
            results = self.db.execute_query(query)
        
        for row in results:
            count = row.get('quantity', 0)
            limit = row.get('min_stock', 0)
            
            # Color coding based on min stock
            tags = []
            if count < limit:
                tags = ['low_stock']
            
            self.tree.insert('', tk.END, values=(
                row.get('store_id', ''),
                row.get('isbn', ''),
                row.get('title', ''),
                count,
                limit
            ), tags=tags)
        
        # Configure color for low inventory
        self.tree.tag_configure('low_stock', background='#ffcccc')
    
    def increase_inventory(self):
        """Increase inventory"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an inventory row")
            return
        
        item = self.tree.item(selected[0])
        store_code = item['values'][0]
        isbn = item['values'][1]
        current_count = item['values'][3]
        
        dialog = InventoryChangeDialog(self.parent, "Increase", store_code, isbn, current_count, self.db)
        self.parent.wait_window(dialog.dialog)
        self.load_inventory()
    
    def decrease_inventory(self):
        """Decrease inventory"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an inventory row")
            return
        
        item = self.tree.item(selected[0])
        store_code = item['values'][0]
        isbn = item['values'][1]
        current_count = item['values'][3]
        
        dialog = InventoryChangeDialog(self.parent, "Decrease", store_code, isbn, current_count, self.db)
        self.parent.wait_window(dialog.dialog)
        self.load_inventory()


class InventoryChangeDialog:
    """Change Inventory Dialog"""
    
    def __init__(self, parent: tk.Frame, operation: str, store_code: int, 
                 isbn: str, current_count: int, db: Database):
        self.operation = operation
        self.store_code = store_code
        self.isbn = isbn
        self.current_count = current_count
        self.db = db
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"{operation} Inventory")
        self.dialog.geometry("400x200")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        main_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            main_frame,
            text=f"Store: {store_code} | ISBN: {isbn}",
            bg='#f0f0f0',
            font=get_persian_font(10, 'bold')
        ).pack(pady=10)
        
        tk.Label(
            main_frame,
            text=f"Current Inventory: {current_count}",
            bg='#f0f0f0',
            font=get_persian_font(10)
        ).pack(pady=5)
        
        tk.Label(
            main_frame,
            text=f"Amount to {operation}:",
            bg='#f0f0f0',
            font=get_persian_font(10)
        ).pack(pady=10)
        
        self.amount_entry = tk.Entry(main_frame, font=('Tahoma', 12), width=20)
        self.amount_entry.pack(pady=5)
        self.amount_entry.focus()
        
        btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        btn_save = tk.Button(
            btn_frame,
            text="Confirm",
            command=self.save,
            bg='#27ae60' if operation == "Increase" else '#e67e22',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        btn_save.pack(side=tk.LEFT, padx=10)
        
        btn_cancel = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.dialog.destroy,
            bg='#95a5a6',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        btn_cancel.pack(side=tk.LEFT, padx=10)
    
    def save(self):
        """Save changes"""
        try:
            amount = int(self.amount_entry.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a positive integer")
            return
        
        if self.operation == "Decrease" and amount > self.current_count:
            messagebox.showerror("Error", f"Cannot decrease more than {self.current_count}")
            return
        
        # Update inventory
        if self.operation == "Increase":
            new_count = self.current_count + amount
        else:
            new_count = self.current_count - amount
        
        query = """
            UPDATE inventory 
            SET quantity = ?
            WHERE store_id = ? AND isbn = ?
        """
        
        if self.db.execute_update(query, (new_count, self.store_code, self.isbn)):
            messagebox.showinfo("Success", f"Inventory {self.operation.lower()}ed successfully")
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Error updating inventory")

