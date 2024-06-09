from PyQt5.QtWidgets import QWidget,QDoubleSpinBox, QDialog,QFormLayout, QRadioButton, QButtonGroup,QMessageBox, QCheckBox,QDateEdit, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QComboBox,QTableWidgetItem, QHeaderView, QAction, QToolBar, QApplication
from PyQt5.QtCore import Qt,QDate,QRectF
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from cliente.equipamento_cliente_controller import EquipamentoClienteController
from cliente.cliente_controller import ClienteController
from ordem_servico.ordem_de_servico_controller import OrdemDeServicoController
from ordem_servico.item_ordem_controller import ItemOrdemController
from produto.produto_controller import ProdutoController
from PyQt5.QtGui import QIcon,QPainter,QTextDocument
from jinja2 import Template
import pdfkit
import os
import time
import subprocess
from datetime import datetime


class OrdemDeServicoUI(QWidget):
    def __init__(self,user_type):
        super().__init__()
        self.controller = OrdemDeServicoController()
        
        self.controller_cliente = ClienteController()
        
        self.controller_item = ItemOrdemController()
        
        self.controller_equipamento = EquipamentoClienteController()
        
        self.user_type= user_type
        self.initUI()
        
        print(f"tipo que chegou na ordem: {user_type}")

    def initUI(self):
        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar por nome:"))
        self.filter_input = QLineEdit()
        self.filter_input.textChanged.connect(self.filter_table)
        filter_layout.addWidget(self.filter_input)

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
        
        if self.user_type == 'usr':
         
            self.btn_active = QPushButton("Atualizar")
            self.btn_active.setStyleSheet(filter_button_style)
            self.btn_active.clicked.connect(self.filter_active)
            filter_layout.addWidget(self.btn_active)
        layout.addLayout(filter_layout)

        self.ordem_table = QTableWidget()
        self.ordem_table.setStyleSheet("""
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
        self.ordem_table.setColumnCount(9)
        self.ordem_table.setHorizontalHeaderLabels(['Código', 'Cliente', 'Equipamento', 'Data Início','Data Final', 'Mão de obra','Valor Final','Observação','Ativo'])
        self.ordem_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.ordem_table)

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

            action_add = QAction("Adicionar", self)
            action_edit = QAction("Editar", self)
            action_close = QAction("Fechar", self)
            action_delete = QAction("Excluir", self)
            action_inactive = QAction("Inativar", self)
            action_ative = QAction("Reativar", self)

            toolbar.addAction(action_add)
            toolbar.addAction(action_edit)  
            toolbar.addAction(action_close)
            toolbar.addAction(action_delete)
            toolbar.addAction(action_inactive)        
            toolbar.addAction(action_ative)

            action_add.triggered.connect(self.show_add_ordem_dialog)
            action_edit.triggered.connect(self.show_edit_ordem_dialog)
            action_close.triggered.connect(self.fechar_ordem)
            action_delete.triggered.connect(self.delete_ordem)
            action_inactive.triggered.connect(self.inactive_ordem)
            action_ative.triggered.connect(self.ative_ordem)
        if self.user_type == 'usr':

            action_add = QAction("Adicionar", self)
            action_edit = QAction("Editar", self)
            action_close = QAction("Fechar", self)
            action_inactive = QAction("Inativar", self)

            toolbar.addAction(action_add)
            toolbar.addAction(action_edit)
            toolbar.addAction(action_close)
            toolbar.addAction(action_inactive)   

            action_add.triggered.connect(self.show_add_ordem_dialog)
            action_edit.triggered.connect(self.show_edit_ordem_dialog)
            action_close.triggered.connect(self.fechar_ordem)
            action_inactive.triggered.connect(self.inactive_ordem)

        self.setLayout(layout)
        
        self.controller.create_table()       
        self.controller_equipamento.create_table()
        
        self.controller_item.create_table()

        self.filter_active()

        self.ordem_table.doubleClicked.connect(self.show_ordem_details)
        

    def filter_table(self):
        filter_text = self.filter_input.text().lower()
        for row in range(self.ordem_table.rowCount()):
            match = False
            for col in range(self.ordem_table.columnCount()):
                item = self.ordem_table.item(row, col)
                if item is not None and item.text().lower().find(filter_text) != -1:
                    match = True
                    break
            self.ordem_table.setRowHidden(row, not match)

    def filter_all(self):
        ordens = self.controller.ListarOrdemServico()
        self.ordem_table.setRowCount(0)
    
        for row_number, ordem in enumerate(ordens):
            self.ordem_table.insertRow(row_number)
        
            for column_number, data in enumerate(ordem):
                item = QTableWidgetItem(str(data))
            
                if column_number == 8: 
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.ordem_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.ordem_table.setItem(row_number, column_number, item)

    def filter_active(self):
        ordens = self.controller.FiltrarOrdemServico(True)
        self.ordem_table.setRowCount(0)
    
        for row_number, ordem in enumerate(ordens):
            self.ordem_table.insertRow(row_number)
        
            for column_number, data in enumerate(ordem):
                item = QTableWidgetItem(str(data))
            
                if column_number == 8:  
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.ordem_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.ordem_table.setItem(row_number, column_number, item)

    def filter_inactive(self):
        ordens = self.controller.FiltrarOrdemServico(False)
        self.ordem_table.setRowCount(0)
    
        for row_number, ordem in enumerate(ordens):
            self.ordem_table.insertRow(row_number)
        
            for column_number, data in enumerate(ordem):
                item = QTableWidgetItem(str(data))
            
                if column_number == 8:  
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.ordem_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.ordem_table.setItem(row_number, column_number, item)

    def add_ordem(self, cliente,observacao, equipamento, data_inicio, mao_de_obra ):
        valor_numerico = float(mao_de_obra.replace('R$', '').replace(',', '.'))
        valor_arredondado = round(valor_numerico, 2)
        self.controller.CadastrarOrdemServico( cliente, equipamento, data_inicio, valor_arredondado, observacao)
        self.filter_active() 
                        
    def edit_ordem(self, cliente,observacao, equipamento, data_inicio, mao_de_obra,id):
        valor_numerico = float(mao_de_obra.replace('R$', '').replace(',', '.'))
        valor_arredondado = round(valor_numerico, 2)
        self.controller.EditarOrdemServico( cliente, equipamento, data_inicio, valor_arredondado,observacao,id)
        self.filter_active()  


    def delete_ordem(self,id):
      
        selected_row = self.ordem_table.currentRow()
        if selected_row != -1:
            id = self.ordem_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir a ordem de serviço ID {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.controller.DeletarOrdemServico(id)
                self.filter_active()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma ordem de serviço para excluir.")

    def inactive_ordem(self):
        selected_row = self.ordem_table.currentRow()
        if selected_row != -1:
            id = self.ordem_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja inativar a ordem de serviço código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller.ValidarOrdemServico(id)
                if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 1:  # Verifica se o cliente está ativo
                        self.controller.InativarOrdemServico(id)
                        self.filter_active()
                    else:
                        QMessageBox.warning(self, "Aviso", "Ordem de serviço já está inativa.")
                else:
                    QMessageBox.warning(self, "Aviso", "Ordem de serviço não encontrada.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma Ordem de serviço para inativar.")
 
    def ative_ordem(self):
        selected_row = self.ordem_table.currentRow()
        if selected_row != -1:
            id = self.ordem_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja reativar a ordem de serviço código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller.ValidarOrdemServico(id)
                if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 0:  # Verifica se o cliente está inativo
                        self.controller.AtivarOrdemServico(id)
                        self.filter_active()
                    else:
                        QMessageBox.warning(self, "Aviso", "Ordem de serviço já está Ativa.")
                else:
                    QMessageBox.warning(self, "Aviso", "Ordem de serviço não encontrada.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma Ordem de serviço de serviço para Ativar.")   
    
    def fechar_ordem(self):
        selected_row = self.ordem_table.currentRow()
        if selected_row != -1:
            id = self.ordem_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja fechar a ordem de serviço código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller.ValidarOrdemServicoFechada(id)
                if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 0:  # Verifica se o cliente está ati                        
                        data_final = datetime.now().strftime("%d/%m/%Y")
                        self.controller.FecharOrdemServico(data_final,id)
                        self.filter_active()
                    else:
                        QMessageBox.warning(self, "Aviso", "Ordem de serviço já está fechada.")
                else:
                    QMessageBox.warning(self, "Aviso", "Ordem de serviço não encontrada.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma Ordem de serviço para fechar.")
    def show_add_ordem_dialog(self):
        clientes_disponiveis = self.controller_cliente.BuscarCliente()
        dialog = AdicionarEditarOrdemDialog(clientes_disponiveis=clientes_disponiveis)
        if dialog.exec_():
            
            cliente = dialog.combo_cliente.currentText().split(' - ')[0]
            observacao = dialog.observacao.text()
            equipamento = dialog.combo_equipamento.currentText().split(' - ')[0]
            data_inicio = dialog.data_inicio_edit.text()
            mao_de_obra = dialog.mao_de_obra.text()
            
            self.add_ordem(cliente,observacao, equipamento, data_inicio, mao_de_obra)
   
    def show_edit_ordem_dialog(self):
        selected_row = self.ordem_table.currentRow()
        if selected_row != -1:
            id_ordem = int(self.ordem_table.item(selected_row, 0).text())
        
        # Método para buscar os dados da ordem pelo ID
            ordens = self.controller.CarregarOrdemServico(id_ordem)
        
            if ordens:
                ordem = ordens[0]  # Supondo que a função retorna uma lista de tuplas, pegamos o primeiro elemento
                cliente = ordem[1]  # Índice do cliente na tupla
                equipamento = ordem[2]  # Índice do equipamento na tupla
                data_inicio = ordem[3]  # Índice da data de início na tupla
                mao_de_obra = ordem[5]
                observacao = ordem[6]
            
                clientes_disponiveis = self.controller_cliente.BuscarCliente()
                
                print(f"cliente que chegou antes de editar: {cliente}")
                equipamentos_disponiveis = self.controller_equipamento.BuscarEquipamentos()
                dialog = AdicionarEditarOrdemDialog(cliente, observacao, equipamento, data_inicio, mao_de_obra,clientes_disponiveis, equipamentos_disponiveis)
                if dialog.exec_():
                    novo_cliente = dialog.combo_cliente.currentText().split(' - ')[0]
                    novo_observacao = dialog.observacao.text()
                    novo_equipamento = dialog.combo_equipamento.currentText().split(' - ')[0]
                    novo_inicio = dialog.data_inicio_edit.text()
                    novo_mao = dialog.mao_de_obra.text()
                
                    self.edit_ordem(novo_cliente,novo_observacao, novo_equipamento, novo_inicio, novo_mao, id_ordem)
            else:
                QMessageBox.warning(self, "Aviso", "Ordem de serviço não encontrada.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma ordem de serviço para editar.")

    def show_ordem_details(self):
        selected_row = self.ordem_table.currentRow()
        if selected_row != -1:
            id_ordem = int(self.ordem_table.item(selected_row, 0).text())
        
        # Método para buscar os dados da ordem pelo ID
            ordens = self.controller.ListarOrdemServico(id_ordem)
        
            if ordens:
                
                ordem = ordens[0] 
                cliente = ordem[1]  
                equipamento = ordem[2]  
                data_inicio = ordem[3]  
                data_final = ordem[4]
                mao_de_obra = ordem[5]
                valor_total = ordem[6]
                observacao = ordem[7]

                cliente_info = {
                'Código': id_ordem,
                'Cliente': cliente,
                'Equipamento': equipamento,
                'Data de início': data_inicio,
                'Data Final': data_final,
                'Mão de obra': mao_de_obra,
                'Valor Total': valor_total,
                'Observação': observacao
            }
            itens_ordem = self.controller_item.ListarItemOrdem(id_ordem)

            dialog = DetalhesOrdemDialog(cliente_info, itens_ordem, self.user_type)
        
        # Definindo o tamanho mínimo e máximo da janela
            dialog.setMinimumSize(700, 500)  # Defina o tamanho mínimo desejado
            dialog.setMaximumSize(900, 700)  # Defina o tamanho máximo desejado

            dialog.exec_()

        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para ver os detalhes.")
    



class AdicionarEditarOrdemDialog(QDialog):
    def __init__(self, cliente_id="",observacao="", equipamento_id="", data_inicio="", mao_de_obra="",clientes_disponiveis=None,equipamentos_disponiveis=None):
        super().__init__()
       
        self.setWindowTitle("Adicionar Ordem de serviço")
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Subindo um nível para acessar a pasta img
        pasta_img = os.path.join(diretorio_atual, '..', 'img')
        # Path para a imagem específica
        caminho_imagem = os.path.join(pasta_img, 'megamotores.png')
        self.setWindowIcon(QIcon(caminho_imagem))  # Adicione o ícone desejado
        self.cliente_id=cliente_id
        self.equipamento_id=equipamento_id
        
        print(f"cliente que chegou na tela de editar: {cliente_id}")
        
        print(f"equipamento que chegou na tela de editar: {equipamento_id}")
        self.controller_cliente = ClienteController()
        
        self.controller_equipamento = EquipamentoClienteController()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Adicione margens para espaçamento

        form_layout = QFormLayout()

        self.combo_cliente = QComboBox()
        self.observacao = QLineEdit(str(observacao))
        self.combo_equipamento =  QComboBox()
        self.data_inicio_edit = QDateEdit()
        self.mao_de_obra = QDoubleSpinBox()
        self.mao_de_obra.setDecimals(2)
        self.mao_de_obra.setMaximum(9999.99)    # Definindo duas casas decimais
        self.mao_de_obra.setPrefix("R$ ")

        if mao_de_obra:
            # Substitui a vírgula pelo ponto e converte para float
            self.mao_de_obra.setValue(mao_de_obra) 
       

        # Configuração de QDateEdit para as datas de início e final
        self.data_inicio_edit.setCalendarPopup(True)
        self.data_inicio_edit.setDate(QDate.fromString(data_inicio, "dd-MM-yyyy"))
        

        # Estilo CSS para os campos de entrada
        style_sheet = """
            QLineEdit, QComboBox, QDateEdit,QDoubleSpinBox{
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus QDateEdit:focus,QDoubleSpinBox:focus{
                border-color: #e74c3c;
            }
        """
        self.combo_cliente.setStyleSheet(style_sheet)
        self.observacao.setStyleSheet(style_sheet)
        self.combo_equipamento.setStyleSheet(style_sheet)
        self.data_inicio_edit.setStyleSheet(style_sheet)
        self.mao_de_obra.setStyleSheet(style_sheet)
        
        form_layout.addRow(QLabel("Cliente:"), self.combo_cliente)
        form_layout.addRow(QLabel("Observação:"), self.observacao)
        form_layout.addRow(QLabel("Equipamento:"), self.combo_equipamento)
        form_layout.addRow(QLabel("Data Início:"), self.data_inicio_edit)
        form_layout.addRow(QLabel("Mão de obra:"), self.mao_de_obra)

        layout.addLayout(form_layout)

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
        
        self.data_inicio_edit.setDate(QDate.currentDate())

        if clientes_disponiveis:
            self.combo_cliente.addItem("Selecione um Cliente")
            for cliente in clientes_disponiveis:
                self.combo_cliente.addItem(f"{cliente[0]} - {cliente[1]}")
            # Se o ID do cliente estiver definido, encontre seu índice na lista e selecione-o
            if cliente_id:
                cliente_ids = [cliente[0] for cliente in clientes_disponiveis]
                if cliente_id in cliente_ids:
                    cliente_index = cliente_ids.index(cliente_id)
                    
                    print(f"cliente index : {cliente_index}")
                    self.combo_cliente.setCurrentIndex(cliente_index+1)
                else:
                    # Caso o ID do cliente não esteja na lista de IDs disponíveis, selecione o primeiro item da lista
                    self.combo_cliente.setCurrentIndex(0)
     
                    
        else:
            clientes_disponiveis = self.controller_cliente.BuscarCliente()

        if equipamentos_disponiveis:
            self.combo_equipamento.addItem("Selecione um Equipamento")
            for equipamento in equipamentos_disponiveis:
                self.combo_equipamento.addItem(f"{equipamento[0]} - {equipamento[1]}")
            # Se o ID do equipamento estiver definido, encontre seu índice na lista e selecione-o
            if equipamento_id:
                equipamento_ids = [equipamento[0] for equipamento in equipamentos_disponiveis]
                if equipamento_id in equipamento_ids:
                    equipamento_index = equipamento_ids.index(equipamento_id)
                    
                    print(f"equipamento index : {equipamento_index}")
                    self.combo_equipamento.setCurrentIndex(equipamento_index+1)
                else:
                    # Caso o ID do equipamento não esteja na lista de IDs disponíveis, selecione o primeiro item da lista
                    self.combo_equipamento.setCurrentIndex(0)      
        else:
            equipamentos_disponiveis = self.controller_equipamento.BuscarEquipamentos()

        self.combo_cliente.currentIndexChanged.connect(self.update_equipamentos)

    def update_equipamentos(self):
        cliente_info = self.combo_cliente.currentText()
        cliente_id = cliente_info.split()[0]

        self.combo_equipamento.clear()
        
        self.combo_equipamento.addItem("Selecione um equipamento")
        # Consulta ao controller de equipamento para recuperar os equipamentos associados ao cliente selecionado
        if cliente_id:
            equipamentos = self.controller_equipamento.BuscarEquipamento(cliente_id)
            for equipamento in equipamentos:
                self.combo_equipamento.addItem(f"{equipamento[0]} - {equipamento[1]}")
        
    def on_save(self):
        if not self.validate_fields():
            return

        self.accept()

    def validate_fields(self):
        # Verificar se todos os campos estão preenchidos
        if not all([ self.data_inicio_edit.date(), self.mao_de_obra.text()]):
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return False

        return True
    
    def has_two_decimal_places(self, number):
    # Converte o número para uma string e verifica se tem duas casas decimais
        decimal_part = str(number).split('.')[1]
        return len(decimal_part) <= 2
    
class DetalhesOrdemDialog(QDialog):
    def __init__(self, ordem_info, itens_ordem, user_type):
        super().__init__()

        self.ordem_info = ordem_info
        self.itens_ordem = itens_ordem
        self.user_type = user_type

        self.controller_cliente=ClienteController()

        self.controller_equipamento=EquipamentoClienteController()

        self.controller_item = ItemOrdemController()  
        
        self.controller_produto = ProdutoController()
        
        self.controller_ordem = OrdemDeServicoController()

        self.setWindowTitle("Detalhes da Ordem de serviço")
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

        for key, value in ordem_info.items():
            label = QLabel(key.capitalize() + ":")
            field = QLineEdit(str(value))
            field.setReadOnly(True)
            field.setStyleSheet("background-color: white; border: 2px solid #3498db; padding: 5px; border-radius: 5px; color: #333;")
            self.campos_cliente[key] = field
            form_layout.addRow(label, field)

        layout.addLayout(form_layout)

        item_table = QLabel("Materiais:")
        layout.addWidget(item_table)

        self.item_table = QTableWidget()
        self.item_table.setStyleSheet("""
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
        self.item_table.setColumnCount(5)  # Adicionando uma coluna extra para a ID do equipamento
        self.item_table.setHorizontalHeaderLabels(['Código','Produto','Quantidade','Valor Unitário','Valor Total'])
        self.item_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.item_table.verticalHeader().setVisible(False)
        ordem_id = self.ordem_info['Código']
        self.itens = self.controller_item.ListarItemOrdem(ordem_id)
        self.update_item_table()
        
        
        layout.addWidget(self.item_table)

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
        id_ordem = self.ordem_info['Código']
        resultado = self.controller_ordem.ValidarOrdemServicoFechada(id_ordem)
        if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 0:
            # Botões de ação
                        action_add = QAction("Adicionar", self)
                        action_edit = QAction("Editar", self)
                        action_delete = QAction("Excluir", self)

                        toolbar.addAction(action_add)
                        toolbar.addAction(action_edit)
                        toolbar.addAction(action_delete)

            # Configurar conexões de sinais e slots para os botões
                        action_add.triggered.connect(self.show_add_item_dialog)
                        action_edit.triggered.connect(self.show_edit_item_dialog)
                        action_delete.triggered.connect(self.delete_item)

        
        action_print = QAction("Imprimir", self)      
        
        toolbar.addAction(action_print)
        
        action_print.triggered.connect(self.print_order)
        self.setLayout(layout)

    
    # Métodos para manipulação de equipamentos...

    def print_order(self):
        # Função para renderizar e imprimir o HTML como PDF
        
        # Obtendo os detalhes do cliente
        id_ordem = self.ordem_info['Código']
        ords = self.controller_ordem.CarregarImpressaoOrdem(id_ordem)
        
        if ords:
            ord = ords[0] 
            cliente_id = ord[1]  
            equipamento_id = ord[2]  
            data_inicio = ord[3]  
            data_final = ord[4]
            mao_de_obra = ord[5]
            valor_total = ord[6]
            total_material = ord[7]
            observacao = ord[8]

            ordem_info = {
                    'Data_inicial': data_inicio,
                    'Data_final': data_final,
                    'mao_de_obra': mao_de_obra,
                    'Total_ordem': valor_total,
                    'Total_material': total_material,
                    'Observacao': observacao
                    
                }
            
            print(f"cliente_id: {cliente_id}")
            clientes = self.controller_cliente.CarregarCliente(cliente_id)

            if clientes:
                cliente = clientes[0] 
                nome = cliente[1]  
                cep = cliente[2]  
                endereco = cliente[3]  
                numero = cliente[4]
                cidade = cliente[5]
                estado = cliente[6]
                cpf_cnjp = cliente[7]
                telefone = cliente[8]

                cliente_info = {
                    'Nome': nome,
                    'Cep': cep,
                    'Endereco': endereco,
                    'Número': numero,
                    'Cidade': cidade,
                    'Estado': estado,
                    'Cpf_cnpj': cpf_cnjp,
                    'Telefone': telefone
                }
                print(f"equipamento_id: {equipamento_id}")
                equips = self.controller_equipamento.CarregarImpressaoEquipamento(equipamento_id)

                if equips:
                    equip = equips[0] 
                    modelo = equip[1]  
                    rpm = equip[2]  
                    polos = equip[3]  
                    fases = equip[4]
                    tensao = equip[5]
                    marca = equip[6]
                    defeito = equip[7]
                

                    equipamento_info = {
                        'Modelo': modelo,
                        'Rpm': rpm,
                        'Polos': polos,
                        'Fases': fases,
                        'Tensao': tensao,
                        'Marca': marca,
                        'Defeito': defeito,
                        'Potencia': defeito
                    }

                    # Obter os itens da ordem de serviço
                    itens_ordem = self.controller_item.ListarItemOrdem(id_ordem)

                                        # Obter o diretório atual do script Python
                    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

                    # Path para salvar o arquivo PDF temporário
                    pdf_path = os.path.join(diretorio_atual,'temp.pdf')

                    # Renderiza o template HTML com os dados fornecidos
                    template_path = os.path.join(diretorio_atual,'teste.html')

                    # Verifica se os arquivos existem nos caminhos especificados
                    if not os.path.exists(template_path):
                        print(f"Arquivo HTML não encontrado em: {template_path}")
                        # Adicione aqui qualquer lógica de tratamento de erro, se necessário

                    html_content = self.render_template(template_path, cliente_info=cliente_info, equipamento_info=equipamento_info, itens_ordem=itens_ordem, ordem_info=ordem_info)

                    # Path para salvar o arquivo HTML temporário
                    html_temp_path = os.path.join(diretorio_atual,'temp_ordem.html')

                    # Adicione a codificação UTF-8 ao abrir o arquivo HTML temporário para escrita
                    with open(html_temp_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)

                    # Converte o HTML para PDF
                    configuration = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
                    pdfkit.from_file(html_temp_path, pdf_path, configuration=configuration, options={'encoding': "UTF-8"})

                                    
                    if os.path.exists(pdf_path):
                            
                            subprocess.run(['cmd', '/c', 'start', '', '/WAIT', pdf_path], shell=True)  
                    else:

                        print("O arquivo PDF não foi encontrado.")
                
                else:
                    QMessageBox.warning(self, "Aviso", "Falha ao carregar informações do equipamento.")    
                # Remove os arquivos temporários
            else:
                QMessageBox.warning(self, "Aviso", "Falha ao carregar informações do cliente.")
        else:
            QMessageBox.warning(self, "Aviso", "Falha ao carregar informações da ordem de serviço.")

    def render_template(self, template_path, **kwargs):
        with open(template_path, 'r', encoding='utf-8') as f:  # Adicione a codificação UTF-8 ao abrir o arquivo HTML
            template_string = f.read()
        template = Template(template_string)
        return template.render(**kwargs)
    
    def add_item(self, produto_id, quantidade,valor_unitario):
       # Adiciona o novo equipamento à lista de equipamentos
       
        ordem_id = self.ordem_info['Código']
        
        # Obtém o ID do cliente
        self.controller_item.CadastrarItemOrdem(ordem_id, produto_id, quantidade,valor_unitario)
        self.itens = self.controller_item.ListarItemOrdem(ordem_id)
        # Atualiza a tabela de equipamentos
        self.update_item_table()
   
    def edit_item(self, produto_id, quantidade,valor_unitario, id):
        self.controller_item.EditarItemOrdem(produto_id, quantidade,valor_unitario, id)
        ordem_id = self.ordem_info['Código']
        self.itens = self.controller_item.ListarItemOrdem(ordem_id)  # Atualiza a lista de itens
        self.update_item_table()  # Atualiza a tabela

    def delete_item(self, id):
        selected_row = self.item_table.currentRow()
        if selected_row != -1:
            id = self.item_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir o Item Código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.controller_item.DeletarItemOrdem(id)
                ordem_id = self.ordem_info['Código']
                self.itens = self.controller_item.ListarItemOrdem(ordem_id)  # Atualiza a lista de itens
                self.update_item_table()  # Atualiza a tabela
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um item para excluir.")
   
    def update_item_table(self):
        # Limpa a tabela de equipamentos
        self.item_table.setRowCount(0)

        # Define o número de linhas da tabela para corresponder ao número de equipamentos
        self.item_table.setRowCount(len(self.itens))

        # Adiciona os equipamentos atualizados à tabela
        for row, equip in enumerate(self.itens):
            id_item = QTableWidgetItem(str(equip['id_item'])) 

            produto_item = QTableWidgetItem(equip['produto_nome'])
            
            quantidade_item = QTableWidgetItem(str(equip['quantidade']))

            valor_unitario_item = QTableWidgetItem(str(equip['valor_unitario']))

            valot_total_item = QTableWidgetItem(str(equip['valor_total']))

            self.item_table.setItem(row, 0, id_item)
            self.item_table.setItem(row, 1, produto_item) 
            self.item_table.setItem(row, 2, quantidade_item)
            self.item_table.setItem(row, 3, valor_unitario_item)
            self.item_table.setItem(row, 4, valot_total_item)
            
          
            

    def show_add_item_dialog(self):
        produtos_disponiveis = self.controller_produto.FiltrarProduto(True)
        dialog = AdicionarEditarItemDialog(produtos_disponiveis=produtos_disponiveis)
       
        if dialog.exec_():
            produto_id = dialog.combo_produto.currentText().split(' - ')[0]
            
            quantidade = dialog.quantidade.text()
            
            valor_unitario = dialog.valor_unitario.text()
            

            self.add_item(produto_id,quantidade,valor_unitario)
    
    def show_edit_item_dialog(self):
        selected_row = self.item_table.currentRow()
        if selected_row != -1:
            id_item = int(self.item_table.item(selected_row, 0).text())
        
        # Método para buscar os dados da ordem pelo ID
            itens = self.controller_item.CarregarItemOrdem(id_item)
        
            if itens:
                item = itens[0]  
                produto = item[2]  
                quantidade = item[3] 
                valor_unitario = item[4] 
                
            
                produtos_disponiveis = self.controller_produto.FiltrarProduto(True)
                
                print(f"cliente que chegou antes de editar: {produto}")
                
        
            # Chame o diálogo de edição de equipamento, passando a lista de marcas e o ID da marca do equipamento
            dialog = AdicionarEditarItemDialog(produto, quantidade,valor_unitario,produtos_disponiveis)
            if dialog.exec_(): 
                novo_produto_id= dialog.combo_produto.currentText().split(' - ')[0]
                novo_quantidade = dialog.quantidade.text()
                novo_valor = dialog.valor_unitario.text()
                
            
                self.edit_item(novo_produto_id, novo_quantidade,novo_valor, id_item)
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um Equipamento para editar.")
   
    def show_item_message(self, index):
            # Obtendo o texto do item clicado na tabela de equipamentos
        equipamento_info = self.item_table.item(index.row(), index.column()).text()

            # Exibindo uma mensagem com o conteúdo do campo clicado
        QMessageBox.information(self, "Detalhes do Equipamento", equipamento_info)
   

class AdicionarEditarItemDialog(QDialog):
    def __init__(self, produto_id="", quantidade="", valor_unitario="", produtos_disponiveis=None):
        super().__init__()
        self.setWindowTitle("Adicionar Materiais utilizados")
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_img = os.path.join(diretorio_atual, '..', 'img')
        caminho_imagem = os.path.join(pasta_img, 'megamotores.png')
        self.setWindowIcon(QIcon(caminho_imagem))
        self.controller = ProdutoController()
        self.produto_id = produto_id
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        form_layout = QFormLayout()

        style_sheet = """
            QLineEdit,QComboBox ,QDoubleSpinBox{
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus , QComboBox:focus, QDoubleSpinBox:focus{
                border-color: #e74c3c;
            }
        """
        
        self.combo_produto = QComboBox()
        self.quantidade = QLineEdit(str(quantidade))
        
        self.editar_valor = QRadioButton("Sim")
        self.editar_valor.setChecked(False)  # Definindo "Não" como padrão
        self.editar_valor_group = QButtonGroup()
        self.editar_valor_group.addButton(self.editar_valor)
        self.editar_valor_group.buttonClicked.connect(self.toggle_valor_editavel)

        self.valor_unitario = QDoubleSpinBox()
        self.valor_unitario.setReadOnly(True)
        self.valor_unitario.setDecimals(2)
        self.valor_unitario.setMaximum(9999.99) # Definindo duas casas decimais

        if valor_unitario:
            # Substitui a vírgula pelo ponto e converte para float
            valor_float = float(valor_unitario.replace(',', '.'))
            self.valor_unitario.setValue(valor_float)

        self.combo_produto.setStyleSheet(style_sheet)
        self.quantidade.setStyleSheet(style_sheet)
        self.valor_unitario.setStyleSheet(style_sheet)

        form_layout.addRow(QLabel("Produto:"), self.combo_produto)
        form_layout.addRow(QLabel("Quantidade:"), self.quantidade)
        form_layout.addRow(QLabel("Editar Valor Manualmente:"), self.editar_valor)
        form_layout.addRow(QLabel("Valor unitário:"), self.valor_unitario)  # Adiciona o campo de valor unitário ao formulário
        
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
        
        if produtos_disponiveis:
            for produto in produtos_disponiveis:
                self.combo_produto.addItem(f"{produto[0]} - {produto[1]}", produto[0])  # Adiciona o ID do produto como dado ao item do combo box

            if self.produto_id and produtos_disponiveis:
                produto_ids = [produto[0] for produto in produtos_disponiveis]
                if self.produto_id in produto_ids:
                    produto_index = produto_ids.index(self.produto_id)
                    self.combo_produto.setCurrentIndex(produto_index)
                else:
                    self.combo_produto.setCurrentIndex(0)
        else:
            produtos_disponiveis = self.controller.FiltrarProduto(True)

        # Conecta a função atualizar_valor_unitario tanto à mudança no produto quanto à mudança no campo de valor
        self.combo_produto.currentIndexChanged.connect(self.atualizar_valor_unitario)
        self.valor_unitario.textChanged.connect(self.atualizar_valor_manual)

    def atualizar_valor_unitario(self):
        # Obtém o ID do produto selecionado
        produto_id = self.combo_produto.currentData()
        # Consulta o valor do produto usando o ID
        valor_produto = self.controller.obter_valor_produto(produto_id)
        # Atualiza o campo de valor unitário na tela
        self.valor_unitario.setValue(valor_produto)

    def atualizar_valor_manual(self):
    # Verifica se o campo de valor unitário não está vazio
        if self.valor_unitario.text():
            # Obtém o valor manualmente digitado pelo usuário
            valor_manual = self.valor_unitario.text().replace(',', '.')  # Substitui a vírgula por um ponto
            # Atualiza o campo de valor unitário com o valor digitado
            self.valor_unitario.setValue(float(valor_manual))

    def toggle_valor_editavel(self):
        # Alterna entre o modo somente leitura e editável do campo de valor unitário
        self.valor_unitario.setReadOnly(not self.valor_unitario.isReadOnly())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = OrdemDeServicoUI()  
    ui.show()
    sys.exit(app.exec_())
