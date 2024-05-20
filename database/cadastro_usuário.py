from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
import sys
import sqlite3
import bcrypt

class CadastroUsuario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Usuário")
        self.setGeometry(100, 100, 400, 250)

        layout = QVBoxLayout()

        self.username_label = QLabel("Nome de Usuário:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.confirm_password_label = QLabel("Confirmar Senha:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)

        self.tipo_usuario_label = QLabel("Tipo de Usuário:")
        self.tipo_usuario_combo = QComboBox()
        self.tipo_usuario_combo.addItems(["adm", "usr"])
        layout.addWidget(self.tipo_usuario_label)
        layout.addWidget(self.tipo_usuario_combo)

        self.cadastrar_button = QPushButton("Cadastrar")
        self.cadastrar_button.clicked.connect(self.cadastrar_usuario)
        layout.addWidget(self.cadastrar_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def cadastrar_usuario(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        tipo_usuario = self.tipo_usuario_combo.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Aviso", "Por favor, preencha todos os campos.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Aviso", "As senhas não coincidem.")
            return

        # Gerar o hash da senha
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect('database/gerenciamento_ordens_servico.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO usuario (username, password, tipo_usuario, ativo) VALUES (?, ?, ?, 1)",
                           (username, password_hash, tipo_usuario))
            conn.commit()
            QMessageBox.information(self, "Sucesso", "Usuário cadastrado com sucesso.")
            self.username_input.clear()
            self.password_input.clear()
            self.confirm_password_input.clear()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar usuário: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    cadastro_usuario = CadastroUsuario()
    cadastro_usuario.show()
    sys.exit(app.exec_())
