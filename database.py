import sqlite3

def create_database():
    #connect to the database

    conn = sqlite3.connect('shoes.db') # if shoes.db does not exist it will create it
    cursor = conn.cursor() # it will point to the specific database

    #create table or schema
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shoes (
            shoes_id INTEGER PRIMARY KEY,
            brand TEXT NOT NULL,
            shoe_name TEXT NOT NULL,
            shape TEXT NOT NULL,
            size INT NOT NULL,
            menwear TEXT NOT NULL,
            womanwear TEX NOT NULL,
            price INT NOT NULL,
            manufacturer TEXT NOT NULL      
        )
    ''')

    conn.commit()

    #close the connection
    conn.close()
    
def insert_data():

    #connect to the database
    conn = sqlite3.connect('shoes.db')
    cursor = conn.cursor()

    
    #insert data into shoes table
    cursor.execute("INSERT INTO shoes(shoes_id,brand,shoe_name,shape,size,menwear,womanwear,price,manufacturer) VALUES(?,?,?,?,?,?,?,?,?)", (1,'nike','jordan','normal','9','Men','No','8000','nike_india'))
    

    #wrote to check the if the data is getting inserted or not
    # query = ''' SELECT * from shoes '''

    # cursor.execute(query)
    # rows = cursor.fetchall()
    # print(rows)

    conn.commit()
    conn.close()

# if __name__ == '__main__':
#     create_database


