from PyQt5.QtWidgets import QWidget, QDialog,QFormLayout, QMessageBox, QCheckBox,QRadioButton, QButtonGroup, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QComboBox,QTableWidgetItem, QHeaderView, QAction, QToolBar, QApplication
from PyQt5.QtCore import Qt,QRegExp
from cliente.equipamento_cliente_controller import EquipamentoClienteController
from cliente.cliente_controller import ClienteController
from marca.marca_controller import MarcaController
from PyQt5.QtGui import QIcon
import re
import requests
import os


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
        self.client_table.setColumnCount(11)
        self.client_table.setHorizontalHeaderLabels(['Código', 'Nome', 'CEP', 'Endereço','Número', 'Cidade','Estado', 'CPF/CNPJ', 'Telefone','Telefone 2','Ativo'])
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
            
                if column_number == 10:  # Coluna 'Ativo'
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
            
                if column_number == 10:  # Coluna 'Ativo'
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
            
                if column_number == 10:  # Coluna 'Ativo'
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

    def add_cliente(self, nome, cep, endereco, numero, cidade, estado, cpf_cnpj, telefone,telefone2):
        self.controller.CadastrarCliente( nome, cep, endereco, numero, cidade, estado, cpf_cnpj, telefone,telefone2)
        self.filter_active()  # Atualizar a tabela após adicionar clientes

    def edit_cliente(self, nome, cep, endereco, numero,cidade, estado, cpf_cnpj, telefone,telefone2, id):
        self.controller.EditarCliente( nome, cep, endereco,numero, cidade, estado, cpf_cnpj, telefone,telefone2,id)
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
            telefone2 = dialog.telefone2.text()
            self.add_cliente(nome, cep, endereco, numero, cidade, estado, cpf_cnpj, telefone,telefone2)
   
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
            telefone2 = self.client_table.item(selected_row, 9).text()
            dialog = AdicionarEditarClienteDialog(nome, cep, endereco,numero, cidade, estado, cpf_cnpj,telefone,telefone2)
            if dialog.exec_():
                novo_nome = dialog.nome.text()
                novo_cep = dialog.cep.text()
                novo_endereco = dialog.endereco.text()
                novo_numero = dialog.numero.text()
                novo_cidade = dialog.cidade.text()
                novo_estado = dialog.estado.currentText()
                novo_cpf_cnpj = dialog.cpf_cnpj.text()
                novo_telefone = dialog.telefone.text()
                novo_telefone2 = dialog.telefone2.text()
                self.edit_cliente(novo_nome, novo_cep, novo_endereco,novo_numero, novo_cidade, novo_estado, novo_cpf_cnpj, novo_telefone,novo_telefone2,id)
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
            'Telefone': self.client_table.item(selected_row, 8).text(),
            'Telefone 2': self.client_table.item(selected_row, 9).text()
        }
            cliente_id = self.client_table.item(selected_row, 0).text()  
            equipamentos = self.controller_equipamento.ListarEquipamentoCliente(cliente_id)

            dialog = DetalhesClienteDialog(cliente_info, equipamentos, self.user_type)
        
        # Definindo o tamanho mínimo e máximo da janela
            dialog.setMinimumSize(700, 500)  # Defina o tamanho mínimo desejado
            dialog.setMaximumSize(900, 700)  # Defina o tamanho máximo desejado

            dialog.exec_()

        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para ver os detalhes.")
    



