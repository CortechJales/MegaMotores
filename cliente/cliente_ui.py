from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox,QCheckBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAction, QToolBar, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from database.database import Database

class ClienteUI(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database('database/gerenciamento_ordens_servico.db')  # Conectar ao banco de dados
        self.create_table()
        self.initUI()
    
    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        cep TEXT,
        endereco TEXT,
        cidade TEXT,
        estado TEXT,
        cpf_cnpj TEXT,
        telefone TEXT,
        ativo BOOLEAN
        )
        '''
        self.db.create_table(sql)

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout()

        # Layout do filtro
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar por nome:"))
        self.filter_input = QLineEdit()
        self.filter_input.textChanged.connect(self.filter_table)
        filter_layout.addWidget(self.filter_input)
        
        # Botões de filtro
        self.btn_all = QPushButton("Todos")
        self.btn_all.clicked.connect(self.filter_all)
        filter_layout.addWidget(self.btn_all)

        self.btn_active = QPushButton("Ativos")
        self.btn_active.clicked.connect(self.filter_active)
        filter_layout.addWidget(self.btn_active)

        self.btn_inactive = QPushButton("Inativos")
        self.btn_inactive.clicked.connect(self.filter_inactive)
        filter_layout.addWidget(self.btn_inactive)

        layout.addLayout(filter_layout)

        # Tabela de clientes
        self.client_table = QTableWidget()
        self.client_table.setColumnCount(9)
        self.client_table.setHorizontalHeaderLabels(['Código', 'Nome', 'CEP', 'Endereço', 'Cidade','Estado', 'CPF/CNPJ', 'Telefone','Ativo'])
        self.client_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.client_table)

        # Barra de ferramentas com botões de ação
        toolbar = QToolBar("Barra de Ferramentas")
        layout.addWidget(toolbar)

        # Botões de ação
        action_add = QAction("Adicionar", self)
        action_edit = QAction("Editar", self)
        action_delete = QAction("Excluir", self)
        action_inactive = QAction("Inativar", self)
        action_ative = QAction("Reativar", self)

        toolbar.addAction(action_add)
        toolbar.addAction(action_edit)
        toolbar.addAction(action_delete)
        toolbar.addAction(action_inactive)        
        toolbar.addAction(action_ative)

        # Configurar conexões de sinais e slots para os botões
        action_add.triggered.connect(self.show_add_cliente_dialog)
        action_edit.triggered.connect(self.show_edit_cliente_dialog)
        action_delete.triggered.connect(self.delete_cliente)
        action_inactive.triggered.connect(self.inactive_cliente)
        action_ative.triggered.connect(self.ative_cliente)

        self.setLayout(layout)
        self.filter_active()

    def filter_table(self):
        filter_text = self.filter_input.text().lower()
        for row in range(self.client_table.rowCount()):
            match = False
            for col in range(self.client_table.columnCount()):
                item = self.client_table.item(row, col)
                if item is not None and item.text().lower().find(filter_text) != -1:
                    match = True
                    break
            self.client_table.setRowHidden(row, not match)

    def filter_all(self):
        query = 'SELECT * FROM cliente'
        clientes = self.db.execute_query(query)
        self.client_table.setRowCount(0)
    
        for row_number, cliente in enumerate(clientes):
            self.client_table.insertRow(row_number)
        
            for column_number, data in enumerate(cliente):
                item = QTableWidgetItem(str(data))
            
                if column_number == 8:  # Coluna 'Ativo'
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.client_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.client_table.setItem(row_number, column_number, item)

    def filter_active(self):
        query = 'SELECT * FROM cliente where ativo=?'
        data = (True,)
        clientes = self.db.execute_query(query, data)
        self.client_table.setRowCount(0)
    
        for row_number, cliente in enumerate(clientes):
            self.client_table.insertRow(row_number)
        
            for column_number, data in enumerate(cliente):
                item = QTableWidgetItem(str(data))
            
                if column_number == 8:  # Coluna 'Ativo'
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.client_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.client_table.setItem(row_number, column_number, item)

    def filter_inactive(self):
        query = 'SELECT * FROM cliente where ativo=?'
        data = (False,)
        clientes = self.db.execute_query(query, data)
        self.client_table.setRowCount(0)
    
        for row_number, cliente in enumerate(clientes):
            self.client_table.insertRow(row_number)
        
            for column_number, data in enumerate(cliente):
                item = QTableWidgetItem(str(data))
            
                if column_number == 8:  # Coluna 'Ativo'
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.client_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.client_table.setItem(row_number, column_number, item)


    def add_cliente(self, nome, cep, endereco, cidade, estado, cpf_cnpj, telefone):
        query = 'INSERT INTO cliente (nome, cep, endereco, cidade, estado, cpf_cnpj,telefone,ativo) VALUES (?, ?, ?, ?,?, ?, ?, ?)'
        data = (nome, cep, endereco, cidade, estado, cpf_cnpj, telefone, True)
        self.db.execute_query_no_return(query, data)
        self.filter_active()  # Atualizar a tabela após adicionar cliente

    def edit_cliente(self, nome, cep, endereco, cidade, estado, cpf_cnpj, telefone, id):
        query = 'UPDATE cliente SET nome=?, cep=?, endereco=?, cidade=?, estado=?, cpf_cnpj=?, telefone=? WHERE id=?'
        data = (nome, cep, endereco, cidade, estado, cpf_cnpj, telefone, id)
        self.db.execute_query_no_return(query, data)
        self.filter_active()

    def delete_cliente(self):
        # Implemente a lógica para excluir um cliente selecionado na tabela
        pass

    def inactive_cliente(self):
        selected_row = self.client_table.currentRow()
        if selected_row != -1:
            id = self.client_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja inativar o cliente código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                query = 'SELECT ativo FROM cliente WHERE id=?'
                data = (id,)
                resultado = self.db.execute_query(query, data)
                if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 1:  # Verifica se o cliente está ativo
                        query = 'UPDATE cliente SET ativo=? WHERE id=?'
                        data = (0, id)
                        self.db.execute_query_no_return(query, data)
                        self.filter_inactive()
                    else:
                        QMessageBox.warning(self, "Aviso", "Cliente já está inativo.")
                else:
                    QMessageBox.warning(self, "Aviso", "Cliente não encontrado.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para inativar.")
    
    
    def ative_cliente(self):
        selected_row = self.client_table.currentRow()
        if selected_row != -1:
            id = self.client_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja reativar o cliente código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                query = 'SELECT ativo FROM cliente WHERE id=?'
                data = (id)
                resultado=self.db.execute_query(query, data)
                if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 0:  # Verifica se o cliente está ativo
                        query = 'UPDATE cliente SET ativo=? WHERE id=?'
                        data = (1, id)
                        self.db.execute_query_no_return(query, data)
                        self.filter_active()
                    else:
                        QMessageBox.warning(self, "Aviso", "Cliente já está Ativo.")
                else:
                    QMessageBox.warning(self, "Aviso", "Cliente não encontrado.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para Ativar.")   

    
           

    def show_add_cliente_dialog(self):
        dialog = AdicionarEditarClienteDialog()
        if dialog.exec_():
            nome = dialog.nome.text()
            cep = dialog.cep.text()
            endereco = dialog.endereco.text()
            cidade = dialog.cidade.text()
            estado = dialog.estado.text()
            cpf_cnpj = dialog.cpf_cnpj.text()
            telefone = dialog.telefone.text()
            self.add_cliente(nome, cep, endereco, cidade, estado, cpf_cnpj, telefone)
   
    def show_edit_cliente_dialog(self):
        selected_row = self.client_table.currentRow()
        if selected_row != -1:
            id = self.client_table.item(selected_row, 0).text()
            nome = self.client_table.item(selected_row, 1).text()
            cep = self.client_table.item(selected_row, 2).text()
            endereco = self.client_table.item(selected_row, 3).text()
            cidade = self.client_table.item(selected_row, 4).text()
            estado = self.client_table.item(selected_row, 5).text()
            cpf_cnpj = self.client_table.item(selected_row, 6).text()            
            telefone = self.client_table.item(selected_row, 7).text()
            dialog = AdicionarEditarClienteDialog(nome, cep, endereco, cidade, estado, cpf_cnpj,telefone)
            if dialog.exec_():
                novo_nome = dialog.nome.text()
                novo_cep = dialog.cep.text()
                novo_endereco = dialog.endereco.text()
                novo_cidade = dialog.cidade.text()
                novo_estado = dialog.estado.text()
                novo_cpf_cnpj = dialog.cpf_cnpj.text()
                novo_telefone = dialog.telefone.text()
                self.edit_cliente(novo_nome, novo_cep, novo_endereco, novo_cidade, novo_estado, novo_cpf_cnpj, novo_telefone,id)
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para editar.")


class AdicionarEditarClienteDialog(QDialog):
    def __init__(self, nome="", cep="", endereco="", cidade="", estado="", cpf_cnpj="", telefone=""):
        super().__init__()
        self.setWindowTitle("Adicionar Cliente")

        layout = QVBoxLayout()

        self.nome = QLineEdit(nome)
        self.nome.setPlaceholderText("Nome")
        layout.addWidget(self.nome)

        self.cep = QLineEdit(cep)
        self.cep.setPlaceholderText("CEP")
        layout.addWidget(self.cep)

        self.endereco = QLineEdit(endereco)
        self.endereco.setPlaceholderText("Endereço")
        layout.addWidget(self.endereco)

        self.cidade = QLineEdit(cidade)
        self.cidade.setPlaceholderText("Cidade")
        layout.addWidget(self.cidade)

        self.estado = QLineEdit(estado)
        self.estado.setPlaceholderText("Estado")
        layout.addWidget(self.estado)

        self.cpf_cnpj = QLineEdit(cpf_cnpj)
        self.cpf_cnpj.setPlaceholderText("CPF/CNPJ")
        layout.addWidget(self.cpf_cnpj)

        self.telefone = QLineEdit(telefone)
        self.telefone.setPlaceholderText("Telefone")
        layout.addWidget(self.telefone)

        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.accept)
        layout.addWidget(btn_salvar)

        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = ClienteUI()
    ui.carregar_clientes()  # Carregar clientes ao iniciar a aplicação
    ui.show()
    sys.exit(app.exec_())
