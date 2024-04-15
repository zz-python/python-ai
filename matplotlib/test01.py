import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def test01():
    # 创建数据
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    # 创建折线图
    plt.plot(x, y)
    # 添加标题和标签
    plt.title('Prime Numbers')
    plt.xlabel('Index')
    plt.ylabel('Value')
    # 显示图形
    plt.show()

def test02():
    # 创建一个新的图形对象
    plt.figure()
    # 在图形对象中创建一个子图
    plt.subplot(1, 1, 1)  # 创建一个 1x1 的子图，选择第一个位置
    # 绘制一条直线
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    # 添加标题和标签
    plt.title('Simple Line Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    # 显示图形
    plt.show()
def test03():
    # 创建一个新的 3D 图形对象
    fig = plt.figure()

    # 在图形对象中创建一个 3D 子图
    ax = fig.add_subplot(111, projection='3d') # (111) 可以分解为三个数字 (1, 1, 1)，它们分别表示子图的行数、列数和选择的位置。

    # 生成数据
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100) # 生成等间隔的一维数组的函数
    x, y = np.meshgrid(x, y) # 接受两个一维数组作为输入，并生成两个二维数组，分别表示在指定范围内的网格点的 x 坐标和 y 坐标
    z = np.sin(np.sqrt(x**2 + y**2))

    # 绘制 3D 曲面图
    ax.plot_surface(x, y, z, cmap='viridis')

    # 添加标题和标签
    ax.set_title('3D Surface Plot')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # 显示图形
    plt.show()



if __name__ == '__main__':
    test03()