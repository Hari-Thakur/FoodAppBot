import openai
import sqlite3

openai.api_key = "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"

def initialize_order():
    return {
        "dish_name": "",
        "quantity": "",
        "restaurant_name": "",
        "instructions": ""
    }

def is_order_complete(order):
    return all(order.values())

def format_order(order):
    return f"{order['dish_name']} - {order['quantity']} - {order['restaurant_name']} - {order['instructions']}"

def update_order(order, new_info):
    fields = ["dish_name", "quantity", "restaurant_name", "instructions"]
    new_values = new_info.split(' - ')
    for field, value in zip(fields, new_values):
        if value.strip():
            order[field] = value.strip()
    return order

def calculate_price(dish_name, quantity, restaurant_name):
    # Connect to the database
    conn = sqlite3.connect('food.db')
    c = conn.cursor()
    
    # Retrieve the price from the database
    c.execute("""
        SELECT price
        FROM menu
        WHERE LOWER(dish_name) LIKE LOWER(?)
        AND LOWER(restaurant_name) LIKE LOWER(?)
    """, (f'%{dish_name}%', f'%{restaurant_name}%'))
    
    price_row = c.fetchone()
    if price_row:
        price = price_row[0]
        # Calculate the total price based on the quantity
        total_price = price * float(quantity)
        conn.close()
        return total_price
    else:
        conn.close()
        return None

def get_order_response(user_input, order):
    current_order_status = format_order(order)

    prompt = (
        "You are a helpful food-delivery app assistant. Your task is to collect complete order details from the user in a conversation.\n"
        "The user may talk in Hindi, English, Telugu, or a mix of these languages. Respond accordingly.\n"
        "Your task is to first understand the user input , next check with the current order status and try to retrive the missing values from the user's input , next u have to respond to the user about the missing values.\n"
        "The order details should include the following fields:\n"
        "1. Dish Name\n"
        "2. Quantity\n"
        "3. Restaurant Name\n"
        "4. Special Instructions\n"
        "The user might provide information in any order and might not provide all details at once. Your job is to understand the provided details, update the current order status, and ask for any missing information. Continue the conversation until all the fields are filled.\n"
        "Respond in two lines:Order Details and Response to user, the first line is the order details collected so far in the format 'Dish Name - Quantity - Restaurant Name - Instructions' and the the second line is the response to the user.\n"
        "Example interactions:\n"
        "User: 'I want to order noodles'\n"
        "Order Details: 'Noodles - - - '\n"
        "Response to user: 'How many servings of noodles would you like to order?'\n"
        "User: 'I want two servings'\n"
        "Order Details: 'Noodles - 2 - - '\n"
        "Response to user: 'From which restaurant would you like to order?'\n"
        "User: 'From The Great Wall'\n"
        "Order Details: 'Noodles - 2 - The Great Wall - '\n"
        "Response to user: 'Do you have any special instructions?'\n"
        "User: 'No special instructions'\n"
        "Order Details: 'Noodles - 2 - The Great Wall - No special instructions'\n"
        "Response to user: 'Thank you! Your order for 2 servings of Noodles from The Great Wall has been placed.'\n\n"
        "User: 'I would like to have 3 plates biryani from Spice Garden with extra spicy'\n"
        "Order Details: 'Biryani - 3 - Spice Garden - extra spicy'\n\n"
        "Response to user: 'Thank you! Your order for 3 plates of Biryani from Spice Garden with extra spicy has been placed.'\n\n"
        "User: 'Mujhe noodles chahiye'\n"
        "Order Details: 'Noodles - - - '\n"
        "Response to user: 'Kitni plates chahiye?'\n"
        "User: 'Do plates'\n"
        "Order Details: 'Noodles - 2 - - '\n"
        "Response to user: 'Kaunse restaurant se order karna hai?'\n"
        "User: 'Great Wall restaurant'\n"
        "Order Details: 'Noodles - 2 - Great Wall - '\n"
        "Response to user: 'Kaunse restaurant se order karna hai?'\n"
        "User: 'Great Wall restaurant'\n"
        "Order Details: 'Noodles - 2 - Great Wall - '\n"
        "Response to user: 'Koi special instructions?'\n"
        "User: 'No instructions'\n"
        "Order Details: 'Noodles - 2 - Great Wall - No instructions'\n"
        "Response to user: 'Dhanyavaad! Aapka order 2 plates Noodles from Great Wall ke liye place kiya gaya hai.'\n\n"
        "User: " + user_input + "\n"
        "Current Order: " + current_order_status + "\n"
        "Output:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful food-delivery app assistant which helps the user to add their order to the cart."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0
    )

    response_text = response['choices'][0]['message']['content'].strip()
    lines = response_text.split('\n')
    order_details = lines[0].strip()
    user_response = lines[1].strip()

    return user_response, order_details

def handle_order_conversation(user_input, current_order):
    user_response, new_order_info = get_order_response(user_input, current_order)
    current_order = update_order(current_order, new_order_info)
    return user_response, current_order

# Connect to the database
conn = sqlite3.connect('food.db')
c = conn.cursor()

# Example usage
current_order = initialize_order()

while not is_order_complete(current_order):
    user_input = input("You: ")
    user_response, current_order = handle_order_conversation(user_input, current_order)
    print(f"Bot: {user_response}")
    print(f"Current Order: {format_order(current_order)}")

# Calculate price
dish_name = current_order['dish_name']
quantity = current_order['quantity']
restaurant_name = current_order['restaurant_name']
price = calculate_price(dish_name, quantity, restaurant_name)

# Insert into the current_order table
if price:
    try:
        c.execute("""
            INSERT INTO current_order (dish_name, quantity, restaurant_name, price, instructions)
            VALUES (?, ?, ?, ?, ?)
        """, (current_order['dish_name'], current_order['quantity'], current_order['restaurant_name'], price, current_order['instructions']))
    except:
        print("inserted")
# Commit changes and close connection
conn.commit()
conn.close()

print("Order complete!")

