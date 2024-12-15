from pkgutil import get_data
from flask import Flask, jsonify, request
import sqlite3
import database
import jwt
import os
from datetime import datetime, timedelta

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
        self.__server.add_url_rule('/update_shoe', '/update_shoe', self.update_shoe, methods=['PATCH'])
        self.__server.add_url_rule('/user_signup', 'user_signup', self.user_signup, methods=['POST'])
        self.__server.add_url_rule('/user_login', 'user_login', self.user_login,methods=['GET'])

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

    
    def update_shoe(self):
        try:
            shoe_id = request.args.get('shoe_id')
            shoe_name = request.args.get('shoe_name')
            update_data = request.get_json()
            # Dynamically generate the SET clause from the request data
            set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
            

            # Prepare the UPDATE query
            
            if not update_data:
                return jsonify({'error': 'No data provided'}), 400
            
            if shoe_id and shoe_name:
                query = f'''UPDATE shoes SET {set_clause} WHERE shoes_id = ? AND shoe_name = ?'''
                params = list(update_data.values()) + [shoe_id, shoe_name]
            elif shoe_id:
                query = f'''UPDATE shoes SET {set_clause} WHERE shoes_id = ?'''
                params = list(update_data.values()) + [shoe_id]
            else:
                return jsonify({"message":"shoe_id or shoe_name is required"})
            
        except sqlite3.Error as e:
            return e
        return database.update_shoe(query,params)
    
    def generate_jwt_token(self,content):
        try:
            print(content)
            # Define secret and algorithm
            secret_key = "random_string"  # Use an environment variable
            algorithm = "HS256"
            
            # Add expiration time
            payload = {
                "data": content,
                "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
            }
            
            # Encode JWT token
            #print(payload,secret_key,algorithm)
            encoded_content = jwt.encode(payload, secret_key, algorithm=algorithm)
            #print(encoded_content)
            return encoded_content  # Returns a token in string format
        except Exception as e:
            print(f"Error generating JWT token: {e}")
            return None

    def validate_user_input(self,email,password):
        if len(email)<=255 and len(password)<=255:
            return True
        else: 
            return False
        
    from werkzeug.security import check_password_hash

    def validate_user(self, password, query, params):
        try:
            # Fetch user data from the database
            current_user = database.fetch_data(query, params)
            print(f"Current user: {current_user}")
            
            if current_user:
                saved_password_hash = current_user[0]['password']  # Assume hashed password
                print(f"Provided password: {password}, Saved hash: {saved_password_hash}")
                
                # Verify hashed password
                if saved_password_hash == password:
                    user_id = current_user[0]['user_id']
                    print(f"Validated user ID: {user_id}")
                    
                    # Generate JWT token
                    jwt_token = self.generate_jwt_token({"user_id": user_id})
                    if jwt_token:
                        print(f"Generated JWT Token: {jwt_token}")
                        return jwt_token
                    else:
                        return {"message": "Failed to generate token"}, 500
                else:
                    return {"message": "Invalid password"}, 401
            else:
                return {"message": "User not found"}, 404
        except Exception as e:
            print(f"Error during user validation: {e}")
            return {"message": "Internal server error"}, 500

    def __get_db_connection(self):
        conn = sqlite3.connect('shoes.db')
        conn.row_factory = sqlite3.Row
        return conn
    def user_signup(self):
        conn = None  # Ensure conn is defined for cleanup
        try:
            # Parse JSON data
            data = request.get_json()
            
            # Validate required fields
            if not data.get('email') or not data.get('password'):
                return jsonify({"message": "Complete all fields"}), 400
            
            email = data['email']
            password = data['password']
            
            # Validate input length
            if not self.validate_user_input(email, password):
                return jsonify({"message": "Reduce password or email length to 255 characters only"}), 400
            
            # Database connection
            conn = self.__get_db_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT 1 FROM user_info WHERE email = ?", (email,))
            result = cursor.fetchone()
            if result:
                return jsonify({"message": "User already exists"}), 409  # HTTP 409 for conflict
            
            # Insert user into database
            query = "INSERT INTO user_info ({columns}) VALUES ({placeholders})".format(
                columns=", ".join(data.keys()),
                placeholders=", ".join(["?"] * len(data))
            )
            cursor.execute(query, list(data.values()))
            conn.commit()
            #cursor.execute("SELECT * FROM user_info")
            #rows = cursor.fetchall()
            #columns = [description[0] for description in cursor.description]
            # columns = 0
            #print(columns)
            #data = [dict(zip(columns, row)) for row in rows]
            #print(data)
            
            return jsonify({"message": "User registered successfully"}), 201  # HTTP 201 for created
        
        except sqlite3.Error as e:
            return jsonify({"message": "Database error", "error": str(e)}), 500
        
        finally:
            if conn:
                conn.close()

        
        # cursor.execute("SELECT * FROM user_info where email = ?",(email,))
        # res = cursor.fetchall
        # print(res)
        
        
    def user_login(self):
        try:
            data = request.get_json()
            if data['email'] is None or data['password'] is None:
                return jsonify({"message":"email or password is required"})
            email = data['email']
            password = data['password']

            conn = self.__get_db_connection()
            cursor = conn.cursor()
            query = '''SELECT * FROM user_info WHERE email = ?'''
            params = (email,)
            user_token = self.validate_user(password,query,params)
            print(user_token)
            if user_token:
                return jsonify({"jwt_token":user_token})
            else:
                return jsonify({"message":"credentials did not match"})
        except sqlite3.Error as e:
            return e
        finally:
            conn.close()
            return jsonify({"message":"user login successfully"})

            


    
    

        
        
        

        



    
    


