from pkgutil import get_data

from flask import Flask, jsonify, request
import sqlite3

class Server:
    def __init__(self, port: int = 8989):
        self.__server = Flask(__name__)
        self.__port = port # By default, server will run on 8989 port

    def start_server(self):
        self.__server.run(port=self.__port)

    def add_routes(self):
        self.__server.add_url_rule('/shoes', '/shoes', self.get_shoes, methods=['GET'])
        self.__server.add_url_rule('/post_shoes', '/post_shoes', self.post_shoes, methods=['POST'])

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
    
    def post_shoes(self):
        conn = self.__get_db_connection()
        cursor = conn.cursor()

        #     cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS shoes (
        #         shoes_id INTEGER PRIMARY KEY,
        #         brand TEXT NOT NULL,
        #         shoe_name TEXT NOT NULL,
        #         shape TEXT NOT NULL,
        #         size INT NOT NULL,
        #         menwear TEXT NOT NULL,
        #         womanwear TEX NOT NULL,
        #         price INT NOT NULL,
        #         manufacturer TEXT NOT NULL      
        #     )
        # ''')
        data = request.get_json()
        #print(data)
        brand = data['brand']
        #print(brand)
        shoe_name = data['shoe_name']
        #print(shoe_name)
        shape = data['shape']
        #print(shape)
        size = data['size']
        #print(size)
        menwear = data['menwear']
        #print(menwear)
        womanwear = data['womanwear']
        #print(womanwear)
        price = data['price']
        #print(price)
        manufacturer = data['manufacturer']
        #print(manufacturer)

        checklist = {
            "brand" : brand,
            "shoe_name" : shoe_name,
            "shape" : shape,
            "size" : size,
            "menwear" : menwear,
            "womanwear" : womanwear,
            "price" : price,
            "manufacturer" : manufacturer
        }

        for shoeinfo, shoevalue in checklist.items():
            if not shoevalue:
                #print(shoevalue)
                return jsonify({"error":shoeinfo+" "+"is required"})
        
        cursor.execute("INSERT INTO shoes(brand,shoe_name,shape,size,menwear,womanwear,price,manufacturer) VALUES(?,?,?,?,?,?,?,?)", (brand,shoe_name,shape,size,menwear,womanwear,price,manufacturer))
        conn.commit()
        return jsonify({"message":"shoe added successfully"})

        



    
    


