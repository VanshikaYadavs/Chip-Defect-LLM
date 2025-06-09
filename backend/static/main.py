from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
import shutil
import uuid

# Add current directory to import path
sys.path.append(os.path.dirname(__file__))

from detect import detect_chip_defects
from llm_report import generate_llm_report, generate_defect_chart

app = FastAPI()

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

    # Run LLM to get explanation
    llm_response = generate_llm_report(detection_result["defect_classes"])

    # Generate defect frequency chart
    chart_path = generate_defect_chart(detection_result["defect_classes"])
    chart_path = chart_path.replace("\\", "/")  # For web compatibility

    # Prepare output image path
    result_image_path = detection_result["output_image_path"].replace("\\", "/")

    return JSONResponse({
        "result_image": result_image_path,
        "defects": detection_result["defect_classes"],
        "llm_report": llm_response,
        "chart_image": chart_path
    })
