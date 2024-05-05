import sys
from PyQt5.QtWidgets import QApplication
from login.login_window import LoginWindow
from main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    if login_window.exec_() == LoginWindow.Accepted:
        main_window = MainWindow()
        main_window.show()
    sys.exit(app.exec_())
