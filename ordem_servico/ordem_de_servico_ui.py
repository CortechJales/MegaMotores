from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem

class OrdemDeServicoUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Ordens de Serviço")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table_os = QTableWidget()
        self.table_os.setColumnCount(4)
        self.table_os.setHorizontalHeaderLabels(['ID', 'Cliente', 'Produtos', 'Status'])
        layout.addWidget(self.table_os)

        btn_adicionar_os = QPushButton("Adicionar Ordem de Serviço")
        layout.addWidget(btn_adicionar_os)

        btn_editar_os = QPushButton("Editar Ordem de Serviço")
        layout.addWidget(btn_editar_os)

        btn_excluir_os = QPushButton("Excluir Ordem de Serviço")
        layout.addWidget(btn_excluir_os)

        btn_carregar_os = QPushButton("Carregar Ordens de Serviço")
        layout.addWidget(btn_carregar_os)
