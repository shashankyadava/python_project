import sqlite3

#connect to the database

conn = sqlite3.connect('shoes.db') # if shoes.db does not exist it will create it
cursor = conn.cursor() # it will point to the specific database

#create table or schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS nike (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')

#create second table or schema
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS adidas (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')

#insert sample data into both tables
cursor.execute("INSERT INTO nike(id,name) VALUES(1,'jordan')")
cursor.execute("INSERT INTO adidas(id,name) VALUES(2,'sambas')")
conn.commit()

#close the connection
conn.close()


