import sqlite3
connection = sqlite3.connect("users.db")
cursor = connection.cursor()
command1 = """CREATE TABLE IF NOT EXISTS admin(adname TEXT, password TEXT)"""
cursor.execute(command1)
cursor.execute("INSERT INTO admin VALUES ('ad1', '456')")
cursor.execute("INSERT INTO admin VALUES ('ad2', '789')")
cursor.execute(command1)
connection.commit()


import sqlite3
connection=sqlite3.connect("users.db")
cursor = connection.cursor()
command = """CREATE TABLE IF NOT EXISTS category(cname TEXT NOT NULL , cid TEXT NOT NULL, PRIMARY KEY(cid))"""
cursor.execute(command)
connection.commit()


import sqlite3
connection = sqlite3.connect("users.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS product (
                    pname TEXT NOT NULL,
                    pid INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    cid INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    max_quantity INT NOT NULL,
                    manufacturing_date TEXT NOT NULL,
                    PRIMARY KEY (pname, pid)
                  )''')

connection.commit()


import sqlite3
connection=sqlite3.connect("users.db")
cursor = connection.cursor()
command = """CREATE TABLE IF NOT EXISTS order1(username TEXT NOT NULL,pname TEXT NOT NULL , quantity INT NOT NULL, price INT NOT NULL, FOREIGN KEY(pname) REFERENCES product(pname), FOREIGN KEY(username) REFERENCES userdata(username))"""
cursor.execute(command)
connection.commit()


import sqlite3
connection = sqlite3.connect("users.db")
cursor = connection.cursor()
command = """CREATE TABLE IF NOT EXISTS userdata(username TEXT, password TEXT,address TEXT)"""
cursor.execute(command)
connection.commit()
