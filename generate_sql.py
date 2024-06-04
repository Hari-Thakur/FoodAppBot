import sqlite3
import openai

openai.api_key = "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"

def fetch_data(sql_command):
    conn = sqlite3.connect('food1.db')
    c = conn.cursor()
    
    commands = sql_command.split(';')
    results = []
    for command in commands:
        command = command.strip()
        if command:
            c.execute(command)
            result = c.fetchall()
            results.append(result)
    conn.close()
    return results

def generate_chatbot_response(user_input, data=None, history=[]):
    if not data:
        data_str = "No data available."
    else:
        data_str = str(data)

    history_str = "\n".join(history)
    
    prompt = (
        "You are a helpful restaurant assistant. The user may ask in Hindi, English, Telugu, or a mix of these languages. "
        "Respond in the user's tone and language. "
        "Remember the interaction and respond accordingly. \n"
        "The user asked: " + user_input + "\n"
        "Here is the data: " + data_str + "\n"
        "Here is the conversation history: " + history_str + "\n"
        "Provide a response to the user based on this data and act like a restaurant chatbot. "
        "If the data is 'No data available', do not assume or make up any information.\n"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful restaurant assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.7
    )

    response_text = response['choices'][0]['message']['content'].strip()
    print(response_text)
    return response_text

def generate_sql_command(user_input):
    prompt = (
        "You are a helpful food-delivery app assistant. Your task is to generate SQL commands based on user queries about menu items, prices,orders, restaurants, recommendations, and more.\n"
        "The user may ask in Hindi, English, Telugu, or a mix of these languages. Respond with the SQL command only.\n"
        "Example interactions:\n"
        "User: 'What dishes do you have?'\n"
        "SQL command: SELECT dish_name FROM menu;\n"
        "User: 'How much is Chowmein?'\n"
        "SQL command: SELECT price FROM menu WHERE LOWER(dish_name) LIKE '%chowmein%';\n"
        "User: 'Tell me about The Great Wall restaurant.'\n"
        "SQL command: SELECT * FROM restaurants WHERE LOWER(name) LIKE '%the great wall%';\n"
        "User: 'Menu dikhao.'\n"
        "SQL command: SELECT dish_name, price FROM menu;\n"
        "User: 'Tindaniki em em unai?'\n"
        "SQL command: SELECT dish_name FROM menu;\n"
        "User: 'Khane me kya kya hai?'\n"
        "SQL command: SELECT dish_name FROM menu;\n"
        "User: 'What would you recommend with Biryani?'\n"
        "SQL command: SELECT dish_name FROM menu;\n"  # Return the entire menu for recommendations
        "User: 'Suggest something to eat.'\n"
        "SQL command: SELECT dish_name FROM menu;\n"  # Return the entire menu for recommendations
        "User: 'Kya acha lagega Biryani ke sath?'\n"
        "SQL command: SELECT dish_name FROM menu;\n"  # Return the entire menu for recommendations
        "User: 'What's the best dish on the menu?'\n"
        "SQL command: SELECT dish_name FROM menu;\n"  # Return the entire menu for recommendations
        "User: 'Can you suggest a good restaurant?'\n"
        "SQL command: SELECT name FROM restaurants;\n"
        "User: 'Which restaurant has the highest ratings?'\n"
        "SQL command: SELECT name FROM restaurants ORDER BY rating DESC;\n"
        "User: 'Chiniese me kuch batao'\n"
        "SQL command: SELECT dish_name FROM menu WHERE LOWER(cuisine) LIKE '%chinese%';\n"
        "User: 'what do u have in chinese?'\n"
        "SQL command: SELECT dish_name FROM menu WHERE LOWER(cuisine) LIKE '%chinese%';\n"
        "User: 'Italian me kuch batao'\n"
        "SQL command: SELECT dish_name FROM menu WHERE LOWER(cuisine) LIKE '%italian%';\n"
        "User: 'What is the price of half plate noodles?'\n"
        "SQL command: SELECT price/2 FROM menu WHERE LOWER(dish_name) LIKE '%noodles%';\n"
        "User: 'Can you tell me the price of a full plate Biryani?'\n"
        "SQL command: SELECT price FROM menu WHERE LOWER(dish_name) LIKE '%biryani%';\n"
        "User: 'what is my previous order?'\n"
        "SQL command: SELECT * FROM previous_order;;\n"
        "User: 'what is my current order?'\n"
        "SQL command: SELECT * FROM current_order;\n"
        "User: " + user_input + "\n"
        "SQL command:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful food-delivery app assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0
    )

    sql_command = response['choices'][0]['message']['content'].strip()
    print(sql_command)
    return sql_command

def main(user_input, conversation_history=[]):
    # Generate SQL command
    sql_command = generate_sql_command(user_input)
    
    # Check if SQL command is needed
    if sql_command == "NO":
        # Directly generate chatbot response
        response_text = generate_chatbot_response(user_input, history=conversation_history)
    else:
        # Fetch data from the database
        data = fetch_data(sql_command)
        # Generate chatbot response
        response_text = generate_chatbot_response(user_input, data, history=conversation_history)
    
    # Update conversation history with the assistant's response
    conversation_history.append(f"Assistant: {response_text}")

    return response_text

# Example usage
user_input = input("Enter query:")
main(user_input)