class AdicionarEditarClienteDialog(QDialog):
    def __init__(self, nome="", cep="", endereco="", numero="", cidade="", estado="", cpf_cnpj="", telefone="", telefone2=""):
        super().__init__()
        self.setWindowTitle("Adicionar Cliente")
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Subindo um nível para acessar a pasta img
        pasta_img = os.path.join(diretorio_atual, '..', 'img')
        # Path para a imagem específica
        caminho_imagem = os.path.join(pasta_img, 'megamotores.png')
        self.setWindowIcon(QIcon(caminho_imagem)) # Adicione o ícone desejado

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
        self.telefone2 = QLineEdit(telefone2)

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
        self.telefone2.setStyleSheet(style_sheet)

        # Adicionando siglas dos estados ao QComboBox
        estados_brasileiros = [
            "","AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
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

        # Adicionando botões de seleção para Pessoa Física e Jurídica
        self.pessoa_fisica = QRadioButton("Pessoa Física (CPF)")
        self.pessoa_juridica = QRadioButton("Pessoa Jurídica (CNPJ)")
        self.nao_informar = QRadioButton("Não informar")
        self.pessoa_fisica.setChecked(True)  # Definindo Pessoa Física como padrão
        self.tipo_pessoa_group = QButtonGroup()
        self.tipo_pessoa_group.addButton(self.pessoa_fisica)
        self.tipo_pessoa_group.addButton(self.pessoa_juridica)
        self.tipo_pessoa_group.addButton(self.nao_informar)
        self.tipo_pessoa_group.buttonClicked.connect(self.update_cpf_cnpj_mask)

        tipo_pessoa_layout = QHBoxLayout()
        tipo_pessoa_layout.addWidget(self.pessoa_fisica)
        tipo_pessoa_layout.addWidget(self.pessoa_juridica)
        
        tipo_pessoa_layout.addWidget(self.nao_informar)
        form_layout.addRow(QLabel("Tipo de Pessoa:"), tipo_pessoa_layout)

        form_layout.addRow(QLabel("CPF/CNPJ:"), self.cpf_cnpj)

        self.celular1 = QRadioButton("Celular")
        self.fixo1 = QRadioButton("Fixo")
        self.nao_informar_tel1 = QRadioButton("Não informar")
        self.celular1.setChecked(True)  # Definindo Pessoa Física como padrão
        self.tipo_celular = QButtonGroup()
        self.tipo_celular.addButton(self.celular1)
        self.tipo_celular.addButton(self.fixo1)
        self.tipo_celular.addButton(self.nao_informar_tel1)
        self.tipo_celular.buttonClicked.connect(self.update_telefone_mask1)
        tipo_celular_layout = QHBoxLayout()
        tipo_celular_layout.addWidget(self.celular1)
        tipo_celular_layout.addWidget(self.fixo1);        
        tipo_celular_layout.addWidget(self.nao_informar_tel1)
        
        form_layout.addRow(QLabel("Tipo de telefone:"), tipo_celular_layout)
        form_layout.addRow(QLabel("Telefone 1:"), self.telefone)

        self.celular2 = QRadioButton("Celular")
        self.fixo2 = QRadioButton("Fixo")
        self.nao_informar_tel2 = QRadioButton("Não informar")
        self.celular2.setChecked(True)  # Definindo Pessoa Física como padrão
        self.tipo_celular2 = QButtonGroup()
        self.tipo_celular2.addButton(self.celular2)
        self.tipo_celular2.addButton(self.fixo2)
        self.tipo_celular2.addButton(self.nao_informar_tel2)
        self.tipo_celular2.buttonClicked.connect(self.update_telefone_mask2)
        tipo_celular_layout2 = QHBoxLayout()
        tipo_celular_layout2.addWidget(self.celular2)
        tipo_celular_layout2.addWidget(self.fixo2);        
        tipo_celular_layout2.addWidget(self.nao_informar_tel2)
        
        form_layout.addRow(QLabel("Tipo de telefone:"), tipo_celular_layout2)
        form_layout.addRow(QLabel("Telefone 2:"), self.telefone2)

        layout.addLayout(form_layout)

        # Adicione um layout de botão para alinhar os botões horizontalmente
        button_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_cancelar = QPushButton("Cancelar")
        btn_salvar.setStyleSheet("background-color: #00a847; color: white; border-radius: 10px; padding: 10px;")
        btn_cancelar.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 10px; padding: 10px;")
        btn_salvar.clicked.connect(self.on_save)
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_salvar)
        button_layout.addWidget(btn_cancelar)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Conectar sinal de edição de CEP ao método de preenchimento automático
        self.cep.textChanged.connect(self.auto_fill_address)

        # Aplicar máscara inicial ao CPF/CNPJ e telefone
        self.update_cpf_cnpj_mask()
        self.update_telefone_mask1()
        self.update_telefone_mask2()

        
        self.cep.setInputMask('00000-000;_')

        # Configurar estado inicial se fornecido
        if estado:
            self.estado.setCurrentText(estado)

        # Verificar e aplicar a máscara correta para CPF/CNPJ ao inicializar
        self.apply_initial_cpf_cnpj_mask(cpf_cnpj)

    def on_save(self):
        if not self.validate_fields():
            return

        self.accept()

    def validate_fields(self):
        # Verificar se todos os campos estão preenchidos
        if not all([self.nome.text()]):
            QMessageBox.warning(self, "Erro", "O nome deve estar preenchido.")
            return False

    
         # Verificar formato do CPF/CNPJ
        cpf_cnpj = self.cpf_cnpj.text().strip()  # Remover espaços em branco
        if cpf_cnpj:  # Verificar se o campo não está vazio
            if self.pessoa_fisica.isChecked():
                if not self.validate_cpf(cpf_cnpj):
                    QMessageBox.warning(self, "Erro", "CPF inválido.")
                    return False
            elif self.pessoa_juridica.isChecked():
                if not self.validate_cnpj(cpf_cnpj):
                    QMessageBox.warning(self, "Erro", "CNPJ inválido.")
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

        def calculate_digit(digits, multipliers):
            s = sum(int(digit) * weight for digit, weight in zip(digits, multipliers))
            d = 11 - s % 11
            return str(d if d < 10 else 0)

        multipliers_first_digit = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        multipliers_second_digit = [6] + multipliers_first_digit

        first_twelve_digits = cnpj[:12]
        cnpj_13 = first_twelve_digits + calculate_digit(first_twelve_digits, multipliers_first_digit)
        cnpj_14 = cnpj_13 + calculate_digit(cnpj_13, multipliers_second_digit)

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
                    self.estado.setCurrentText(data.get("uf", ""))
            except Exception as e:
                print(f"Erro ao buscar endereço: {e}")

    def update_cpf_cnpj_mask(self):
        if self.pessoa_fisica.isChecked():
            self.cpf_cnpj.setInputMask('000.000.000-00;_')
        else:
            if self.pessoa_juridica.isChecked():
                self.cpf_cnpj.setInputMask('00.000.000/0000-00;_')
            else:
                self.cpf_cnpj.setInputMask('')  
    
    def update_telefone_mask1(self):
        if self.celular1.isChecked():
            self.telefone.setInputMask('(00)00000-0000;_')

        else:
            if self.fixo1.isChecked():
                self.telefone.setInputMask('(00)0000-0000;_')
            else:
                self.telefone.setInputMask('')  
                 
    def update_telefone_mask2(self):
        if self.celular2.isChecked():
            self.telefone2.setInputMask('(00)00000-0000;_')

        else:
            if self.fixo2.isChecked():
                self.telefone2.setInputMask('(00)0000-0000;_')
            else:
                self.telefone2.setInputMask('')  
    def apply_initial_cpf_cnpj_mask(self, cpf_cnpj):
        cpf_cnpj = re.sub(r'\D', '', cpf_cnpj)
        if len(cpf_cnpj) == 11:
            self.pessoa_fisica.setChecked(True)
        elif len(cpf_cnpj) == 14:
            self.pessoa_juridica.setChecked(True)

    # Aplicar a máscara apenas se o valor correspondente for um CPF ou CNPJ
        if len(cpf_cnpj) in (11, 14):
            self.update_cpf_cnpj_mask()  # Aplicar a máscara CPF ou CNPJ
            self.cpf_cnpj.setText(cpf_cnpj)  # Adicionar o valor ao campo
