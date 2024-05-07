from PyQt5.QtWidgets import QWidget, QDialog,QFormLayout, QMessageBox, QCheckBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAction, QToolBar, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from cliente.cliente_controller import ClienteController

from cliente.equipamento_cliente_controller import EquipamentoClienteController

class ClienteUI(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ClienteController()
        
        self.controller_equipamento = EquipamentoClienteController()
        self.initUI()

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
        
        self.controller.create_table()       
        self.controller_equipamento.create_table()
        self.filter_active()

        # Adicionar evento de clique duplo na tabela de clientes
        self.client_table.doubleClicked.connect(self.show_cliente_details)
        

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
        clientes = self.controller.ListarCliente()
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
        clientes = self.controller.FiltrarCliente(True)
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
        clientes = self.controller.FiltrarCliente(False)
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
        self.controller.CadastrarCliente( nome, cep, endereco, cidade, estado, cpf_cnpj, telefone)
        self.filter_active()  # Atualizar a tabela após adicionar clientes

    def edit_cliente(self, nome, cep, endereco, cidade, estado, cpf_cnpj, telefone, id):
        self.controller.EditarCliente( nome, cep, endereco, cidade, estado, cpf_cnpj, telefone,id)
        self.filter_active()  # Atualizar a tabela após adicionar clientes


    def delete_cliente(self,id):
      
        selected_row = self.client_table.currentRow()
        if selected_row != -1:
            id = self.client_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir o cliente ID {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.controller.DeletarCliente(id)
                self.filter_active()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para excluir.")

    def inactive_cliente(self):
        selected_row = self.client_table.currentRow()
        if selected_row != -1:
            id = self.client_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja inativar o cliente código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller.ValidarCliente(id)
                if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 1:  # Verifica se o cliente está ativo
                        self.controller.InativarCliente(id)
                        self.filter_all()
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
                resultado = self.controller.ValidarCliente(id)
                if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 0:  # Verifica se o cliente está inativo
                        self.controller.AtivarCliente(id)
                        self.filter_all()
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

    def show_cliente_details(self):
        selected_row = self.client_table.currentRow()
        if selected_row != -1:
           
            cliente_info = {
            'Código': self.client_table.item(selected_row, 0).text(),   
            'nome': self.client_table.item(selected_row, 1).text(),
            'cep': self.client_table.item(selected_row, 2).text(),
            'endereco': self.client_table.item(selected_row, 3).text(),
            'cidade': self.client_table.item(selected_row, 4).text(),
            'estado': self.client_table.item(selected_row, 5).text(),
            'cpf_cnpj': self.client_table.item(selected_row, 6).text(),
            'telefone': self.client_table.item(selected_row, 7).text()
        }
            cliente_id = self.client_table.item(selected_row, 0).text()  
            equipamentos = self.controller_equipamento.ListarEquipamentoCliente(cliente_id)

            dialog = DetalhesClienteDialog(cliente_info, equipamentos)
            dialog.exec_()

        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para ver os detalhes.")
    
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
class DetalhesClienteDialog(QDialog):
    def __init__(self,cliente_info, equipamentos):
        super().__init__()
        
        self.controller_equipamento = EquipamentoClienteController()
        self.cliente_info = cliente_info

        self.setWindowTitle("Detalhes do Cliente")
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        for key, value in cliente_info.items():
            label = QLabel(key.capitalize() + ":")
            field = QLabel(str(value))  # Criando um QLabel para o valor correspondente
            form_layout.addRow(label, field)

        layout.addLayout(form_layout)

        equip_label = QLabel("Equipamentos:")
        layout.addWidget(equip_label)

        self.equip_table = QTableWidget()
        self.equip_table.setColumnCount(1)
        self.equip_table.setHorizontalHeaderLabels(['Descrição'])
        self.equip_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.equip_table.setRowCount(len(equipamentos))

        for row, equip in enumerate(equipamentos):
            descricao_item = QTableWidgetItem(equip['descricao'])
            self.equip_table.setItem(row, 0, descricao_item)

        layout.addWidget(self.equip_table)

        
        # Barra de ferramentas com botões de ação para os equipamentos
        equip_toolbar = QToolBar("Barra de Ferramentas")
        
        # Criando um layout horizontal para centralizar o botão
        h_layout = QHBoxLayout()
        h_layout.addStretch()  # Adiciona um espaço elástico à esquerda do botão
        
        # Botões de ação para os equipamentos
        action_add_equip = QAction("Adicionar Equipamento", self)
        equip_toolbar.addAction(action_add_equip)
        
        h_layout.addWidget(equip_toolbar)  # Adiciona a barra de ferramentas ao layout horizontal
        h_layout.addStretch()  # Adiciona um espaço elástico à direita do botão

        # Configurar conexões de sinais e slots para os botões dos equipamentos
        action_add_equip.triggered.connect(self.show_add_equipamento_dialog)

        layout.addLayout(h_layout)  # Adiciona o layout horizontal ao layout vertical principal

        self.setLayout(layout)

    # Métodos para manipulação de equipamentos...
    
    def add_equipamento(self,descricao):
       # Adiciona o novo equipamento à lista de equipamentos
       
        cliente_id = self.cliente_info['Código']
        
        # Obtém o ID do cliente
        self.controller_equipamento.CadastrarEquipamentoCliente(descricao,cliente_id)
        self.equipamentos = self.controller_equipamento.ListarEquipamentoCliente(cliente_id)
        # Atualiza a tabela de equipamentos
        self.update_equip_table()
   

        
    def update_equip_table(self):
        # Limpa a tabela de equipamentos
        self.equip_table.setRowCount(0)

        # Adiciona os equipamentos atualizados à tabela
        for row, equip in enumerate(self.equipamentos):
            descricao_item = QTableWidgetItem(equip['descricao'])
            self.equip_table.insertRow(row)
            self.equip_table.setItem(row, 0, descricao_item)
    
    def show_add_equipamento_dialog(self):
        dialog = AdicionarEditarEquipamentoDialog()
        if dialog.exec_():
            descricao = dialog.descricao.text()
            self.add_equipamento(descricao)
   
    
       
class AdicionarEditarEquipamentoDialog(QDialog):
    def __init__(self, descricao=""):
        super().__init__()
        self.setWindowTitle("Adicionar Equipamento")

        layout = QVBoxLayout()

        self.descricao = QLineEdit(descricao)
        self.descricao.setPlaceholderText("Descrição")
        layout.addWidget(self.descricao)

        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.accept)
        layout.addWidget(btn_salvar)

        self.setLayout(layout)  


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = ClienteUI()  
    ui.show()
    sys.exit(app.exec_())
