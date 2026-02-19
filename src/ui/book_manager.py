"""
Book Management Module
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.database import Database
from src.ui.fonts import get_persian_font


class BookManager:
    """Book Management"""
    
    def __init__(self, parent: tk.Frame, db: Database):
        self.parent = parent
        self.db = db
        
        self.create_widgets()
        self.load_books()
    
    def create_widgets(self):
        """Create widgets"""
        # Top frame - buttons
        top_frame = tk.Frame(self.parent, bg='#f0f0f0')
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        btn_add = tk.Button(
            top_frame,
            text="➕ Add Book",
            command=self.add_book,
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
            command=self.edit_book,
            bg='#3498db',
            fg='white',
            font=get_persian_font(10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        btn_edit.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(
            top_frame,
            text="🔄 Refresh",
            command=self.load_books,
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
        columns = ('isbn', 'title', 'author', 'publisher', 'price', 'publisher_id')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('isbn', text='ISBN')
        self.tree.heading('title', text='Title')
        self.tree.heading('author', text='Author')
        self.tree.heading('publisher', text='Publisher')
        self.tree.heading('price', text='Price')
        self.tree.heading('publisher_id', text='Publisher ID')
        
        self.tree.column('isbn', width=120, anchor=tk.CENTER)
        self.tree.column('title', width=250, anchor=tk.CENTER)
        self.tree.column('author', width=150, anchor=tk.CENTER)
        self.tree.column('publisher', width=150, anchor=tk.CENTER)
        self.tree.column('price', width=100, anchor=tk.CENTER)
        self.tree.column('publisher_id', width=120, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_books(self):
        """Load books list"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        query = "SELECT isbn, title, author, publisher, price, publisher_id FROM books ORDER BY title"
        results = self.db.execute_query(query)
        
        for row in results:
            price = row.get('price', 0)
            if price:
                price_str = f"{price:,.0f}"
            else:
                price_str = "0"
            
            self.tree.insert('', tk.END, values=(
                row.get('isbn', ''),
                row.get('title', ''),
                row.get('author', ''),
                row.get('publisher', ''),
                price_str,
                row.get('publisher_id', '')
            ))
    
    def add_book(self):
        """Add new book"""
        dialog = BookDialog(self.parent, self.db, None)
        self.parent.wait_window(dialog.dialog)
        self.load_books()
    
    def edit_book(self):
        """Edit book"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book")
            return
        
        item = self.tree.item(selected[0])
        isbn = item['values'][0]
        
        query = "SELECT * FROM books WHERE isbn = ?"
        results = self.db.execute_query(query, (isbn,))
        
        if results:
            dialog = BookDialog(self.parent, self.db, results[0])
            self.parent.wait_window(dialog.dialog)
            self.load_books()


class BookDialog:
    """Add/Edit Book Dialog"""
    
    def __init__(self, parent: tk.Frame, db: Database, book_data: dict = None):
        self.db = db
        self.book_data = book_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Book" if not book_data else "Edit Book")
        self.dialog.geometry("550x400")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        main_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Fields
        tk.Label(main_frame, text="ISBN:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.isbn_entry = tk.Entry(main_frame, font=get_persian_font(10), width=35)
        self.isbn_entry.grid(row=0, column=1, pady=10, padx=10)
        if book_data:
            self.isbn_entry.insert(0, book_data.get('isbn', ''))
            self.isbn_entry.config(state=tk.DISABLED)
        
        tk.Label(main_frame, text="Title:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.title_entry = tk.Entry(main_frame, font=get_persian_font(10), width=35)
        self.title_entry.grid(row=1, column=1, pady=10, padx=10)
        if book_data:
            self.title_entry.insert(0, book_data.get('title', ''))
        
        tk.Label(main_frame, text="Author:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.author_entry = tk.Entry(main_frame, font=get_persian_font(10), width=35)
        self.author_entry.grid(row=2, column=1, pady=10, padx=10)
        if book_data:
            self.author_entry.insert(0, book_data.get('author', ''))
        
        tk.Label(main_frame, text="Publisher:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=3, column=0, sticky=tk.W, pady=10)
        self.publisher_entry = tk.Entry(main_frame, font=get_persian_font(10), width=35)
        self.publisher_entry.grid(row=3, column=1, pady=10, padx=10)
        if book_data:
            self.publisher_entry.insert(0, book_data.get('publisher', ''))
        
        tk.Label(main_frame, text="Price:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=4, column=0, sticky=tk.W, pady=10)
        self.price_entry = tk.Entry(main_frame, font=get_persian_font(10), width=35)
        self.price_entry.grid(row=4, column=1, pady=10, padx=10)
        if book_data:
            self.price_entry.insert(0, str(book_data.get('price', 0)))
        
        tk.Label(main_frame, text="Publisher ID:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=5, column=0, sticky=tk.W, pady=10)
        self.pub_code_entry = tk.Entry(main_frame, font=get_persian_font(10), width=35)
        self.pub_code_entry.grid(row=5, column=1, pady=10, padx=10)
        if book_data:
            self.pub_code_entry.insert(0, str(book_data.get('publisher_id', '')))
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
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
        """Save book"""
        isbn = self.isbn_entry.get().strip()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        publisher = self.publisher_entry.get().strip()
        price = self.price_entry.get().strip()
        pub_code = self.pub_code_entry.get().strip()
        
        if not isbn or not title:
            messagebox.showerror("Error", "Please fill required fields (ISBN and Title)")
            return
        
        try:
            price_val = float(price) if price else 0
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
            return
        
        pub_code_val = int(pub_code) if pub_code else None
        
        if self.book_data:
            query = """
                UPDATE books 
                SET title = ?, author = ?, publisher = ?, price = ?, publisher_id = ?
                WHERE isbn = ?
            """
            params = (title, author, publisher, price_val, pub_code_val, isbn)
        else:
            query = """
                INSERT INTO books (isbn, title, author, publisher, price, publisher_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (isbn, title, author, publisher, price_val, pub_code_val)
        
        if self.db.execute_update(query, params):
            messagebox.showinfo("Success", "Book saved successfully")
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Error saving book")