class DetalhesClienteDialog(QDialog):
    def __init__(self, cliente_info, equipamentos, user_type):
        super().__init__()

        self.cliente_info = cliente_info
        self.equipamentos = equipamentos
        self.user_type = user_type
        self.controller_equipamento = EquipamentoClienteController()  # Adicionando o atributo controller_equipamento
        
        self.controller_marca = MarcaController()
        self.setWindowTitle("Detalhes do Cliente")
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Subindo um nível para acessar a pasta img
        pasta_img = os.path.join(diretorio_atual, '..', 'img')
        # Path para a imagem específica
        caminho_imagem = os.path.join(pasta_img, 'megamotores.png')
        self.setWindowIcon(QIcon(caminho_imagem))

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
        self.equip_table.setColumnCount(9)  # Adicionando uma coluna extra para a ID do equipamento
        self.equip_table.setHorizontalHeaderLabels(['Código', 'Modelo','RPM','Polos','Fases','Tensão','Marca','Potência','Defeito'])
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
        
        self.equip_table.doubleClicked.connect(self.show_equipamento_message)
        self.setLayout(layout)

    
    # Métodos para manipulação de equipamentos...
    
    def add_equipamento(self,modelo,rpm,polos,fases,tensao,marca_id,potencia,defeito):
       # Adiciona o novo equipamento à lista de equipamentos
       
        cliente_id = self.cliente_info['Código']
        
        # Obtém o ID do cliente
        self.controller_equipamento.CadastrarEquipamentoCliente(modelo,rpm,polos,fases,tensao,marca_id,potencia,defeito,cliente_id)
        self.equipamentos = self.controller_equipamento.ListarEquipamentoCliente(cliente_id)
        # Atualiza a tabela de equipamentos
        self.update_equip_table()
   
    def edit_equipamento(self,modelo,rpm,polos,fases,tensao,marca_id,potencia,defeito, id):
        self.controller_equipamento.EditarequipamentoCliente(modelo,rpm,polos,fases,tensao,marca_id,potencia,defeito,id)
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
            id_item = QTableWidgetItem(str(equip['id'])) 

            modelo_item = QTableWidgetItem(equip['modelo'])
            
            rpm_item = QTableWidgetItem(equip['rpm'])
            
            polos_item = QTableWidgetItem(equip['polos'])
            
            fases_item = QTableWidgetItem(equip['fases'])
            
            tensao_item = QTableWidgetItem(equip['tensao'])
            
            marca_item = QTableWidgetItem(equip['marca_id'])

            potencia_item = QTableWidgetItem(equip['potencia'])
            
            defeito_item = QTableWidgetItem(equip['defeito'])
            self.equip_table.setItem(row, 0, id_item)
            self.equip_table.setItem(row, 1, modelo_item) 
            self.equip_table.setItem(row, 2, rpm_item)
            self.equip_table.setItem(row, 3, polos_item)
            self.equip_table.setItem(row, 4, fases_item)
            self.equip_table.setItem(row, 5, tensao_item)
            self.equip_table.setItem(row, 6, marca_item)
            self.equip_table.setItem(row, 7, potencia_item)
            self.equip_table.setItem(row, 8, defeito_item)
            

    def show_add_equipamento_dialog(self):
        marcas_disponiveis = self.controller_marca.BuscarMarca()
        dialog = AdicionarEditarEquipamentoDialog(marcas_disponiveis=marcas_disponiveis)
       
        if dialog.exec_():
            modelo = dialog.modelo.text()
            
            rpm = dialog.rpm.text()
            
            polos = dialog.polos.text()
            
            fases = dialog.fases.text()
            
            tensao = dialog.tensao.text()
            
            marca_id = dialog.line_marca.text().split(' - ')[0]
            
            potencia = dialog.potencia.text()

            defeito = dialog.defeito.text()


            self.add_equipamento(modelo,rpm,polos,fases,tensao,marca_id,potencia,defeito)
    
    def show_edit_equipamento_dialog(self):
        selected_row = self.equip_table.currentRow()
        if selected_row != -1:
            id = self.equip_table.item(selected_row, 0).text()
            modelo = self.equip_table.item(selected_row, 1).text()
            rpm = self.equip_table.item(selected_row, 2).text()
            polos = self.equip_table.item(selected_row, 3).text()
            fases = self.equip_table.item(selected_row, 4).text()
            tensao = self.equip_table.item(selected_row, 5).text()
            marca_id = self.equip_table.item(selected_row, 6).text()
            potencia = self.equip_table.item(selected_row, 7).text()
            defeito = self.equip_table.item(selected_row, 8).text()

            # Obtenha a lista de todas as marcas disponíveis
            marcas_disponiveis = self.controller_marca.BuscarMarca()
            print(f"marca que chegou antes de editar: {marca_id}")
            # Chame o diálogo de edição de equipamento, passando a lista de marcas e o ID da marca do equipamento
            dialog = AdicionarEditarEquipamentoDialog(modelo, rpm, polos, fases, tensao, marca_id,potencia, defeito, marcas_disponiveis)
            if dialog.exec_():
                novo_modelo = dialog.modelo.text()
                novo_rpm = dialog.rpm.text()
                novo_polos = dialog.polos.text()
                novo_fases = dialog.fases.text()
                novo_tensao = dialog.tensao.text()
                novo_marca_id = dialog.line_marca.text().split(' - ')[0]
                novo_potencia = dialog.potencia.text()
                novo_defeito = dialog.defeito.text()
            
                self.edit_equipamento(novo_modelo, novo_rpm, novo_polos, novo_fases, novo_tensao, novo_marca_id,novo_potencia, novo_defeito, id)
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um Equipamento para editar.")
   
    def show_equipamento_message(self, index):
            # Obtendo o texto do item clicado na tabela de equipamentos
        equipamento_info = self.equip_table.item(index.row(), index.column()).text()

            # Exibindo uma mensagem com o conteúdo do campo clicado
        QMessageBox.information(self, "Detalhes do Equipamento", equipamento_info)
   
       
