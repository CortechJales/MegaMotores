from PyQt5.QtWidgets import QMainWindow, QAction, QStackedWidget, QHBoxLayout, QWidget, QSpacerItem, QPushButton, QSizePolicy, QLabel, QApplication
from PyQt5.QtGui import QIcon, QFont, QPixmap
from cliente.cliente_ui import ClienteUI
from produto.produto_ui import ProdutoUI
from marca.marca_ui import MarcaUI
from ordem_servico.ordem_de_servico_ui import OrdemDeServicoUI
from ordem_servico.orcamento_ui import OrcamentoUI
from database.cadastro_usuário import CadastroUsuario
from login.login_window import LoginWindow
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self, user_type=None):
        super().__init__()

        self.setWindowTitle("Sistema de Gerenciamento")
        self.setGeometry(100, 100, 900, 600)
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_imagens = os.path.join(diretorio_atual, 'img')
        caminho_imagem = os.path.join(pasta_imagens, 'megamotores.png')
        self.setWindowIcon(QIcon(caminho_imagem))

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.cliente_ui = ClienteUI(user_type)
        self.produto_ui = ProdutoUI(user_type)
        self.marca_ui = MarcaUI(user_type)
        self.ordem_de_servico_ui = OrdemDeServicoUI(user_type)
        self.orcamento_ui = OrcamentoUI(user_type)
        self.cadastro_ui = CadastroUsuario()

        self.central_widget.addWidget(self.cliente_ui)
        self.central_widget.addWidget(self.produto_ui)
        self.central_widget.addWidget(self.marca_ui)
        self.central_widget.addWidget(self.ordem_de_servico_ui)
        self.central_widget.addWidget(self.orcamento_ui)
        self.central_widget.addWidget(self.cadastro_ui)

        self.create_toolbar(user_type)
        self.center_on_screen()

    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def create_toolbar(self, user_type):
        toolbar = self.addToolBar("Toolbar")

        # Adicionando logo à toolbar
        logo_label = QLabel(self)
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_imagens = os.path.join(diretorio_atual, 'img')
        caminho_imagem = os.path.join(pasta_imagens, 'mega.png')
        pixmap = QPixmap(caminho_imagem)
        scaled_pixmap = pixmap.scaled(340, 60)  # Ajustar o tamanho conforme necessário
        logo_label.setPixmap(scaled_pixmap)
        toolbar.addWidget(logo_label)

        # Definindo ação para cada botão da toolbar
        cliente_action = QAction("Clientes", self)
        cliente_action.triggered.connect(lambda: self.change_page(self.cliente_ui))

        produto_action = QAction("Produtos", self)
        produto_action.triggered.connect(lambda: self.change_page(self.produto_ui))

        marca_action = QAction("Marca", self)
        marca_action.triggered.connect(lambda: self.change_page(self.marca_ui))

        orcamento_action = QAction("Orçamento", self)
        orcamento_action.triggered.connect(lambda: self.change_page(self.orcamento_ui))
        
        ordem_de_servico_action = QAction("Ordens de Serviço", self)
        ordem_de_servico_action.triggered.connect(lambda: self.change_page(self.ordem_de_servico_ui))

        if user_type == 'adm':
            usuario_action = QAction("Usuários", self)
            usuario_action.triggered.connect(lambda: self.change_page(self.cadastro_ui))

        actions = [cliente_action, produto_action, marca_action, orcamento_action, ordem_de_servico_action]
        if user_type == 'adm':
            actions.append(usuario_action)

        button_style = """
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 10px;
            margin-left: 10px;
            margin-top: 5px;
        """

        for action in actions:
            action_button = QPushButton(action.text(), self)
            action_button.setStyleSheet(button_style)
            action_button.clicked.connect(action.trigger)
            toolbar.addWidget(action_button)

        # Adicionar botão de deslogar à direita
        layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)

        btn_logout = QPushButton("Deslogar")
        btn_logout.setMinimumWidth(100)
        btn_logout.clicked.connect(self.show_login_dialog)
        btn_logout.setStyleSheet("""
            background-color: #FF5733;
            color: white;
            border: 2px solid #FF5733;
            border-radius: 5px;
            padding: 5px 10px;
            margin-left: 10px;
        """)
        btn_logout.setFont(QFont("Arial", 10))

        layout.addWidget(btn_logout)

        widget = QWidget()
        widget.setLayout(layout)

        toolbar.addWidget(widget)

    def change_page(self, page):
        # Altera para a página especificada e chama filter_active() se for uma UI válida
        self.central_widget.setCurrentWidget(page)
        if hasattr(page, 'filter_active') and callable(getattr(page, 'filter_active')):
            page.filter_active()

    def show_login_dialog(self):
        self.hide()
        self.login_window = LoginWindow()
        self.login_window.show()
        if self.login_window.exec_() == LoginWindow.Accepted:
            user_type = self.login_window.user_type
            self.handle_login_success(user_type)

    def handle_login_success(self, user_type):
        self.user_type = user_type
        self.show_main_window(user_type)

    def show_main_window(self, user_type):
        self.login_window.close()
        self.main_window = MainWindow(user_type)
        self.main_window.show()

    def close_application(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
