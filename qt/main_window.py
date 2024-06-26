from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import  QDesktopServices
from url_window import UrlWindow
from website_window import WebsiteWindow
from db_window import DbWindow
from train_window import TrainWindow

class MWindow(QMainWindow):
    show_child_signal = Signal()  # 定义一个信号，用于通知子窗口显示
    show_child3_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):

        self.resize(1200, 800)

        self.setWindowTitle('演示')

        # 创建主窗口的中央小部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 创建顶部的按钮布局
        button_layout = QHBoxLayout()

        # 创建两个按钮
        self.button1 = QPushButton("域名收集")
        self.button1.setStyleSheet("background-color: lightblue; font-size: 16px; padding: 10px;")
        self.button2 = QPushButton("域名截图")
        self.button2.setStyleSheet("background-color: lightblue; font-size: 16px; padding: 10px;")
        self.button3 = QPushButton("截图分析")
        self.button3.setStyleSheet("background-color: lightblue; font-size: 16px; padding: 10px;")
        self.button4 = QPushButton("数据标注")
        self.button4.setStyleSheet("background-color: lightblue; font-size: 16px; padding: 10px;")
        self.button5 = QPushButton("数据训练")
        self.button5.setStyleSheet("background-color: lightblue; font-size: 16px; padding: 10px;")

        # 将按钮添加到布局中
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button3)
        button_layout.addWidget(self.button4)
        button_layout.addWidget(self.button5)

        # 创建一个 QStackedWidget
        self.stacked_widget = QStackedWidget()

        # 创建两个子窗口实例
        self.child_window1 = DbWindow()
        self.child_window2 = WebsiteWindow()
        self.child_window3 = UrlWindow()

        self.child_window5 = TrainWindow()

        # 将子窗口添加到 QStackedWidget 中
        self.stacked_widget.addWidget(self.child_window5)
        self.stacked_widget.addWidget(self.child_window3)
        self.stacked_widget.addWidget(self.child_window2)
        self.stacked_widget.addWidget(self.child_window1)

        # 将按钮布局和 QStackedWidget 添加到主布局中
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stacked_widget)

        # 连接按钮点击信号到槽函数
        self.button1.clicked.connect(self.show_child_window1)
        self.button2.clicked.connect(self.show_child_window2)
        self.button3.clicked.connect(self.show_child_window3)
        self.button4.clicked.connect(self.open_browser)
        self.button5.clicked.connect(self.show_child_window5)
         # 连接父窗口的信号到子窗口的槽函数
        self.show_child_signal.connect(self.child_window2.show_and_trigger_method)
        self.show_child3_signal.connect(self.child_window3.show_and_trigger_method)

    def show_child_window1(self):
        # 切换到子窗口1
        self.stacked_widget.setCurrentWidget(self.child_window1)

    def show_child_window2(self):
        self.stacked_widget.setCurrentWidget(self.child_window2)
        self.show_child_signal.emit()
    def show_child_window3(self):
        self.stacked_widget.setCurrentWidget(self.child_window3)
        self.show_child3_signal.emit()
    def show_child_window5(self):
        self.stacked_widget.setCurrentWidget(self.child_window5)
    def open_browser(self):
        print("open_browser")
        url = QUrl("http://makesense.bimant.com/")
        QDesktopServices.openUrl(url)

if __name__ == "__main__":
    app = QApplication()
    window = MWindow()
    window.show()
    app.exec()