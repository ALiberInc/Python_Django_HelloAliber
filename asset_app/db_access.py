import psycopg2

connection = psycopg2.connect(
    host='127.0.0.1', 
    dbname='hello_aliber_db', 
    user='postgres', 
    password='0000')