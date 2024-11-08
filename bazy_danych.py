import sqlite3
from sqlite3 import Error

#create tables for database
def Create_connection(db_file):
    def decorator(func):
        def wrapper(*args,**kwargs):
            with sqlite3.connect(db_file) as conn:
                result = func(conn,*args,**kwargs)
            return result
        return wrapper
    return decorator