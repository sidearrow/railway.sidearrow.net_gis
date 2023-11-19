import pymysql
from pymysql import cursors

def get_connection():
    return pymysql.connect(
        host="localhost",
        port=13306,
        password="root",
        user="root",
        database="railway_data",
        cursorclass=cursors.DictCursor
    )
