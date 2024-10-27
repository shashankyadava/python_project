import sqlite3
from DataBase import create_tables

def insert_data():

    #create tables or schema if it doesn't exist
    create_tables()

    #connect to the database
    conn = sqlite3.connect('shoes.db')
    cursor = conn.cursor()

    #insert data into the nike table
    cursor.execute("INSERT INTO nike(nike_id,model,size,color,type,price) VALUES(?,?,?,?,?,?)", (1,'jordan',9,'black','men',1000.00))
    #insert data into the adidas table
    cursor.execute("INSERT INTO adidas(adidas_id,model,size,color,type,price) VALUES(?,?,?,?,?,?)", (1,'sambas',9,'black','men',1000.00))

    #insert data into shoes_list_table
    cursor.execute("INSERT INTO shoes_list(shoes_id,shoe_name,adidas_id,nike_id) VALUES(?,?,?,?)", (1,'jordan',None,1))
    cursor.execute("INSERT INTO shoes_list(shoes_id,shoe_name,adidas_id,nike_id) VALUES(?,?,?,?)", (2,'sambas',1,None))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_data()