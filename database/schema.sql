    -- Bookstore Chain Management System Database
    -- SQLite Schema

    -- Drop tables if they exist (for re-run)
    DROP TABLE IF EXISTS sales;
    DROP TABLE IF EXISTS inventory;
    DROP TABLE IF EXISTS books;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS employees;
    DROP TABLE IF EXISTS stores;
    DROP TABLE IF EXISTS publishers;

    -- Publishers table
    CREATE TABLE publishers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT,
        address TEXT
    );

    -- Stores table
    CREATE TABLE stores (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        address TEXT,
        phone TEXT
    );

    -- Books table
    CREATE TABLE books (
        isbn TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT,
        publisher TEXT,
        price REAL NOT NULL,
        publisher_id INTEGER,
        FOREIGN KEY (publisher_id) REFERENCES publishers(id)
    );

    -- Customers table
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        debt REAL DEFAULT 0
    );

    -- Employees table
    CREATE TABLE employees (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        gender TEXT CHECK (gender IN ('Male', 'Female')),
        store_id INTEGER,
        FOREIGN KEY (store_id) REFERENCES stores(id)
    );

    -- Inventory table
    CREATE TABLE inventory (
        store_id INTEGER,
        isbn TEXT,
        quantity INTEGER NOT NULL DEFAULT 0,
        min_stock INTEGER DEFAULT 100,
        PRIMARY KEY (store_id, isbn),
        FOREIGN KEY (store_id) REFERENCES stores(id),
        FOREIGN KEY (isbn) REFERENCES books(isbn)
    );

    -- Sales table
    CREATE TABLE sales (
        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_date DATE NOT NULL DEFAULT (date('now')),
        customer_id INTEGER,
        isbn TEXT,
        quantity INTEGER NOT NULL,
        employee_code TEXT,
        store_id INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (isbn) REFERENCES books(isbn),
        FOREIGN KEY (employee_code) REFERENCES employees(code),
        FOREIGN KEY (store_id) REFERENCES stores(id)
    );

    -- Sample data
    -- Publishers
        INSERT INTO publishers (id, name, phone, address) VALUES
        (1, 'Ailar', '021-12345678', 'Tehran'),
        (2, 'Cheshmeh Publishing', '021-87654321', 'Tehran'),
        (3, 'Scientific Publications', '031-12345678', 'Isfahan');

    -- Stores
    INSERT INTO stores (id, name, city, address, phone) VALUES
    (4545, 'Shahr Ketab Central', 'Tehran', 'Enghelab Street', '021-12345678'),
    (2545, 'Shahr Ketab Isfahan', 'Isfahan', 'Chahar Bagh Street', '031-87654321'),
    (4571, 'Shahr Ketab Shiraz', 'Shiraz', 'Zand Street', '071-12345678'),
    (2549, 'Shahr Ketab Mashhad', 'Mashhad', 'Imam Reza Street', '051-87654321');

    -- Books
    INSERT INTO books (isbn, title, author, publisher, price, publisher_id) VALUES
    ('36-2091', 'Microeconomics', 'Pishro', 'Ailar', 1000.00, 1),
    ('25-4545', 'Wealth of Nations', 'Smith', 'Cheshmeh Publishing', 500.00, 2),
    ('12-5674', 'History of Iran', 'Ahmadi', 'Scientific Publications', 650.00, 3),
    ('45-7845', 'Philosophy', 'Hakimi', 'Ailar', 900.00, 1),
    ('364578', 'Persian Literature', 'Saadi', 'Cheshmeh Publishing', 750.00, 2),
    ('7893562541', 'Mathematics', 'Riazi', 'Scientific Publications', 450.00, 3),
    ('7845-45', 'Physics', 'Physicist', 'Ailar', 850.00, 1);

    -- Customers
    INSERT INTO customers (id, name, phone, address, debt) VALUES
    (124525, 'Naseri', '4578254', 'Sadi Street', 0),
    (564578, 'Rezaei', '2547866', 'Imam Street', 2536000),
    (525252, 'Mosayebi', '45796211', 'Zanjan Street', 0),
    (898585, 'Moini', '5687525', 'Khorasan Street', 0),
    (123456, 'Mohibi', '4587566', 'Jamali Street', 450000);

    -- Employees
    INSERT INTO employees (code, name, phone, address, gender, store_id) VALUES
    ('0023546582', 'Shirazi', '09364562541', 'Tehran', 'Female', 4545),
    ('0047853651', 'Motalbi', '09112547854', 'Tehran', 'Female', 4545),
    ('0224584752', 'Matani', '09125478965', 'Shiraz', 'Male', 4571),
    ('7893562541', 'Ahmadi', '09123456789', 'Isfahan', 'Male', 2545),
    ('0456879851', 'Karimi', '09187654321', 'Mashhad', 'Male', 2549);

    -- Inventory
    INSERT INTO inventory (store_id, isbn, quantity, min_stock) VALUES
    (4545, '36-2091', 1000, 100),
    (4545, '25-4545', 500, 50),
    (2545, '36-2091', 650, 50),
    (2545, '25-4545', 560, 50),
    (4571, '45-7845', 900, 100),
    (2545, '45-7845', 750, 100),
    (4545, '12-5674', 300, 50);

    -- Sales
    INSERT INTO sales (invoice_date, customer_id, isbn, quantity, employee_code, store_id) VALUES
    ('2024-01-15', 124525, '36-2091', 1, '0023546582', 4545),
    ('2024-01-16', 124525, '36-2091', 2, '0047853651', 4545),
    ('2024-02-10', 564578, '364578', 5, '0224584752', 4571),
    ('2024-02-20', 525252, '7893562541', 2, '7893562541', 2545),
    ('2024-03-05', 898585, '7845-45', 10, '7893562541', 2545),
    ('2024-03-10', 123456, '36-2091', 3, '0023546582', 4545),
    ('2024-03-15', 123456, '25-4545', 2, '0047853651', 4545);


