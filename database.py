import psycopg2
from config import host, user, password, db_name

connection = psycopg2.connect( #connecting with our PostgreSQL database
    host=host,
    user=user,
    password=password,
    database=db_name
    )
connection.autocommit = True

class Query():
    def execute_query(self, sql, arr):
        with connection.cursor() as cursor:
            cursor.execute(sql, arr)
    def fetch_query(self, sql, arr):
        with connection.cursor() as cursor:
            cursor.execute(sql, arr)
            result = cursor.fetchall()
        return result
    def fetch_one(self, sql, arr):
        with connection.cursor() as cursor:
            cursor.execute(sql, arr)
            result = cursor.fetchone()
        return result