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
            
            self.btn_active = QPushButton("Abertos")
            self.btn_active.setStyleSheet(filter_button_style)
            self.btn_active.clicked.connect(self.filter_aberto)
            filter_layout.addWidget(self.btn_active)

            self.btn_inactive = QPushButton("Fechados")
            self.btn_inactive.setStyleSheet(filter_button_style)
            self.btn_inactive.clicked.connect(self.filter_fechado)
            filter_layout.addWidget(self.btn_inactive)
        
        if self.user_type == 'usr':
         
            self.btn_active = QPushButton("Atualizar")
            self.btn_active.setStyleSheet(filter_button_style)
            self.btn_active.clicked.connect(self.filter_active)
            filter_layout.addWidget(self.btn_active)
            
            self.btn_active = QPushButton("Abertos")
            self.btn_active.setStyleSheet(filter_button_style)
            self.btn_active.clicked.connect(self.filter_aberto)
            filter_layout.addWidget(self.btn_active)

            self.btn_inactive = QPushButton("Fechados")
            self.btn_inactive.setStyleSheet(filter_button_style)
            self.btn_inactive.clicked.connect(self.filter_fechado)
            filter_layout.addWidget(self.btn_inactive)
        self.btn_print = QPushButton("Imprimir")
        self.btn_print.setStyleSheet(filter_button_style)
        self.btn_print.clicked.connect(self.print_order)
        filter_layout.addWidget(self.btn_print)
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
        self.ordem_table.setColumnCount(11)
        self.ordem_table.setHorizontalHeaderLabels(['Código', 'Cliente', 'Equipamento', 'Data Início','Data Final', 'Mão de obra','Valor Final','Observação','Passado','Aprovado','Ativo'])
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
            action_open = QAction("Reabrir", self)
            action_delete = QAction("Excluir", self)
            action_orcamento = QAction("Orçamento", self)
            action_inactive = QAction("Inativar", self)
            action_ative = QAction("Reativar", self)

            toolbar.addAction(action_add)
            toolbar.addAction(action_edit)  
            toolbar.addAction(action_close)
            toolbar.addAction(action_open)
            toolbar.addAction(action_delete)
            toolbar.addAction(action_orcamento)
            toolbar.addAction(action_inactive)        
            toolbar.addAction(action_ative)

            action_add.triggered.connect(self.show_add_ordem_dialog)
            action_edit.triggered.connect(self.show_edit_ordem_dialog)
            action_close.triggered.connect(self.fechar_ordem)
            action_open.triggered.connect(self.abrir_ordem)
            action_delete.triggered.connect(self.delete_ordem)
            action_orcamento.triggered.connect(self.orcamento_ordem)
            action_inactive.triggered.connect(self.inactive_ordem)
            action_ative.triggered.connect(self.ative_ordem)
        if self.user_type == 'usr':

            action_add = QAction("Adicionar", self)
            action_edit = QAction("Editar", self)
            action_close = QAction("Fechar", self)
            action_open = QAction("Reabrir", self)
            action_orcamento = QAction("Orçamento", self)
            action_inactive = QAction("Inativar", self)

            toolbar.addAction(action_add)
            toolbar.addAction(action_edit)
            toolbar.addAction(action_close)
            toolbar.addAction(action_open)
            toolbar.addAction(action_orcamento)
            toolbar.addAction(action_inactive)   

            action_add.triggered.connect(self.show_add_ordem_dialog)
            action_edit.triggered.connect(self.show_edit_ordem_dialog)
            action_close.triggered.connect(self.fechar_ordem)
            action_open.triggered.connect(self.abrir_ordem)
            action_orcamento.triggered.connect(self.orcamento_ordem)
            action_inactive.triggered.connect(self.inactive_ordem)

        self.setLayout(layout)
        
        self.controller.create_table()       
        self.controller_equipamento.create_table()
        
        self.controller_item.create_table()

        self.filter_active()

        self.ordem_table.doubleClicked.connect(self.show_ordem_details)
        

    def filter_table(self):
        filter_text = self.filter_input.text().lower()
        visible_products = []
        for row in range(self.ordem_table.rowCount()):
            match = False
            for col in range(self.ordem_table.columnCount()):
                item = self.ordem_table.item(row, col)
                if item is not None and item.text().lower().find(filter_text) != -1:
                    match = True
                    break
            self.ordem_table.setRowHidden(row, not match)
            if match:
                # Adiciona o produto visível à lista
                id = self.ordem_table.item(row, 0).text()
                cliente = self.ordem_table.item(row, 1).text()
                equipamento = self.ordem_table.item(row, 2).text()
                data_inicio = self.ordem_table.item(row, 3).text()
                data_final = self.ordem_table.item(row, 4).text()
                mao_de_obra = self.ordem_table.item(row, 5).text()
                valor_final = self.ordem_table.item(row, 6).text()
                observacao = self.ordem_table.item(row, 7).text()
                visible_products.append({
                    'id': id,
                    'cliente': cliente,
                    'equipamento': equipamento,
                    'data_inicio': data_inicio,
                    'data_final': data_final,
                    'mao_de_obra': mao_de_obra,
                    'valor_final': valor_final,
                    'observacao': observacao
                    
                })
        return visible_products

    def filter_all(self):
        ordens = self.controller.ListarTodasOrdemServico(False,False)
        self.ordem_table.setRowCount(0)
    
        for row_number, ordem in enumerate(ordens):
            self.ordem_table.insertRow(row_number)
        
            for column_number, data in enumerate(ordem):
                item = QTableWidgetItem(str(data))
            
                if column_number == 10: 
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
        # Captura a posição atual da barra de rolagem
        current_scroll_position = self.ordem_table.verticalScrollBar().value()

        # Simula a obtenção dos dados filtrados
        ordens = self.controller.FiltrarOrdemServico(True, False, False)
        
        # Limpa a tabela
        self.ordem_table.setRowCount(0)

        # Preenche a tabela com os novos dados
        for row_number, ordem in enumerate(ordens):
            self.ordem_table.insertRow(row_number)
            
            for column_number, data in enumerate(ordem):
                item = QTableWidgetItem(str(data))
                
                if column_number == 10:
                    # Configuração para coluna especial (por exemplo, checkbox)
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
                    # Configuração para outras colunas
                    self.ordem_table.setItem(row_number, column_number, item)
        
        # Restaura a posição da barra de rolagem
        self.ordem_table.verticalScrollBar().setValue(current_scroll_position)

    def filter_inactive(self):
        ordens = self.controller.FiltrarOrdemServico(False,False,False)
        self.ordem_table.setRowCount(0)
    
        for row_number, ordem in enumerate(ordens):
            self.ordem_table.insertRow(row_number)
        
            for column_number, data in enumerate(ordem):
                item = QTableWidgetItem(str(data))
            
                if column_number == 10:  
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
    def filter_aberto(self):
        ordens = self.controller.FiltrarOrdemServico(True,False,False)
        self.ordem_table.setRowCount(0)
    
        for row_number, ordem in enumerate(ordens):
            self.ordem_table.insertRow(row_number)
        
            for column_number, data in enumerate(ordem):
                item = QTableWidgetItem(str(data))
            
                if column_number == 10:  
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

    def filter_fechado(self):
        ordens = self.controller.FiltrarOrdemServico(True,False,True)
        self.ordem_table.setRowCount(0)
    
        for row_number, ordem in enumerate(ordens):
            self.ordem_table.insertRow(row_number)
        
            for column_number, data in enumerate(ordem):
                item = QTableWidgetItem(str(data))
            
                if column_number == 10:  
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
        self.controller.CadastrarOrdemServico( cliente, equipamento, data_inicio, valor_arredondado, observacao,0)
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
    def orcamento_ordem(self):
        selected_row = self.ordem_table.currentRow()
        if selected_row != -1:
            id = self.ordem_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja tornar a ordem de serviço código {id} um orçamento?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:         
                        self.controller.OrcamentoOrdemServico(id)
                        self.filter_active()   
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma Ordem de serviço para tornar um orçamento.")
    def abrir_ordem(self):
        selected_row = self.ordem_table.currentRow()
        if selected_row != -1:
            id = self.ordem_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja reabrir a ordem de serviço código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller.ValidarOrdemServicoFechada(id)
                if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 1:  
                        self.controller.AbrirOrdemServico(id)
                        self.filter_active()
                    else:
                        QMessageBox.warning(self, "Aviso", "Ordem de serviço já está aberta.")
                else:
                    QMessageBox.warning(self, "Aviso", "Ordem de serviço não encontrada.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma Ordem de serviço para reabrir.")
    def print_order(self):
        
        visible_products = self.filter_table()
        
        data_atual = datetime.now().strftime("%d/%m/%Y")
        info = {
                        'data': data_atual
                    }
 # Obter os itens da ordem de serviço

                                        # Obter o diretório atual do script Python
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))

                    # Path para salvar o arquivo PDF temporário
        pdf_path = os.path.join(diretorio_atual,'temp2.pdf')

                    # Renderiza o template HTML com os dados fornecidos
        template_path = os.path.join(diretorio_atual,'teste2.html')

                    # Verifica se os arquivos existem nos caminhos especificados
        if not os.path.exists(template_path):
            print(f"Arquivo HTML não encontrado em: {template_path}")
                        # Adicione aqui qualquer lógica de tratamento de erro, se necessário

        html_content = self.render_template(template_path,  visible_products=visible_products, info=info)

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

    def render_template(self, template_path, **kwargs):
        with open(template_path, 'r', encoding='utf-8') as f:  # Adicione a codificação UTF-8 ao abrir o arquivo HTML
            template_string = f.read()
        template = Template(template_string)
        return template.render(**kwargs)
    def show_add_ordem_dialog(self):
        clientes_disponiveis = self.controller_cliente.BuscarCliente()
        dialog = AdicionarEditarOrdemDialog(clientes_disponiveis=clientes_disponiveis)
        if dialog.exec_():
            
            cliente = dialog.line_cliente.text().split(' - ')[0]
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
                observacao = ordem[8]
            
                clientes_disponiveis = self.controller_cliente.BuscarCliente()
                equipamentos_disponiveis = self.controller_equipamento.BuscarEquipamentos()
                
              
                
                dialog = AdicionarEditarOrdemDialog(cliente, observacao, equipamento, data_inicio, mao_de_obra, clientes_disponiveis, equipamentos_disponiveis)
                
                # Atualiza a lista de equipamentos com base no cliente selecionado
                dialog.update_equipamentos()
                
                if dialog.exec_():
                    novo_cliente = dialog.line_cliente.text().split(' - ')[0]
                    novo_observacao = dialog.observacao.text()
                    novo_equipamento = dialog.combo_equipamento.currentText().split(' - ')[0]
                    novo_inicio = dialog.data_inicio_edit.text()
                    novo_mao = dialog.mao_de_obra.text()
                
                    self.edit_ordem(novo_cliente, novo_observacao, novo_equipamento, novo_inicio, novo_mao, id_ordem)
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
                orcamento_passado = ordem[8]
                orcamento_aprovado = ordem[9]

                cliente_info = {
                    'Código': id_ordem,
                    'Cliente': cliente,
                    'Equipamento': equipamento,
                    'Data de início': data_inicio,
                    'Data Final': data_final,
                    'Mão de obra': mao_de_obra,
                    'Valor Total': valor_total,
                    'Observação': observacao,
                    'Orçamento Passado': orcamento_passado,
                    'Orçamento Aprovado': orcamento_aprovado
                }
                
                itens_ordem = self.controller_item.ListarItemOrdem(id_ordem)
                
                dialog = DetalhesOrdemDialog(cliente_info, itens_ordem, self.user_type)
                
                # Definindo o tamanho mínimo e máximo da janela
                dialog.setMinimumSize(900, 700)  # Defina o tamanho mínimo desejado
                dialog.setMaximumSize(1000, 800)  # Defina o tamanho máximo desejado
                
                # Executando o diálogo de detalhes de ordem
                if dialog.exec_():
                    # Esta parte do código será executada após o diálogo ser fechado

                    print("Diálogo fechado com sucesso")
                    self.filter_active()  # Chama a função filter_ativado da classe principal
            else:
                QMessageBox.warning(self, "Aviso", "Selecione um cliente para ver os detalhes.")
    



