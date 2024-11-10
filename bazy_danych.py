import sqlite3
from sqlite3 import Error
import os

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
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_company TEXT UNIQUE NOT NULL,
                    country TEXT NOT NULL   
                );
        ''')

        cur.execute('''
                CREATE TABLE IF NOT EXISTS vehicles(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    model TEXT UNIQUE NOT NULL,
                    FOREIGN KEY (brand) REFERENCES company(name_company)
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
    columns = []
    question_mark = []

    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON;')
    cur.execute(f'''PRAGMA table_info ({table})''')
    columns = [column[1] for column in cur.fetchall() if column[1] != 'id']
    temp = len(columns)
    question_mark = ['?' for i in range(temp)]
    question_mark = ','.join(question_mark)
    columns = ', '.join(columns)

    sql = f'INSERT OR IGNORE INTO {table}({columns}) VALUES ({question_mark})'
    cur.execute(sql, values)
    conn.commit()

@Create_connection(db_file)
def select_all(conn, table):
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {table}')
    rows = cur.fetchall()

    print(rows)

@Create_connection(db_file)
def select_where(conn, table, **query):
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f'{k} = ?')
        values += (v,)
    q = ' AND '.join(qs)
    cur.execute(f'SELECT * FROM {table} WHERE {q}', values)
    rows = cur.fetchall()

    print(rows)

@Create_connection(db_file)
def update_user(conn):
    print('--Dane z bazy danych--')
    cur = conn.cursor()
    #download names for all tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    table_names = [table[0] for table in tables]
    for i in range(len(table_names)):
        print('')
        print(f'Tabela: {table_names[i]}')
        cur.execute(f'''PRAGMA table_info ({table_names[i]})''')
        columns = [column[1] for column in cur.fetchall() if column[1] != 'id']
        print('Nazwy kolumn:', end= ' ')
        for j in range(len(columns)):
            print(columns[j], end= ' ')
        print(' \n -- -- --')

    while True:
        print('Wybierz nazwe tablicy, numer wiersza oraz kolumne z wartoscia do zmiany: ')
        user_answer = input('tablica, wiersz(id),kolumna=wartosc: ')
        user = [i.strip() for i in user_answer.split(',')]
        table = user[0]
        _id = user[1]
        #tworzenie slownika do **kwargs w funkcji update()
        update_data = {}
        for kv in user[2:]:
            k, v = kv.split('=')
            update_data[k.strip()] = v.strip()

        
        if update(table, _id, **update_data) == True:
            print('Zamiana dokonana')
        else:
            print('Proba nie udana')

        user = input('Czy chcesz kontynuowac? T/N: ')
        if user.upper() == 'N':
            break
        os.system('cls')


@Create_connection(db_file)
def update(conn, table, id, **kwargs):
    parameters = [f'{k}=?' for k in kwargs.keys()]
    parameters = ', '.join(parameters)

    values = tuple(v for v in kwargs.values())
    values += (id,)

    #values = tuple(kwargs.values()) + (id,)

    sql = f'''UPDATE {table} SET {parameters} WHERE id=?'''

    print(parameters, values)
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        return True
    except Error as e:
        print(e)


    


if __name__ == '__main__':
    create_tables()
    adding_data('company', ('Ford','Germany'))
    adding_data('company', ('Mitshubishi', 'Japan'))

    adding_data('vehicles', ('Ford', 'Mustang GT'))
    adding_data('vehicles', ('Mitshubishi','Colt'))

    select_all('company')
    select_all('vehicles')

    update_user()
    '''update('company', 2, country='Niemcy')
    if update('company', 2, country='Niemcy'):
        print('Udana zamiana')'''