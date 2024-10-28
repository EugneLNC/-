import sys
import psutil
import GPUtil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QComboBox, QPushButton, 
                             QFileDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QProgressBar, 
                             QWidget, QGridLayout, QMenuBar, QAction)
from PyQt5.QtCore import QTimer


class ModelRunPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口大小为 1980x1080
        self.setWindowTitle('Model Demonstration Page')
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

        # 创建硬件选择、模型选择、输入选择按钮
        hardware_label = QLabel('Select Hardware:')
        self.hardware_combo = QComboBox()
        self.hardware_combo.addItems(['CPU', 'GPU'])

        model_label = QLabel('Select Model:')
        self.model_combo = QComboBox()
        self.model_combo.addItems(['Model 1', 'Model 2', 'Model 3'])  # 模型列表占位符

        input_label = QLabel('Select Input:')
        self.input_button = QPushButton('Choose Input File')
        self.input_button.clicked.connect(self.choose_input)

        # 将按钮横向排列
        top_button_layout = QHBoxLayout()
        top_button_layout.addWidget(hardware_label)
        top_button_layout.addWidget(self.hardware_combo)
        top_button_layout.addWidget(model_label)
        top_button_layout.addWidget(self.model_combo)
        top_button_layout.addWidget(input_label)
        top_button_layout.addWidget(self.input_button)

        # 创建推理结果窗口
        self.result_window = QTextEdit()
        self.result_window.setReadOnly(True)
        self.result_window.setPlaceholderText('Inference results will be displayed here...')
        
        # 创建数据结果窗口
        self.runtime_data_display = QTextEdit()
        self.runtime_data_display.setReadOnly(True)
        self.runtime_data_display.setPlaceholderText('Model runtime data will be displayed here...')

        # 添加 CPU/GPU 实时监控图标框架
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
        main_layout.addWidget(self.result_window, 1, 0)  # 推理结果放在左下方
        main_layout.addWidget(self.runtime_data_display, 1, 1)  # 运行数据放在右下方
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
        from trainmodel import ModelTrainingPage
        self.new_window = ModelTrainingPage()
        self.new_window.show()

    def open_history_log_page(self):
        self.close()
        from history import HistoryLogPage
        self.new_window = HistoryLogPage()
        self.new_window.show()

    def choose_input(self):
        # 打开文件选择对话框，选择输入文件
        file_name, _ = QFileDialog.getOpenFileName(self, 'Choose Input File', '', 'Images (*.png *.jpg *.jpeg);;All Files (*)')
        if file_name:
            self.input_button.setText(file_name)
        else:
            self.input_button.setText('No file chosen')

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model_run_page = ModelRunPage()
    model_run_page.show()
    sys.exit(app.exec_())
