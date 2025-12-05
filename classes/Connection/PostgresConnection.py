from classes.Connection.BaseDBConnection import BaseDBConnection
import psycopg2


class PostgresConnection(BaseDBConnection):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(self.connection_string)

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        dados = cursor.fetchall()
        return dados

    def close(self):
        if self.conn:
            self.conn.close()
