import sqlite3
import random
from datetime import datetime, timedelta

# Connect to database (it creates the file if it doesn't exist)
conn = sqlite3.connect('sales.db')
c = conn.cursor()

# 1. Create Tables (The Structure)
c.execute('''CREATE TABLE IF NOT EXISTS products
             (product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)''')

c.execute('''CREATE TABLE IF NOT EXISTS sales
             (sale_id INTEGER PRIMARY KEY, product_id INTEGER, 
              date TEXT, quantity INTEGER, total_amount REAL)''')

# 2. Add Fake Data (The Content)
categories = ['Electronics', 'Clothing', 'Home', 'Toys']
products = [('Laptop', 'Electronics', 1200), ('T-Shirt', 'Clothing', 25), 
            ('Blender', 'Home', 50), ('Lego Set', 'Toys', 80), ('Headphones', 'Electronics', 150)]

print("Adding products...")
for p in products:
    c.execute("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", p)

print("Adding sales...")
# Generate 100 fake sales over the last 30 days
for i in range(100):
    product_id = random.randint(1, len(products))
    # Get price of selected product
    price = c.execute("SELECT price FROM products WHERE product_id = ?", (product_id,)).fetchone()[0]
    qty = random.randint(1, 5)
    total = price * qty
    date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
    
    c.execute("INSERT INTO sales (product_id, date, quantity, total_amount) VALUES (?, ?, ?, ?)", 
              (product_id, date, qty, total))

conn.commit()
conn.close()
print("Success! Database 'sales.db' created.")

