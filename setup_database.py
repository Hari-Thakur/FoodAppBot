import sqlite3

def setup_database():
    conn = sqlite3.connect('foodappbot.db')
    c = conn.cursor()
    
    # Create restaurants table
    c.execute('''CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY,
        name TEXT,
        branch TEXT,
        address TEXT,
        coordinates TEXT,
        rating REAL,
        contact_person TEXT,
        contact_phone TEXT
    )''')
    
    # Create menu table
    c.execute('''CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY,
        resto_id INTEGER,
        dish TEXT,
        price REAL,
        portion TEXT,
        rating REAL,
        image_url TEXT,
        FOREIGN KEY (resto_id) REFERENCES restaurants(id)
    )''')

    # Create previous orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        resto_id INTEGER,
        dish_name TEXT,
        order_quantity INTEGER,
        price INTEGER,
        rating INTEGER,
        feedback TEXT,
        FOREIGN KEY (resto_id) REFERENCES restaurants(id)
    )''')
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        address TEXT,
        coordinates TEXT,
        current_order TEXT,
        preferences TEXT,
        allergies TEXT,
        previous_orders INTEGER,
        status TEXT
    )''')
    
    conn.commit()
    conn.close()

def populate_database():
    conn = sqlite3.connect('foodappbot.db')
    c = conn.cursor()

    restaurants = [
        ("The Great Wall", "Main Branch", "123 Main St", "12.9715987,77.5945627", 4.5, "John Doe", "1234567890"),
        ("Taco Palace", "Downtown", "456 Elm St", "34.0522342,-118.2436849", 4.2, "Jane Smith", "0987654321"),
        ("Sushi World", "Uptown", "789 Oak St", "40.712776,-74.005974", 4.8, "Akira Yamada", "5555555555"),
        ("Pasta Heaven", "Central", "321 Maple St", "37.774929,-122.419416", 4.6, "Maria Rossi", "6666666666"),
        ("Burger Town", "Eastside", "654 Pine St", "51.507351,-0.127758", 4.4, "Bill Johnson", "7777777777"),
        ("Curry House", "West End", "987 Cedar St", "28.613939,77.209021", 4.7, "Anita Singh", "8888888888")
    ]

    for resto in restaurants:
        c.execute("INSERT INTO restaurants (name, branch, address, coordinates, rating, contact_person, contact_phone) VALUES (?, ?, ?, ?, ?, ?, ?)", resto)
    
    menu_items = [
        (1, "Noodles", 200, "Full", 4.7, "https://example.com/noodles.jpg"),
        (1, "Chowmein", 150, "Half", 4.5, "https://example.com/chowmein.jpg"),
        (1, "Momos", 100, "Plate", 4.8, "https://example.com/momos.jpg"),
        (2, "Tacos", 120, "Each", 4.6, "https://example.com/tacos.jpg"),
        (2, "Burritos", 250, "Full", 4.4, "https://example.com/burritos.jpg"),
        (2, "Quesadillas", 180, "Each", 4.5, "https://example.com/quesadillas.jpg"),
        (3, "Sushi Roll", 300, "Roll", 4.9, "https://example.com/sushiroll.jpg"),
        (3, "Tempura", 220, "Plate", 4.7, "https://example.com/tempura.jpg"),
        (3, "Miso Soup", 100, "Bowl", 4.6, "https://example.com/misosoup.jpg"),
        (4, "Spaghetti", 200, "Plate", 4.8, "https://example.com/spaghetti.jpg"),
        (4, "Lasagna", 250, "Piece", 4.6, "https://example.com/lasagna.jpg"),
        (4, "Ravioli", 180, "Plate", 4.7, "https://example.com/ravioli.jpg"),
        (5, "Cheeseburger", 150, "Each", 4.5, "https://example.com/cheeseburger.jpg"),
        (5, "Veggie Burger", 130, "Each", 4.4, "https://example.com/veggieburger.jpg"),
        (5, "Fries", 80, "Portion", 4.6, "https://example.com/fries.jpg"),
        (6, "Butter Chicken", 300, "Plate", 4.8, "https://example.com/butterchicken.jpg"),
        (6, "Paneer Tikka", 250, "Plate", 4.7, "https://example.com/paneertikka.jpg"),
        (6, "Biryani", 200, "Plate", 4.9, "https://example.com/biryani.jpg")
    ]

    for item in menu_items:
        c.execute("INSERT INTO menu (resto_id, dish, price, portion, rating, image_url) VALUES (?, ?, ?, ?, ?, ?)", item)
    
    users = [
        ("John Doe", "1234567890", "123 Main St", "12.9715987,77.5945627", "", "", "", None, ""),
        ("Jane Smith", "0987654321", "456 Elm St", "34.0522342,-118.2436849", "", "", "", None, ""),
        ("Akira Yamada", "5555555555", "789 Oak St", "40.712776,-74.005974", "", "", "", None, ""),
        ("Maria Rossi", "6666666666", "321 Maple St", "37.774929,-122.419416", "", "", "", None, ""),
        ("Bill Johnson", "7777777777", "654 Pine St", "51.507351,-0.127758", "", "", "", None, "")
    ]
    for user in users:
        c.execute("INSERT INTO users (name, phone, address, coordinates, current_order, preferences, allergies, previous_orders, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user)

    orders = [
        (1, "Noodles", 2, 200, 5, "Delicious"),
        (1, "Chowmein", 1, 150, 4, "Good"),
        (2, "Tacos", 3, 120, 4, "Nice"),
        (2, "Burritos", 2, 250, 5, "Excellent"),
        (3, "Sushi Roll", 2, 300, 4, "Okay"),
        (3, "Tempura", 1, 220, 5, "Fantastic"),
        (4, "Spaghetti", 1, 200, 4, "Yummy"),
        (4, "Lasagna", 2, 250, 3, "Not great"),
        (5, "Cheeseburger", 3, 150, 5, "Amazing"),
        (5, "Fries", 1, 80, 4, "Tasty")
    ]
    for order in orders:
        c.execute("INSERT INTO orders (resto_id, dish_name, order_quantity, price, rating, feedback) VALUES (?, ?, ?, ?, ?, ?)", order)

    conn.commit()
    conn.close()

setup_database()
populate_database()
