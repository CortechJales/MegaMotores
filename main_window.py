from PyQt5.QtWidgets import QMainWindow, QAction, QStackedWidget, QHBoxLayout, QWidget, QSpacerItem, QPushButton, QSizePolicy, QMessageBox, QMenu, QApplication
from cliente.cliente_ui import ClienteUI
from produto.produto_ui import ProdutoUI
from ordem_servico.ordem_de_servico_ui import OrdemDeServicoUI
from login.login_window import LoginWindow
from PyQt5.QtGui import QIcon, QFont
import sys

class MainWindow(QMainWindow):
    def __init__(self,user_type=None):
        super().__init__()

        self.setWindowTitle("Sistema de Gerenciamento")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("img/logotipo.png"))

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        
        self.cliente_ui = ClienteUI(user_type)
        self.produto_ui = ProdutoUI()
        self.ordem_de_servico_ui = OrdemDeServicoUI()

        self.central_widget.addWidget(self.cliente_ui)
        self.central_widget.addWidget(self.produto_ui)
        self.central_widget.addWidget(self.ordem_de_servico_ui)

        self.create_toolbar()
        self.center_on_screen()
        
    def center_on_screen(self):
        # Obter a geometria da tela primária
        screen_geometry = QApplication.primaryScreen().geometry()

        # Obter a geometria da janela de login
        window_geometry = self.frameGeometry()

        # Definir a posição da janela de login para o centro da tela
        window_geometry.moveCenter(screen_geometry.center())

        # Aplicar a nova posição da janela de login
        self.move(window_geometry.topLeft())

    def create_toolbar(self):
        toolbar = self.addToolBar("Toolbar")

        cliente_action = QAction("Clientes", self)
        cliente_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.cliente_ui))

        produto_action = QAction("Produtos", self)
        produto_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.produto_ui))

        ordem_de_servico_action = QAction("Ordens de Serviço", self)
        ordem_de_servico_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.ordem_de_servico_ui))

        toolbar.addAction(cliente_action)
        toolbar.addAction(produto_action)
        toolbar.addAction(ordem_de_servico_action)

        # Adicionar botão de deslogar à direita
        layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)

        btn_logout = QPushButton("Deslogar")
        btn_logout.setMinimumWidth(100)
        btn_logout.clicked.connect(self.show_logout_menu)
        btn_logout.setStyleSheet("background-color: #f0f0f0; color: #666; border: 1px solid #ccc; border-radius: 5px;")
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
        self.hide()  # Esconde a janela principal
        self.login_window = LoginWindow()  # Cria uma nova instância da janela de login
        self.login_window.show()  # Mostra a janela de login
        if self.login_window.exec_() == LoginWindow.Accepted:
            user_type = self.login_window.user_type  # Obtendo o user_type da LoginWindow
            self.handle_login_success(user_type)

    
    def handle_login_success(self, user_type):
        self.user_type = user_type
        self.show_main_window(user_type)  # Passa o user_type recebido como argumento


    def show_main_window(self, user_type):
        self.login_window.close()  # Fecha a janela de login
        self.main_window = MainWindow(user_type)  # Passa o user_type recebido como argumento
        self.main_window.show()
 

    def close_application(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
