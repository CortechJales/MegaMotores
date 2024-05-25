from PyQt5.QtWidgets import QWidget, QDialog, QDoubleSpinBox, QMessageBox,QCheckBox,QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAction, QToolBar, QApplication
from PyQt5.QtCore import Qt
from marca.marca_controller import MarcaController
from PyQt5.QtGui import QIcon,QDoubleValidator

class MarcaUI(QWidget):
    def __init__(self,user_type):
        super().__init__()
        self.controller = MarcaController()
        self.user_type= user_type
        self.initUI()
        

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout()
 # Layout do filtro
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar por Nome / Código:"))
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
        self.marca_table = QTableWidget()
        self.marca_table.setStyleSheet("""
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
        self.marca_table.setColumnCount(3)
        self.marca_table.setHorizontalHeaderLabels(['Código', 'nome', 'Ativo'])
        self.marca_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.marca_table)

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
            action_add.triggered.connect(self.show_add_marca_dialog)
            action_edit.triggered.connect(self.show_edit_marca_dialog)
            action_delete.triggered.connect(self.delete_marca)
            action_inactive.triggered.connect(self.inactive_marca)
            action_ative.triggered.connect(self.ative_marca)
        if self.user_type == 'usr':
            # Botões de ação
            action_add = QAction("Adicionar", self)
            action_edit = QAction("Editar", self)
            action_inactive = QAction("Inativar", self)

            toolbar.addAction(action_add)
            toolbar.addAction(action_edit)
            toolbar.addAction(action_inactive)  

        # Configurar conexões de sinais e slots para os botões
            action_add.triggered.connect(self.show_add_marca_dialog)
            action_edit.triggered.connect(self.show_edit_marca_dialog)
            action_inactive.triggered.connect(self.inactive_marca)

        self.controller.create_table()
        self.setLayout(layout)
        self.filter_active()

    def filter_table(self):
        filter_text = self.filter_input.text().lower()
        for row in range(self.marca_table.rowCount()):
            match = False
            for col in range(self.marca_table.columnCount()):
                item = self.marca_table.item(row, col)
                if item is not None and item.text().lower().find(filter_text) != -1:
                    match = True
                    break
            self.marca_table.setRowHidden(row, not match)

    def filter_all(self):
        marcas = self.controller.ListarMarca()
        self.marca_table.setRowCount(0)
    
        for row_number, marca in enumerate(marcas):
            self.marca_table.insertRow(row_number)
        
            for column_number, data in enumerate(marca):
                item = QTableWidgetItem(str(data))
            
                if column_number == 2:  # Coluna 'Ativo'
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.marca_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.marca_table.setItem(row_number, column_number, item)

    def filter_active(self):
        marcas = self.controller.FiltraMarca(True)
        self.marca_table.setRowCount(0)
    
        for row_number, marca in enumerate(marcas):
            self.marca_table.insertRow(row_number)
        
            for column_number, data in enumerate(marca):
                item = QTableWidgetItem(str(data))
            
                if column_number == 2:  # Coluna 'Ativo'
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.marca_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.marca_table.setItem(row_number, column_number, item)

    def filter_inactive(self):
        marcas = self.controller.FiltraMarca(False)
        self.marca_table.setRowCount(0)
    
        for row_number, marca in enumerate(marcas):
            self.marca_table.insertRow(row_number)
        
            for column_number, data in enumerate(marca):
                item = QTableWidgetItem(str(data))
            
                if column_number == 2:  # Coluna 'Ativo'
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(data))
                    checkbox.setEnabled(False)
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.marca_table.setCellWidget(row_number, column_number, cell_widget)
                else:
                    self.marca_table.setItem(row_number, column_number, item)

    def add_marca(self, nome):
        self.controller.CadastrarMarca(nome)
        self.filter_active()  # Atualizar a tabela após adicionar clientes

    def edit_marca(self, nome, id):
        self.controller.EditarMarca(nome, id)
        self.filter_active()  # Atualizar a tabela após adicionar clientes


    def delete_marca(self,id):
      
        selected_row = self.marca_table.currentRow()
        if selected_row != -1:
            id = self.marca_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir a Marca código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.controller.DeletarMarca(id)
                self.filter_active()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um Produto para excluir.")

    def inactive_marca(self):
        selected_row = self.marca_table.currentRow()
        if selected_row != -1:
            id = self.marca_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja inativar a marca código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller.ValidarMarca(id)
                if resultado:
                    estado_produto = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_produto == 1:  # Verifica se o cliente está ativo
                        self.controller.InativarMarca(id)
                        self.filter_active()
                    else:
                        QMessageBox.warning(self, "Aviso", "marca já está inativo.")
                else:
                    QMessageBox.warning(self, "Aviso", "marca não encontrado.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma marca para inativar.")
 
    def ative_marca(self):
        selected_row = self.marca_table.currentRow()
        if selected_row != -1:
            id = self.marca_table.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja reativar a marca código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                resultado = self.controller.ValidarMarca(id)
                if resultado:
                    estado_cliente = resultado[0][0]  # Obtém o estado do cliente da consulta
                    if estado_cliente == 0:  # Verifica se o cliente está inativo
                        self.controller.AtivarMarca(id)
                        self.filter_active()
                    else:
                        QMessageBox.warning(self, "Aviso", "marca já está Ativo.")
                else:
                    QMessageBox.warning(self, "Aviso", "marca não encontrado.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um marca para Ativar.")   

    def show_add_marca_dialog(self):
        dialog = AdicionarEditarMarcaDialog()
        if dialog.exec_():
            nome = dialog.nome.text()
            self.add_marca(nome)
   
    def show_edit_marca_dialog(self):
        selected_row = self.marca_table.currentRow()
        if selected_row != -1:
            id = self.marca_table.item(selected_row, 0).text()
            nome = self.marca_table.item(selected_row, 1).text()
            dialog = AdicionarEditarMarcaDialog(nome)
            if dialog.exec_():
                novo_nome = dialog.nome.text()
               
                
                self.edit_marca(novo_nome, id)
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma marca para editar.")


class AdicionarEditarMarcaDialog(QDialog):
    def __init__(self, nome=""):
        super().__init__()
        self.setWindowTitle("Adicionar Marca")
        self.setWindowIcon(QIcon("img/megamotores.png"))  # Adicione o ícone desejado
        self.controller = MarcaController()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20) 

        form_layout = QFormLayout()
        
        self.nome = QLineEdit(nome)

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
        self.nome.setStyleSheet(style_sheet)

        form_layout.addRow(QLabel("Nome:"), self.nome)
       
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
        if not all([self.nome.text()]):
            QMessageBox.warning(self, "Erro", "O campo deve ser preenchido.")
            return False
        
        return True
   
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MarcaUI()  
    ui.show()
    sys.exit(app.exec_())
