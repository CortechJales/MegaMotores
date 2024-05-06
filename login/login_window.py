from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from database.database import Database
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QIcon

import bcrypt
import sys

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 150)
        self.setWindowIcon(QIcon("img/logotipo.png"))
        self.db = Database('database/gerenciamento_ordens_servico.db')  # Conectar ao banco de dados
        self.create_table()  # Criar a tabela se não existir
       

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuário")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        btn_login = QPushButton("Login")
        btn_login.clicked.connect(self.efetuar_login)
        layout.addWidget(btn_login)

        self.setLayout(layout)
        self.center_on_screen()

    login_successful = pyqtSignal()
    
    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS usuario (
            username TEXT PRIMARY KEY,
            password TEXT,
            tipo_usuario TEXT,
            ativo BOOLEAN
           )
        '''
        self.db.create_table(sql)

    def efetuar_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        print(f"Tentativa de login com usuário: {username} e senha: {password}")
        user_type = self.verificar_login(username, password)
        if user_type:
            print("Login bem-sucedido!")
            self.user_type = user_type
            self.accept()
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "Aviso", "Credenciais inválidas!")

    def verificar_login(self, username, password):
        query = 'SELECT * FROM usuario WHERE username=?'
        data = (username,)  # Certifique-se de que a tupla tenha uma vírgula ao final
        user_data = self.db.execute_query(query, data)
        if user_data:
            hashed_password = user_data[0][1]  # Acessando a senha da primeira linha retornada
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return user_data[0][2]  # Retorna o tipo de usuário (admin ou normal) da primeira linha
        return None
    def center_on_screen(self):
        # Obter a geometria da tela primária
        screen_geometry = QApplication.primaryScreen().geometry()

        # Obter a geometria da janela de login
        window_geometry = self.frameGeometry()

        # Definir a posição da janela de login para o centro da tela
        window_geometry.moveCenter(screen_geometry.center())

        # Aplicar a nova posição da janela de login
        self.move(window_geometry.topLeft())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
