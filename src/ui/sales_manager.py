"""
Sales Recording Module
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.database import Database
from src.ui.fonts import get_persian_font


class SalesManager:
    """Sales Recording Management"""
    
    def __init__(self, parent: tk.Frame, db: Database):
        self.parent = parent
        self.db = db
        self.sale_items = []  # Sale items list
        
        self.create_widgets()
        self.load_stores()
        self.load_customers()
        self.load_employees()
    
    def create_widgets(self):
        """Create widgets"""
        # Top frame - sale information
        top_frame = tk.LabelFrame(self.parent, text="Sale Information", bg='#f0f0f0', font=get_persian_font(11, 'bold'))
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        inner_frame = tk.Frame(top_frame, bg='#f0f0f0')
        inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Store
        tk.Label(inner_frame, text="Store:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.store_combo = ttk.Combobox(inner_frame, width=30, font=get_persian_font(10))
        self.store_combo.grid(row=0, column=1, pady=5, padx=5)
        self.store_combo.bind('<<ComboboxSelected>>', lambda e: self.load_employees())
        
        # Customer
        tk.Label(inner_frame, text="Customer:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
        self.customer_combo = ttk.Combobox(inner_frame, width=30, font=get_persian_font(10))
        self.customer_combo.grid(row=0, column=3, pady=5, padx=5)
        
        # Employee
        tk.Label(inner_frame, text="Employee:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.employee_combo = ttk.Combobox(inner_frame, width=30, font=get_persian_font(10))
        self.employee_combo.grid(row=1, column=1, pady=5, padx=5)
        
        # Date
        tk.Label(inner_frame, text="Date:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)
        self.date_entry = tk.Entry(inner_frame, width=30, font=get_persian_font(10))
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=1, column=3, pady=5, padx=5)
        
        # Middle frame - add books
        middle_frame = tk.LabelFrame(self.parent, text="Add Book to Invoice", bg='#f0f0f0', font=get_persian_font(11, 'bold'))
        middle_frame.pack(fill=tk.X, padx=10, pady=10)
        
        inner_middle = tk.Frame(middle_frame, bg='#f0f0f0')
        inner_middle.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(inner_middle, text="Book:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.book_combo = ttk.Combobox(inner_middle, width=40, font=get_persian_font(10))
        self.book_combo.grid(row=0, column=1, pady=5, padx=5)
        self.load_books()
        
        tk.Label(inner_middle, text="Quantity:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
        self.quantity_entry = tk.Entry(inner_middle, width=15, font=get_persian_font(10))
        self.quantity_entry.grid(row=0, column=3, pady=5, padx=5)
        
        btn_add_item = tk.Button(
            inner_middle,
            text="➕ Add to Invoice",
            command=self.add_item,
            bg='#3498db',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        btn_add_item.grid(row=0, column=4, pady=5, padx=5)
        
        # Invoice items table frame
        table_frame = tk.LabelFrame(self.parent, text="Invoice Items", bg='#f0f0f0', font=get_persian_font(11, 'bold'))
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Items table
        columns = ('isbn', 'title', 'quantity', 'unit_price', 'total')
        self.items_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        self.items_tree.heading('isbn', text='ISBN')
        self.items_tree.heading('title', text='Title')
        self.items_tree.heading('quantity', text='Quantity')
        self.items_tree.heading('unit_price', text='Unit Price')
        self.items_tree.heading('total', text='Total')
        
        self.items_tree.column('isbn', width=120, anchor=tk.CENTER)
        self.items_tree.column('title', width=300, anchor=tk.CENTER)
        self.items_tree.column('quantity', width=100, anchor=tk.CENTER)
        self.items_tree.column('unit_price', width=120, anchor=tk.CENTER)
        self.items_tree.column('total', width=120, anchor=tk.CENTER)
        
        scrollbar_items = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar_items.set)
        
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_items.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Remove from invoice button
        btn_remove_item = tk.Button(
            table_frame,
            text="🗑️ Remove from Invoice",
            command=self.remove_item,
            bg='#e74c3c',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        btn_remove_item.pack(pady=5)
        
        # Bottom frame - buttons
        bottom_frame = tk.Frame(self.parent, bg='#f0f0f0')
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.total_label = tk.Label(
            bottom_frame,
            text="Total: 0 Rials",
            bg='#f0f0f0',
            font=get_persian_font(12, 'bold'),
            fg='#27ae60'
        )
        self.total_label.pack(side=tk.LEFT, padx=10)
        
        btn_clear = tk.Button(
            bottom_frame,
            text="🗑️ Clear Invoice",
            command=self.clear_invoice,
            bg='#95a5a6',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        btn_save = tk.Button(
            bottom_frame,
            text="💾 Save Sale",
            command=self.save_sale,
            bg='#27ae60',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_save.pack(side=tk.LEFT, padx=5)
    
    def load_stores(self):
        """Load stores"""
        query = "SELECT id, name FROM stores ORDER BY id"
        results = self.db.execute_query(query)
        
        store_list = []
        for row in results:
            store_list.append(f"{row.get('id')} - {row.get('name')}")
        
        self.store_combo['values'] = store_list
    
    def load_customers(self):
        """Load customers"""
        query = "SELECT id, name FROM customers ORDER BY name"
        results = self.db.execute_query(query)
        
        customer_list = []
        for row in results:
            customer_list.append(f"{row.get('id')} - {row.get('name')}")
        
        self.customer_combo['values'] = customer_list
    
    def load_employees(self):
        """Load employees"""
        store = self.store_combo.get()
        if not store:
            self.employee_combo['values'] = []
            return
        
        store_code = int(store.split(' - ')[0])
        query = "SELECT id, name FROM employees WHERE store_id = ?"
        results = self.db.execute_query(query, (store_code,))
        
        employee_list = []
        for row in results:
            employee_list.append(f"{row.get('id')} - {row.get('name')}")
        
        self.employee_combo['values'] = employee_list
    
    def load_books(self):
        """Load books"""
        query = "SELECT isbn, title, price FROM books ORDER BY title"
        results = self.db.execute_query(query)
        
        book_list = []
        self.books_dict = {}
        for row in results:
            isbn = row.get('isbn', '')
            title = row.get('title', '')
            price = row.get('price', 0)
            book_list.append(f"{isbn} - {title}")
            self.books_dict[f"{isbn} - {title}"] = {'isbn': isbn, 'price': price}
        
        self.book_combo['values'] = book_list
    
    def add_item(self):
        """Add book to invoice"""
        book = self.book_combo.get()
        quantity = self.quantity_entry.get().strip()
        
        if not book or not quantity:
            messagebox.showwarning("Warning", "Please select book and quantity")
            return
        
        try:
            qty = int(quantity)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer")
            return
        
        if book not in self.books_dict:
            messagebox.showerror("Error", "Selected book is invalid")
            return
        
        book_info = self.books_dict[book]
        isbn = book_info['isbn']
        price = book_info['price']
        total = price * qty
        
        # Check for duplicates
        for item in self.sale_items:
            if item['isbn'] == isbn:
                messagebox.showwarning("Warning", "This book has already been added to invoice")
                return
        
        # Add to list
        self.sale_items.append({
            'isbn': isbn,
            'title': book.split(' - ', 1)[1],
            'quantity': qty,
            'price': price,
            'total': total
        })
        
        # Add to table
        self.items_tree.insert('', tk.END, values=(
            isbn,
            book.split(' - ', 1)[1],
            qty,
            f"{price:,.0f}",
            f"{total:,.0f}"
        ))
        
        # Update total
        self.update_total()
        
        # Clear fields
        self.quantity_entry.delete(0, tk.END)
    
    def remove_item(self):
        """Remove from invoice"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a row")
            return
        
        item = self.items_tree.item(selected[0])
        isbn = item['values'][0]
        
        # Remove from list
        self.sale_items = [item for item in self.sale_items if item['isbn'] != isbn]
        
        # Remove from table
        self.items_tree.delete(selected[0])
        
        # Update total
        self.update_total()
    
    def update_total(self):
        """Update total"""
        total = sum(item['total'] for item in self.sale_items)
        self.total_label.config(text=f"Total: {total:,.0f} Rials")
    
    def clear_invoice(self):
        """Clear invoice"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the invoice?"):
            self.sale_items = []
            for item in self.items_tree.get_children():
                self.items_tree.delete(item)
            self.update_total()
    
    def save_sale(self):
        """Save sale"""
        # Check required fields
        store = self.store_combo.get()
        customer = self.customer_combo.get()
        employee = self.employee_combo.get()
        date = self.date_entry.get().strip()
        
        if not store or not customer or not employee or not date:
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        if not self.sale_items:
            messagebox.showerror("Error", "Please add at least one book to invoice")
            return
        
        # Extract codes
        store_code = int(store.split(' - ')[0])
        customer_code = int(customer.split(' - ')[0])
        employee_code = employee.split(' - ')[0]
        
        # Save each sale row
        success = True
        for item in self.sale_items:
            query = """
                INSERT INTO sales (invoice_date, customer_id, isbn, quantity, employee_code, store_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (date, customer_code, item['isbn'], item['quantity'], employee_code, store_code)
            
            if not self.db.execute_update(query, params):
                success = False
                break
            
            # Decrease inventory
            update_inv_query = """
                UPDATE inventory 
                SET quantity = quantity - ?
                WHERE store_id = ? AND isbn = ?
            """
            if not self.db.execute_update(update_inv_query, (item['quantity'], store_code, item['isbn'])):
                success = False
                break
        
        if success:
            messagebox.showinfo("Success", "Sale saved successfully")
            self.clear_invoice()
        else:
            messagebox.showerror("Error", "Error saving sale")

