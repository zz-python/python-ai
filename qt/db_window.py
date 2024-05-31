from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QTableWidgetItem, QTableWidget, QTextBrowser
from PySide6 import QtGui
from PySide6.QtGui import QPixmap
from pathlib import Path
from datetime import datetime
import sqlite3


db_path = Path('./assets/db/dns.db').resolve()

class DbWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.load_data()

    def setupUI(self):
        self.setWindowTitle("Db Window")
        self.resize(1600, 900)

        # E:\clib\data\test2.jpg
        self.path_input = QLineEdit(self)
        self.create_db_button = QPushButton("初始化数据库", self)
        self.insert_button = QPushButton("插入域名", self)

        self.table_widget = QTableWidget()
        self.image_origin_label = QLabel(self)
        self.image_yolo_label = QLabel(self)

        self.textLog = QTextBrowser()

        # 设置布局
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.path_input)
        input_layout.addWidget(self.create_db_button)
        input_layout.addWidget(self.insert_button)

        images_layout = QHBoxLayout()
        images_layout.addWidget(self.table_widget)
        images_layout.addWidget(self.image_yolo_label)

        layout.addLayout(input_layout)
        layout.addLayout(images_layout)
        layout.addWidget(self.textLog)
        self.setLayout(layout)

        # 连接按钮点击信号到槽函数
        self.create_db_button.clicked.connect(self.create_db)
        self.insert_button.clicked.connect(self.insert_db)

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

    def create_db(self):
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS domain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                update_time TEXT,
                tag INTEGER
            );
            CREATE UNIQUE INDEX idx_name ON "domain" (name);
            CREATE INDEX idx_update_time ON domain (update_time);
        ''')
        # cursor.execute('''
        #     CREATE UNIQUE INDEX idx_name ON "domain" (name);
        # ''')
        # cursor.execute('''
        #     CREATE INDEX idx_update_time ON domain (update_time);
        # ''')
        conn.commit()
        conn.close()
        self.textLog.append("初始化数据库成功。")

    def insert_db(self):
        name = self.path_input.text()
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # 插入数据
        cursor.execute('''
            REPLACE INTO domain (name, tag, update_time)
            VALUES (?, ?, ?)
        ''', (name, 0, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        # cursor.execute('''
        #     INSERT INTO users (name, age)
        #     VALUES (?, ?)
        # ''', ('Alice', 25))

        # 多行插入
        # users = [('Bob', 30), ('Charlie', 35)]
        # cursor.executemany('''
        #     INSERT INTO users (name, age)
        #     VALUES (?, ?)
        # ''', users)

        conn.commit()
        conn.close()
        self.textLog.append(name + "添加成功。")
        self.load_data()