import bcrypt

# Senha em texto simples
senha_plana = "teste"

# Gerar o hash da senha
senha_hash = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt())

print("Hash da senha:", senha_hash)
