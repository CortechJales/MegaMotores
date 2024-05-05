from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem

class ProdutoUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Produtos")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table_produtos = QTableWidget()
        self.table_produtos.setColumnCount(6)
        self.table_produtos.setHorizontalHeaderLabels(['ID', 'Nome', 'Descrição', 'Preço', 'Quantidade', 'Ativo'])
        layout.addWidget(self.table_produtos)

        btn_adicionar_produto = QPushButton("Adicionar Produto")
        layout.addWidget(btn_adicionar_produto)

        btn_editar_produto = QPushButton("Editar Produto")
        layout.addWidget(btn_editar_produto)

        btn_excluir_produto = QPushButton("Excluir Produto")
        layout.addWidget(btn_excluir_produto)

        btn_carregar_produtos = QPushButton("Carregar Produtos")
        layout.addWidget(btn_carregar_produtos)
