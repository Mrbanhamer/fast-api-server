import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import hashlib
from utils.hash_password import password_hash

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

def verify_password(stored_hash, stored_salt_hex, provided_password):
    # 1. Convert the hex salt back to bytes (since urandom produces bytes)
    salt = bytes.fromhex(stored_salt_hex)
    
    # 2. Match the exact logic from your utility: salt + password
    combined = salt + provided_password.encode('utf-8')
    
    # 3. Hash and compare
    current_hash = hashlib.sha256(combined).hexdigest()
    return current_hash == stored_hash

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

def log_new_user(name, last_name, email, password, salt):
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        sql = "INSERT INTO users (first_name, last_name, email, password, salt) VALUES (%s, %s, %s, %s, %s)"
        val = (name, last_name, email, password, salt)
        mycursor.execute(sql, val)
        mydb.commit()
        print(f"User {name} added with ID: {mycursor.lastrowid}")
    except Error as err:
        print(f"Error: {err}")
    finally:
        mycursor.close()
        mydb.close()

def is_ticket_in_db(ticket_id):
    """Checks if the session ticket exists in our tickets table."""
    if not ticket_id:
        return False
    try:
        mydb = connect()
        cursor = mydb.cursor()
        cursor.execute("SELECT user_id FROM tickets WHERE ticket_id = %s", (ticket_id,))
        result = cursor.fetchone()
        return result is not None
    except Error:
        return False
    finally:
        cursor.close()
        mydb.close()

def log_new_user(name, last_name, email, password):
    try:
        mydb = connect()
        cursor = mydb.cursor()
        
        # 1. Use your specific helper function!
        # It returns (hashed_string, salt_hex)
        hashed_pw, salt_hex = password_hash(password)
        
        # 2. Insert into the database
        sql = """
            INSERT INTO users (first_name, last_name, email, password, salt) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (name, last_name, email, hashed_pw, salt_hex))
        
        mydb.commit()
        return True
    except Error as e:
        print(f"Signup error: {e}")
        return False
    finally:
        cursor.close()
        mydb.close()

def get_user_id_from_email(email):
    try:
        mydb = connect()
        cursor = mydb.cursor()
        # We just need the ID to create the session ticket
        sql = "SELECT id FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        
        # result will be a tuple like (1,) so we return the first element
        return result[0] if result else None
    except Error as e:
        print(f"Error fetching user ID: {e}")
        return None
    finally:
        cursor.close()
        mydb.close()

def create_task(user_id, title, description):
    try:
        mydb = connect()
        cursor = mydb.cursor()
        sql = "INSERT INTO tasks (user_id, title, description) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, title, description))
        mydb.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        mydb.close()

def get_all_tasks(user_id):
    try:
        mydb = connect()
        cursor = mydb.cursor(dictionary=True)
        sql = "SELECT id, title, description, completed FROM tasks WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching tasks: {e}")
        return []
    finally:
        cursor.close()
        mydb.close()

def get_one_task(task_id, user_id):
    try:
        mydb = connect()
        cursor = mydb.cursor(dictionary=True)
        sql = "SELECT * FROM tasks WHERE id = %s AND user_id = %s"
        cursor.execute(sql, (task_id, user_id))
        return cursor.fetchone()
    finally:
        cursor.close()
        mydb.close()

def update_task(task_id, user_id, completed):
    try:
        mydb = connect()
        cursor = mydb.cursor()
        sql = "UPDATE tasks SET completed = %s WHERE id = %s AND user_id = %s"
        cursor.execute(sql, (completed, task_id, user_id))
        mydb.commit()
        return True
    finally:
        cursor.close()
        mydb.close()

def delete_task(task_id, user_id):
    try:
        mydb = connect()
        cursor = mydb.cursor()
        sql = "DELETE FROM tasks WHERE id = %s AND user_id = %s"
        cursor.execute(sql, (task_id, user_id))
        mydb.commit()
        return True
    finally:
        cursor.close()
        mydb.close()

if __name__ == '__main__':
    print(make_database())

