import os
import sqlite3

class Database:
    def __init__(self):
        # Obtém o diretório do script atual
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Constrói o caminho absoluto para o arquivo do banco de dados
        caminho_banco_dados = os.path.join(diretorio_atual, 'gerenciamento_ordens_servico.db')
        self.connection = sqlite3.connect(caminho_banco_dados)
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
