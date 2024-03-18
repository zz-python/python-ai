import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    def __init__(self, gamma=2, alpha=None, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.alpha = alpha
        self.reduction = reduction

    def forward(self, inputs, targets):
        # 计算交叉熵损失
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        
        # 计算 softmax
        pt = torch.exp(-ce_loss)
        
        # 计算 Focal Loss
        focal_loss = (1 - pt) ** self.gamma * ce_loss
        
        if self.alpha is not None:
            focal_loss = self.alpha * focal_loss
        
        if self.reduction == 'mean':
            return torch.mean(focal_loss)
        elif self.reduction == 'sum':
            return torch.sum(focal_loss)
        else:
            return focal_loss

# 使用示例
# 定义模型
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.fc = nn.Linear(10, 5)

    def forward(self, x):
        return self.fc(x)

model = MyModel()
criterion = FocalLoss()

# 定义输入数据和标签
input_data = torch.randn(3, 10)
target = torch.tensor([0, 1, 2])

# 计算损失
loss = criterion(model(input_data), target)
print(loss)
print(f'zzzz {loss}')
