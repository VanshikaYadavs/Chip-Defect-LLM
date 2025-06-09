# detect.py

import os
from ultralytics import YOLO
from PIL import Image
import uuid

# Load model once
model_path = os.path.join(os.path.dirname(__file__), "../models/yolov8_chip.pt")
model = YOLO(model_path)


def detect_chip_defects(image_path: str, save_dir: str = "backend/static"):
    # Run YOLOv8 detection
    results = model(image_path)

    # Save output image
    unique_filename = f"result_{uuid.uuid4().hex[:8]}.jpg"
    output_path = os.path.join(save_dir, unique_filename)
    results[0].save(filename=output_path)

    # Get detected labels (e.g., crack, corrosion, etc.)
    labels = results[0].names
    detections = results[0].boxes.cls.tolist()
    class_names = [labels[int(cls_id)] for cls_id in detections]

    return {
        "output_image_path": output_path,
        "defect_classes": class_names
    }
