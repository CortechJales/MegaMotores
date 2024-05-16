from PyQt5.QtWidgets import QWidget, QDialog,QFormLayout, QMessageBox, QCheckBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAction, QToolBar, QApplication
from PyQt5.QtCore import Qt
from cliente.cliente_controller import ClienteController
from PyQt5.QtGui import QIcon

from cliente.equipamento_cliente_controller import EquipamentoClienteController

class ClienteUI(QWidget):
    def __init__(self,user_type):
        super().__init__()
        self.controller = ClienteController()
        
        self.controller_equipamento = EquipamentoClienteController()
        
        self.user_type= user_type
        self.initUI()
        
        print(f"tipo que chegou na cliente: {user_type}")

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout()

        # Layout do filtro
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar por nome:"))
        self.filter_input = QLineEdit()
        self.filter_input.textChanged.connect(self.filter_table)
        filter_layout.addWidget(self.filter_input)
        if self.user_type == 'adm':
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
        
        if self.user_type == 'adm':
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
        if self.user_type == 'usr':
            # Botões de ação
            action_add = QAction("Adicionar", self)
            action_edit = QAction("Editar", self)
            action_inactive = QAction("Inativar", self)

            toolbar.addAction(action_add)
            toolbar.addAction(action_edit)
            toolbar.addAction(action_inactive)   

        # Configurar conexões de sinais e slots para os botões
            action_add.triggered.connect(self.show_add_cliente_dialog)
            action_edit.triggered.connect(self.show_edit_cliente_dialog)
            action_inactive.triggered.connect(self.inactive_cliente)

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
                        self.filter_active()
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

            dialog = DetalhesClienteDialog(cliente_info, equipamentos,self.user_type)
            dialog.exec_()

        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para ver os detalhes.")
    

class AdicionarEditarClienteDialog(QDialog):
    def __init__(self, nome="", cep="", endereco="", cidade="", estado="", cpf_cnpj="", telefone=""):
        super().__init__()
        self.setWindowTitle("Adicionar Cliente")
        self.setWindowIcon(QIcon("icon.png"))  # Adicione o ícone desejado

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Adicione margens para espaçamento

        form_layout = QFormLayout()

        self.nome = QLineEdit(nome)
        self.cep = QLineEdit(cep)
        self.endereco = QLineEdit(endereco)
        self.cidade = QLineEdit(cidade)
        self.estado = QLineEdit(estado)
        self.cpf_cnpj = QLineEdit(cpf_cnpj)
        self.telefone = QLineEdit(telefone)

        # Estilo CSS para os campos de entrada
        style_sheet = """
            QLineEdit {
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #e74c3c;
            }
        """
        self.nome.setStyleSheet(style_sheet)
        self.cep.setStyleSheet(style_sheet)
        self.endereco.setStyleSheet(style_sheet)
        self.cidade.setStyleSheet(style_sheet)
        self.estado.setStyleSheet(style_sheet)
        self.cpf_cnpj.setStyleSheet(style_sheet)
        self.telefone.setStyleSheet(style_sheet)

        form_layout.addRow(QLabel("Nome:"), self.nome)
        form_layout.addRow(QLabel("CEP:"), self.cep)
        form_layout.addRow(QLabel("Endereço:"), self.endereco)
        form_layout.addRow(QLabel("Cidade:"), self.cidade)
        form_layout.addRow(QLabel("Estado:"), self.estado)
        form_layout.addRow(QLabel("CPF/CNPJ:"), self.cpf_cnpj)
        form_layout.addRow(QLabel("Telefone:"), self.telefone)

        layout.addLayout(form_layout)

        # Adicione um layout de botão para alinhar os botões horizontalmente
        button_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_cancelar = QPushButton("Cancelar")
        btn_salvar.setStyleSheet("background-color: #2ecc71; color: white; border-radius: 10px; padding: 10px;")
        btn_cancelar.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 10px; padding: 10px;")
        btn_salvar.clicked.connect(self.accept)
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_salvar)
        button_layout.addWidget(btn_cancelar)

        layout.addLayout(button_layout)

        self.setLayout(layout)
