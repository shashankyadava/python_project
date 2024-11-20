from pkgutil import get_data
from flask import Flask, jsonify, request
import sqlite3
import database

class Server:
    def __init__(self, port: int = 8989):
        self.__server = Flask(__name__)
        self.__port = port # By default, server will run on 8989 port

    def start_server(self):
        self.__server.run(port=self.__port)

    def add_routes(self):
        self.__server.add_url_rule('/shoes', '/shoes', self.get_shoes, methods=['GET'])
        self.__server.add_url_rule('/post_shoes', '/post_shoes', self.post_shoes, methods=['POST'])

    # @staticmethod
    # def __get_db_connection():
    #     conn = sqlite3.connect('shoes.db')
    #     conn.row_factory = sqlite3.Row
    #     return conn
    
    def get_shoes(self):
        query = ''' SELECT * from shoes '''
        return database.fetch_data(query)
    
    def post_shoes(self):
        
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
        try:
            data = request.get_json()
        except sqlite3.Error as e:
            return e
        
        return database.insert_data(data)

        
        
        

        



    
    


