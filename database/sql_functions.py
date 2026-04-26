from database.sql_connector import connect
import mysql.connector 

# --- TASK CRUD FUNCTIONS ---

def create_task(user_id, title, description):
    mydb = connect()
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO tasks (user_id, title, description) VALUES (%s, %s, %s)", (user_id, title, description))
    mydb.commit()
    cursor.close()
    mydb.close()

def get_all_tasks(user_id):
    mydb = connect()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    results = cursor.fetchall()
    cursor.close()
    mydb.close()
    return results

def get_one_task(task_id, user_id):
    mydb = connect()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    return result

def update_task(task_id, user_id, completed):
    mydb = connect()
    cursor = mydb.cursor()
    cursor.execute("UPDATE tasks SET completed = %s WHERE id = %s AND user_id = %s", (completed, task_id, user_id))
    mydb.commit()
    cursor.close()
    mydb.close()

def delete_task(task_id, user_id):
    mydb = connect()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
    mydb.commit()
    cursor.close()
    mydb.close()