class Produto:
    def __init__(self, id, nome, descricao, preco, quantidade, ativo=True):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade
        self.ativo = ativo
