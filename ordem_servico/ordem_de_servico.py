class OrdemDeServico:
    def __init__(self, id, cliente, produtos, status="Aberta"):
        self.id = id
        self.cliente = cliente
        self.produtos = produtos
        self.status = status
