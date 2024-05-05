from cliente import Cliente

class ClienteController:
    def __init__(self):
        self.clientes = []

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def editar_cliente(self, id, nome, cep, endereco, cidade, estado, cpf_cnpj, telefone):
        for cliente in self.clientes:
            if cliente.id == id:
                cliente.nome = nome
                cliente.cep = cep
                cliente.endereco = endereco
                cliente.cidade = cidade
                cliente.estado = estado
                cliente.cpf_cnpj = cpf_cnpj
                cliente.telefone = telefone
                break

    def excluir_cliente(self, id):
        self.clientes = [cliente for cliente in self.clientes if cliente.id != id]

    def buscar_cliente_por_id(self, id):
        for cliente in self.clientes:
            if cliente.id == id:
                return cliente

    def carregar_clientes(self):
        # Aqui você carrega os clientes do banco de dados para a lista self.clientes
        # Por exemplo:
        # self.clientes = [Cliente(1, "Cliente A", ...), Cliente(2, "Cliente B", ...)]
        pass
