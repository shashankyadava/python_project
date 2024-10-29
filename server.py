from pkgutil import get_data

from flask import Flask, jsonify
import sqlite3

class Server:
    def __init__(self, port: int = 8989):
        self.__server = Flask(__name__)
        self.__port = port # By default, server will run on 8989 port

    def start_server(self):
        self.__server.run(port=self.__port)

    def add_routes(self):
        self.__server.add_url_rule('/data', '/data', self.get_data, methods=['GET'])
        self.__server.add_url_rule('/shoes', '/shoes', self.get_shoes, methods=['GET'])

    @staticmethod
    def __get_db_connection():
        conn = sqlite3.connect('shoes.db')
        conn.row_factory = sqlite3.Row
        return conn

    def get_data(self):
        conn = self.__get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM shoes_list')
        rows = cursor.fetchall()

        # Convert data into a list of dictionaries
        data = [dict(row) for row in rows]

        conn.close()
        return jsonify(data)

    def get_shoes(self):
        conn = self.__get_db_connection()
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
