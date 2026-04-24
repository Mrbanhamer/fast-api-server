import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import hashlib

def connect():
    load_dotenv()
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv("DB_PASSWORD"),
        database='serverdb'
    )

def make_database():
    try:
        mydb = connect()
        cursor = mydb.cursor()
        
        # 1. Users Table (Added salt column)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                salt VARCHAR(255)
            )
        """)

        # 2. Tickets Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id VARCHAR(255) PRIMARY KEY,
                user_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # 3. Tasks Table (The CRUD Resource)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        mydb.commit()
        print("Database and Tables verified successfully!")
    except Error as err:
        print(f"Database setup error: {err}")
    finally:
        cursor.close()
        mydb.close()

# --- AUTH FUNCTIONS ---

def verify_password(stored_hash, stored_salt, provided_password):
    # Hashes the attempt with the same salt to see if they match
    hash_obj = hashlib.sha256((provided_password + stored_salt).encode())
    return hash_obj.hexdigest() == stored_hash

def login(email, provided_password):
    try:
        mydb = connect()
        cursor = mydb.cursor(dictionary=True)
        # Check 'users' table (fixed from 'namn')
        sql = "SELECT id, password, salt FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()

        if user and verify_password(user['password'], user['salt'], provided_password):
            return user['id'] # Return ID to create ticket
        return False
    finally:
        cursor.close()
        mydb.close()

# --- SESSION FUNCTIONS ---

def save_ticket(user_id, ticket_id):
    try:
        mydb = connect()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO tickets (ticket_id, user_id) VALUES (%s, %s)", (ticket_id, user_id))
        mydb.commit()
    finally:
        cursor.close()
        mydb.close()

def get_user_id_from_ticket(ticket_id):
    try:
        mydb = connect()
        cursor = mydb.cursor()
        cursor.execute("SELECT user_id FROM tickets WHERE ticket_id = %s", (ticket_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        cursor.close()
        mydb.close()

if __name__ == '__main__':
    print(make_database())

