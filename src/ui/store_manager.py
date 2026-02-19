"""
Store Management Module
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.database import Database
from src.ui.fonts import get_persian_font


class StoreManager:
    """Store Management"""
    
    def __init__(self, parent: tk.Frame, db: Database):
        self.parent = parent
        self.db = db
        
        self.create_widgets()
        self.load_stores()
    
    def create_widgets(self):
        """Create widgets"""
        # Top frame - buttons
        top_frame = tk.Frame(self.parent, bg='#f0f0f0')
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        btn_add = tk.Button(
            top_frame,
            text="➕ Add Store",
            command=self.add_store,
            bg='#27ae60',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_add.pack(side=tk.LEFT, padx=5)
        
        btn_edit = tk.Button(
            top_frame,
            text="✏️ Edit",
            command=self.edit_store,
            bg='#3498db',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_edit.pack(side=tk.LEFT, padx=5)
        
        btn_delete = tk.Button(
            top_frame,
            text="🗑️ Delete",
            command=self.delete_store,
            bg='#e74c3c',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_delete.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(
            top_frame,
            text="🔄 Refresh",
            command=self.load_stores,
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
        columns = ('id', 'name', 'city', 'address', 'phone')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('city', text='City')
        self.tree.heading('address', text='Address')
        self.tree.heading('phone', text='Phone')
        
        self.tree.column('id', width=80, anchor=tk.CENTER)
        self.tree.column('name', width=200, anchor=tk.CENTER)
        self.tree.column('city', width=120, anchor=tk.CENTER)
        self.tree.column('address', width=250, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_stores(self):
        """Load stores list"""
        # Clear previous data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        query = "SELECT id, name, city, address, phone FROM stores ORDER BY id"
        results = self.db.execute_query(query)
        
        for row in results:
            self.tree.insert('', tk.END, values=(
                row.get('id', ''),
                row.get('name', ''),
                row.get('city', ''),
                row.get('address', ''),
                row.get('phone', '')
            ))
    
    def add_store(self):
        """Add new store"""
        dialog = StoreDialog(self.parent, self.db, None)
        self.parent.wait_window(dialog.dialog)
        self.load_stores()
    
    def edit_store(self):
        """Edit store"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a store")
            return
        
        item = self.tree.item(selected[0])
        store_code = item['values'][0]
        
        # Get store information
        query = "SELECT * FROM stores WHERE id = ?"
        results = self.db.execute_query(query, (store_code,))
        
        if results:
            dialog = StoreDialog(self.parent, self.db, results[0])
            self.parent.wait_window(dialog.dialog)
            self.load_stores()
    
    def delete_store(self):
        """Delete store"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a store")
            return
        
        item = self.tree.item(selected[0])
        store_code = item['values'][0]
        store_name = item['values'][1]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete store '{store_name}'?"):
            query = "DELETE FROM stores WHERE id = ?"
            if self.db.execute_update(query, (store_code,)):
                messagebox.showinfo("Success", "Store deleted successfully")
                self.load_stores()
            else:
                messagebox.showerror("Error", "Error deleting store")


class StoreDialog:
    """Add/Edit Store Dialog"""
    
    def __init__(self, parent: tk.Frame, db: Database, store_data: dict = None):
        self.db = db
        self.store_data = store_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Store" if not store_data else "Edit Store")
        self.dialog.geometry("500x300")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Main frame
        main_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Fields
        tk.Label(main_frame, text="ID:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.code_entry = tk.Entry(main_frame, font=get_persian_font(10), width=30)
        self.code_entry.grid(row=0, column=1, pady=10, padx=10)
        if store_data:
            self.code_entry.insert(0, str(store_data.get('id', '')))
            self.code_entry.config(state=tk.DISABLED)
        
        tk.Label(main_frame, text="Name:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.name_entry = tk.Entry(main_frame, font=get_persian_font(10), width=30)
        self.name_entry.grid(row=1, column=1, pady=10, padx=10)
        if store_data:
            self.name_entry.insert(0, store_data.get('name', ''))
        
        tk.Label(main_frame, text="City:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.city_entry = tk.Entry(main_frame, font=get_persian_font(10), width=30)
        self.city_entry.grid(row=2, column=1, pady=10, padx=10)
        if store_data:
            self.city_entry.insert(0, store_data.get('city', ''))
        
        tk.Label(main_frame, text="Address:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=3, column=0, sticky=tk.W, pady=10)
        self.address_entry = tk.Entry(main_frame, font=get_persian_font(10), width=30)
        self.address_entry.grid(row=3, column=1, pady=10, padx=10)
        if store_data:
            self.address_entry.insert(0, store_data.get('address', ''))
        
        tk.Label(main_frame, text="Phone:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=4, column=0, sticky=tk.W, pady=10)
        self.phone_entry = tk.Entry(main_frame, font=get_persian_font(10), width=30)
        self.phone_entry.grid(row=4, column=1, pady=10, padx=10)
        if store_data:
            self.phone_entry.insert(0, store_data.get('phone', ''))
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        btn_save = tk.Button(
            btn_frame,
            text="Save",
            command=self.save,
            bg='#27ae60',
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
        """Save store"""
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        city = self.city_entry.get().strip()
        address = self.address_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not code or not name or not city:
            messagebox.showerror("Error", "Please fill required fields")
            return
        
        try:
            code = int(code)
        except ValueError:
            messagebox.showerror("Error", "Code must be a number")
            return
        
        if self.store_data:
            # Edit
            query = """
                UPDATE stores 
                SET name = ?, city = ?, address = ?, phone = ?
                WHERE id = ?
            """
            params = (name, city, address, phone, code)
        else:
            # Add
            query = """
                INSERT INTO stores (id, name, city, address, phone)
                VALUES (?, ?, ?, ?, ?)
            """
            params = (code, name, city, address, phone)
        
        if self.db.execute_update(query, params):
            messagebox.showinfo("Success", "Store saved successfully")
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Error saving store")
