import sqlite3

def openConn():
    conn= sqlite3.connect("sqlassignment.db")
    print("Connected to databse")
    return conn