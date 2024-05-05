from produto import Produto

class ProdutoController:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    def editar_produto(self, id, nome, descricao, preco, quantidade):
        for produto in self.produtos:
            if produto.id == id:
                produto.nome = nome
                produto.descricao = descricao
                produto.preco = preco
                produto.quantidade = quantidade
                break

    def excluir_produto(self, id):
        self.produtos = [produto for produto in self.produtos if produto.id != id]

    def buscar_produto_por_id(self, id):
        for produto in self.produtos:
            if produto.id == id:
                return produto

    def carregar_produtos(self):
        # Aqui você carrega os produtos do banco de dados para a lista self.produtos
        # Por exemplo:
        # self.produtos = [Produto(1, "Produto A", ...), Produto(2, "Produto B", ...)]
        pass
