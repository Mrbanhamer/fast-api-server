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
        val = (name, last_name, email, hashlib.sha256(password.encode('utf-8')).hexdigest())
        
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

def login(email, password):
    try:
        mydb = connect()
        mycursor = mydb.cursor()



    except mysql.connector.Error as err:
        print(f'Error: {err}')

    

if __name__ == '__main__':
    print(login())

