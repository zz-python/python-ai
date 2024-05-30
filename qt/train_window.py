from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QTableWidgetItem, QTableWidget, QTextBrowser
from PySide6 import QtGui
from PySide6.QtGui import QPixmap
from pathlib import Path
import os
import random
import shutil


assets_path = Path('./assets').resolve()

class TrainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Train Window")
        self.resize(1600, 900)

        self.dir_image_button = QPushButton("图片归档", self)
        self.train_button = QPushButton("开始训练", self)

        self.textLog = QTextBrowser()

        # 设置布局
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.dir_image_button)
        input_layout.addWidget(self.train_button)


        layout.addLayout(input_layout)
        layout.addWidget(self.textLog)
        self.setLayout(layout)

        # 连接按钮点击信号到槽函数
        self.dir_image_button.clicked.connect(self.dir_image)
        self.train_button.clicked.connect(self.train_image)

    def dir_image(self):
        # 原数据集目录
        root_dir = str(assets_path)
        # 划分比例
        train_ratio = 0.8
        valid_ratio = 0.1
        test_ratio = 0.1

        # 设置随机种子
        random.seed(42)

        # 拆分后数据集目录
        split_dir = str(assets_path) + '\\img_split'
        os.makedirs(os.path.join(split_dir, 'train/images'), exist_ok=True)
        os.makedirs(os.path.join(split_dir, 'train/labels'), exist_ok=True)
        os.makedirs(os.path.join(split_dir, 'valid/images'), exist_ok=True)
        os.makedirs(os.path.join(split_dir, 'valid/labels'), exist_ok=True)
        os.makedirs(os.path.join(split_dir, 'test/images'), exist_ok=True)
        os.makedirs(os.path.join(split_dir, 'test/labels'), exist_ok=True)

        # 获取图片文件列表
        # image_files = os.listdir(os.path.join(root_dir, 'img'))
        image_files = self.list_files_with_extension(os.path.join(root_dir, 'img'), '.png')
        label_files = self.list_files_with_extension(os.path.join(root_dir, 'img'), '.txt')

        # 随机打乱文件列表
        combined_files = list(zip(image_files, label_files))
        random.shuffle(combined_files)
        image_files_shuffled, label_files_shuffled = zip(*combined_files)

        # 根据比例计算划分的边界索引
        train_bound = int(train_ratio * len(image_files_shuffled))
        valid_bound = int((train_ratio + valid_ratio) * len(image_files_shuffled))

        print("zzz", train_bound, valid_bound, image_files, label_files)

        # 将图片和标签文件移动到相应的目录
        # for i, (image_file, label_file) in enumerate(zip(image_files_shuffled, label_files_shuffled)):
        #     if i < train_bound:
        #         shutil.move(os.path.join(root_dir, 'images', image_file), os.path.join(split_dir, 'train/images', image_file))
        #         shutil.move(os.path.join(root_dir, 'labels', label_file), os.path.join(split_dir, 'train/labels', label_file))
        #     elif i < valid_bound:
        #         shutil.move(os.path.join(root_dir, 'images', image_file), os.path.join(split_dir, 'valid/images', image_file))
        #         shutil.move(os.path.join(root_dir, 'labels', label_file), os.path.join(split_dir, 'valid/labels', label_file))
        #     else:
        #         shutil.move(os.path.join(root_dir, 'images', image_file), os.path.join(split_dir, 'test/images', image_file))
        #         shutil.move(os.path.join(root_dir, 'labels', label_file), os.path.join(split_dir, 'test/labels', label_file))


    def train_image(self):
        print("train_image")

    def list_files_with_extension(self, directory, extension):
        # 获取目录中的所有文件和子目录
        items = os.listdir(directory)
        # 过滤具有指定后缀的文件
        files = [item for item in items if item.endswith(extension)]
        return files