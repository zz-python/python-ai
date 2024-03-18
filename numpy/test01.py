
import numpy as np

def test01():
    nump_1d = np.array([1,2,3,])
    nump_2d = np.array([[1,2],[3,4]])
    ##使用dtype 来固定类型（np.bool是布尔类型）
    nump_1da = np.array([1,0,1,1,1,0],dtype=np.bool_)
    print(nump_1d)
    print(nump_2d)
    print(nump_1da)

    # 同构和异构
    list1 = [1,1.2,True,'abc']
    print(list1)
    print(type(list1))
    # 在numpy中
    arr2 = np.array(list1)
    print(arr2)
    print(type(arr2))

def test02():
    for i in range(0,6):
        print(i)
    print(list(range(0,6)))

    arr=np.arange(6)
    print(arr)
    # 指定起始位置和终止位置
    arr=np.arange(10,20)
    print(arr)
    # 指定步长
    arr=np.arange(10,20,3)
    print(arr)

    # reshape：改变数组的维度
    print('reshape：改变数组的维度')
    arr=np.arange(6).reshape((2,3))
    print(arr)
    arr=np.arange(6).reshape((3,2))
    print(arr)

def test03():
    # 等差数列 参数：起始位置，终止位置，元素个数
    arr=np.linspace(1,10,5)
    print(arr)
    # 等比数列参数：起始位置，终止位置，元素个数
    # 比如这个3，表示的是10的3次方，1000
    arr=np.logspace(1,3,5)
    print(arr)
    arr=np.logspace(1,4,4)
    print(arr)

# n维数组创建
def test04():
    arr=np.ones((2,3))
    print(arr)
    arr=np.zeros((3,2))
    print(arr)
    arr=np.eye(3)
    print(arr)
    # help(np.eye)
    arr=np.empty((4,6))
    print(arr)

if __name__ == '__main__':
    # test01()
    # test02()
    # test03()
    test04()