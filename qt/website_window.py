from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtGui import QPixmap
from pathlib import Path
import sqlite3
from selenium import webdriver

img_save_path = Path('./assets/img').resolve()
db_path = Path('./assets/db/dns.db').resolve()

class WebsiteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.load_data()

    def setupUI(self):
        self.setWindowTitle("Website Window")
        self.resize(1600, 900)

        # E:\clib\data\test2.jpg
        self.path_input = QLineEdit(self)
        self.load_button = QPushButton("捕获图片", self)
        self.del_button = QPushButton("删除图片", self)

        self.table_widget = QTableWidget()
        self.image_origin_label = QLabel(self)
        self.image_origin_label.setFixedSize(800, 600)

        # self.path_input.setText("https://baidu.com")
        # 设置布局
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.path_input)
        input_layout.addWidget(self.load_button)
        input_layout.addWidget(self.del_button)

        images_layout = QHBoxLayout()
        images_layout.addWidget(self.table_widget)
        images_layout.addWidget(self.image_origin_label)

        layout.addLayout(input_layout)
        layout.addLayout(images_layout)
        self.setLayout(layout)

        # 连接按钮点击信号到槽函数
        self.load_button.clicked.connect(self.load_image)
        self.del_button.clicked.connect(self.del_image)
        self.table_widget.cellClicked.connect(self.cell_clicked)


    def load_data(self):
        # 连接到数据库
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM domain ORDER BY update_time DESC')
        rows = cursor.fetchall()

        # 获取列名
        col_names = [description[0] for description in cursor.description]

        # 设置表格行数和列数
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(col_names))

        # 设置表头
        self.table_widget.setHorizontalHeaderLabels(col_names)

        # 填充表格数据
        for row_idx, row in enumerate(rows):
            for col_idx, item in enumerate(row):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

        # 关闭连接
        conn.close()

    def cell_clicked(self, row, column):
        # 获取被点击的单元格数据
        item = self.table_widget.item(row, column)
        if column == 1:
            self.currentName = item.text()
            self.currentId = self.table_widget.item(row, 0).text()
            self.path_input.setText("https://"+item.text())
            self.show_image()
        # if item:
        #     QMessageBox.information(self, "Cell Clicked", f"You clicked: {item.text()}")

    def load_image(self):
        # 获取输入框中的路径
        url = self.path_input.text()
        if not self.path_input.text().strip():
            QMessageBox.warning(self, "Input Error", "域名不能为空")
            return
        # 加载并显示图片
        driver = webdriver.Chrome()
        driver.get(url)
        # 等待页面加载完成
        driver.implicitly_wait(1)  # 根据实际情况调整
        # 获取网页内容的尺寸
        width = driver.execute_script("return document.body.scrollWidth")
        height = driver.execute_script("return document.body.scrollHeight")
        print(f"width = {width},height = {height}")
        # 设置浏览器窗口大小
        driver.set_window_size(width, height)
        # 保存网页内容的截图
        driver.save_screenshot(img_save_path / (self.currentId + ".png"))
        self.show_image()

    def del_image(self):
        print("del_image")
        image_path = str(img_save_path) + "\\" + self.currentId + ".png"
        file_path = Path(image_path)
        if file_path.is_file():
            file_path.unlink()
          
            image_path = str(img_save_path) + "\\0.png"
            pixmap = QPixmap(image_path)
            self.image_origin_label.setPixmap(pixmap)
            self.image_origin_label.setScaledContents(True)
        else:
            print(f"File '{file_path}' does not exist.")

    def show_image(self):
        # 获取输入框中的路径 F:\project\zz-python\python-ai\qt\assets\img\test.png
        image_path = str(img_save_path) + "\\" + self.currentId + ".png"
        file_path = Path(image_path)
        if file_path.is_file():
            # 加载并显示图片
            pixmap = QPixmap(image_path)
            self.image_origin_label.setPixmap(pixmap)
            self.image_origin_label.setScaledContents(True)
        else:
            print(f"File '{file_path}' does not exist.")
            image_path = str(img_save_path) + "\\0.png"
            pixmap = QPixmap(image_path)
            self.image_origin_label.setPixmap(pixmap)
            self.image_origin_label.setScaledContents(True)

    def show_and_trigger_method(self):
        self.load_data()
