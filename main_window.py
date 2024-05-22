from PyQt5.QtWidgets import QMainWindow, QAction, QStackedWidget, QHBoxLayout, QWidget, QSpacerItem, QPushButton, QSizePolicy, QMessageBox, QMenu, QApplication, QLabel
from cliente.cliente_ui import ClienteUI
from produto.produto_ui import ProdutoUI
from ordem_servico.ordem_de_servico_ui import OrdemDeServicoUI
from marca.marca_ui import MarcaUI
from database.cadastro_usuário import CadastroUsuario
from login.login_window import LoginWindow
from PyQt5.QtGui import QIcon, QFont,QPixmap
import sys



class MainWindow(QMainWindow):
    def __init__(self, user_type=None):
        super().__init__()

        self.setWindowTitle("Sistema de Gerenciamento")
        self.setGeometry(100, 100, 900, 600)
        self.setWindowIcon(QIcon("img/megamotores.png"))

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.cliente_ui = ClienteUI(user_type)
        self.produto_ui = ProdutoUI(user_type)
        self.marca_ui = MarcaUI(user_type)
        self.ordem_de_servico_ui = OrdemDeServicoUI()
        self.cadastro_ui = CadastroUsuario()

        self.central_widget.addWidget(self.cliente_ui)
        self.central_widget.addWidget(self.produto_ui)
        self.central_widget.addWidget(self.marca_ui)
        self.central_widget.addWidget(self.ordem_de_servico_ui)
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

        logo_label = QLabel(self)
        pixmap = QPixmap("img/mega.png")
        scaled_pixmap = pixmap.scaled(340, 60)  # Ajustar o tamanho conforme necessário
        logo_label.setPixmap(scaled_pixmap)
        toolbar.addWidget(logo_label)

        cliente_action = QAction("Clientes", self)
        cliente_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.cliente_ui))

        produto_action = QAction("Produtos", self)
        produto_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.produto_ui))

        marca_action = QAction("Marca", self)
        marca_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.marca_ui))

        ordem_de_servico_action = QAction("Ordens de Serviço", self)
        ordem_de_servico_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.ordem_de_servico_ui))

        
        if user_type == 'adm':
            usuario_action = QAction("Usuários", self)
            usuario_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.cadastro_ui))
        # Estilo para os botões da barra de ferramentas
        button_style = """
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 10px;
            margin-left: 10px;
            margin-top: 5px;
        
        """
        if user_type == 'adm':
            for action in [cliente_action, produto_action,marca_action, ordem_de_servico_action, usuario_action]:
                action_button = QPushButton(action.text(), self)
                action_button.setStyleSheet(button_style)
                action_button.clicked.connect(action.trigger)
                toolbar.addWidget(action_button)
        else:
            for action in [cliente_action, produto_action, marca_action, ordem_de_servico_action]:
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
        btn_logout.clicked.connect(self.show_login_dialog)  # Modificado aqui
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


    def show_logout_menu(self):
        menu = QMenu()

        login_action = QAction("Voltar para o login", self)
        login_action.triggered.connect(self.show_login_dialog)

        close_action = QAction("Fechar", self)
        close_action.triggered.connect(self.close_application)

        menu.addAction(login_action)
        menu.addAction(close_action)

        menu.exec_(self.sender().mapToGlobal(self.sender().rect().bottomRight()))

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
