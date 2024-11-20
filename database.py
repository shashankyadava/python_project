import sqlite3
from flask import jsonify

def __get_db_connection():
    conn = sqlite3.connect('shoes.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    #connect to the database

    conn = __get_db_connection() # get the connection to the database 
    cursor = conn.cursor() # it will point to the specific database
    #random comment
    #create table or schema
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shoes (
            shoes_id INTEGER PRIMARY KEY,
            brand TEXT NOT NULL,
            shoe_name TEXT NOT NULL,
            shape TEXT NOT NULL,
            size INT NOT NULL,
            menwear TEXT NOT NULL,
            womanwear TEX NOT NULL,
            price INT NOT NULL,
            manufacturer TEXT NOT NULL      
        )
    ''')

    conn.commit()

    #close the connection
    conn.close()
def fetch_data(query):
    try:
        conn = __get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        print(columns)
    except sqlite3.Error as e:
        print("Error found: {e}")
        return e
    
    #convert the rows to a list of dictionaries
    try:
        data = [dict(zip(columns, row)) for row in rows]
        print(data)
        return jsonify(data)
    except sqlite3.Error as e:
        print("Error as:{e}")
        return e
    
    finally:
        conn.close()
        
            
            

    
def insert_data(data):

    for shoeinfo, shoevalue in data.items():
        if not shoevalue:
            #print(shoevalue)
            return jsonify({"error":shoeinfo+" "+"is required"})
        # checklist[shoeinfo] = shoevalue
        
        query = "INSERT INTO shoes ({columns}) VALUES ({value_placeholders})".format(
            columns = ", ".join(data.keys()),
            value_placeholders = ", ".join(["?"]*len(data))
        )
        # cursor.execute("INSERT INTO shoes(brand,shoe_name,shape,size,menwear,womanwear,price,manufacturer) VALUES(?,?,?,?,?,?,?,?)", (brand,shoe_name,shape,size,menwear,womanwear,price,manufacturer))
        try:
            conn = __get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query,list(data.values()))
            conn.commit()
            return jsonify({"message":"shoe added successfully"})
        except sqlite3.Error as e:
            print("Error occured: {e}")
        finally:
            conn.close()
            print("Connection closed")