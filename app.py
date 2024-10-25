from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)
