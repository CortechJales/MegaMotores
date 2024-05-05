from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem

class ClienteUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Clientes")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table_clientes = QTableWidget()
        self.table_clientes.setColumnCount(8)
        self.table_clientes.setHorizontalHeaderLabels(['ID', 'Nome', 'CEP', 'Endereço', 'Cidade', 'Estado', 'CPF/CNPJ', 'Telefone'])
        layout.addWidget(self.table_clientes)

        btn_adicionar_cliente = QPushButton("Adicionar Cliente")
        layout.addWidget(btn_adicionar_cliente)

        btn_editar_cliente = QPushButton("Editar Cliente")
        layout.addWidget(btn_editar_cliente)

        btn_excluir_cliente = QPushButton("Excluir Cliente")
        layout.addWidget(btn_excluir_cliente)

        btn_carregar_clientes = QPushButton("Carregar Clientes")
        layout.addWidget(btn_carregar_clientes)
