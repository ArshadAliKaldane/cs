import sqlite3 as sql

def db_connect():
	return sql.connect("finance.db")

def get_cursor(db):
	return db.cursor()

def select(q, a):
    con = db_connect()
    cur = get_cursor(con)
    cur.execute(q, a)
    data = cur.fetchall()
    con.close()
    return data

def query(q, a):
    con = db_connect()
    cur = get_cursor(con)
    cur.execute(q, a)
    con.commit()
    con.close()