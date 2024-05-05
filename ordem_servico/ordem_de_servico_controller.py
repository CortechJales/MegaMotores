from ordem_de_servico import OrdemDeServico

class OrdemDeServicoController:
    def __init__(self):
        self.ordens_de_servico = []

    def adicionar_ordem_de_servico(self, ordem_de_servico):
        self.ordens_de_servico.append(ordem_de_servico)

    def editar_ordem_de_servico(self, id, cliente, produtos, status):
        for os in self.ordens_de_servico:
            if os.id == id:
                os.cliente = cliente
                os.produtos = produtos
                os.status = status
                break

    def excluir_ordem_de_servico(self, id):
        self.ordens_de_servico = [os for os in self.ordens_de_servico if os.id != id]

    def buscar_ordem_de_servico_por_id(self, id):
        for os in self.ordens_de_servico:
            if os.id == id:
                return os

    def carregar_ordens_de_servico(self):
        # Aqui você carrega as ordens de serviço do banco de dados para a lista self.ordens_de_servico
        # Por exemplo:
        # self.ordens_de_servico = [OrdemDeServico(1, "Cliente A", [...]), OrdemDeServico(2, "Cliente B", [...])]
        pass
