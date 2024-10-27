import sqlite3

def create_tables():
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

if __name__ == '__main__':
    create_tables()
    