class AdicionarEditarEquipamentoDialog(QDialog):
    def __init__(self, modelo="", rpm="", polos="", fases="", tensao="", marca_id="", potencia="", defeito="", marcas_disponiveis=None):
        super().__init__()
        self.setWindowTitle("Adicionar Equipamento")
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Subindo um nível para acessar a pasta img
        pasta_img = os.path.join(diretorio_atual, '..', 'img')
        # Path para a imagem específica
        caminho_imagem = os.path.join(pasta_img, 'megamotores.png')
        self.setWindowIcon(QIcon(caminho_imagem))
        self.controller = MarcaController()
        self.marca_id=marca_id
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        print(f"marca que chegou no editor: {marca_id}")
        form_layout = QFormLayout()

        style_sheet = """
            QLineEdit,QComboBox {
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus , QComboBox:focus{
                border-color: #e74c3c;
            }
        """
        self.modelo = QLineEdit(modelo)
        self.rpm = QLineEdit(rpm)
        self.polos = QLineEdit(polos)
        self.fases = QLineEdit(fases)
        self.tensao = QLineEdit(tensao) 
        self.line_marca = QLineEdit()
        self.line_marca.setReadOnly(True)
        self.btn_selecionar_marca = QPushButton("Selecionar Produto")
        self.btn_selecionar_marca.clicked.connect(self.open_marca_selection_dialog)
        self.potencia = QLineEdit(potencia)
        self.defeito = QLineEdit(defeito)
        
        self.modelo.setStyleSheet(style_sheet)
        self.rpm.setStyleSheet(style_sheet)
        self.polos.setStyleSheet(style_sheet)
        self.fases.setStyleSheet(style_sheet)
        self.tensao.setStyleSheet(style_sheet)
        self.line_marca.setStyleSheet(style_sheet)
        self.potencia.setStyleSheet(style_sheet)
        self.defeito.setStyleSheet(style_sheet)

        form_layout.addRow(QLabel("Modelo:"), self.modelo)
        form_layout.addRow(QLabel("RPM:"), self.rpm)
        form_layout.addRow(QLabel("Polos:"), self.polos)
        form_layout.addRow(QLabel("Fases:"), self.fases)
        form_layout.addRow(QLabel("Tensão:"), self.tensao)
        form_layout.addRow(QLabel("Marca:"), self.line_marca)
        form_layout.addWidget(self.btn_selecionar_marca) 
        form_layout.addRow(QLabel("Potência:"), self.potencia)
        form_layout.addRow(QLabel("Defeito:"), self.defeito)
        
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_cancelar = QPushButton("Cancelar")
        btn_salvar.setStyleSheet("background-color: #00a847; color: white; border-radius: 10px; padding: 10px;")
        btn_cancelar.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 10px; padding: 10px;")
        btn_salvar.clicked.connect(self.accept)
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_salvar)
        button_layout.addWidget(btn_cancelar)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        if marcas_disponiveis:
            for marca in marcas_disponiveis:
                
                 if str(marca[0]) == str(marca_id):
                    self.line_marca.setText(f"{marca[0]} - {marca[1]}")
                    break
    def open_marca_selection_dialog(self):
        dialog = MarcaSelectionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            marca_id, marca_nome = dialog.get_selected_cliente()
            self.line_marca.setText(f"{marca_id} - {marca_nome}")
            self.marca_id = marca_id  # Atualiza os equipamentos com base no cliente selecionado
class MarcaSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Selecionar Marca")
        self.selected_marca_id = None
        self.selected_marca_nome = None

        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar por nome:"))
        self.filter_input = QLineEdit()
        self.filter_input.textChanged.connect(self.filter_table)
        filter_layout.addWidget(self.filter_input)

        self.btn_select = QPushButton("Selecionar")
        self.btn_select.clicked.connect(self.select_cliente)

        filter_layout.addWidget(self.btn_select)
        layout.addLayout(filter_layout)

        self.produto_table = QTableWidget()
        self.produto_table.setColumnCount(2)
        self.produto_table.setHorizontalHeaderLabels(['ID', 'Nome'])
        self.produto_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.produto_table)

        self.setLayout(layout)
        self.load_produtos()

        self.setFixedSize(600, 400)

    def load_produtos(self):
        produtos = self.parent().controller.BuscarMarca()
        print(produtos)  # Adicione esta linha para depuração
        self.produto_table.setRowCount(len(produtos))
        for row, cliente in enumerate(produtos):
            self.produto_table.setItem(row, 0, QTableWidgetItem(str(cliente[0])))  # Certifique-se de converter para string
            self.produto_table.setItem(row, 1, QTableWidgetItem(cliente[1]))

    def filter_table(self):
        filter_text = self.filter_input.text().lower()
        for row in range(self.produto_table.rowCount()):
            item = self.produto_table.item(row, 1)  # Nome do cliente
            if item is not None:
                self.produto_table.setRowHidden(row, filter_text not in item.text().lower())
            else:
                self.produto_table.setRowHidden(row, True)

    def select_cliente(self):
        selected_row = self.produto_table.currentRow()
        if selected_row >= 0:
            self.selected_marca_id = self.produto_table.item(selected_row, 0).text()
            self.selected_marca_nome = self.produto_table.item(selected_row, 1).text()
            self.accept()

    def get_selected_cliente(self):
        return self.selected_marca_id, self.selected_marca_nome
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = ClienteUI()  
    ui.show()
    sys.exit(app.exec_())