class AdicionarEditarOrdemDialog(QDialog):
    print("Diálogo fechado com sucesso")
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
        layout.setContentsMargins(10, 10, 10, 10)

        form_layout = QFormLayout()

        self.line_cliente = QLineEdit()
        self.line_cliente.setReadOnly(True)
        self.btn_selecionar_cliente = QPushButton("Selecionar Cliente")
        self.btn_selecionar_cliente.clicked.connect(self.open_cliente_selection_dialog)

        self.observacao = QLineEdit(str(observacao))
        self.combo_equipamento = QComboBox()
        self.data_inicio_edit = QDateEdit()
        self.mao_de_obra = QDoubleSpinBox()
        self.mao_de_obra.setDecimals(2)
        self.mao_de_obra.setMaximum(9999.99)
        self.mao_de_obra.setPrefix("R$ ")

        if mao_de_obra:
            self.mao_de_obra.setValue(mao_de_obra)

        self.data_inicio_edit.setCalendarPopup(True)
        self.data_inicio_edit.setDate(QDate.fromString(data_inicio, "dd/MM/yyyy"))

        style_sheet = """
            QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {
                border-color: #e74c3c;
            }
        """
        self.line_cliente.setStyleSheet(style_sheet)
        self.observacao.setStyleSheet(style_sheet)
        self.combo_equipamento.setStyleSheet(style_sheet)
        self.data_inicio_edit.setStyleSheet(style_sheet)
        self.mao_de_obra.setStyleSheet(style_sheet)

        form_layout.addRow(QLabel("Cliente:"), self.line_cliente)
        form_layout.addWidget(self.btn_selecionar_cliente)
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

        if data_inicio == "":
            self.data_inicio_edit.setDate(QDate.currentDate())

        if clientes_disponiveis:
            for cliente in clientes_disponiveis:
                if cliente[0] == cliente_id:
                    self.line_cliente.setText(f"{cliente[0]} - {cliente[1]}")
                    break

        if equipamentos_disponiveis:
            self.combo_equipamento.addItem("Selecione um Equipamento")
            for equipamento in equipamentos_disponiveis:
                self.combo_equipamento.addItem(f"{equipamento[0]} - {equipamento[1]}")
            if equipamento_id:
                equipamento_ids = [equipamento[0] for equipamento in equipamentos_disponiveis]
                if equipamento_id in equipamento_ids:
                    equipamento_index = equipamento_ids.index(equipamento_id)
                    self.combo_equipamento.setCurrentIndex(equipamento_index + 1)
                else:
                    self.combo_equipamento.setCurrentIndex(0)
        else:
            equipamentos_disponiveis = self.controller_equipamento.BuscarEquipamentos()

        self.setFixedSize(500, 300)

    def open_cliente_selection_dialog(self):
        dialog = ClienteSelectionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            cliente_id, cliente_nome = dialog.get_selected_cliente()
            self.line_cliente.setText(f"{cliente_id} - {cliente_nome}")
            self.cliente_id = cliente_id
            self.update_equipamentos()  # Atualiza os equipamentos com base no cliente selecionado

    def update_equipamentos(self):
        cliente_info = self.line_cliente.text()
        cliente_id = cliente_info.split()[0] if cliente_info else ""

        self.combo_equipamento.clear()
        self.combo_equipamento.addItem("Selecione um equipamento")

        if cliente_id:
            equipamentos = self.controller_equipamento.BuscarEquipamento(cliente_id)
            for equipamento in equipamentos:
                self.combo_equipamento.addItem(f"{equipamento[0]} - {equipamento[1]}")
            
            # Defina o equipamento atual, se houver
            if self.equipamento_id:
                equipamento_id_str = str(self.equipamento_id)  # Garanta que o ID seja uma string
                # Encontre o índice do equipamento atual na lista
                for index in range(self.combo_equipamento.count()):
                    item_text = self.combo_equipamento.itemText(index)
                    if item_text.startswith(equipamento_id_str):
                        self.combo_equipamento.setCurrentIndex(index)
                        break
        else:
            # Se não há cliente selecionado, carregue todos os equipamentos ou mantenha vazio
            self.combo_equipamento.addItem("Nenhum equipamento disponível")



    def on_save(self):
        if not self.validate_fields():
            return
        self.accept()

    def validate_fields(self):
        if not all([self.data_inicio_edit.date(), self.mao_de_obra.text()]):
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return False
        return True

    def has_two_decimal_places(self, number):
        decimal_part = str(number).split('.')[1]
        return len(decimal_part) <= 2
class ClienteSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Selecionar Cliente")
        self.selected_cliente_id = None
        self.selected_cliente_nome = None

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

        self.cliente_table = QTableWidget()
        self.cliente_table.setColumnCount(2)
        self.cliente_table.setHorizontalHeaderLabels(['ID', 'Nome'])
        self.cliente_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.cliente_table)

        self.setLayout(layout)
        self.load_clientes()

        self.setFixedSize(600, 400)

    def load_clientes(self):
        clientes = self.parent().controller_cliente.BuscarCliente()
        print(clientes)  # Adicione esta linha para depuração
        self.cliente_table.setRowCount(len(clientes))
        for row, cliente in enumerate(clientes):
            self.cliente_table.setItem(row, 0, QTableWidgetItem(str(cliente[0])))  # Certifique-se de converter para string
            self.cliente_table.setItem(row, 1, QTableWidgetItem(cliente[1]))

    def filter_table(self):
        filter_text = self.filter_input.text().lower()
        for row in range(self.cliente_table.rowCount()):
            item = self.cliente_table.item(row, 1)  # Nome do cliente
            if item is not None:
                self.cliente_table.setRowHidden(row, filter_text not in item.text().lower())
            else:
                self.cliente_table.setRowHidden(row, True)

    def select_cliente(self):
        selected_row = self.cliente_table.currentRow()
        if selected_row >= 0:
            self.selected_cliente_id = self.cliente_table.item(selected_row, 0).text()
            self.selected_cliente_nome = self.cliente_table.item(selected_row, 1).text()
            self.accept()

    def get_selected_cliente(self):
        return self.selected_cliente_id, self.selected_cliente_nome
    
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

    def closeEvent(self, event):
        # Sobrescrever closeEvent para emitir o sinal aceito ao fechar a janela
        self.accept()
    # Métodos para manipulação de equipamentos...
    def atualizar_campos_cliente(self):
        id_ordem = self.ordem_info['Código']
        self.clearCamposCliente
        ordens = self.controller_ordem.ListarOrdemServico(id_ordem)
        
        if ordens:
            ordem = ordens[0] 
            cliente = ordem[1]  
            equipamento = ordem[2]  
            data_inicio = ordem[3]  
            data_final = ordem[4]
            mao_de_obra = ordem[5]
            valor_total = ordem[6]
            observacao = ordem[7]
            orcamento_passado = ordem[8]
            orcamento_aprovado = ordem[9]

            cliente_info = {
                'Código': id_ordem,
                'Cliente': cliente,
                'Equipamento': equipamento,
                'Data de início': data_inicio,
                'Data Final': data_final,
                'Mão de obra': mao_de_obra,
                'Valor Total': valor_total,
                'Observação': observacao,
                'Orçamento Passado': orcamento_passado,
                'Orçamento Aprovado': orcamento_aprovado
            }

            for key, value in cliente_info.items():
                if key in self.campos_cliente:
                    self.campos_cliente[key].setText(str(value))
            
            # Forçar atualização da interface gráfica
            self.update()  # ou self.repaint()

            # Exemplo de print para debug
            # print("Campos do cliente atualizados:", cliente_info)
        else:
            print(f"Nenhuma ordem de serviço encontrada para o código {id_ordem}")
    def clearCamposCliente(self):
        # Limpa os widgets existentes
        for field in self.campos_cliente.values():
            field.deleteLater()
        self.campos_cliente.clear()
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
            orcamento_passado = ord[9]
            orcamento_aprovado = ord[10]

            ordem_info = {
                    'Codigo': id_ordem,
                    'Data_inicial': data_inicio,
                    'Data_final': data_final,
                    'mao_de_obra': mao_de_obra,
                    'Total_ordem': valor_total,
                    'Total_material': total_material,
                    'Observacao': observacao,
                    'Orcamento_Passado': orcamento_passado,
                    'Orcamento_Aprovado': orcamento_aprovado
                    
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
                telefone2 = cliente[9]

                cliente_info = {
                    'Nome': nome,
                    'Cep': cep,
                    'Endereco': endereco,
                    'Número': numero,
                    'Cidade': cidade,
                    'Estado': estado,
                    'Cpf_cnpj': cpf_cnjp,
                    'Telefone': telefone,
                    'Telefone2': telefone2
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
                    potencia = equip[7]
                    defeito = equip[8]
                

                    equipamento_info = {
                        'Modelo': modelo,
                        'Rpm': rpm,
                        'Polos': polos,
                        'Fases': fases,
                        'Tensao': tensao,
                        'Marca': marca,
                        'Defeito': defeito,
                        'Potencia': potencia
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
        self.atualizar_campos_cliente()
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
            produto_id = dialog.line_produto.text().split(' - ')[0]
            
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
                novo_produto_id= dialog.line_produto.text().split(' - ')[0]
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
        
        self.line_produto = QLineEdit()
        self.line_produto.setReadOnly(True)
        self.btn_selecionar_produto = QPushButton("Selecionar Produto")
        self.btn_selecionar_produto.clicked.connect(self.open_produto_selection_dialog)
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
            valor_float = float(str(valor_unitario).replace(',', '.'))
            self.valor_unitario.setValue(valor_float)

        self.line_produto.setStyleSheet(style_sheet)
        self.quantidade.setStyleSheet(style_sheet)
        self.valor_unitario.setStyleSheet(style_sheet)

        form_layout.addRow(QLabel("Produto:"), self.line_produto)
        form_layout.addWidget(self.btn_selecionar_produto)
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
        
        self.setFixedSize(600, 400)
        if produtos_disponiveis:
            for produto in produtos_disponiveis:
                if produto[0] == produto_id:
                    self.line_produto.setText(f"{produto[0]} - {produto[1]}")
                    break

        # Conecta a função atualizar_valor_unitario tanto à mudança no produto quanto à mudança no campo de valor
       
        self.line_produto.textChanged.connect(self.atualizar_valor_unitario)
        self.valor_unitario.textChanged.connect(self.atualizar_valor_manual)

    def open_produto_selection_dialog(self):
        dialog = MaterialSelectionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            cliente_id, cliente_nome = dialog.get_selected_cliente()
            self.line_produto.setText(f"{cliente_id} - {cliente_nome}")
            self.cliente_id = cliente_id  # Atualiza os equipamentos com base no cliente selecionado
    
    def atualizar_valor_unitario(self):
        # Obtém o texto do QLineEdit
        texto = self.line_produto.text()
        
        # Supondo que o ID e o nome do produto estejam separados por ' - '
        if ' - ' in texto:
            produto_id = texto.split(' - ')[0]
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

class MaterialSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Selecionar Produto")
        self.selected_produto_id = None
        self.selected_produto_nome = None

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
        self.produto_table.setColumnCount(3)
        self.produto_table.setHorizontalHeaderLabels(['ID', 'Nome','Valor'])
        self.produto_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.produto_table)

        self.setLayout(layout)
        self.load_produtos()

        self.setFixedSize(600, 400)

    def load_produtos(self):
        produtos = self.parent().controller.FiltrarProduto(True)
        print(produtos)  # Adicione esta linha para depuração
        self.produto_table.setRowCount(len(produtos))
        for row, cliente in enumerate(produtos):
            self.produto_table.setItem(row, 0, QTableWidgetItem(str(cliente[0])))  # Certifique-se de converter para string
            self.produto_table.setItem(row, 1, QTableWidgetItem(cliente[1]))
            self.produto_table.setItem(row, 2, QTableWidgetItem(cliente[2]))

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
            self.selected_cliente_id = self.produto_table.item(selected_row, 0).text()
            self.selected_cliente_nome = self.produto_table.item(selected_row, 1).text()
            self.accept()

    def get_selected_cliente(self):
        return self.selected_cliente_id, self.selected_cliente_nome

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = OrdemDeServicoUI()  
    ui.show()
    sys.exit(app.exec_())
