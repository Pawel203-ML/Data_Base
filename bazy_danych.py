import sqlite3
from sqlite3 import Error

db_file = 'database.db'

#create connection with database for all functions
def Create_connection(db_file):
    """
    Create connection with database
    :param db_file: name file with database    
    """
    def decorator(func):
        def wrapper(*args,**kwargs):
            try:
                with sqlite3.connect(db_file) as conn:
                    result = func(conn,*args,**kwargs)
                return result
            except Error as e:
                print(e)
        return wrapper
    return decorator

#create tables for database 
@Create_connection(db_file)
def create_tables(conn):
    """
    Create tables in database
    :param conn: Connection with SQLite Database
    """
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
    """
    Adding data to database file
    :param conn: Connection with SQLite Database
    :param table: name of table
    :param values: tuple with data for table
    """
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
    conn.commit()

@Create_connection(db_file)
def select_all(conn, table):
    pass

if __name__ == '__main__':
    create_tables()
