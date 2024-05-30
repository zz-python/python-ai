from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QTextBrowser
from PySide6 import QtGui
from PySide6.QtGui import QPixmap
from pathlib import Path
import sqlite3
import cv2
import os
# 不然每次YOLO处理都会输出调试信息
os.environ['YOLO_VERBOSE'] = 'False'
from ultralytics import YOLO 
import easyocr

img_save_path = Path('./assets/img').resolve()
db_path = Path('./assets/db/dns.db').resolve()
model_path = Path('./assets/model').resolve()

class UrlWindow(QWidget):

    reader = None

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.load_data()

    def setupUI(self):
        self.setWindowTitle("New Window")
        self.resize(1600, 900)

        # E:\clib\data\test2.jpg
        self.path_input = QLineEdit(self)
        self.load_button = QPushButton("加载图片", self)
        self.combo_box = QComboBox()
        self.combo_box.addItems(["yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt", "best.pt", "best1000.pt"])
        self.yolo_button = QPushButton("图像检测", self)
        self.ocr_button = QPushButton("文字检测", self)

        self.table_widget = QTableWidget()
        self.table_widget.setFixedWidth(250)
        self.image_origin_label = QLabel(self)
        self.image_origin_label.setFixedSize(200, 150)
        self.textLog = QTextBrowser()
        self.textLog.setFixedHeight(150)
        self.image_yolo_label = QLabel(self)
        self.image_yolo_label.setFixedSize(900, 500)

        picture_path = str(img_save_path) + "\\0.png" # bus.jpg
        
        self.path_input.setText(picture_path)
        # 设置布局
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.path_input)
        input_layout.addWidget(self.load_button)
        input_layout.addWidget(self.combo_box)
        input_layout.addWidget(self.yolo_button)
        input_layout.addWidget(self.ocr_button)

        content_right_top_layout = QHBoxLayout()
        content_right_top_layout.addWidget(self.image_origin_label)
        content_right_top_layout.addWidget(self.textLog )

        content_right_layout = QVBoxLayout()
        content_right_layout.addLayout(content_right_top_layout)
        content_right_layout.addWidget(self.image_yolo_label)

        # log_layout = QVBoxLayout()
        # log_layout.addWidget(self.image_origin_label)
        # log_layout.addWidget(self.textLog )

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.table_widget)
        content_layout.addLayout(content_right_layout)


        layout.addLayout(input_layout)
        layout.addLayout(content_layout)
        self.setLayout(layout)

        # 连接按钮点击信号到槽函数
        self.load_button.clicked.connect(self.show_image)
        # self.combo_box.currentIndexChanged.connect(self.on_combobox_changed)
        self.yolo_button.clicked.connect(self.yolo_image)
        self.ocr_button.clicked.connect(self.ocr_image)
        self.table_widget.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        # 连接到数据库
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM domain')
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
            self.path_input.setText(str(img_save_path) + "\\" + self.currentId + ".png")
            self.show_image()
        # if item:
        #     QMessageBox.information(self, "Cell Clicked", f"You clicked: {item.text()}")

    def show_image(self):
        # 获取输入框中的路径
        image_path = self.path_input.text()
        file_path = Path(image_path)
        if file_path.is_file():
            # 加载并显示图片
            pixmap = QPixmap(image_path)
            self.image_origin_label.setPixmap(pixmap)
            self.image_origin_label.setScaledContents(True)
        else:
            print(f"File '{file_path}' does not exist.")
            # image_path = "F:\\project\\zz-python\\python-ai\\qt\\assets\\img\\0.png"
            image_path = str(img_save_path) + "\\0.png"
            pixmap = QPixmap(image_path)
            self.image_origin_label.setPixmap(pixmap)
            self.image_origin_label.setScaledContents(True)       

    def convert_cv_qt(cv_img):
        """Convert from an opencv image to QImage."""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        return convert_to_Qt_format

    def yolo_image(self):
        model_name = self.combo_box.currentText()
        print("model_name",model_name)
        self.model = YOLO(model_path /model_name)
        # 获取输入框中的路径
        image_path = self.path_input.text()
        results = self.model(image_path)
        
        img = results[0].plot()   
        # cv2.imshow("YOLOv8 Inference", img)

        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        # print(img.shape[1], img.shape[0], h, w, ch) 
        qt_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.image_yolo_label.setPixmap(QtGui.QPixmap.fromImage(qt_img))
        self.image_yolo_label.setScaledContents(True)

    def ocr_image(self):
        image_path = self.path_input.text()
        img = cv2.imread(image_path)
        if self.reader is None:
            print("create reader")
            self.reader = easyocr.Reader(['ch_sim', 'en']) # 'en'
        # 使用 EasyOCR 进行 OCR
        result = self.reader.readtext(img)
        # 打印识别结果
        self.textLog.clear()
        for detection in result:
            # print(detection[1])
            self.textLog.append(detection[1])

    def show_and_trigger_method(self):
        self.load_data()