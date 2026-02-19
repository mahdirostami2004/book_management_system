"""
Reports and Search Module
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from src.database import Database
from src.ui.fonts import get_persian_font


class ReportsManager:
    """Reports Management"""
    
    def __init__(self, parent: tk.Frame, db: Database):
        self.parent = parent
        self.db = db
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create widgets"""
        # Left frame - reports list
        left_frame = tk.Frame(self.parent, bg='#f0f0f0', width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_frame.pack_propagate(False)
        
        tk.Label(
            left_frame,
            text="Available Reports",
            bg='#f0f0f0',
            font=get_persian_font(12, 'bold')
        ).pack(pady=10)
        
        # Reports list
        reports_list = [
            "1. Store details in Isfahan city",
            "2. Stores without books by Pishro",
            "3. Store sales amount (date range)",
            "4. Store employees list",
            "5. Sales of customer Naseri",
            "6. Books related to Wealth",
            "7. Debt to publisher Ailar",
            "8. Customers with debt over 10000",
            "9. Purchases of customer Mohibi",
            "10. Unsold books (last 3 months)",
            "11. Stores with low inventory (Microeconomics)"
        ]
        
        self.reports_listbox = tk.Listbox(
            left_frame,
            font=get_persian_font(10),
            selectmode=tk.SINGLE,
            height=20
        )
        self.reports_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for report in reports_list:
            self.reports_listbox.insert(tk.END, report)
        
        self.reports_listbox.bind('<<ListboxSelect>>', self.on_report_select)
        
        # Right frame - parameters and results
        right_frame = tk.Frame(self.parent, bg='#f0f0f0')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Parameters frame
        params_frame = tk.LabelFrame(
            right_frame,
            text="Report Parameters",
            bg='#f0f0f0',
            font=get_persian_font(11, 'bold')
        )
        params_frame.pack(fill=tk.X, pady=10)
        
        self.params_container = tk.Frame(params_frame, bg='#f0f0f0')
        self.params_container.pack(fill=tk.X, padx=10, pady=10)
        
        # Execute button
        btn_execute = tk.Button(
            params_frame,
            text="▶️ Run Report",
            command=self.execute_report,
            bg='#27ae60',
            fg='white',
            font=get_persian_font(11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        btn_execute.pack(pady=10)
        
        # Results frame
        results_frame = tk.LabelFrame(
            right_frame,
            text="Results",
            bg='#f0f0f0',
            font=get_persian_font(11, 'bold')
        )
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Results table
        self.results_tree = ttk.Treeview(results_frame, show='headings', height=15)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        self.current_report = None
        self.param_widgets = {}
    
    def on_report_select(self, event):
        """When report is selected"""
        selection = self.reports_listbox.curselection()
        if not selection:
            return
        
        report_num = selection[0] + 1
        self.current_report = report_num
        
        # Clear previous parameters
        for widget in self.params_container.winfo_children():
            widget.destroy()
        self.param_widgets = {}
        
        # Create appropriate parameters for each report
        if report_num == 1:
            # Report 1: No parameters
            tk.Label(
                self.params_container,
                text="This report has no parameters",
                bg='#f0f0f0',
                font=get_persian_font(10)
            ).pack()
        
        elif report_num == 2:
            # Report 2: No parameters
            tk.Label(
                self.params_container,
                text="This report has no parameters",
                bg='#f0f0f0',
                font=get_persian_font(10)
            ).pack()
        
        elif report_num == 3:
            # Report 3: Store ID and date range
            tk.Label(self.params_container, text="Store ID:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
            self.param_widgets['store_code'] = tk.Entry(self.params_container, width=20, font=get_persian_font(10))
            self.param_widgets['store_code'].grid(row=0, column=1, pady=5, padx=5)
            
            tk.Label(self.params_container, text="From Date (YYYY-MM-DD):", bg='#f0f0f0', font=get_persian_font(10)).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
            self.param_widgets['date_from'] = tk.Entry(self.params_container, width=20, font=get_persian_font(10))
            self.param_widgets['date_from'].grid(row=1, column=1, pady=5, padx=5)
            
            tk.Label(self.params_container, text="To Date (YYYY-MM-DD):", bg='#f0f0f0', font=get_persian_font(10)).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
            self.param_widgets['date_to'] = tk.Entry(self.params_container, width=20, font=get_persian_font(10))
            self.param_widgets['date_to'].grid(row=2, column=1, pady=5, padx=5)
        
        elif report_num == 4:
            # Report 4: Store ID
            tk.Label(self.params_container, text="Store ID:", bg='#f0f0f0', font=get_persian_font(10)).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
            self.param_widgets['store_code'] = tk.Entry(self.params_container, width=20, font=get_persian_font(10))
            self.param_widgets['store_code'].grid(row=0, column=1, pady=5, padx=5)
        
        elif report_num in [5, 6, 7, 8, 9, 10, 11]:
            # Other reports without parameters or with specific parameters
            if report_num == 5:
                tk.Label(
                    self.params_container,
                    text="This report is for customer 'Naseri'",
                    bg='#f0f0f0',
                    font=get_persian_font(10)
                ).pack()
            elif report_num == 6:
                tk.Label(
                    self.params_container,
                    text="This report shows books related to 'Wealth'",
                    bg='#f0f0f0',
                    font=get_persian_font(10)
                ).pack()
            elif report_num == 7:
                tk.Label(
                    self.params_container,
                    text="This report calculates debt to publisher 'Ailar'",
                    bg='#f0f0f0',
                    font=get_persian_font(10)
                ).pack()
            elif report_num == 8:
                tk.Label(
                    self.params_container,
                    text="This report shows customers with debt over 10000",
                    bg='#f0f0f0',
                    font=get_persian_font(10)
                ).pack()
            elif report_num == 9:
                tk.Label(
                    self.params_container,
                    text="This report shows purchases of customer 'Mohibi'",
                    bg='#f0f0f0',
                    font=get_persian_font(10)
                ).pack()
            elif report_num == 10:
                tk.Label(
                    self.params_container,
                    text="This report shows unsold books in the last 3 months",
                    bg='#f0f0f0',
                    font=get_persian_font(10)
                ).pack()
            elif report_num == 11:
                tk.Label(
                    self.params_container,
                    text="This report shows stores with low inventory for book 'Microeconomics'",
                    bg='#f0f0f0',
                    font=get_persian_font(10)
                ).pack()
    
    def execute_report(self):
        """Execute selected report"""
        if not self.current_report:
            messagebox.showwarning("Warning", "Please select a report")
            return
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Clear previous columns
        for col in self.results_tree['columns']:
            self.results_tree.heading(col, text='')
            self.results_tree.column(col, width=0)
        
        query = None
        params = None
        
        # Define queries
        if self.current_report == 1:
            # 1. Store details in Isfahan city
            query = "SELECT id, name, city, address, phone FROM stores WHERE city = 'Isfahan'"
        
        elif self.current_report == 2:
            # 2. Store IDs that don't have books by Pishro
            query = """
                SELECT DISTINCT s.id, s.name, s.city
                FROM stores s
                WHERE s.id NOT IN (
                    SELECT DISTINCT i.store_id
                    FROM inventory i
                    INNER JOIN books b ON i.isbn = b.isbn
                    WHERE b.author = 'Pishro'
                )
            """
        
        elif self.current_report == 3:
            # 3. Store sales amount in date range
            store_code = self.param_widgets.get('store_code')
            date_from = self.param_widgets.get('date_from')
            date_to = self.param_widgets.get('date_to')
            
            if not store_code or not date_from or not date_to:
                messagebox.showerror("Error", "Please enter all parameters")
                return
            
            try:
                store_code_val = int(store_code.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Store ID must be a number")
                return
            
            query = """
                SELECT 
                    s.isbn,
                    b.title,
                    SUM(s.quantity) AS total_quantity,
                    b.price,
                    SUM(s.quantity * b.price) AS total_amount
                FROM sales s
                INNER JOIN books b ON s.isbn = b.isbn
                WHERE s.store_id = ? 
                    AND s.invoice_date >= ? 
                    AND s.invoice_date <= ?
                GROUP BY s.isbn, b.title, b.price
                ORDER BY total_amount DESC
            """
            params = (store_code_val, date_from.get().strip(), date_to.get().strip())
        
        elif self.current_report == 4:
            # 4. Store employees list
            store_code = self.param_widgets.get('store_code')
            if not store_code:
                messagebox.showerror("Error", "Please enter Store ID")
                return
            
            try:
                store_code_val = int(store_code.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Store ID must be a number")
                return
            
            query = """
                SELECT id, name, phone, address, gender
                FROM employees
                WHERE store_id = ?
                ORDER BY name
            """
            params = (store_code_val,)
        
        elif self.current_report == 5:
            # 5. Sales details for customer Naseri
            query = """
                SELECT 
                    s.invoice_id,
                    s.invoice_date,
                    b.title AS book_title,
                    s.quantity,
                    b.price,
                    (s.quantity * b.price) AS amount
                FROM sales s
                INNER JOIN books b ON s.isbn = b.isbn
                INNER JOIN customers c ON s.customer_id = c.id
                WHERE c.name = 'Naseri'
                ORDER BY s.invoice_date DESC
            """
        
        elif self.current_report == 6:
            # 6. Books related to Wealth
            query = """
                SELECT isbn, title, author, publisher, price
                FROM books
                WHERE title LIKE '%Servat Melal%'
                ORDER BY title
            """
        
        elif self.current_report == 7:
            # 7. Debt amount to publisher Ailar
            query = """
                SELECT 
                    SUM(i.quantity * b.price) AS total_debt
                FROM inventory i
                INNER JOIN books b ON i.isbn = b.isbn
                INNER JOIN publishers p ON b.publisher_id = p.id
                WHERE p.name = 'Aylar'
            """
        
        elif self.current_report == 8:
            # 8. Customers with debt over 10000
            query = """
                SELECT id, name, phone, address, debt
                FROM customers
                WHERE debt > 10000
                ORDER BY debt DESC
            """
        
        elif self.current_report == 9:
            # 9. Purchases of customer Mohibi
            query = """
                SELECT 
                    s.invoice_id,
                    s.invoice_date,
                    s.store_id,
                    st.name AS store_name,
                    b.title AS book_title,
                    s.quantity,
                    b.price,
                    (s.quantity * b.price) AS amount
                FROM sales s
                INNER JOIN books b ON s.isbn = b.isbn
                INNER JOIN customers c ON s.customer_id = c.id
                INNER JOIN stores st ON s.store_id = st.id
                WHERE c.name = 'Mohebbi'
                ORDER BY s.invoice_date DESC
            """
        
        elif self.current_report == 10:
            # 10. Unsold books in last 3 months
            three_months_ago = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            query = """
                SELECT DISTINCT
                    b.isbn,
                    b.title,
                    b.author,
                    b.price
                FROM books b
                WHERE b.isbn NOT IN (
                    SELECT DISTINCT s.isbn
                    FROM sales s
                    WHERE s.invoice_date >= ?
                )
                ORDER BY b.title
            """
            params = (three_months_ago,)    
        
        elif self.current_report == 11:
            # 11. Stores with low inventory for book Microeconomics
            query = """
                SELECT 
                    s.id,
                    s.name,
                    s.city,
                    i.quantity,
                    i.min_stock
                FROM stores s
                INNER JOIN inventory i ON s.id = i.store_id
                INNER JOIN books b ON i.isbn = b.isbn
                WHERE b.title = 'Eghtesad Khord'
                    AND i.quantity < i.min_stock
                ORDER BY s.id
            """
        
        if query:       
            results = self.db.execute_query(query, params)
            
            if results:
                # Determine columns
                columns = list(results[0].keys())
                self.results_tree['columns'] = columns
                
                # Configure headers and column widths
                for col in columns:
                    self.results_tree.heading(col, text=col)
                    self.results_tree.column(col, width=150, anchor=tk.CENTER)
                
                # Add data
                for row in results:
                    values = []
                    for col in columns:
                        val = row.get(col, '')
                        if isinstance(val, (int, float)):
                            if isinstance(val, float):
                                values.append(f"{val:,.2f}")
                            else:
                                values.append(f"{val:,}")
                        else:
                            values.append(str(val) if val else '')
                    self.results_tree.insert('', tk.END, values=values)
                
                messagebox.showinfo("Success", f"Report executed with {len(results)} rows")
            else:
                messagebox.showinfo("Info", "No results found")
        else:
            messagebox.showerror("Error", "Selected report is invalid")

