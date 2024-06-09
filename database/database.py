import os
import sqlite3
import shutil
import time
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class Database:
    def __init__(self):
        # Obtém o diretório do script atual
        self.diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Constrói o caminho absoluto para o arquivo do banco de dados
        self.caminho_banco_dados = os.path.join(self.diretorio_atual, 'backup_2024-06-07.db')
        self.connection = sqlite3.connect(self.caminho_banco_dados)
        self.cursor = self.connection.cursor()
      # Define o ID da pasta no Google Drive onde o arquivo será enviado
        self.PASTA_ID = '1u4AjbIKQhaqvnyy3TJZ-P_9ZDZ-3VL-x'

        # Define o caminho para o arquivo de credenciais baixado do Google Cloud Console
        self.CREDENCIAIS_ARQUIVO =os.path.join(self.diretorio_atual, 'megamotores-0ce33685e841.json')

    # Métodos existentes da classe Database...

    def fazer_backup_e_enviar_para_google_drive(self):
        hoje = datetime.now()
        if hoje.weekday() == 4:
            print("Iniciando processo de backup...")
            destino_backup = os.path.join(self.diretorio_atual,  f"backup_{hoje.strftime('%Y-%m-%d')}.db")
            print(f"Caminho do arquivo de backup: {destino_backup}")
            
            # Verifica se já existe um arquivo de backup com a data atual
            if os.path.exists(destino_backup):
                print("Já existe um backup para hoje. Pulando o processo de backup.")
                return

            try:
                # Copia o arquivo de banco de dados para o local de backup
                shutil.copy(self.caminho_banco_dados, destino_backup)
                print("Backup realizado com sucesso.")

                print("Enviando arquivo para o Google Drive...")
                
                # Carrega as credenciais do arquivo JSON
                credenciais = service_account.Credentials.from_service_account_file(self.CREDENCIAIS_ARQUIVO)

                # Cria um serviço da API do Google Drive
                service = build('drive', 'v3', credentials=credenciais)

                # Define os metadados do arquivo
                metadados = {
                    'name': os.path.basename(destino_backup),
                    'parents': [self.PASTA_ID]
                }

                # Faz o upload do arquivo para o Google Drive
                media = MediaFileUpload(destino_backup)

                arquivo_drive = service.files().create(body=metadados, media_body=media, fields='id').execute()

                print(f'Arquivo enviado para o Google Drive com o ID: {arquivo_drive["id"]}')
                
            except Exception as e:
                print(f'Erro ao enviar arquivo para o Google Drive: {e}')
    
    def excluir_backup_local(self):
        try:
            # Lista todos os arquivos no diretório
            arquivos = os.listdir(self.diretorio_atual)
            # Itera sobre os arquivos
            for arquivo in arquivos:
                # Verifica se o arquivo começa com o nome "backup"
                if arquivo.startswith("backup"):
                    # Constrói o caminho completo do arquivo
                    caminho_arquivo = os.path.join(self.diretorio_atual, arquivo)
                    # Tenta remover o arquivo
                    os.remove(caminho_arquivo)
                    print(f"Arquivo de backup '{arquivo}' excluído com sucesso.")
        except Exception as e:
            print(f'Erro ao excluir arquivos de backup: {e}')

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
