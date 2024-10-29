import sqlite3

def create_database():
    #connect to the database

    conn = sqlite3.connect('shoes.db') # if shoes.db does not exist it will create it
    cursor = conn.cursor() # it will point to the specific database

    #create table or schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nike (
            nike_id INTEGER PRIMARY KEY,
            model TEXT NOT NULL,
            size INTEGER,
            color TEXT,
            type TEXT,
            price REAL
        )
    ''')

    #create second table or schema
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS adidas (
            adidas_id INTEGER PRIMARY KEY,
            model TEXT NOT NULL,
            size INTEGER,
            color TEXT,
            type TEXT,
            price REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shoes_list (
            shoes_id INTEGER PRIMARY KEY,
            shoe_name TEXT NOT NULL,
            adidas_id INTEGER,
            nike_id INTEGER,
            FOREIGN KEY (adidas_id) REFERENCES adidas(adidas_id),
            FOREIGN KEY (nike_id) REFERENCES nike(nike_id)   
        )
    ''')

    conn.commit()

    #close the connection
    conn.close()
    
def insert_data():

    #connect to the database
    conn = sqlite3.connect('shoes.db')
    cursor = conn.cursor()

    #insert data into the nike table
    cursor.execute("INSERT INTO nike(nike_id,model,size,color,type,price) VALUES(?,?,?,?,?,?)", (1,'jordan',9,'black','men',1000.00))
    #insert data into the adidas table
    cursor.execute("INSERT INTO adidas(adidas_id,model,size,color,type,price) VALUES(?,?,?,?,?,?)", (1,'sambas',9,'black','men',1000.00))

    #insert data into shoes_list_table
    cursor.execute("INSERT INTO shoes_list(shoes_id,shoe_name,adidas_id,nike_id) VALUES(?,?,?,?)", (1,'jordan',None,1))
    cursor.execute("INSERT INTO shoes_list(shoes_id,shoe_name,adidas_id,nike_id) VALUES(?,?,?,?)", (2,'sambas',1,None))

    conn.commit()
    conn.close()

