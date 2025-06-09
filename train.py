# train.py

from ultralytics import YOLO

# Load base model (YOLOv8n is the smallest and fastest, or use yolov8s)
model = YOLO('yolov8n.pt')

# Train the model on your dataset
model.train(
    data='data/roboflow_yolov8/data.yaml',
    epochs=30,
    imgsz=640,
    batch=16
)

# Save best model
model.export(format='torchscript')  # Optional, for deployment formats
