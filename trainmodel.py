import sys
import psutil
import GPUtil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QComboBox, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QTextEdit, QProgressBar, 
                             QWidget, QGridLayout, QLineEdit, QMenuBar, QAction)
from PyQt5.QtCore import QTimer

class ModelTrainingPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口大小为 1980x1080
        self.setWindowTitle('Model Training Page')
        self.setGeometry(100, 100, 1980, 1080)

        # 创建菜单栏并添加页面跳转功能
        menubar = self.menuBar()
        pages_menu = menubar.addMenu('Pages')

        # 添加菜单项
        run_model_action = QAction('Model Demonstration Page', self)
        run_model_action.triggered.connect(self.open_model_demo_page)
        pages_menu.addAction(run_model_action)

        train_model_action = QAction('Model Training Page', self)
        train_model_action.triggered.connect(self.open_model_training_page)
        pages_menu.addAction(train_model_action)

        history_log_action = QAction('History Logging Page', self)
        history_log_action.triggered.connect(self.open_history_log_page)
        pages_menu.addAction(history_log_action)

        # 创建主窗口布局
        main_widget = QWidget()
        main_layout = QGridLayout()  # 使用网格布局便于调整
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 创建框架选择、超参数、暂停与恢复按钮
        framework_label = QLabel('Select Model Framework:')
        self.framework_combo = QComboBox()
        self.framework_combo.addItems(['TensorFlow', 'PyTorch', 'Keras'])  # 框架列表

        # 超参数调整
        lr_label = QLabel('Learning Rate:')
        self.lr_input = QLineEdit()
        self.lr_input.setPlaceholderText('Enter learning rate')

        batch_label = QLabel('Batch Size:')
        self.batch_input = QLineEdit()
        self.batch_input.setPlaceholderText('Enter batch size')

        # 暂停和恢复按钮
        self.pause_button = QPushButton('Pause')
        self.resume_button = QPushButton('Resume')

        self.pause_button.clicked.connect(self.pause_training)
        self.resume_button.clicked.connect(self.resume_training)

        # 将按钮横向排列
        top_button_layout = QHBoxLayout()
        top_button_layout.addWidget(framework_label)
        top_button_layout.addWidget(self.framework_combo)
        top_button_layout.addWidget(lr_label)
        top_button_layout.addWidget(self.lr_input)
        top_button_layout.addWidget(batch_label)
        top_button_layout.addWidget(self.batch_input)
        top_button_layout.addWidget(self.pause_button)
        top_button_layout.addWidget(self.resume_button)

        # 创建训练进度显示窗口
        self.progress_display = QTextEdit()
        self.progress_display.setReadOnly(True)
        self.progress_display.setPlaceholderText('Training progress will be displayed here...')

        # 添加 CPU/GPU 实时监控窗口
        self.cpu_progress = QProgressBar()
        self.gpu_progress = QProgressBar()

        self.cpu_progress.setRange(0, 100)
        self.gpu_progress.setRange(0, 100)

        self.cpu_label = QLabel("CPU Usage:")
        self.gpu_label = QLabel("GPU Usage:")

        cpu_layout = QHBoxLayout()
        cpu_layout.addWidget(self.cpu_label)
        cpu_layout.addWidget(self.cpu_progress)

        gpu_layout = QHBoxLayout()
        gpu_layout.addWidget(self.gpu_label)
        gpu_layout.addWidget(self.gpu_progress)

        # 添加网格布局组件
        main_layout.addLayout(top_button_layout, 0, 0, 1, 2)  # 将按钮组放在第一行
        main_layout.addWidget(self.progress_display, 1, 0, 1, 2)  # 训练进度放在中间
        main_layout.addLayout(cpu_layout, 2, 0)  # CPU 使用率放在下方
        main_layout.addLayout(gpu_layout, 2, 1)  # GPU 使用率放在下方

        # 创建定时器用于更新 CPU/GPU 实时监控
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_usage)
        self.timer.start(1000)  # 每秒更新一次

    def open_model_demo_page(self):
        self.close()
        from runmodel import ModelRunPage
        self.new_window = ModelRunPage()
        self.new_window.show()

    def open_model_training_page(self):
        self.close()
        self.new_window = ModelTrainingPage()
        self.new_window.show()

    def open_history_log_page(self):
        self.close()
        from history import HistoryLogPage
        self.new_window = HistoryLogPage()
        self.new_window.show()

    def update_usage(self):
        # 获取 CPU 使用率
        cpu_usage = int(psutil.cpu_percent(interval=1))  # 将浮点数转换为整数
        self.cpu_progress.setValue(cpu_usage)
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")

        # 获取 GPU 使用率
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_usage = int(gpus[0].load * 100)  # 将 GPU 使用率转换为整数
            self.gpu_progress.setValue(gpu_usage)
            self.gpu_label.setText(f"GPU Usage: {gpu_usage}%")
        else:
            self.gpu_progress.setValue(0)
            self.gpu_label.setText("GPU Usage: N/A")

    def pause_training(self):
        self.timer.stop()
        self.progress_display.append("Training paused.")

    def resume_training(self):
        self.timer.start(1000)
        self.progress_display.append("Training resumed.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    training_page = ModelTrainingPage()
    training_page.show()
    sys.exit(app.exec_())
