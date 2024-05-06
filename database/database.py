import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()

    def execute_query(self, query, data=None):
        if data:
            self.cursor.execute(query, data)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute_query_no_return(self, query, data=None):
        if data:
         self.cursor.execute(query, data)
        else:
            self.cursor.execute(query)
        self.connection.commit()  # Certifica-se de que a transação seja commitada no banco de dados

    def fetch_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()
