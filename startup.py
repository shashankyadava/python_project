#startup.py
from flask import Flask
from DataBase import create_tables
from app import app

#app = Flask(__name__)

@app.route('/')
def home():
    return "Flask server is running!"

if __name__ == '__main__':
    app.run(debug=True,host='127.0.1.1',port=8000)
    create_tables()