import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import hashlib


def connect():
    load_dotenv()
    password = os.getenv("DB_PASSWORD")
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = password,
        database = 'serverdb'
    )
    return mydb

def make_database():
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        
        # Using a multi-line string for clarity
        sql_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        )
        """
        
        mycursor.execute(sql_query)
        print("Table 'users' verified/created successfully!")
        
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")

    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mycursor.close()
            mydb.close()

def log_new_user(name, last_name, email, password):
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        
        # 1. The SQL Template
        sql = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        
        # 2. The Data (stored as a tuple)
        # will always hash the password before storing
        # will probably make this into a different file called 'cryptorgrapy.py' or something
        val = (name, last_name, email, password)
        
        # 3. Execute combining both
        mycursor.execute(sql, val)
        
        # 4. Save the changes!
        mydb.commit()
        
        print(f"User {name} was successfully added with ID: {mycursor.lastrowid}")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        # Clean up
        mycursor.close()
        mydb.close()

def login(email, provided_password):
    try:
        mydb = connect()
        # dictionary=True allows us to access columns by name
        mycursor = mydb.cursor(dictionary=True)

        # 1. Extract the hash AND the salt
        sql = "SELECT password, salt FROM namn WHERE email = %s"
        mycursor.execute(sql, (email,))
        
        user_record = mycursor.fetchone()

        # 2. Check if user exists
        if user_record is None:
            print("Login failed: User not found.")
            return False

        # 3. Use your custom verify_password function
        # user_record['password'] is the stored_hash
        # user_record['salt'] is the stored_salt
        is_valid = verify_password(
            user_record['password'], 
            user_record['salt'], 
            provided_password
        )

        if is_valid:
            print("Login Successful!")
            return True
        else:
            print("Login failed: Incorrect password.")
            return False

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    finally:
        if 'mycursor' in locals(): mycursor.close()
        if 'mydb' in locals(): mydb.close()

def save_ticket(user_id, ticket_id):
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        sql = "INSERT INTO tickets (ticket_id, user_id) VALUES (%s, %s)"
        mycursor.execute(sql, (ticket_id, user_id))
        mydb.commit()
    except Error as e:
        print(f"Error saving ticket: {e}")
    finally:
        mycursor.close()
        mydb.close()

def is_ticket_in_db(ticket_id):
    if not ticket_id:
        return False
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        # We just need to see if any row exists with this ticket_id
        sql = "SELECT user_id FROM tickets WHERE ticket_id = %s"
        mycursor.execute(sql, (ticket_id,))
        
        result = mycursor.fetchone()
        return result is not None  # Returns True if ticket exists, False otherwise
    except Error as e:
        print(f"Error verifying ticket: {e}")
        return False
    finally:
        mycursor.close()
        mydb.close()

    

if __name__ == '__main__':
    print(login())

