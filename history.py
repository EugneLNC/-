import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, 
                             QPushButton, QFileDialog, QHBoxLayout, QMessageBox, QGridLayout, QHeaderView, QMenuBar, QAction)
from PyQt5.QtCore import Qt

class HistoryLogPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口大小为 1980x1080
        self.setWindowTitle('History Logging Page')
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
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 数据表格
        self.history_table = QTableWidget()
        self.history_table.setRowCount(0)  # 初始无记录
        self.history_table.setColumnCount(6)  # 设置6列作为示例
        self.history_table.setHorizontalHeaderLabels(['Model Name', 'Runtime (s)', 'Accuracy (%)', 'Batch Size', 'Learning Rate', 'Error Info'])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.history_table)

        # 导入历史数据按钮
        import_data_button = QPushButton('Import History Data')
        import_data_button.clicked.connect(self.import_history_data)
        main_layout.addWidget(import_data_button)

        # 导出历史记录按钮
        export_button = QPushButton('Export History to CSV')
        export_button.clicked.connect(self.export_to_csv)
        main_layout.addWidget(export_button)

        # 对比功能按钮
        compare_button = QPushButton('Compare Models')
        compare_button.clicked.connect(self.compare_models)
        main_layout.addWidget(compare_button)

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
        self.new_window = HistoryLogPage()
        self.new_window.show()

    def import_history_data(self):
        # 打开文件选择对话框
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv);;All Files (*)')
        if file_name:
            try:
                with open(file_name, mode='r') as file:
                    reader = csv.reader(file)
                    next(reader)  # 跳过表头
                    self.history_table.setRowCount(0)  # 清除现有表格中的数据
                    for row_data in reader:
                        row_position = self.history_table.rowCount()
                        self.history_table.insertRow(row_position)
                        for column, data in enumerate(row_data):
                            self.history_table.setItem(row_position, column, QTableWidgetItem(data))
                QMessageBox.information(self, 'Success', 'History data imported successfully!')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to import data: {e}')
        else:
            QMessageBox.warning(self, 'Error', 'No file selected for import.')

    def export_to_csv(self):
        # 选择导出文件的位置
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save CSV', '', 'CSV Files (*.csv);;All Files (*)')

        if file_name:
            try:
                with open(file_name, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    # 写入表头
                    writer.writerow(['Model Name', 'Runtime (s)', 'Accuracy (%)', 'Batch Size', 'Learning Rate', 'Error Info'])

                    # 写入表格内容
                    for row in range(self.history_table.rowCount()):
                        row_data = []
                        for column in range(self.history_table.columnCount()):
                            item = self.history_table.item(row, column)
                            row_data.append(item.text() if item else '')
                        writer.writerow(row_data)

                QMessageBox.information(self, 'Success', f'History exported to {file_name} successfully!')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to export history: {e}')
        else:
            QMessageBox.warning(self, 'Error', 'No file selected for export.')

    def compare_models(self):
        if self.history_table.rowCount() < 2:
            QMessageBox.warning(self, 'Error', 'Please add or import at least two models to compare.')
            return

        comparison_text = "Comparison of Models:\n"
        for row in range(self.history_table.rowCount()):
            model_name = self.history_table.item(row, 0).text()
            runtime = self.history_table.item(row, 1).text()
            accuracy = self.history_table.item(row, 2).text()
            batch_size = self.history_table.item(row, 3).text()
            learning_rate = self.history_table.item(row, 4).text()

            comparison_text += f"Model: {model_name}, Runtime: {runtime}s, Accuracy: {accuracy}%, Batch Size: {batch_size}, Learning Rate: {learning_rate}\n"

        QMessageBox.information(self, 'Model Comparison', comparison_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    history_page = HistoryLogPage()
    history_page.show()
    sys.exit(app.exec_())