class DetalhesClienteDialog(QDialog):
    def __init__(self, cliente_info, equipamentos, user_type):
        super().__init__()

        self.cliente_info = cliente_info
        self.equipamentos = equipamentos
        self.user_type = user_type
        self.controller_equipamento = EquipamentoClienteController()  # Adicionando o atributo controller_equipamento

        self.setWindowTitle("Detalhes do Cliente")
        self.setWindowIcon(QIcon("icon.png"))

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        form_layout = QFormLayout()

        self.campos_cliente = {}

        for key, value in cliente_info.items():
            label = QLabel(key.capitalize() + ":")
            field = QLineEdit(str(value))
            field.setReadOnly(True)
            field.setStyleSheet("background-color: white; border: 2px solid #3498db; padding: 5px; border-radius: 5px;")
            self.campos_cliente[key] = field
            form_layout.addRow(label, field)

        layout.addLayout(form_layout)

        equip_label = QLabel("Equipamentos:")
        layout.addWidget(equip_label)

        self.equip_table = QTableWidget()
        self.equip_table.setColumnCount(2)  # Adicionando uma coluna extra para a ID do equipamento
        self.equip_table.setHorizontalHeaderLabels(['Código', 'Descrição'])
        self.equip_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.equip_table.setRowCount(len(equipamentos))

        for row, equip in enumerate(equipamentos):
            id_item = QTableWidgetItem(str(equip['id']))  # Adicionando a ID do equipamento
            descricao_item = QTableWidgetItem(equip['descricao'])
            self.equip_table.setItem(row, 0, id_item)  # Adicionando a ID na primeira coluna
            self.equip_table.setItem(row, 1, descricao_item)

        layout.addWidget(self.equip_table)

        # Barra de ferramentas com botões de ação para os equipamentos
        equip_toolbar = QToolBar("Barra de Ferramentas")
        equip_toolbar.setStyleSheet("background-color: #ecf0f1; padding: 10px; border-radius: 10px;")

        if self.user_type == 'adm':
            # Botões de ação para os equipamentos
            action_add_equip = QAction("Adicionar", self)
            action_edit_equip = QAction("Editar", self)
            action_delete_equip = QAction("Excluir", self)
            action_inactive_equip = QAction("Inativar", self)
            action_ative_equip = QAction("Reativar", self)

            equip_toolbar.addAction(action_add_equip)
            equip_toolbar.addAction(action_edit_equip)
            equip_toolbar.addAction(action_delete_equip)
            equip_toolbar.addAction(action_inactive_equip)
            equip_toolbar.addAction(action_ative_equip)

            # Configurar conexões de sinais e slots para os botões dos equipamentos
            action_add_equip.triggered.connect(self.show_add_equipamento_dialog)
            action_edit_equip.triggered.connect(self.show_edit_equipamento_dialog)
            action_delete_equip.triggered.connect(self.delete_equipamento)
            action_inactive_equip.triggered.connect(self.inactive_equipamento)
            action_ative_equip.triggered.connect(self.ative_equipamento)

        elif self.user_type == 'usr':
            # Botões de ação para os equipamentos
            action_add_equip = QAction("Adicionar", self)
            action_edit_equip = QAction("Editar", self)
            action_inactive_equip = QAction("Inativar", self)

            equip_toolbar.addAction(action_add_equip)
            equip_toolbar.addAction(action_edit_equip)
            equip_toolbar.addAction(action_inactive_equip)

            # Configurar conexões de sinais e slots para os botões dos equipamentos
            action_add_equip.triggered.connect(self.show_add_equipamento_dialog)
            action_edit_equip.triggered.connect(self.show_edit_equipamento_dialog)
            action_inactive_equip.triggered.connect(self.inactive_equipamento)

        layout.addWidget(equip_toolbar)

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
   
    def edit_equipamento(self, descricao, id):
        self.controller_equipamento.EditarequipamentoCliente( descricao,id)
        cliente_id = self.cliente_info['Código']
        self.equipamentos = self.controller_equipamento.ListarEquipamentoCliente(cliente_id)
        self.update_equip_table()  # Atualizar a tabela após adicionar clientes


    def delete_equipamento(self,id):
      
        selected_row = self.equip_table.currentRow()
        if selected_row != -1:
            id = self.equip_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir o equipamento Código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.controller_equipamento.DeletarEquipamentoCliente(id)
                cliente_id = self.cliente_info['Código']
                self.equipamentos = self.controller_equipamento.ListarEquipamentoCliente(cliente_id)
                self.update_equip_table()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para excluir.")

    def inactive_equipamento(self):
        selected_row = self.equip_table.currentRow()
        if selected_row != -1:
            id = self.equip_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja inativar o equipamento código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller_equipamento.ValidarEquipamentoCliente(id)
                if resultado:
                    estado_equipamento = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_equipamento == 1:  # Verifica se o cliente está ativo
                        self.controller_equipamento.InativarEquipamentoCliente(id)
                        cliente_id = self.cliente_info['Código']
                        self.equipamentos = self.controller_equipamento.ListarEquipamentoCliente(cliente_id)
                        self.update_equip_table()
                    else:
                        QMessageBox.warning(self, "Aviso", "Equipamento já está inativo.")
                else:
                    QMessageBox.warning(self, "Aviso", "Equipamento não encontrado.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um Equipamento para inativar.")
 
    def ative_equipamento(self):
        selected_row = self.equip_table.currentRow()
        if selected_row != -1:
            id = self.equip_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja reativar o equipamento código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller_equipamento.ValidarEquipamentoCliente(id)
                if resultado:
                    estado_equipamento = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_equipamento == 0:  # Verifica se o cliente está inativo
                        self.controller_equipamento.AtivarEquipamentoCliente(id)
                        cliente_id = self.cliente_info['Código']
                        self.equipamentos = self.controller_equipamento.ListarEquipamentoCliente(cliente_id)
                        self.update_equip_table()
                        
                    else:
                        QMessageBox.warning(self, "Aviso", "Equipamento já está Ativo.")
                else:
                    QMessageBox.warning(self, "Aviso", "Equipamento não encontrado.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um Equipamento para Ativar.")
        
    def update_equip_table(self):
        # Limpa a tabela de equipamentos
        self.equip_table.setRowCount(0)

        # Define o número de linhas da tabela para corresponder ao número de equipamentos
        self.equip_table.setRowCount(len(self.equipamentos))

        # Adiciona os equipamentos atualizados à tabela
        for row, equip in enumerate(self.equipamentos):
            id_item = QTableWidgetItem(str(equip['id']))  # Adicionando a ID do equipamento
            descricao_item = QTableWidgetItem(equip['descricao'])
            self.equip_table.setItem(row, 0, id_item)  # Adicionando a ID na primeira coluna
            self.equip_table.setItem(row, 1, descricao_item)

    def show_add_equipamento_dialog(self):
        dialog = AdicionarEditarEquipamentoDialog()
        if dialog.exec_():
            descricao = dialog.descricao.text()
            self.add_equipamento(descricao)
    
    def show_edit_equipamento_dialog(self):
        selected_row = self.equip_table.currentRow()
        if selected_row != -1:
            id = self.equip_table.item(selected_row, 0).text()
            descricao = self.equip_table.item(selected_row, 1).text()
            
            dialog = AdicionarEditarEquipamentoDialog(descricao)
            if dialog.exec_():
                novo_descricao = dialog.descricao.text()
                
                self.edit_equipamento(novo_descricao,id)
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um Equipamento para editar.")
   
    
       
class AdicionarEditarEquipamentoDialog(QDialog):
    def __init__(self, descricao=""):
        super().__init__()
        self.setWindowTitle("Adicionar Equipamento")
        self.setWindowIcon(QIcon("icon.png"))

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        form_layout = QFormLayout()

        
        self.descricao = QLineEdit(descricao)

        style_sheet = """
            QLineEdit {
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #e74c3c;
            }
        """
        self.descricao.setStyleSheet(style_sheet)
        form_layout.addRow(QLabel("Descrição:"), self.descricao)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_cancelar = QPushButton("Cancelar")
        btn_salvar.setStyleSheet("background-color: #2ecc71; color: white; border-radius: 10px; padding: 10px;")
        btn_cancelar.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 10px; padding: 10px;")
        btn_salvar.clicked.connect(self.accept)
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_salvar)
        button_layout.addWidget(btn_cancelar)

        layout.addLayout(button_layout)

        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = ClienteUI()  
    ui.show()
    sys.exit(app.exec_())
