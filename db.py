import sqlite3
conn=sqlite3.connect("sqlassignment.db").cursor()
print("database create Succesfull")
conn.execute("CREATE TABLE IF NOT EXISTS user (userid INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, password TEXT NOT NULL, fullname TEXT NOT NULL, phone TEXT NOT NULL, address TEXT, city TEXT, state TEXT, country TEXT, pincode TEXT NOT NULL)")
print("user table created ")
conn.execute('''CREATE TABLE IF NOT EXISTS content(cid INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, body TEXT NOT NULL, summary TEXT NOT NULL, docs BLOB NOT NULL, categories TEXT NOT NULL, userid INTEGER,CONSTRAINT fk_user FOREIGN KEY (userid) REFERENCES user(userid))''')
print("content table created successfully")
conn.close()




