class Cliente:
    def __init__(self, id, nome, cep, endereco, cidade, estado, cpf_cnpj, telefone, ativo=True):
        self.id = id
        self.nome = nome
        self.cep = cep
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.cpf_cnpj = cpf_cnpj
        self.telefone = telefone
        self.ativo = ativo
