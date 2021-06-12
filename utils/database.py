import sqlite3
import traceback
from werkzeug.security import generate_password_hash
def create_connection(db_name):
	conn = sqlite3.connect(db_name)
	return conn

def create_userinfo_table(conn):
	try:
		cursor = conn.cursor()
		cursor.execute("DROP TABLE userinfo")
		cursor.execute("CREATE TABLE userinfo (name text, password text)")
		cursor.execute("INSERT INTO userinfo values(?, ?)", ("Person1", generate_password_hash("hello1234")))
		cursor.execute("INSERT INTO userinfo values(?,?)", ("Person2", generate_password_hash("helloworld")))
		conn.commit()
	except:
		conn.rollback()
		traceback.print_exc()

def view_table(conn):
	cursor = conn.cursor()
	return cursor.execute("Select * from userinfo").fetchall()
