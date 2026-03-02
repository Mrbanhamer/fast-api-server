import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv


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
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS namn (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        last_name VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255)
    )
    """
    )
    mydb.commit()
    mycursor.close()
    mydb.close()

def log_new_user():
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("""
        """    
    )
    mydb.commit()
    mycursor.close()
    mydb.close()

make_database()