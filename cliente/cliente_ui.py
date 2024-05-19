from PyQt5.QtWidgets import QWidget, QDialog,QFormLayout, QMessageBox, QCheckBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QComboBox,QTableWidgetItem, QHeaderView, QAction, QToolBar, QApplication
from PyQt5.QtCore import Qt
from cliente.cliente_controller import ClienteController
from PyQt5.QtGui import QIcon
import re
import requests

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

        # Estilo para os botões de filtro
        filter_button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """

        if self.user_type == 'adm':
            self.btn_all = QPushButton("Todos")
            self.btn_all.setStyleSheet(filter_button_style)
            self.btn_all.clicked.connect(self.filter_all)
            filter_layout.addWidget(self.btn_all)

            self.btn_active = QPushButton("Ativos")
            self.btn_active.setStyleSheet(filter_button_style)
            self.btn_active.clicked.connect(self.filter_active)
            filter_layout.addWidget(self.btn_active)

            self.btn_inactive = QPushButton("Inativos")
            self.btn_inactive.setStyleSheet(filter_button_style)
            self.btn_inactive.clicked.connect(self.filter_inactive)
            filter_layout.addWidget(self.btn_inactive)

        layout.addLayout(filter_layout)

        # Tabela de clientes
        self.client_table = QTableWidget()
        self.client_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #3498db;
                padding: 5px;
                border-radius: 5px;
                color: #333;
            }
            
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                border: 1px solid #ddd;
            }
            QTableWidget::item {
                border: none;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #8fdefe;
                color: black;
            }
        """)
        self.client_table.setColumnCount(10)
        self.client_table.setHorizontalHeaderLabels(['Código', 'Nome', 'CEP', 'Endereço','Número', 'Cidade','Estado', 'CPF/CNPJ', 'Telefone','Ativo'])
        self.client_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.client_table)

        # Barra de ferramentas com botões de ação
        toolbar = QToolBar("Barra de Ferramentas")
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #ecf0f1;
                padding: 10px;
                border-radius: 10px;
            }
            QToolButton {
                background-color: #3498db;
                color: white;
                padding: 5px 10px;
                border: none;
                border-radius: 5px;
                margin-right: 5px;
            }
            QToolButton:hover {
                background-color: #2980b9;
            }
        """)
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
            
                if column_number == 9:  # Coluna 'Ativo'
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
            
                if column_number == 9:  # Coluna 'Ativo'
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
            
                if column_number == 9:  # Coluna 'Ativo'
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

    def add_cliente(self, nome, cep, endereco, numero, cidade, estado, cpf_cnpj, telefone):
        self.controller.CadastrarCliente( nome, cep, endereco, numero, cidade, estado, cpf_cnpj, telefone)
        self.filter_active()  # Atualizar a tabela após adicionar clientes

    def edit_cliente(self, nome, cep, endereco, numero,cidade, estado, cpf_cnpj, telefone, id):
        self.controller.EditarCliente( nome, cep, endereco,numero, cidade, estado, cpf_cnpj, telefone,id)
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
            numero = dialog.numero.text()
            cidade = dialog.cidade.text()
            estado = dialog.estado.currentText()
            cpf_cnpj = dialog.cpf_cnpj.text()
            telefone = dialog.telefone.text()
            self.add_cliente(nome, cep, endereco, numero, cidade, estado, cpf_cnpj, telefone)
   
    def show_edit_cliente_dialog(self):
        selected_row = self.client_table.currentRow()
        if selected_row != -1:
            id = self.client_table.item(selected_row, 0).text()
            nome = self.client_table.item(selected_row, 1).text()
            cep = self.client_table.item(selected_row, 2).text()
            endereco = self.client_table.item(selected_row, 3).text()
            numero = self.client_table.item(selected_row, 4).text()
            cidade = self.client_table.item(selected_row, 5).text()
            estado = self.client_table.item(selected_row, 6).text()
            cpf_cnpj = self.client_table.item(selected_row, 7).text()            
            telefone = self.client_table.item(selected_row, 8).text()
            dialog = AdicionarEditarClienteDialog(nome, cep, endereco,numero, cidade, estado, cpf_cnpj,telefone)
            if dialog.exec_():
                novo_nome = dialog.nome.text()
                novo_cep = dialog.cep.text()
                novo_endereco = dialog.endereco.text()
                novo_numero = dialog.numero.text()
                novo_cidade = dialog.cidade.text()
                novo_estado = dialog.estado.currentText()
                novo_cpf_cnpj = dialog.cpf_cnpj.text()
                novo_telefone = dialog.telefone.text()
                self.edit_cliente(novo_nome, novo_cep, novo_endereco,novo_numero, novo_cidade, novo_estado, novo_cpf_cnpj, novo_telefone,id)
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para editar.")

    def show_cliente_details(self):
        selected_row = self.client_table.currentRow()
        if selected_row != -1:
           
            cliente_info = {
            'Código': self.client_table.item(selected_row, 0).text(),   
            'Nome': self.client_table.item(selected_row, 1).text(),
            'Cep': self.client_table.item(selected_row, 2).text(),
            'endereco': self.client_table.item(selected_row, 3).text(),
            'Número': self.client_table.item(selected_row, 4).text(),
            'Cidade': self.client_table.item(selected_row, 5).text(),
            'Estado': self.client_table.item(selected_row, 6).text(),
            'Cpf_cnpj': self.client_table.item(selected_row, 7).text(),
            'Telefone': self.client_table.item(selected_row, 8).text()
        }
            cliente_id = self.client_table.item(selected_row, 0).text()  
            equipamentos = self.controller_equipamento.ListarEquipamentoCliente(cliente_id)

            dialog = DetalhesClienteDialog(cliente_info, equipamentos,self.user_type)
            dialog.exec_()

        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para ver os detalhes.")
    


class AdicionarEditarClienteDialog(QDialog):
    def __init__(self, nome="", cep="", endereco="", numero="", cidade="", estado="", cpf_cnpj="", telefone=""):
        super().__init__()
        self.setWindowTitle("Adicionar Cliente")
        self.setWindowIcon(QIcon("icon.png"))  # Adicione o ícone desejado

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Adicione margens para espaçamento

        form_layout = QFormLayout()

        self.nome = QLineEdit(nome)
        self.cep = QLineEdit(cep)
        self.endereco = QLineEdit(endereco)
        self.numero = QLineEdit(numero)
        self.cidade = QLineEdit(cidade)
        self.estado = QComboBox()
        self.cpf_cnpj = QLineEdit(cpf_cnpj)
        self.telefone = QLineEdit(telefone)

        # Estilo CSS para os campos de entrada
        style_sheet = """
            QLineEdit, QComboBox {
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #e74c3c;
            }
        """
        self.nome.setStyleSheet(style_sheet)
        self.cep.setStyleSheet(style_sheet)
        self.endereco.setStyleSheet(style_sheet)
        self.numero.setStyleSheet(style_sheet)
        self.cidade.setStyleSheet(style_sheet)
        self.estado.setStyleSheet(style_sheet)
        self.cpf_cnpj.setStyleSheet(style_sheet)
        self.telefone.setStyleSheet(style_sheet)

        # Adicionando siglas dos estados ao QComboBox
        estados_brasileiros = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
            "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
            "SP", "SE", "TO"
        ]
        self.estado.addItems(estados_brasileiros)

        form_layout.addRow(QLabel("Nome:"), self.nome)
        form_layout.addRow(QLabel("CEP:"), self.cep)
        form_layout.addRow(QLabel("Endereço:"), self.endereco)
        form_layout.addRow(QLabel("Número:"), self.numero)
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
        btn_salvar.clicked.connect(self.on_save)
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_salvar)
        button_layout.addWidget(btn_cancelar)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Conectar sinal de edição de CEP ao método de preenchimento automático
        self.cep.textChanged.connect(self.auto_fill_address)

        # Aplicar máscara ao CPF/CNPJ
        self.cpf_cnpj.setInputMask('000.000.000-00;_')
        
        self.cep.setInputMask('00000-000;_')

        # Aplicar máscara ao telefone
        self.telefone.setInputMask('(00)00000-0000;_')

    def on_save(self):
        if not self.validate_fields():
            return

        self.accept()

    def validate_fields(self):
        # Verificar se todos os campos estão preenchidos
        if not all([self.nome.text(), self.cep.text(), self.endereco.text(), self.numero.text(), self.cidade.text(), self.estado.currentText(), self.cpf_cnpj.text(), self.telefone.text()]):
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return False

        # Verificar formato do CEP
        if not re.match(r'^\d{5}-\d{3}$', self.cep.text()):
            QMessageBox.warning(self, "Erro", "CEP inválido. Use o formato 00000-000.")
            return False

        # Verificar formato do CPF/CNPJ
        if not (self.validate_cpf(self.cpf_cnpj.text()) or self.validate_cnpj(self.cpf_cnpj.text())):
            QMessageBox.warning(self, "Erro", "CPF/CNPJ inválido.")
            return False

        return True

    def validate_cpf(self, cpf):
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11:
            return False

        def calculate_digit(digits):
            s = sum(int(digit) * i for digit, i in zip(digits, range(len(digits)+1, 1, -1)))
            d = 11 - s % 11
            return str(d if d < 10 else 0)

        first_nine_digits = cpf[:9]
        cpf_10 = first_nine_digits + calculate_digit(first_nine_digits)
        cpf_11 = cpf_10 + calculate_digit(cpf_10)

        return cpf == cpf_11

    def validate_cnpj(self, cnpj):
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) != 14:
            return False

        def calculate_digit(digits):
            s = sum(int(digit) * weight for digit, weight in zip(digits, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]))
            d = 11 - s % 11
            return str(d if d < 10 else 0)

        first_twelve_digits = cnpj[:12]
        cnpj_13 = first_twelve_digits + calculate_digit(first_twelve_digits)
        cnpj_14 = cnpj_13 + calculate_digit(cnpj_13)

        return cnpj == cnpj_14

    def auto_fill_address(self):
        cep = self.cep.text().replace("-", "")
        if len(cep) == 8:
            try:
                response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
                data = response.json()
                if "erro" not in data:
                    self.endereco.setText(data.get("logradouro", ""))
                    self.cidade.setText(data.get("localidade", ""))
                    estado = data.get("uf", "")
                    index = self.estado.findText(estado)
                    if index != -1:
                        self.estado.setCurrentIndex(index)
            except requests.exceptions.RequestException:
                pass
class DetalhesClienteDialog(QDialog):
    def __init__(self, cliente_info, equipamentos, user_type):
        super().__init__()

        self.cliente_info = cliente_info
        self.equipamentos = equipamentos
        self.user_type = user_type
        self.controller_equipamento = EquipamentoClienteController()  # Adicionando o atributo controller_equipamento

        self.setWindowTitle("Detalhes do Cliente")
        self.setWindowIcon(QIcon("img/megamotores.png"))

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        form_layout = QFormLayout()

        self.campos_cliente = {}

        for key, value in cliente_info.items():
            label = QLabel(key.capitalize() + ":")
            field = QLineEdit(str(value))
            field.setReadOnly(True)
            field.setStyleSheet("background-color: white; border: 2px solid #3498db; padding: 5px; border-radius: 5px; color: #333;")
            self.campos_cliente[key] = field
            form_layout.addRow(label, field)

        layout.addLayout(form_layout)

        equip_label = QLabel("Equipamentos:")
        layout.addWidget(equip_label)

        self.equip_table = QTableWidget()
        self.equip_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #3498db;
                padding: 5px;
                border-radius: 5px;
                color: #333;
            }
            
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                border: 1px solid #ddd;
            }
            QTableWidget::item {
                border: none;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #8fdefe;
                color: black;
            }
        """)
        self.equip_table.setColumnCount(2)  # Adicionando uma coluna extra para a ID do equipamento
        self.equip_table.setHorizontalHeaderLabels(['Código', 'Descrição'])
        self.equip_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.equip_table.verticalHeader().setVisible(False)
        cliente_id = self.cliente_info['Código']
        self.equipamentos = self.controller_equipamento.ListarEquipamentoCliente(cliente_id)
        self.update_equip_table()
        
        
        layout.addWidget(self.equip_table)

        # Barra de ferramentas com botões de ação
        toolbar = QToolBar("Barra de Ferramentas")
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #ecf0f1;
                padding: 10px;
                border-radius: 10px;
            }
            QToolButton {
                background-color: #3498db;
                color: white;
                padding: 5px 10px;
                border: none;
                border-radius: 5px;
                margin-right: 5px;
            }
            QToolButton:hover {
                background-color: #2980b9;
            }
        """)
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
            action_add.triggered.connect(self.show_add_equipamento_dialog)
            action_edit.triggered.connect(self.show_edit_equipamento_dialog)
            action_delete.triggered.connect(self.delete_equipamento)
            action_inactive.triggered.connect(self.inactive_equipamento)
            action_ative.triggered.connect(self.ative_equipamento)

        elif self.user_type == 'usr':
            # Botões de ação
            action_add = QAction("Adicionar", self)
            action_edit = QAction("Editar", self)
            action_inactive = QAction("Inativar", self)

            toolbar.addAction(action_add)
            toolbar.addAction(action_edit)
            toolbar.addAction(action_inactive)   

            # Configurar conexões de sinais e slots para os botões
            action_add.triggered.connect(self.show_add_equipamento_dialog)
            action_edit.triggered.connect(self.show_edit_equipamento_dialog)
            action_inactive.triggered.connect(self.inactive_equipamento)

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
