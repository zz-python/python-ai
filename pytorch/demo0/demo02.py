import torch
import numpy as np
from torch.autograd import Variable
import matplotlib.pyplot as plt

torch.manual_seed(2017) # 固定随机种子，确保实验的可重复性

x_train	= np.array([[3.3],	[4.4],	[5.5],	[6.71],	[6.93],	[4.168], [9.779], [6.182],	[7.59],	[2.167], [7.042], [10.791],	[5.313], [7.997], [3.1]], dtype=np.float32)
y_train	= np.array([[1.7], [2.76],	[2.09],	[3.19],	[1.694], [1.573], [3.366],	[2.596], [2.53], [1.221], [2.827], [3.465],	[1.65],	[2.904], [1.3]], dtype=np.float32)

#plt.xlim(right=12)
#plt.ylim(top=4)
#plt.plot(x_train, y_train, 'bo')
#plt.show()

print("torch")
x_train	= torch.from_numpy(x_train)
y_train	= torch.from_numpy(y_train)
# 定义参数
w =	Variable(torch.randn(1), requires_grad=True)
b =	Variable(torch.zeros(1), requires_grad=True)	

x_train	= Variable(x_train)
y_train	= Variable(y_train)
def linear_model(x):
	return x * w + b
y_ = linear_model(x_train)
plt.plot(x_train.data.numpy(), y_train.data.numpy(), 'bo', label='real')
plt.plot(x_train.data.numpy(), y_.data.numpy(), 'ro', label='estimated')
plt.legend() # 显示图例 loc='upper left'
plt.show()
print("计算误差")
def get_loss(y_, y_train):
    return torch.mean((y_ - y_train) ** 2)
loss = get_loss(y_,	y_train)
print(loss)

loss.backward()
print(w.grad)
print(b.grad)

w.data = w.data - 1e-2 * w.grad.data # 1e-2 0.01
b.data = b.data - 1e-2 * b.grad.data

y_ = linear_model(x_train)
plt.plot(x_train.data.numpy(), y_train.data.numpy(), 'bo', label='real')
plt.plot(x_train.data.numpy(), y_.data.numpy(),	'ro', label='estimated')
plt.legend()
plt.show()

print("再更新")
for index in range(10):
    y_ = linear_model(x_train)
    loss = get_loss(y_,	y_train)
    
    w.grad.zero_()
    b.grad.zero_()
    loss.backward()
    
    w.data = w.data - 1e-2 * w.grad.data
    b.data = b.data - 1e-2 * b.grad.data
    print('loss', index, loss)

y_	=	linear_model(x_train)
plt.plot(x_train.data.numpy(),	y_train.data.numpy(),	'bo',	label='real')
plt.plot(x_train.data.numpy(),	y_.data.numpy(),	'ro',	label='estimated')
plt.legend()
plt.show()