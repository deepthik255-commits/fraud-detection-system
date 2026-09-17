import sqlite3

connection = sqlite3.connect("fraud.db", check_same_thread=False)

cursor = connection.cursor()

# ---------------- USERS ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    email TEXT UNIQUE,

    password TEXT,

    role TEXT

)
""")

# ---------------- TRANSACTIONS ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    amount REAL,

    frequency INTEGER,

    location TEXT,

    device TEXT,

    time TEXT,

    account_age INTEGER,

    prediction INTEGER,

    probability REAL,

    status TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

# ---------------- ALERTS ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    transaction_id INTEGER,

    message TEXT,

    severity TEXT,

    status TEXT DEFAULT 'Unread',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

# ---------------- FRAUD CASES ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS fraud_cases(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    transaction_id INTEGER,

    case_status TEXT DEFAULT 'Open',

    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

# ---------------- SETTINGS ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    theme TEXT DEFAULT 'Dark',

    notification INTEGER DEFAULT 1

)
""")

# ---------------- WALLET ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS wallet(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    account_name TEXT,

    balance REAL DEFAULT 0

)
""")

connection.commit()
# Default Users

cursor.execute("""
INSERT OR IGNORE INTO users(name,email,password,role)
VALUES
('Administrator','admin@gmail.com','admin123','Admin')
""")

cursor.execute("""
INSERT OR IGNORE INTO users(name,email,password,role)
VALUES
('Normal User','user@gmail.com','user123','User')
""")

connection.commit()