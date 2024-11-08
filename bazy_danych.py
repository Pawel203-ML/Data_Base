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
                CREATE TABLE IF NOT EXISTS company(
                    id INTEGER PRIMARY KEY,
                    name_company TEXT NOT NULL,
                    country TEXT NOT NULL   
                );
        ''')

        cur.execute('''
                CREATE TABLE IF NOT EXISTS vehicles(
                    id INTEGER PRIMARY KEY,
                    brand TEXT NOT NULL,
                    weight TEXT NOT NULL,
                    FOREIGN KEY (brand) REFERENCES company(id)
                );
        ''')
    except Error as e:
        print(e)

@Create_connection(db_file)
def adding_data(conn, table, values):
    cur = conn.cursor()
    cur.execute(f'''PRAGMA table_info ({table})''')
    columns = [column[1] for column in cur.fetchall() if column != 'id']
    temp = len(columns)
    question_mark = ('?' for i in range(temp))
    question_mark = ','.join(question_mark)
    columns = ', '.join(columns)

    sql = f'INSERT INTO {table}({columns}) VALUES ({question_mark})'
    print(sql)
    cur.execute(sql, values)

if __name__ == '__main__':
    create_tables()
