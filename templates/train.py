from flask import Flask, render_template, request, jsonify
import sqlite3
import openai
import os
import speech_recognition as sr
from pydub import AudioSegment
import io

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
openai.api_key = "sk-proj-DO6bbk3XDygHim4wMbXsT3BlbkFJaBLCAQQ9SFvZ7BtQttfP"


# Function to set up the database
def setup_database():
    conn = sqlite3.connect('food.db')
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
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        address TEXT,
        coordinates TEXT,
        preferences TEXT,
        allergies TEXT
    )''')
    
    conn.commit()
    conn.close()

# Function to populate the database with initial data
def populate_database():
    conn = sqlite3.connect('food.db')
    c = conn.cursor()
    
    # Insert some restaurants
    c.execute("INSERT INTO restaurants (name, branch, address, coordinates, rating, contact_person, contact_phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
              ("The Great Wall", "Main Branch", "123 Main St", "12.9715987,77.5945627", 4.5, "John Doe", "1234567890"))
    
    # Insert some menu items
    c.execute("INSERT INTO menu (resto_id, dish, price, portion, rating, image_url) VALUES (?, ?, ?, ?, ?, ?)",
              (1, "Noodles", 200, "Full", 4.7, "https://example.com/noodles.jpg"))
    c.execute("INSERT INTO menu (resto_id, dish, price, portion, rating, image_url) VALUES (?, ?, ?, ?, ?, ?)",
              (1, "Chowmein", 150, "Half", 4.5, "https://example.com/chowmein.jpg"))
    c.execute("INSERT INTO menu (resto_id, dish, price, portion, rating, image_url) VALUES (?, ?, ?, ?, ?, ?)",
              (1, "Momos", 100, "Plate", 4.8, "https://example.com/momos.jpg"))

    conn.commit()
    conn.close()

# Call setup and populate functions
setup_database()
populate_database()

# Function to fetch data from the database
def fetch_menu_items():
    conn = sqlite3.connect('swiggy.db')
    c = conn.cursor()
    c.execute("SELECT dish FROM menu")
    dishes = [row[0] for row in c.fetchall()]
    conn.close()
    return dishes

# Function to process chatbot response
def process_chatbot_response(user_input):
    menu_items = fetch_menu_items()
    prompt = (
        "You are a helpful restaurant assistant. "
        "The user may ask in Hindi or English or Telugu or a mix of Hindi and English or a mix of Telugu and English. "
        "When responding, adapt to the user's tone ,language and preferences. "
        "The available dishes are: " + ", ".join(menu_items) + ". "
        "Respond in users language and also include user language phrases if the user uses them. "
        "User: " + user_input
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful restaurant assistant. Adapt to the user's tone and language, and respond like a restaurant reception accordingly"},
            {"role": "user", "content": prompt}
        ]
    )

    response_text = response['choices'][0]['message']['content'].strip()
    return response_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user_input = data.get('user_input')
    
    # Process the user input with the chatbot logic
    response_text = process_chatbot_response(user_input)
    
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
