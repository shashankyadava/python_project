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
def fetch_data(query, params=None):
    try:
        conn = __get_db_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query,params)
        else:
            cursor.execute(query)
        # print(cursor)
        rows = cursor.fetchall()
        # print(rows)
        columns = [description[0] for description in cursor.description]
        # columns = 0
        print(columns)
    except sqlite3.Error as e:
        print("Error found: {e}")
        return e
    
    #convert the rows to a list of dictionaries
    try:
        data = [dict(zip(columns, row)) for row in rows]
       # print(data)
        return jsonify(data)
    except sqlite3.Error as e:
        print(e)
        return e
    
    finally:
        conn.close()

    #return columns
         
def insert_data(data):
    #data = jsonify(data)
    for shoeinfo, shoevalue in data.items():
        if not shoevalue:
            
            return jsonify({"error":shoeinfo+" "+"is required"})
        # checklist[shoeinfo] = shoevalue
        print(shoevalue)
        
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
            print(e)
            return e
        finally:
            conn.close()
            print("Connection closed")


def remove_data(query,params=None):
    #need to check if id exist in the database or not
    #if not then we have to manage it
    #if it exists then , we have working code to tackle it
    try:
        conn = __get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM shoes WHERE shoes_id = ?",params)
        result = cursor.fetchone()
        
        if result:
            cursor.execute(query,params)
            conn.commit()
            return jsonify({"message":"shoe deleted successfully"})
        else:
            return jsonify({"message":"shoe not found"})

    except sqlite3.Error as e:
        print("Erro occured:",{e})
        return e
    finally:
        conn.close()
        print("Connection closed")






def update_shoe(query,params=None):
    
    try:
        # Connect to the database
        conn = __get_db_connection()
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query, params)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'shoe not found or no changes made'}), 404

        return jsonify({'message': 'shoe updated successfully'}), 200

    except sqlite3.Error as e:
        return jsonify({'error': f"Database error: {e}"}), 500

    finally:
        # Close the database connection
        conn.close()



    