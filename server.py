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
        self.__server.add_url_rule('/shoes', '/shoes', self.get_shoes, methods=['GET'])

    @staticmethod
    def __get_db_connection():
        conn = sqlite3.connect('shoes.db')
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_shoes(self):
        conn = self.__get_db_connection()
        cursor = conn.cursor()

        # SQL query to join shoes_list_table with adidas and nike
        #random comment
        query = ''' SELECT * from shoes '''

        cursor.execute(query)
        rows = cursor.fetchall()

        #convert the rows to a list of dictionaries
        data = []
        for row in rows:
            shoe_info = {
                "shoe_id": row["shoes_id"],
                "brand": row["brand"],
                "shoe_name": row["shoe_name"],
                "shape" :row["shape"],
                "size": row["size"],
                "menwear": row["menwear"],
                "womanwear": row["womanwear"],
                "price": row["price"],
                "manufacturer": row["manufacturer"]
            }
            data.append(shoe_info)

        conn.close()
        return jsonify(data)
    
    


