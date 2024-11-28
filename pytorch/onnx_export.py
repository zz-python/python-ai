import torch
import torchvision
import onnx

dummy_input = torch.randn(1, 3, 224, 224)  # 示例输入张量
model = torchvision.models.resnet18(pretrained=True)  # 使用预训练的 ResNet 模型
torch.onnx.export(model, dummy_input, "model.onnx")

# 加载 ONNX 模型
onnx_model = onnx.load("model.onnx")
# 检查模型是否有效
onnx.checker.check_model(onnx_model)
print("ONNX 模型导出成功且有效")

# 打印输入名称
for input in onnx_model.graph.input:
    print(f"Input name: {input.name}")

# 打印输出名称
for output in onnx_model.graph.output:
    print(f"Output name: {output.name}")