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
        self.__server.add_url_rule('/create_shoes', '/create_shoes', self.create_shoes, methods=['POST'])
        self.__server.add_url_rule('/remove_shoe', '/remove_shoe', self.remove_shoe, methods=['DELETE'])

    # @staticmethod
    # def __get_db_connection():
    #     conn = sqlite3.connect('shoes.db')
    #     conn.row_factory = sqlite3.Row
    #     return conn
    
    def get_shoes(self):
        try:
            shoe_id = request.args.get('shoe_id')
            shoe_name = request.args.get('shoe_name')
            if shoe_id and shoe_name:
                query = ''' SELECT * from shoes where shoes_id = ? AND shoe_name = ?'''
                params = (shoe_id,shoe_name,)
            elif shoe_id:
                query = ''' SELECT * from shoes where shoes_id = ? '''
                params = (shoe_id)
            elif shoe_name:
                query = ''' SELECT * from shoes where shoe_name = ?'''
                params = (shoe_name,)
            else:
                query = ''' SELECT * from shoes '''
                params = None

        except sqlite3.Error as e:
            print(e)
            return e

        return database.fetch_data(query,params)
    
    def create_shoes(self):
        
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


    def remove_shoe(self):
        try:
            shoe_id = request.args.get('shoe_id')
            shoe_name = request.args.get('shoe_name')
            if shoe_id and shoe_name:
                query = ''' DELETE from shoes where shoes_id = ? AND shoe_name = ? '''
                params = (shoe_id,shoe_name,)
            elif shoe_id:
                query = ''' DELETE from shoes where shoes_id = ? '''
                params = (shoe_id,)
            else:
                return jsonify({"message":"shoe_id or shoe_name is required"})
        except sqlite3.Error as e:
            print(e)
            return e
        return database.remove_data(query,params)




    
    

        
        
        

        



    
    


