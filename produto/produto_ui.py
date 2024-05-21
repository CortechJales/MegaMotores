from PyQt5.QtWidgets import QWidget, QDialog, QDoubleSpinBox, QMessageBox,QCheckBox,QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAction, QToolBar, QApplication
from PyQt5.QtCore import Qt
from produto.produto_controller import ProdutoController
from PyQt5.QtGui import QIcon,QDoubleValidator

class ProdutoUI(QWidget):
    def __init__(self,user_type):
        super().__init__()
        self.controller = ProdutoController()
        self.user_type= user_type
        self.initUI()
        

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout()
 # Layout do filtro
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar por Descrição / Código:"))
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
        self.product_table = QTableWidget()
        self.product_table.setStyleSheet("""
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
        self.product_table.setColumnCount(4)
        self.product_table.setHorizontalHeaderLabels(['Código', 'Descrição', 'Valor', 'Ativo'])
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.product_table)

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
            action_add.triggered.connect(self.show_add_produto_dialog)
            action_edit.triggered.connect(self.show_edit_produto_dialog)
            action_delete.triggered.connect(self.delete_produto)
            action_inactive.triggered.connect(self.inactive_produto)
            action_ative.triggered.connect(self.ative_produto)
        if self.user_type == 'usr':
            # Botões de ação
            action_add = QAction("Adicionar", self)
            action_edit = QAction("Editar", self)
            action_inactive = QAction("Inativar", self)

            toolbar.addAction(action_add)
            toolbar.addAction(action_edit)
            toolbar.addAction(action_inactive)  

        # Configurar conexões de sinais e slots para os botões
            action_add.triggered.connect(self.show_add_produto_dialog)
            action_edit.triggered.connect(self.show_edit_produto_dialog)
            action_inactive.triggered.connect(self.inactive_produto)

        self.controller.create_table()
        self.setLayout(layout)
        self.filter_active()

    def filter_table(self):
        filter_text = self.filter_input.text().lower()
        for row in range(self.product_table.rowCount()):
            match = False
            for col in range(self.product_table.columnCount()):
                item = self.product_table.item(row, col)
                if item is not None and item.text().lower().find(filter_text) != -1:
                    match = True
                    break
            self.product_table.setRowHidden(row, not match)

    def filter_all(self):
        produtos = self.controller.ListarProduto()
        self.product_table.setRowCount(0)
    
        for row_number, produto in enumerate(produtos):
            self.product_table.insertRow(row_number)
        
            for column_number, data in enumerate(produto):
                item = QTableWidgetItem(str(data))
            
                if column_number == 3:  # Coluna 'Ativo'
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.product_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.product_table.setItem(row_number, column_number, item)

    def filter_active(self):
        produtos = self.controller.FiltrarProduto(True)
        self.product_table.setRowCount(0)
    
        for row_number, produto in enumerate(produtos):
            self.product_table.insertRow(row_number)
        
            for column_number, data in enumerate(produto):
                item = QTableWidgetItem(str(data))
            
                if column_number == 3:  # Coluna 'Ativo'
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.product_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.product_table.setItem(row_number, column_number, item)

    def filter_inactive(self):
        produtos = self.controller.FiltrarProduto(False)
        self.product_table.setRowCount(0)
    
        for row_number, produto in enumerate(produtos):
            self.product_table.insertRow(row_number)
        
            for column_number, data in enumerate(produto):
                item = QTableWidgetItem(str(data))
            
                if column_number == 3:  # Coluna 'Ativo'
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.product_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.product_table.setItem(row_number, column_number, item)

    def add_produto(self, id, descricao, valor):
        self.controller.CadastrarProduto( descricao, valor, id)
        self.filter_active()  # Atualizar a tabela após adicionar clientes

    def edit_produto(self, descricao,valor, id):
        self.controller.EditarProduto( descricao,valor, id)
        self.filter_active()  # Atualizar a tabela após adicionar clientes


    def delete_produto(self,id):
      
        selected_row = self.product_table.currentRow()
        if selected_row != -1:
            id = self.product_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir o produto ID {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.controller.DeletarProduto(id)
                self.filter_active()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um Produto para excluir.")

    def inactive_produto(self):
        selected_row = self.product_table.currentRow()
        if selected_row != -1:
            id = self.product_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja inativar o produto código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller.ValidarProduto(id)
                if resultado:
                    estado_produto = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_produto == 1:  # Verifica se o cliente está ativo
                        self.controller.InativarProduto(id)
                        self.filter_active()
                    else:
                        QMessageBox.warning(self, "Aviso", "produto já está inativo.")
                else:
                    QMessageBox.warning(self, "Aviso", "produto não encontrado.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um produto para inativar.")
 
    def ative_produto(self):
        selected_row = self.product_table.currentRow()
        if selected_row != -1:
            id = self.product_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja reativar o produto código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller.ValidarProduto(id)
                if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 0:  # Verifica se o cliente está inativo
                        self.controller.AtivarProduto(id)
                        self.filter_active()
                    else:
                        QMessageBox.warning(self, "Aviso", "Produto já está Ativo.")
                else:
                    QMessageBox.warning(self, "Aviso", "Produo não encontrado.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um Produto para Ativar.")   

    def show_add_produto_dialog(self):
        dialog = AdicionarProdutoDialog()
        if dialog.exec_():
            id = dialog.id.text()
            descricao = dialog.descricao.text()
            valor = dialog.valor.text()
           
            self.add_produto(id, descricao, valor)
   
    def show_edit_produto_dialog(self):
        selected_row = self.product_table.currentRow()
        if selected_row != -1:
            id = self.product_table.item(selected_row, 0).text()
            descricao = self.product_table.item(selected_row, 1).text()
            valor = self.product_table.item(selected_row, 2).text()
            dialog = EditarProdutoDialog(id,descricao,valor)
            if dialog.exec_():
                novo_descricao = dialog.descricao.text()
                novo_valor = dialog.valor.text()
                
                self.edit_produto(novo_descricao, novo_valor, id)
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para editar.")


class AdicionarProdutoDialog(QDialog):
    def __init__(self, id="", descricao="", valor=""):
        super().__init__()
        self.setWindowTitle("Adicionar Produto")
        self.setWindowIcon(QIcon("img/megamotores.png"))  # Adicione o ícone desejado
        self.controller = ProdutoController()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20) 

        form_layout = QFormLayout()
        
        self.id = QLineEdit(id)
        self.descricao = QLineEdit(descricao)
        self.valor = QDoubleSpinBox()
        self.valor.setDecimals(2)
        self.valor.setMaximum(9999.99)    # Definindo duas casas decimais
        

        # Estilo CSS para os campos de entrada
        style_sheet = """
            QLineEdit, QComboBox, QDoubleSpinBox {
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus{
                border-color: #e74c3c;
            }
        """
        self.id.setStyleSheet(style_sheet)
        self.descricao.setStyleSheet(style_sheet)
        self.valor.setStyleSheet(style_sheet)

        form_layout.addRow(QLabel("Código:"), self.id)
        form_layout.addRow(QLabel("Descrição:"), self.descricao)
        form_layout.addRow(QLabel("Valor:"), self.valor)
       
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
    
    def on_save(self):
        if not self.validate_fields():
            return

        self.accept()

    def validate_fields(self):
        # Verificar se todos os campos estão preenchidos
        if not all([self.id.text(), self.descricao.text(), self.valor.text()]):
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return False

        # Verificar se o valor digitado é maior que zero
        valor = self.valor.value()  # Obtendo o valor do QDoubleSpinBox
        if valor <= 0:
            QMessageBox.warning(self, "Erro", "O valor do produto deve ser maior que zero.")
            return False

        # Verificar se o valor tem duas casas decimais
        if not self.has_two_decimal_places(valor):
            QMessageBox.warning(self, "Erro", "O valor do produto seguir o padrão de 100,00.")
            return False

        # Verificar se o ID do produto já está cadastrado
        id_produto = self.id.text()  # Supondo que você esteja usando algum widget para capturar o ID do produto
        if self.controller.ValidarProdutoCadastrado(id_produto):
            QMessageBox.warning(self, "Erro", "ID do produto já cadastrado.")
            return False

        return True

    def has_two_decimal_places(self, number):
    # Converte o número para uma string e verifica se tem duas casas decimais
        decimal_part = str(number).split('.')[1]
        return len(decimal_part) <= 2
class EditarProdutoDialog(QDialog):
    def __init__(self, id="", descricao="", valor=""):
        super().__init__()
        self.setWindowTitle("Adicionar Produto")
        self.setWindowIcon(QIcon("img/megamotores.png"))  # Adicione o ícone desejado
        self.controller = ProdutoController()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20) 

        form_layout = QFormLayout()
        
        self.id = QLineEdit(id)
        self.id.setReadOnly(True)
        self.descricao = QLineEdit(descricao)
        self.valor = QDoubleSpinBox()
        self.valor.setDecimals(2)
        self.valor.setMaximum(9999.99) # Definindo duas casas decimais

        if valor:
            # Substitui a vírgula pelo ponto e converte para float
            valor_float = float(valor.replace(',', '.'))
            self.valor.setValue(valor_float)

        # Estilo CSS para os campos de entrada
        style_sheet = """
            QLineEdit, QComboBox, QDoubleSpinBox {
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus{
                border-color: #e74c3c;
            }
        """
        self.id.setStyleSheet(style_sheet)
        self.descricao.setStyleSheet(style_sheet)
        self.valor.setStyleSheet(style_sheet)

        form_layout.addRow(QLabel("Código:"), self.id)
        form_layout.addRow(QLabel("Descrição:"), self.descricao)
        form_layout.addRow(QLabel("Valor:"), self.valor)
       
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
    
    def on_save(self):
        if not self.validate_fields():
            return

        self.accept()

    def validate_fields(self):
        # Verificar se todos os campos estão preenchidos
        if not all([self.id.text(), self.descricao.text(), self.valor.text()]):
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return False

        # Verificar se o valor digitado é maior que zero
        valor = self.valor.value()  # Obtendo o valor do QDoubleSpinBox
        if valor <= 0:
            QMessageBox.warning(self, "Erro", "O valor do produto deve ser maior que zero.")
            return False

        # Verificar se o valor tem duas casas decimais
        if not self.has_two_decimal_places(valor):
            QMessageBox.warning(self, "Erro", "O valor do produto seguir o padrão de 100,00.")
            return False

        # Verificar se o ID do produto já está cadastrado

        return True

    def has_two_decimal_places(self, number):
    # Converte o número para uma string e verifica se tem duas casas decimais
        decimal_part = str(number).split('.')[1]
        return len(decimal_part) <= 2

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = ProdutoUI()  
    ui.show()
    sys.exit(app.exec_())
