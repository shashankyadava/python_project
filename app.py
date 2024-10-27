#app.py
from flask import Flask, jsonify , request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('shoes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM shoes_list')
    rows = cursor.fetchall()
    
    # Convert data into a list of dictionaries
    data = [dict(row) for row in rows]
    
    conn.close()
    return jsonify(data)

@app.route('/shoes', methods=['GET'])
def get_shoes():
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to join shoes_list_table with adidas and nike
    query = '''
    SELECT 
        s.shoes_id,
        s.shoe_name,
        a.model AS adidas_model,
        n.model AS nike_model,
        COALESCE(a.price, n.price) AS price
    FROM 
        shoes_list s
    LEFT JOIN 
        adidas a ON s.adidas_id = a.adidas_id
    LEFT JOIN 
        nike n ON s.nike_id = n.nike_id
    ''' 

    cursor.execute(query)
    rows = cursor.fetchall()

    #convert the rows to a list of dictionaries
    data = []
    for row in rows:
        shoe_info = {
            "shoe_id": row["shoes_id"],
            "shoe_name": row["shoe_name"],
            "brand": "adidas" if row["adidas_model"] else "nike",
            "model_name": row["adidas_model"] if row["adidas_model"] else row["nike_model"],
            "price": row["price"]
        }
        data.append(shoe_info)

    conn.close()
    return jsonify(data)


#post api to get the data

@app.route('/addshoe',methods=['POST'])
def add_shoe():

    #Parse the json data
    data = request.get_json()

    #Extract data from jason
    nike_data = data.get('nike')
    adidas_data = data.get('adidas')
    shoes_list_data = data.get('shoes_list')

    #connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert into nike table
        if nike_data:
            cursor.execute(
                "INSERT INTO nike(nike_id, model, size, color, type, price) VALUES(?,?,?,?,?,?)",
                (nike_data['nike_id'], nike_data['model'], nike_data['size'], nike_data['color'], nike_data['type'], nike_data['price'])
            )
        
        # Insert into adidas table
        if adidas_data:
            cursor.execute(
                "INSERT INTO adidas(adidas_id, model, size, color, type, price) VALUES(?,?,?,?,?,?)",
                (adidas_data['adidas_id'], adidas_data['model'], adidas_data['size'], adidas_data['color'], adidas_data['type'], adidas_data['price'])
            )
        
        # Insert into shoes_list table
        if shoes_list_data:
            cursor.execute(
                "INSERT INTO shoes_list(shoes_id, shoe_name, adidas_id, nike_id) VALUES(?,?,?,?)",
                (shoes_list_data['shoes_id'], shoes_list_data['shoe_name'], shoes_list_data['adidas_id'], shoes_list_data['nike_id'])
            )

        conn.commit()
        response = {"message":"Data inserted successfully"}

    except sqlite3.Error as e:
        #Rollback if there's an error and return error message
        conn.rollback()
        response = {"error":str(e)}
        
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True,host='127.0.1.1',port=8000)


