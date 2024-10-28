import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                             QMessageBox, QMainWindow)
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login Page')
        self.setGeometry(100, 100, 300, 150)

        # 创建布局
        layout = QVBoxLayout()

        # 用户名标签和输入框
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # 密码标签和输入框
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # 登录按钮
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == 'admin' and password == '1111111':
            QMessageBox.information(self, 'Login Success', 'Welcome, admin!')
            self.open_model_run_page()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Incorrect username or password.')

    def open_model_run_page(self):
        # 登录成功后跳转到模型演示页面
        self.close()  # 关闭登录窗口
        from runmodel import ModelRunPage
        self.model_run_page = ModelRunPage()  # 打开模型演示页面
        self.model_run_page.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
