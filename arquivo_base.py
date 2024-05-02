import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QDialog, QMessageBox, QComboBox, QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QIcon, QFont
import sqlite3

def conectar_banco():
    conn = sqlite3.connect('gerenciamento_ordens_servico.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                      id INTEGER PRIMARY KEY,
                      nome TEXT,
                      cep TEXT,
                      endereco TEXT,
                      cidade TEXT,
                      estado TEXT,
                      cpf_cnpj TEXT,
                      telefone TEXT,
                      ativo BOOLEAN
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS equipamento_cliente (
                      id INTEGER PRIMARY KEY,
                      descricao TEXT,
                      cliente_id INTEGER,
                      ativo BOOLEAN,
                      FOREIGN KEY(cliente_id) REFERENCES clientes(id)
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                      id INTEGER PRIMARY KEY,
                      descricao TEXT,
                      valor REAL,
                      ativo BOOLEAN
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ordens_servico (
                      id INTEGER PRIMARY KEY,
                      cliente_id INTEGER,
                      data_inicio DATA,
                      data_final DATA,
                      mao_de_obra REAL,
                      valor_total REAL,
                      ativo BOOLEAN
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS itens_ordem (
                      id INTEGER PRIMARY KEY,
                      ordem_id INTEGER,
                      produto_id INTEGER,
                      quantidade INTEGER,
                      FOREIGN KEY(ordem_id) REFERENCES ordens_servico(id),
                      FOREIGN KEY(produto_id) REFERENCES produtos(id)
                      )''')
    conn.commit()
    return conn, cursor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gerenciamento de Ordens de Serviço")
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowIcon(QIcon("img/logotipo.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.btn_clientes = QPushButton("Gerenciar Clientes")
        self.btn_clientes.clicked.connect(self.abrir_janela_clientes)
        self.layout.addWidget(self.btn_clientes)

        self.btn_produtos = QPushButton("Gerenciar Produtos")
        self.btn_produtos.clicked.connect(self.abrir_janela_produtos)
        self.layout.addWidget(self.btn_produtos)

        self.btn_ordens_servico = QPushButton("Gerenciar Ordens de Serviço")
        self.btn_ordens_servico.clicked.connect(self.abrir_janela_ordens_servico)
        self.layout.addWidget(self.btn_ordens_servico)

    def abrir_janela_clientes(self):
        self.clientes_window = ClientesWindow()
        self.clientes_window.show()

    def abrir_janela_produtos(self):
        self.produtos_window = ProdutosWindow()
        self.produtos_window.show()

    def abrir_janela_ordens_servico(self):
        self.ordens_servico_window = OrdensServicoWindow()
        self.ordens_servico_window.show()

class ClientesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Clientes")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table_clientes = QTableWidget()
        self.table_clientes.setColumnCount(8)
        self.table_clientes.setHorizontalHeaderLabels(['ID', 'Nome', 'CEP', 'Endereço', 'Cidade','Estado', 'CPF/CNPJ', 'telefone'])
        self.layout.addWidget(self.table_clientes)

        self.btn_adicionar_cliente = QPushButton("Adicionar Cliente")
        self.btn_adicionar_cliente.clicked.connect(self.adicionar_cliente)
        self.layout.addWidget(self.btn_adicionar_cliente)

        self.btn_editar_cliente = QPushButton("Editar Cliente")
        self.btn_editar_cliente.clicked.connect(self.editar_cliente)
        self.layout.addWidget(self.btn_editar_cliente)

        self.btn_excluir_cliente = QPushButton("Excluir Cliente")
        self.btn_excluir_cliente.clicked.connect(self.excluir_cliente)
        self.layout.addWidget(self.btn_excluir_cliente)

        self.btn_inativar_cliente = QPushButton("Inativar Cliente")
        self.btn_inativar_cliente.clicked.connect(self.inativar_cliente)
        self.layout.addWidget(self.btn_inativar_cliente)

        self.btn_carregar_todos_clientes = QPushButton("Carregar Todos Cliente")
        self.btn_carregar_todos_clientes.clicked.connect(self.carregar_todos_clientes)
        self.layout.addWidget(self.btn_carregar_todos_clientes)
       
        self.btn_carregar_clientes_ativos = QPushButton("Filtrar clientes ativos")
        self.btn_carregar_clientes_ativos.clicked.connect(self.carregar_clientes)
        self.layout.addWidget(self.btn_carregar_clientes_ativos)

        self.btn_carregar_clientes_inativos = QPushButton("Filtrar clientes inativos")
        self.btn_carregar_clientes_inativos.clicked.connect(self.carregar_clientes_inativos)
        self.layout.addWidget(self.btn_carregar_clientes_inativos)

        self.conn, self.cursor = conectar_banco()
        self.carregar_clientes()

    def carregar_clientes(self):
        self.table_clientes.setRowCount(0)
        self.cursor.execute("SELECT * FROM clientes WHERE ativo = ?", (True,))
        clientes = self.cursor.fetchall()
        for row_number, cliente in enumerate(clientes):
            self.table_clientes.insertRow(row_number)
            for column_number, data in enumerate(cliente):
                self.table_clientes.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def carregar_todos_clientes(self):
        self.table_clientes.setRowCount(0)
        self.cursor.execute("SELECT * FROM clientes")
        clientes = self.cursor.fetchall()
        for row_number, cliente in enumerate(clientes):
            self.table_clientes.insertRow(row_number)
            for column_number, data in enumerate(cliente):
                self.table_clientes.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            
    def carregar_clientes_inativos(self):
        self.table_clientes.setRowCount(0)
        self.cursor.execute("SELECT * FROM clientes WHERE ativo = ?", (False,))
        clientes = self.cursor.fetchall()
        for row_number, cliente in enumerate(clientes):
            self.table_clientes.insertRow(row_number)
            for column_number, data in enumerate(cliente):
                self.table_clientes.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def adicionar_cliente(self):
        dialog = AdicionarEditarClienteDialog()
        if dialog.exec_():
            nome = dialog.nome.text()
            cep = dialog.cep.text()            
            endereco = dialog.endereco.text()            
            cidade = dialog.cidade.text()
            estado = dialog.estado.text()
            cpf_cnpj = dialog.cpf_cnpj.text()
            telefone = dialog.telefone.text()
            
            self.cursor.execute("INSERT INTO clientes (nome, cep, endereco, cidade, estado, cpf_cnpj,telefone,ativo) VALUES (?, ?, ?, ?,?, ?, ?, ?)", (nome,cep, endereco, cidade, estado, cpf_cnpj, telefone, True))
            self.conn.commit()
            self.carregar_clientes()

    def editar_cliente(self):
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            id = self.table_clientes.item(selected_row, 0).text()
            nome = self.table_clientes.item(selected_row, 1).text()
            cep = self.table_clientes.item(selected_row, 2).text()
            endereco = self.table_clientes.item(selected_row, 3).text()
            cidade = self.table_clientes.item(selected_row, 4).text()
            estado = self.table_clientes.item(selected_row, 5).text()
            cpf_cnpj = self.table_clientes.item(selected_row, 6).text()            
            telefone = self.table_clientes.item(selected_row, 7).text()
            dialog = AdicionarEditarClienteDialog(nome, cep, endereco, cidade, estado, cpf_cnpj,telefone)
            if dialog.exec_():
                novo_nome = dialog.nome.text()
                novo_cep = dialog.cep.text()
                novo_endereco = dialog.endereco.text()
                novo_cidade = dialog.cidade.text()
                novo_estado = dialog.estado.text()
                novo_cpf_cnpj = dialog.cpf_cnpj.text()
                novo_telefone = dialog.telefone.text()
                self.cursor.execute("UPDATE clientes SET nome=?, cep=?, endereco=?, cidade=?, estado=?, cpf_cnpj=?,telefone=? WHERE id=?", (novo_nome, novo_cep, novo_endereco, novo_cidade, novo_estado, novo_cpf_cnpj, novo_telefone, id))
                self.conn.commit()
                self.carregar_clientes()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para editar.")

    def excluir_cliente(self):
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            id = self.table_clientes.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir o cliente ID {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.cursor.execute("DELETE FROM clientes WHERE id=?", (id,))
                self.conn.commit()
                self.carregar_clientes()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para excluir.")
    
    def inativar_cliente(self):
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            id = self.table_clientes.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja inativar o cliente código {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.cursor.execute("UPDATE clientes SET ativo=? WHERE id=?", (False, id))
                self.conn.commit()
                self.carregar_clientes()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para excluir.")    

class AdicionarEditarClienteDialog(QDialog):
    def __init__(self, nome="",cep="",endereco="",cidade="",estado="", cpf_cnpj="", telefone=""):
        super().__init__()
        self.setWindowTitle("Adicionar/Editar Cliente")

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
        layout.addWidget(self.cpf_cnpj);        

        self.telefone = QLineEdit(telefone)
        self.telefone.setPlaceholderText("Telefone")
        layout.addWidget(self.telefone)

        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.accept)
        layout.addWidget(btn_salvar)

        self.setLayout(layout)

class ProdutosWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Produtos")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table_produtos = QTableWidget()
        self.table_produtos.setColumnCount(5)
        self.table_produtos.setHorizontalHeaderLabels(['ID', 'Nome', 'Descrição', 'Código', 'Preço'])
        self.layout.addWidget(self.table_produtos)

        self.btn_adicionar_produto = QPushButton("Adicionar Produto")
        self.btn_adicionar_produto.clicked.connect(self.adicionar_produto)
        self.layout.addWidget(self.btn_adicionar_produto)

        self.btn_editar_produto = QPushButton("Editar Produto")
        self.btn_editar_produto.clicked.connect(self.editar_produto)
        self.layout.addWidget(self.btn_editar_produto)

        self.btn_excluir_produto = QPushButton("Excluir Produto")
        self.btn_excluir_produto.clicked.connect(self.excluir_produto)
        self.layout.addWidget(self.btn_excluir_produto)

        self.conn, self.cursor = conectar_banco()
        self.carregar_produtos()

    def carregar_produtos(self):
        self.table_produtos.setRowCount(0)
        self.cursor.execute("SELECT * FROM produtos")
        produtos = self.cursor.fetchall()
        for row_number, produto in enumerate(produtos):
            self.table_produtos.insertRow(row_number)
            for column_number, data in enumerate(produto):
                self.table_produtos.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def adicionar_produto(self):
        dialog = AdicionarEditarProdutoDialog()
        if dialog.exec_():
            nome = dialog.nome.text()
            descricao = dialog.descricao.text()
            codigo = dialog.codigo.text()
            preco = dialog.preco.text()
            self.cursor.execute("INSERT INTO produtos (nome, descricao, codigo, preco) VALUES (?, ?, ?, ?)", (nome, descricao, codigo, preco))
            self.conn.commit()
            self.carregar_produtos()

    def editar_produto(self):
        selected_row = self.table_produtos.currentRow()
        if selected_row != -1:
            id = self.table_produtos.item(selected_row, 0).text()
            nome = self.table_produtos.item(selected_row, 1).text()
            descricao = self.table_produtos.item(selected_row, 2).text()
            codigo = self.table_produtos.item(selected_row, 3).text()
            preco = self.table_produtos.item(selected_row, 4).text()
            dialog = AdicionarEditarProdutoDialog(nome, descricao, codigo, preco)
            if dialog.exec_():
                novo_nome = dialog.nome.text()
                nova_descricao = dialog.descricao.text()
                novo_codigo = dialog.codigo.text()
                novo_preco = dialog.preco.text()
                self.cursor.execute("UPDATE produtos SET nome=?, descricao=?, codigo=?, preco=? WHERE id=?", (novo_nome, nova_descricao, novo_codigo, novo_preco, id))
                self.conn.commit()
                self.carregar_produtos()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um produto para editar.")

    def excluir_produto(self):
        selected_row = self.table_produtos.currentRow()
        if selected_row != -1:
            id = self.table_produtos.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir o produto ID {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.cursor.execute("DELETE FROM produtos WHERE id=?", (id,))
                self.conn.commit()
                self.carregar_produtos()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um produto para excluir.")

class AdicionarEditarProdutoDialog(QDialog):
    def __init__(self, nome="", descricao="", codigo="", preco=""):
        super().__init__()
        self.setWindowTitle("Adicionar/Editar Produto")

        layout = QVBoxLayout()

        self.nome = QLineEdit(nome)
        self.nome.setPlaceholderText("Nome")
        layout.addWidget(self.nome)

        self.descricao = QLineEdit(descricao)
        self.descricao.setPlaceholderText("Descrição")
        layout.addWidget(self.descricao)

        self.codigo = QLineEdit(codigo)
        self.codigo.setPlaceholderText("Código")
        layout.addWidget(self.codigo)

        self.preco = QLineEdit(preco)
        self.preco.setPlaceholderText("Preço")
        layout.addWidget(self.preco)

        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.accept)
        layout.addWidget(btn_salvar)

        self.setLayout(layout)

class OrdensServicoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Ordens de Serviço")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table_ordens_servico = QTableWidget()
        self.table_ordens_servico.setColumnCount(6)
        self.table_ordens_servico.setHorizontalHeaderLabels(['ID', 'Cliente', 'Data Início', 'Data Final', 'Mão de Obra', 'Valor Total'])
        self.layout.addWidget(self.table_ordens_servico)

        self.btn_adicionar_ordem = QPushButton("Adicionar Ordem de Serviço")
        self.btn_adicionar_ordem.clicked.connect(self.adicionar_ordem)
        self.layout.addWidget(self.btn_adicionar_ordem)

        self.btn_editar_ordem = QPushButton("Editar Ordem de Serviço")
        self.btn_editar_ordem.clicked.connect(self.editar_ordem)
        self.layout.addWidget(self.btn_editar_ordem)

        self.btn_excluir_ordem = QPushButton("Excluir Ordem de Serviço")
        self.btn_excluir_ordem.clicked.connect(self.excluir_ordem)
        self.layout.addWidget(self.btn_excluir_ordem)

        self.conn, self.cursor = conectar_banco()
        self.carregar_ordens_servico()

    def carregar_ordens_servico(self):
        self.table_ordens_servico.setRowCount(0)
        self.cursor.execute("SELECT ordens_servico.id, clientes.nome, ordens_servico.data_inicio, ordens_servico.data_final, ordens_servico.mao_de_obra, ordens_servico.valor_total FROM ordens_servico JOIN clientes ON ordens_servico.cliente_id = clientes.id")
        ordens_servico = self.cursor.fetchall()
        for row_number, ordem_servico in enumerate(ordens_servico):
            self.table_ordens_servico.insertRow(row_number)
            for column_number, data in enumerate(ordem_servico):
                self.table_ordens_servico.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def adicionar_ordem(self):
        dialog = AdicionarEditarOrdemServicoDialog(self.conn, self.cursor)
        if dialog.exec_():
            self.carregar_ordens_servico()

    def editar_ordem(self):
        selected_row = self.table_ordens_servico.currentRow()
        if selected_row != -1:
            id = self.table_ordens_servico.item(selected_row, 0).text()
            dialog = AdicionarEditarOrdemServicoDialog(self.conn, self.cursor, id)
            if dialog.exec_():
                self.carregar_ordens_servico()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma ordem de serviço para editar.")

    def excluir_ordem(self):
        selected_row = self.table_ordens_servico.currentRow()
        if selected_row != -1:
            id = self.table_ordens_servico.item(selected_row, 0).text()
            resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir a ordem de serviço ID {id}?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.cursor.execute("DELETE FROM ordens_servico WHERE id=?", (id,))
                self.conn.commit()
                self.carregar_ordens_servico()
        else:
            QMessageBox.warning(self, "Aviso", "Selecione uma ordem de serviço para excluir.")

class AdicionarEditarOrdemServicoDialog(QDialog):
    def __init__(self, conn, cursor, id=None):
        super().__init__()
        self.setWindowTitle("Adicionar/Editar Ordem de Serviço")
        self.conn = conn
        self.cursor = cursor

        layout = QVBoxLayout()

        self.combo_clientes = QComboBox()
        self.combo_clientes.addItem("Selecione um cliente")
        self.cursor.execute("SELECT id, nome FROM clientes")
        clientes = self.cursor.fetchall()
        for cliente in clientes:
            self.combo_clientes.addItem(f"{cliente[0]} - {cliente[1]}")
        layout.addWidget(self.combo_clientes)

        self.data_inicio = QLineEdit()
        self.data_inicio.setPlaceholderText("Data de Início (AAAA-MM-DD)")
        layout.addWidget(self.data_inicio)

        self.data_final = QLineEdit()
        self.data_final.setPlaceholderText("Data Final (AAAA-MM-DD)")
        layout.addWidget(self.data_final)

        self.mao_de_obra = QLineEdit()
        self.mao_de_obra.setPlaceholderText("Mão de Obra")
        layout.addWidget(self.mao_de_obra)

        self.table_itens_ordem = QTableWidget()
        self.table_itens_ordem.setColumnCount(3)
        self.table_itens_ordem.setHorizontalHeaderLabels(['Produto', 'Quantidade', 'Preço'])
        layout.addWidget(self.table_itens_ordem)

        self.btn_adicionar_item = QPushButton("Adicionar Item")
        self.btn_adicionar_item.clicked.connect(self.adicionar_item)
        layout.addWidget(self.btn_adicionar_item)

        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.salvar)
        layout.addWidget(btn_salvar)

        self.setLayout(layout)

        if id:
            self.carregar_ordem_servico(id)

    def carregar_ordem_servico(self, id):
        self.cursor.execute("SELECT * FROM ordens_servico WHERE id=?", (id,))
        ordem_servico = self.cursor.fetchone()
        self.combo_clientes.setCurrentIndex(self.combo_clientes.findText(f"{ordem_servico[1]} - {ordem_servico[2]}"))
        self.data_inicio.setText(ordem_servico[3])
        self.data_final.setText(ordem_servico[4])
        self.mao_de_obra.setText(str(ordem_servico[5]))

        self.cursor.execute("SELECT produtos.nome, itens_ordem.quantidade, produtos.preco FROM itens_ordem JOIN produtos ON itens_ordem.produto_id = produtos.id WHERE itens_ordem.ordem_id=?", (id,))
        itens_ordem = self.cursor.fetchall()
        self.table_itens_ordem.setRowCount(0)
        for row_number, item in enumerate(itens_ordem):
            self.table_itens_ordem.insertRow(row_number)
            for column_number, data in enumerate(item):
                self.table_itens_ordem.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def adicionar_item(self):
        dialog = AdicionarItemDialog(self.conn, self.cursor)
        if dialog.exec_():
            nome_produto = dialog.combo_produtos.currentText()
            quantidade = dialog.quantidade.text()
            preco_produto = dialog.preco_produto.text()
            self.table_itens_ordem.insertRow(self.table_itens_ordem.rowCount())
            self.table_itens_ordem.setItem(self.table_itens_ordem.rowCount() - 1, 0, QTableWidgetItem(nome_produto))
            self.table_itens_ordem.setItem(self.table_itens_ordem.rowCount() - 1, 1, QTableWidgetItem(quantidade))
            self.table_itens_ordem.setItem(self.table_itens_ordem.rowCount() - 1, 2, QTableWidgetItem(preco_produto))

    def salvar(self):
        cliente_id = self.combo_clientes.currentText().split(' - ')[0]
        data_inicio = self.data_inicio.text()
        data_final = self.data_final.text()
        mao_de_obra = self.mao_de_obra.text()

        self.cursor.execute("INSERT INTO ordens_servico (cliente_id, data_inicio, data_final, mao_de_obra) VALUES (?, ?, ?, ?)", (cliente_id, data_inicio, data_final, mao_de_obra))
        ordem_id = self.cursor.lastrowid

        for row in range(self.table_itens_ordem.rowCount()):
            nome_produto = self.table_itens_ordem.item(row, 0).text()
            quantidade = self.table_itens_ordem.item(row, 1).text()
            self.cursor.execute("SELECT id, preco FROM produtos WHERE nome=?", (nome_produto,))
            produto = self.cursor.fetchone()
            produto_id = produto[0]
            preco_produto = produto[1]
            self.cursor.execute("INSERT INTO itens_ordem (ordem_id, produto_id, quantidade) VALUES (?, ?, ?)", (ordem_id, produto_id, quantidade))

        self.conn.commit()
        self.accept()

class AdicionarItemDialog(QDialog):
    def __init__(self, conn, cursor):
        super().__init__()
        self.setWindowTitle("Adicionar Item")

        layout = QVBoxLayout()

        self.combo_produtos = QComboBox()
        self.combo_produtos.addItem("Selecione um produto")
        cursor.execute("SELECT nome FROM produtos")
        produtos = cursor.fetchall()
        for produto in produtos:
            self.combo_produtos.addItem(produto[0])
        layout.addWidget(self.combo_produtos)

        self.quantidade = QLineEdit()
        self.quantidade.setPlaceholderText("Quantidade")
        layout.addWidget(self.quantidade)

        self.preco_produto = QLineEdit()
        self.preco_produto.setPlaceholderText("Preço")
        layout.addWidget(self.preco_produto)

        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.accept)
        layout.addWidget(btn_salvar)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
