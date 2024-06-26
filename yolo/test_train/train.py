from ultralytics import YOLO
 
# ultralytics\cfg\models\v8\yolov8.yaml
# model = YOLO('F:\\project\\zz-python\\python-ai\\yolo\\test_train\\my_yolov8.yaml')
 
# Load a pretrained YOLO model (recommended for training)
# model = YOLO('F:\\project\\zz-python\\python-ai\\yolo\\model\\yolov8n.pt')
model = YOLO('F:\\project\\zz-python\\python-ai\\yolo\\test_train\\yolov8n.yaml')
 
# ultralytics-main\ultralytics\cfg\datasets\coco128.yaml
# results = model.train(data='F:\\project\\zz-python\\python-ai\\yolo\\test_train\\my_coco128.yaml', epochs=3)
results = model.train(data='F:\\project\\zz-python\\python-ai\\yolo\\test_train\\coco128.yaml', epochs=1000)
 
# Evaluate the model's performance on the validation set
results = model.val()
 
 
#下面是预测和导出
# # Perform object detection on an image using the model
# results = model('https://ultralytics.com/images/bus.jpg')
#
# # Export the model to ONNX format
# success = model.export(format='onnx')

# yolo task=detect mode=train model=F:\project\zz-python\python-ai\yolo\test_train\my_yolov8.yaml data=F:\project\zz-python\python-ai\yolo\test_train\my_coco128.yaml epochs=3 batch=1








