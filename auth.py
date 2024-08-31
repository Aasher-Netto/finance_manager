import bcrypt
import sqlite3
from database import get_db_connection

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(''' 
        INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        conn.close()
        return "User registered successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return "Error: Username already exists."

if __name__ == "__main__":
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    register_user(username, password)

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT password FROM users WHERE username = ?
    ''', (username,))
    result = cursor.fetchone()

    conn.close()

    if result and bcrypt.checkpw(password.encode('utf-8'), result['password']):
        print("Login successful!")
        return True
    else:
        print("Login failed: Invalid username or password.")
        return False

if __name__ == "__main__":
    pass 