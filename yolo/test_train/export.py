from ultralytics import YOLO
 
# Load a pretrained YOLO model (recommended for training)
model = YOLO('F:\\project\\zz-python\\python-ai\\yolo\\model\\yolov8n.pt')
 
success = model.export(format='onnx')

print(success)







