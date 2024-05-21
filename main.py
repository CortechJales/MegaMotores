import sys
from PyQt5.QtWidgets import QApplication
from login.login_window import LoginWindow
from main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    if login_window.exec_() == LoginWindow.Accepted:
        user_type = login_window.user_type  # Obtendo o user_type da LoginWindow
        main_window = MainWindow(user_type)  # Passando o user_type para a MainWindow
        main_window.show()
    sys.exit(app.exec_())

 