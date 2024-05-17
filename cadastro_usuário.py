import sqlite3
import bcrypt

# Senha em texto simples
senha_plana = "usuario"

# Gerar o hash da senha
senha_hash = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt())

print("Hash da senha:", senha_hash)
conn = sqlite3.connect('database/gerenciamento_ordens_servico.db')
cursor = conn.cursor()
nome_usuario = "usuario"
tipo_usuario = "usr"  # Se este for um usuário administrador

# Inserir os dados do usuário no banco de dados
cursor.execute("INSERT INTO usuario (username, password, tipo_usuario, ativo) VALUES (?, ?, ?, 1)",
               (nome_usuario, senha_hash, tipo_usuario))
conn.commit()

print("Usuário cadastrado com sucesso.")