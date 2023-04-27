# Misc #
import json
import requests
from threading import Thread
import mysql.connector
from mysql.connector import Error

# CoinGecko API #
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()


# JSON Handling: Creating a usable .json file out of the response from CoinGecko API #
response = requests.get("https://api.coingecko.com/api/v3/coins/list?include_platform=false")
data = response.json()
write_file = open("all_coins.json", "w")
write_file.write(json.dumps(data, indent=4))
    

# SQL Connection Function #
def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

# Short: connection to SQL server and database #
connection = create_server_connection("localhost", "joe", "587HzwO69NFQl0sC7e1O6o", "cointracker")

# Database creation function #
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

# Short: SQL query database creation #
create_database_query = "CREATE DATABASE IF NOT EXISTS cointracker"

create_database(connection, create_database_query)


# SQL query execution function
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")



# SQL Queries #
create_tracking_table = """
CREATE TABLE IF NOT EXISTS tracking (
    id VARCHAR(255),
    name VARCHAR(255),
    PRIMARY KEY (id)
    );
"""
execute_query(connection, create_tracking_table)


# Inserting all coin IDs to "tracking" table # 
with open("all_coins.json", "r") as json_file:
	json_load = json.load(json_file)
for x in json_load:
    x = x["id"]
    try:
        cursor = connection.cursor()
        cursor.execute("""INSERT IGNORE INTO tracking (id) VALUES(%s);""", [x])
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")
print("New coin IDs added successful")
