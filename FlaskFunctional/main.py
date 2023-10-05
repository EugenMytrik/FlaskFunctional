from flask import Flask, jsonify
import sqlite3
from faker import Faker
import random

app = Flask(__name__)

# Функція для створення і наповнення таблиці customers
def create_customers_table():
    fake = Faker()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      first_name TEXT,
                      last_name TEXT,
                      email TEXT
                  )''')

    for _ in range(100):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        cursor.execute("INSERT INTO customers (first_name, last_name, email) VALUES (?, ?, ?)",
                       (first_name, last_name, email))

    conn.commit()
    conn.close()

# Викликаємо функцію для створення та наповнення таблиці customers
create_customers_table()

def create_tracks_table():
    fake = Faker()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tracks (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      artist TEXT,
                      length_seconds INTEGER,
                      release_date DATE
                  )''')

    for _ in range(100):
        artist = fake.name()
        length_seconds = random.randint(180, 600)  # Випадкова довжина треку в секундах
        release_date = fake.date_between(start_date='-10y', end_date='today')  # Випадкова дата випуску

        cursor.execute("INSERT INTO tracks (artist, length_seconds, release_date) VALUES (?, ?, ?)",
                       (artist, length_seconds, release_date))

    conn.commit()
    conn.close()

# Викликаємо функцію для створення та наповнення таблиці tracks
create_tracks_table()

@app.route('/names', methods=['GET'])
def get_unique_names():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT first_name) FROM customers")
    result = cursor.fetchone()[0]
    conn.close()
    return f'unique_names_count: {result}'

@app.route('/tracks', methods=['GET'])
def get_tracks_count():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tracks")
    result = cursor.fetchone()[0]
    conn.close()
    return f'tracks_count: {result}'

@app.route('/tracks-sec', methods=['GET'])
def get_track_info():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT length_seconds, id, artist, release_date FROM tracks")
    result = cursor.fetchall()
    conn.close()
    track_info = [{'length_seconds': row[0], 'id': row[1], 'artist': row[2], 'release_date': row[3]} for row in result]
    return jsonify({'track_info': track_info})

if __name__ == '__main__':
    app.run(debug=True)
