import sqlite3
conn=sqlite3.connect("tasks.db")
c=conn.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS tasks (
        task TEXT,
        task_status TEXT,
        due_date DATE)
    """)

def add_task(task, task_status, due_date):
    try:
        c.execute("""INSERT INTO tasks (task, task_status, due_date) 
            VALUES (?, ?, ? )""", (task, task_status, due_date))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)

def read_all():
    try:
        c.execute("SELECT * FROM tasks")
        return c.fetchall()
    except Exception as e:
        print(e)

def read_unique_tasks():
    try:
        c.execute("SELECT DISTINCT Task FROM tasks")
        return c.fetchall()
    except Exception as e:
        print(e)

def get_task_by_name(task):
    try:
        c.execute(f"SELECT * FROM tasks WHERE task='{task}'")
        return c.fetchall()
    except Exception as e:
        print(e)

def update_task_data(new_task, new_status, new_date, task, status, date):
    try:
        c.execute(f"UPDATE tasks SET task = ?, task_status = ?, due_date= ? WHERE task=? and task_status=? and due_date=?", (new_task, new_status, new_date, task, status, date))
        conn.commit()
        c.execute("SELECT * FROM tasks")
        return c.fetchall()
    except Exception as e:
        conn.rollback()
        print(e)

def delete_task(task, status, due_date):
    try:
        c.execute("DELETE FROM tasks WHERE task=? and task_status=? and due_date=?",
                  (task, status, due_date))
        conn.commit()
        c.execute("SELECT * FROM tasks")
        return c.fetchall()
    except Exception as e:
        conn.rollback()
        print(e)
