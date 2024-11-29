import torch
from torch.autograd import Variable
'''
import matplotlib.pyplot as plt
import numpy as np

x =	np.arange(-3, 3.01,	0.1)
y =	x ** 2
plt.plot(x,	y)
plt.plot(2,	4, 'ro')
plt.show()
'''

# 构建一个函数y=x2,然后求x=2的导数。
x =	Variable(torch.FloatTensor([2]),	requires_grad=True)
y =	x ** 2
y.backward() # 反向传播后，梯度会存储在参与计算的每个张量的 grad 属性中
print(x.grad)

# 构建函数2
x =	Variable(torch.Tensor([2]),	requires_grad=True)
y =	x + 2
z =	y ** 2 + 3
print(z)
z.backward()
print(x.grad)

# mean
x = torch.tensor([1.0, 2.0, 3.0, 4.0])
mean_value = torch.mean(x)
print(mean_value)  # 输出: 2.5

# 构建函数3
x =	Variable(torch.randn(10, 20),	requires_grad=True)
y =	Variable(torch.randn(10, 5),	requires_grad=True)
w =	Variable(torch.randn(20, 5),	requires_grad=True)
out	= torch.mean(y - torch.matmul(x, w))	#	torch.matmul 矩阵乘法
out.backward()
# print(x.grad)
# print(y.grad)
# print(w.grad)
