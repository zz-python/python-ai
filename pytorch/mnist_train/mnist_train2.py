import torch
import torch.nn as nn
import torch.nn.functional as F

from torchvision import datasets, transforms
from torch.utils.data import DataLoader

from utils import plot_image, plot_curve, one_hot

class SimpleClassifier(nn.Module):
    def __init__(self, input_size=28*28, num_classes=10):
        super(SimpleClassifier, self).__init__()
        # 定义网络层
        self.fc1 = nn.Linear(input_size, 128)  # 输入层到隐藏层
        self.fc2 = nn.Linear(128, 64)         # 隐藏层到隐藏层
        self.fc3 = nn.Linear(64, num_classes) # 隐藏层到输出层
    
    def forward(self, x):
        # 前向传播定义
        x = x.view(x.size(0), -1)  # 将 28x28 图片展平为一维向量
        x = F.relu(self.fc1(x))    # 激活函数 ReLU
        x = F.relu(self.fc2(x))
        x = self.fc3(x)            # 输出层不需要激活（在训练中用CrossEntropyLoss包含Softmax）
        return x

# 训练函数
def train_model(model, train_loader, criterion, optimizer, epochs=5):
    for epoch in range(epochs):
        model.train()  # 设置为训练模式
        running_loss = 0.0
        for images, labels in train_loader:
            # 清空梯度
            optimizer.zero_grad()
            # 前向传播
            outputs = model(images)
            loss = criterion(outputs, labels)
            # 反向传播和优化
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {running_loss/len(train_loader):.4f}")

# 测试函数
def evaluate_model(model, test_loader):
    model.eval()  # 设置为评估模式
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print(f"Accuracy: {100 * correct / total:.2f}%")

# 数据预处理
transform = transforms.Compose([
    transforms.ToTensor(),               # 转为 Tensor
    transforms.Normalize((0.5,), (0.5,)) # 标准化到 [-1, 1]
])
# 下载 MNIST 数据集
train_dataset = datasets.MNIST(root='mnist_data', train=True, transform=transform, download=True)
test_dataset = datasets.MNIST(root='mnist_data', train=False, transform=transform, download=True)
# 加载数据
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)
#print(train_loader)
#x, y = next(iter(train_loader))
#print(x.shape, y.shape, x.min(), x.max())
#plot_image(x, y, 'image sample')

# 初始化模型、损失函数和优化器
model = SimpleClassifier()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练模型
train_model(model, train_loader, criterion, optimizer, epochs=5)

# 评估模型
evaluate_model(model, test_loader)