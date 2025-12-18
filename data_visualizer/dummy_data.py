import sqlite3
import random
from datetime import datetime, timedelta

DB_FILE = "data_visualizer.db"

def populate_dummy_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. CLEAR EXISTING DATA (Optional: Keeps it clean)
    print("Clearing old data...")
    cursor.execute("DELETE FROM sales")
    cursor.execute("DELETE FROM products")

    # 2. GENERATE 50+ PRODUCTS
    # We mix-and-match words to create realistic tech names
    categories = ["Computers", "Audio", "Displays", "Accessories", "Peripherals"]
    adjectives = ["Pro", "Ultra", "Slim", "Gaming", "Ergo", "Max", "Air", "Studio"]
    nouns = ["Laptop", "Monitor", "Keyboard", "Mouse", "Headset", "Webcam", "Dock", "Tablet"]
    
    products = []
    print("Generating 50+ products...")
    
    for i in range(1, 60):  # Generating 59 products
        category = random.choice(categories)
        name = f"{random.choice(adjectives)} {random.choice(nouns)} {random.randint(100, 900)}"
        
        # Logic: Make costs 60-80% of price for realistic profit margins
        price = round(random.uniform(50.0, 3000.0), 2)
        cost = round(price * random.uniform(0.60, 0.80), 2)
        
        products.append((i, name, category, price, cost))

    cursor.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)

    # 3. GENERATE 100+ SALES
    # We create a timeline of sales over the past year
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    sales_data = []
    
    print("Generating 100+ sales records...")
    
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(1, 151): # Generating 150 sales rows
        sale_id = i
        product_id = random.randint(1, 59) # Must match the product IDs above
        
        # Random date within the last year
        random_days = random.randint(0, 365)
        sale_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        
        quantity = random.choices([1, 2, 3, 5, 10], weights=[70, 15, 5, 5, 5])[0]
        region = random.choice(regions)
        
        sales_data.append((sale_id, product_id, sale_date, quantity, region))

    cursor.executemany("INSERT INTO sales VALUES (?,?,?,?,?)", sales_data)

    conn.commit()
    conn.close()
    print("✅ Success! Database populated with dummy data.")

if __name__ == "__main__":
    populate_dummy_data()