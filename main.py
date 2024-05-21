from flask import Flask, render_template, request, jsonify
import sqlite3
import anthropic
import os
import speech_recognition as sr
from pydub import AudioSegment
import io

app = Flask(__name__)

client = anthropic.Client(api_key="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")

def generate_sql_command(user_input):
    prompt = (
        "You are a helpful assistant. Your task is to output only 2 things - an SQL query or 'NO SQL NEEDED' nothing else. "
        "Understand the user query and generate SQL queries from the interpreted text. The user may ask in Hindi, English, Telugu, or a mix of these languages. "
        "Understand the user's language and interpret what the input is about, and then based on this generate SQL queries. "
        "If user asks about particular cuisine return the whole dishes from the menu sql command - SELECT dish FROM menu;\n"
        "The database schema is as follows:\n"
        "Table: restaurants (id, name, branch, address, coordinates, rating, contact_person, contact_phone)\n"
        "Table: menu (id, resto_id, dish, price, portion, rating, image_url)\n"
        "Table: orders (id, resto_id, dish_name, order_quantity, price, rating, feedback)\n"
        "Table: users (name, phone, address, coordinates, current_order, preferences, allegeries, previous_orders)\n\n"
        "Keep <user_id> as 1 always.And dont use '<>' at any cost in the queries\n"
        "In the queries where information is inserted or updated in the database also attach the commmand to view the content which is added\n"
        "Examples:\n"
        "User: Chiniese me kuch batao\n OR "
        "User: what do u have in chinese? \n OR"
        "User: Italian me kuch batao\n etc"
        "SQL: SELECT dish FROM menu;\n"
        "User: 'What dishes do you have?'\n OR "
        "User: 'Khane me kya hai?'\n OR"
        "User: Tindaniki em-em unai?\n"
        "SQL: SELECT dish FROM menu;\n"
        "User: Whats the price of noodles?\n"
        "SQL: SELECT price FROM menu WHERE LOWER(dish) LIKE 'noodle%';\n"
        "User: 'Tell me about The Great Wall restaurant.'\n"
        "SQL: SELECT * FROM restaurants WHERE name = 'The Great Wall';\n"
        "User: 'How much is Chowmein?'\n"
        "SQL: SELECT price FROM menu WHERE LOWER(dish) LIKE 'chowmein';\n"
        "User: 'What is my previous order?'\n"
        "SQL: SELECT * FROM orders WHERE id = (SELECT previous_orders FROM users WHERE id = 1);\n"
        "User: 'What are my last two orders?'\n"
        "SQL: SELECT * FROM orders WHERE id IN (SELECT previous_orders FROM users WHERE id = 1 ORDER BY id DESC LIMIT 2);\n"
        "User: 'How much did my last order cost?'\n"
        "SQL: SELECT price FROM orders WHERE id = (SELECT previous_orders FROM users WHERE id = 1 ORDER BY id DESC LIMIT 1);\n"
        "User: 'What is my current order?'\n"
        "SQL: SELECT current_order FROM users WHERE id = 1;\n"
        "User: 'i would like to order 1 plate noodles'\n"
        "SQL: UPDATE users SET current_order = IFNULL(current_order, '') || '1 plate noodles, ', status = 'pending' WHERE id = 1;SELECT current_order FROM users WHERE id = 1;\n"
        "User: also add one plate biryani\n"
        "SQL: UPDATE users SET current_order = IFNULL(current_order, '') || '1 plate biryani, ', status = 'pending' WHERE id = 1;SELECT current_order FROM users WHERE id = 1;\n"
        "User: I would like to confirm my order.\n"
        "SQL: INSERT INTO orders (resto_id, dish_name, order_quantity, price, rating, feedback) SELECT 1, dish_name, order_quantity, price, rating, feedback FROM ( SELECT 1 AS resto_id, TRIM(SUBSTR(current_order, INSTR(current_order, ',') + 1)) AS dish_name, 1 AS order_quantity, (SELECT price FROM menu WHERE dish = TRIM(SUBSTR(current_order, INSTR(current_order, ',') + 1))) AS price, NULL AS rating, NULL AS feedback FROM users WHERE id = 1) AS order_details; UPDATE users SET previous_orders = ( SELECT GROUP_CONCAT(id) FROM orders WHERE resto_id = 1 AND dish_name IN (SELECT TRIM(SUBSTR(current_order, INSTR(current_order, ',') + 1)) FROM users WHERE id = 1) ), current_order = NULL, status = 'confirmed' WHERE id = 1;SELECT * FROM orders WHERE id IN ( SELECT previous_orders FROM users WHERE id = 1);\n"
        "User: What's my previous order?\n"
        "SQL: SELECT * FROM orders WHERE id IN ( SELECT previous_orders FROM users WHERE id = 1);\n"
        "User: The taste of my previous order was not nice.\n"
        "SQL: UPDATE orders SET feedback = 'The taste was not nice' WHERE id = ( SELECT previous_orders FROM users WHERE id = 1 ) AND feedback IS NULL;SELECT * FROM orders WHERE id IN ( SELECT previous_orders FROM users WHERE id = 1);\n\n"
        "Generate the SQL command needed to retrieve the information requested by the user. If no SQL command is needed, respond with 'NO SQL NEEDED'.\n"
        "\n\nHuman: " + user_input + "\nAssistant:"
    )

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        temperature=0.7,
        system="You are a helpful restaurant assistant",
        messages=[
        {
            "role": "user",
            "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
         }
        ]

    )
    sql_command = response.content[0].text

    print(sql_command)
    return sql_command

def fetch_data(sql_command):
    conn = sqlite3.connect('foodappbot.db')
    c = conn.cursor()
    
    # Remove "SQL:" prefix if present
    if sql_command.startswith("SQL:"):
        sql_command = sql_command[4:].strip()

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

# Function to generate chatbot response
def generate_chatbot_response(user_input, data=None):
    if not data:
        data_str = "No data available."
    else:
        data_str = str(data)
        
    prompt = (
        "You are a helpful restaurant assistant. The user may ask in Hindi, English, Telugu, or a mix of these languages. "
        "Respond in the user's tone and language. "
        "Remember the interaction and respond accordingly. \n"
        "The user asked: " + user_input + "\n"
        "Here is the data: " + data_str + "\n"
        "Provide a response to the user based on this data and act like a restaurant chatbot. "
        "If the data is 'No data available', do not assume or make up any information.\n"
        "\n\nHuman: " + user_input + "\nAssistant:"
    )

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        temperature=1,
        system="You are a helpful restaurant assistant",
        messages=[
        {
            "role": "user",
            "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
         }
        ]

    )
    response_text = response.content[0].text
    print(response_text)
    return response_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user_input = data.get('user_input')
    
    # Generate SQL command
    sql_command = generate_sql_command(user_input)
    
    # Check if SQL command is needed
    if sql_command == "NO SQL NEEDED":
        # Directly generate chatbot response
        response_text = generate_chatbot_response(user_input)
    else:
        # Fetch data from the database
        data = fetch_data(sql_command)
        # Generate chatbot response
        response_text = generate_chatbot_response(user_input, data)
    
    return jsonify({'response': response_text})

@app.route('/recognize', methods=['POST'])
def recognize():
    recognizer = sr.Recognizer()
    audio_file = request.files['audio_data']
    audio_data = audio_file.read()

    # Convert the audio data to a WAV file using pydub
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
    wav_io = io.BytesIO()
    audio_segment.export(wav_io, format="wav")
    wav_io.seek(0)

    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Sorry, I did not get that"
        except sr.RequestError:
            text = "Sorry, the service is down"
    
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
