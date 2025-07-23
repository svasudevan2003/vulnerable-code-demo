# app.py
from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Hardcoded secret - BAD PRACTICE
SECRET_KEY = "supersecretkey123"

# Setup in-memory SQLite DB
def init_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    return conn

db_conn = init_db()

@app.route('/')
def home():
    return "Welcome to the Vulnerable App"

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    # SQL Injection Vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"[DEBUG] Executing query: {query}")

    try:
        c = db_conn.cursor()
        c.execute(query)
        result = c.fetchone()
        if result:
            return f"Hello {username}, you are logged in."
        else:
            return "Invalid credentials", 401
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
