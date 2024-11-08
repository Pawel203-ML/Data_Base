import sqlite3
from sqlite3 import Error

db_file = 'database.db'

#create connection with database for all functions
def Create_connection(db_file):
    def decorator(func):
        def wrapper(*args,**kwargs):
            with sqlite3.connect(db_file) as conn:
                result = func(conn,*args,**kwargs)
            return result
        return wrapper
    return decorator

#create tables for database 
@Create_connection(db_file)
def create_tables(conn):
    try:
        cur = conn.cursor()

        cur.execute('''
                CREATE TABLE IF NOT EXISTS owner(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL   
                );
        ''')

        cur.execute('''
                CREATE TABLE IF NOT EXISTS vehicles(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    fuel TEXT NOT NULL,
                    capacity TEXT NOT NULL,
                    FOREIGN KEY (name) REFERENCES owner(id)
                );
        ''')
    except Error as e:
        print(e)

if __name__ == '__main__':
    create_tables()
