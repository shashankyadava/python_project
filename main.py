# This is the entry point for our app.
from database import create_database
from server import Server

# TODO: This method will be moved to a new startup file
def startup():
    # Connect to the database
    #random comment
    create_database()
    #insert_data()

    # insert some dummy data
    # TODO: This will be removed in future after the support of POST API becomes stable.
    # insert_data()

    # Create server and add routes
    server = Server()
    server.add_routes()

    # Start server
    server.start_server()

if __name__ == '__main__':
    startup()