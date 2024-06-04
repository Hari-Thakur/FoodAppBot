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
        "You are a chatbot for feedback handling and complaint issues"
        "The user asked: " + user_input + "\n"
        "Here is the data: " + data_str + "\n"
        "Here is the conversation history: " + history_str + "\n"
        "Provide a response to the user based on this data and act like a restaurant chatbot. "
        "If the data is 'No data available', do not assume or make up any information.\n"
        "If the data isnt available or the complaint or issue is big return a message like - Kindly contact our support at Foodappbot@gmail.com 24/7 we will be eager to help.\n"
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
        "You are a helpful food-delivery app assistant. Your task is to generate SQL commands based on user queries about feedback, support, or complaints.\n"
        "The user may ask in Hindi, English, Telugu, or a mix of these languages. Respond with the SQL command only.\n"
        "Example interactions:\n"
        "User: 'The taste of my order was not good.'\n"
        "SQL command: INSERT INTO feedback (feedback_text) VALUES ('taste not good');\n"
        "User: 'I have a complaint about my order , that my food was bitter.'\n"
        "SQL command: INSERT INTO complaints (complaint_text) VALUES ('bitter food');\n"
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
        # Execute the generated SQL command
        conn = sqlite3.connect('food1.db')
        c = conn.cursor()
        c.execute(sql_command)
        conn.commit()
        conn.close()
        
        # Generate chatbot response
        response_text = generate_chatbot_response(user_input, history=conversation_history)
    
    # Update conversation history with the assistant's response
    conversation_history.append(f"Assistant: {response_text}")

    return response_text

# Example usage
user_input = input("Enter your feedback, support request, or complaint:")
main(user_input)
