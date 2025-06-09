chip-defect-llm/
│
├── backend/                          ← Python backend
│   ├── main.py                       ← FastAPI app entrypoint
│   ├── detect.py                     ← YOLOv8 detection logic
│   ├── llm_report.py                 ← LLM prompt + response generation
│   ├── models/
│   │   └── yolov8_chip.pt            ← Trained YOLOv8 model
│   ├── static/                       ← Folder for uploaded + result images
│   └── requirements.txt              ← Python dependencies
│
├── data/                             ← Your dataset
│   └── roboflow_yolov8/              ← Unzipped YOLOv8 dataset
│       ├── train/
│       ├── valid/
│       ├── data.yaml
│
├── frontend/                         ← ReactJS frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── api.js                    ← API calls to FastAPI
│   ├── package.json
│   └── tailwind.config.js
│
├── README.md
└── .gitignore
