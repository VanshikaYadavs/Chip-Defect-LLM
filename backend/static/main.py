from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import sys
import os
import shutil
import uuid

# Add current directory to import path
sys.path.append(os.path.dirname(__file__))

from detect import detect_chip_defects
from PIL import Image
import numpy as np
from llm_report import generate_llm_report, generate_defect_chart


app = FastAPI()

# Serve static files (images, charts) at /static
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploads directory for images and charts
UPLOAD_DIR = "backend/static"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "Welcome to the Chip Defect Detection API! Visit /health for status."}


@app.get("/health")
def health():
    return {"status": "Chip Defect Detection API is running!"}


@app.post("/detect")
async def detect_image(file: UploadFile = File(...)):
    # Save uploaded image
    filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    # Run detection
    detection_result = detect_chip_defects(file_path)

    # Prepare static URLs for result image and chart
    def to_static_url(path):
        if not path:
            return None
        filename = os.path.basename(path)
        return f"/static/{filename}"

    # Heuristic: If no defects, check if image is likely a PCB
    def is_likely_pcb(image_path):
        try:
            img = Image.open(image_path).convert('RGB')
            arr = np.array(img)
            # Looser green threshold: allow for lighting, blur, etc.
            avg = arr.mean(axis=(0,1))
            greenish = avg[1] > avg[0] and avg[1] > avg[2] and avg[1] > 40  # Lowered from 60
            # Wider aspect ratio: allow for more portrait/landscape
            h, w = arr.shape[:2]
            aspect = w / h if h > 0 else 1
            aspect_ok = 0.5 < aspect < 2.5  # Widened from 0.7-2.0
            # Allow some noise: if greenish OR aspect_ok, accept
            return greenish or aspect_ok
        except Exception:
            return False

    if not detection_result["defect_classes"]:
        if not is_likely_pcb(file_path):
            return JSONResponse({
                "result_image": None,
                "defects": [],
                "llm_report": "No PCB visible in the image.",
                "chart_image": None
            })
        else:
            return JSONResponse({
                "result_image": to_static_url(detection_result["output_image_path"]),
                "defects": [],
                "llm_report": "✅ No defects were detected in the chip. Everything looks fine!",
                "chart_image": None
            })

    # Run LLM to get explanation
    llm_response = generate_llm_report(detection_result["defect_classes"])

    # Generate defect frequency chart
    chart_path = generate_defect_chart(detection_result["defect_classes"])

    return JSONResponse({
        "result_image": to_static_url(detection_result["output_image_path"]),
        "defects": detection_result["defect_classes"],
        "llm_report": llm_response,
        "chart_image": to_static_url(chart_path)
    })
