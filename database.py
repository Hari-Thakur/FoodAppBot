import sqlite3

def setup_database():
    # Connect to the database
    conn = sqlite3.connect('food1.db')
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dish_name TEXT NOT NULL,
            price REAL NOT NULL,
            restaurant_name TEXT NOT NULL,
            cuisine TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS current_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dish_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            restaurant_name TEXT NOT NULL,
            price REAL NOT NULL,
            instructions TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_text TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_text TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS support (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            support_text TEXT NOT NULL,
            FOREIGN KEY(order_id) REFERENCES current_order(id),
            FOREIGN KEY(customer_id) REFERENCES customer(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating REAL NOT NULL,
            address TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS previous_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dish_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            restaurant_name TEXT NOT NULL,
            price REAL NOT NULL,
            instructions TEXT
        )
    ''')

    # Insert sample data
    sample_menu_data = [
        ('Noodles', 100, 'The Great Wall', 'Chinese'),
        ('Biryani', 150, 'Spice Garden', 'Indian'),
        ('Pizza', 200, 'Italiano', 'Italian'),
        ('Burger', 80, 'Fast Food Corner', 'American'),
        ('Pasta', 120, 'Italiano', 'Italian'),
        ('Fried Rice', 90, 'The Great Wall', 'Chinese'),
        ('Sandwich', 70, 'Fast Food Corner', 'American'),
        ('Tacos', 130, 'Mexicano', 'Mexican'),
        ('Sushi', 300, 'Japanese Delights', 'Japanese'),
        ('Salad', 50, 'Healthy Bites', 'Healthy')
    ]

    c.executemany('''
        INSERT INTO menu (dish_name, price, restaurant_name, cuisine)
        VALUES (?, ?, ?, ?)
    ''', sample_menu_data)

    sample_current_order_data = [
        ('Noodles', 2, 'The Great Wall', 200, 'No spicy'),
        ('Biryani', 1, 'Spice Garden', 150, 'Extra spicy'),
        ('Pizza', 1, 'Italiano', 200, 'No olives'),
        ('Burger', 3, 'Fast Food Corner', 240, 'Extra cheese'),
        ('Pasta', 2, 'Italiano', 240, 'Gluten-free'),
        ('Fried Rice', 1, 'The Great Wall', 90, 'No peas'),
        ('Sandwich', 2, 'Fast Food Corner', 140, 'No mayo'),
        ('Tacos', 1, 'Mexicano', 130, 'Extra meat'),
        ('Sushi', 1, 'Japanese Delights', 300, 'No wasabi'),
        ('Salad', 3, 'Healthy Bites', 150, 'No dressing')
    ]

    c.executemany('''
        INSERT INTO current_order (dish_name, quantity, restaurant_name, price, instructions)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_current_order_data)

    sample_customer_data = [
        ('Alice', '1234567890'),
        ('Bob', '0987654321'),
        ('Charlie', '1112223334'),
        ('David', '4445556667'),
        ('Eve', '7778889990'),
        ('Frank', '5556667778'),
        ('Grace', '8889990001'),
        ('Heidi', '2223334445'),
        ('Ivan', '3334445556'),
        ('Judy', '4445556668')
    ]

    c.executemany('''
        INSERT INTO customer (name, contact)
        VALUES (?, ?)
    ''', sample_customer_data)

    sample_restaurant_data = [
        ('The Great Wall', 4.5, '123 China St'),
        ('Spice Garden', 4.7, '456 India Rd'),
        ('Italiano', 4.3, '789 Italy Ave'),
        ('Fast Food Corner', 4.0, '101 USA Blvd'),
        ('Mexicano', 4.2, '202 Mexico St'),
        ('Japanese Delights', 4.8, '303 Japan St'),
        ('Healthy Bites', 4.6, '404 Health Rd')
    ]

    c.executemany('''
        INSERT INTO restaurants (name, rating, address)
        VALUES (?, ?, ?)
    ''', sample_restaurant_data)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
