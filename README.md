# Crowd Detection API

A Flask-based REST API for real-time crowd detection in images using YOLOv8 and DBSCAN clustering.

## Features

- 🎯 **Person Detection** — Detects individuals in images using YOLOv8n
- 👥 **Crowd Clustering** — Groups nearby people using DBSCAN algorithm
- ⚙️ **Configurable Parameters** — Adjust confidence, crowd, and distance thresholds
- 🚀 **REST API** — Easy-to-use Flask endpoints
- 📊 **Detailed Output** — Returns bounding boxes, confidence scores, and crowd membership

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone/Navigate to the project:**
   ```bash
   cd crowd-detection
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Start the Server

```bash
python app.py
```

The API will be available at `http://localhost:9009`

### Environment Variables

Configure the service using environment variables:

```bash
# Model settings
MODEL_PATH=models/yolov8n.pt     # Path to YOLOv8 model (default: models/yolov8n.pt)
CONF_THRESHOLD=0.3               # Confidence threshold for detections (default: 0.3)

# Crowd detection settings
CROWD_THRESHOLD=3               # Minimum people to form a crowd (default: 3)
DISTANCE_THRESHOLD=150          # Maximum distance between people in pixels (default: 150)

# Server settings
PORT=9009                        # Server port (default: 9009)
```

**Example:**
```bash
set DISTANCE_THRESHOLD=200
set CROWD_THRESHOLD=5
python app.py
```

## API Endpoints

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "service": "crowd-detection",
  "model_loaded": true
}
```

### Detect Crowds
```
POST /detect
```

**Parameters:**
- `file` (multipart/form-data) — Image file (JPG, PNG, etc.)

**Response:**
```json
{
  "success": true,
  "total_people": 17,
  "crowd_count": 2,
  "crowds": [
    {
      "count": 8,
      "members": [[x1, y1], [x2, y2], ...]
    },
    {
      "count": 5,
      "members": [[x1, y1], [x2, y2], ...]
    }
  ],
  "detections": [
    {
      "bbox": [x1, y1, x2, y2],
      "class_name": "person",
      "confidence": 0.8418
    },
    ...
  ]
}
```

## Usage Examples

### Using cURL

#### Health Check
```bash
curl http://localhost:9009/health
```

**What it does:**
- Verifies the API server is running and the model is loaded
- No authentication or file upload needed
- Use this to test connectivity before sending detection requests

**Response:**
```json
{
  "status": "ok",
  "service": "crowd-detection",
  "model_loaded": true
}
```

**Command Breakdown:**
- `curl` — Command-line HTTP client
- `http://localhost:9009/health` — Health check endpoint
- Default method: GET

---

#### Detect Crowds in Image
```bash
curl.exe -X POST http://localhost:9009/detect -F "file=@test.jpg"
```

**What it does:**
- Sends an image to the API for crowd detection
- Returns detected people and identified crowds
- Processes the image and returns detailed analysis

**Command Breakdown:**
- `curl.exe` — Windows command-line HTTP client (use `curl` on macOS/Linux)
- `-X POST` — HTTP method (POST request)
- `http://localhost:9009/detect` — Detection endpoint
- `-F "file=@test.jpg"` — Form data flag with file upload
  - `-F` — Multipart form data (for file upload)
  - `"file=@test.jpg"` — Field name `file` with local file `test.jpg`

**Response Example (with 17 people detected):**
```json
{
  "success": true,
  "total_people": 17,
  "crowd_count": 2,
  "crowds": [
    {
      "count": 8,
      "members": [[400, 550], [450, 580], [420, 600], [470, 620], [390, 640], [480, 650], [410, 670], [460, 690]]
    },
    {
      "count": 5,
      "members": [[150, 400], [200, 420], [180, 450], [220, 480], [170, 500]]
    }
  ],
  "detections": [
    {"bbox": [577, 511, 738, 740], "class_name": "person", "confidence": 0.8418},
    {"bbox": [390, 585, 567, 739], "class_name": "person", "confidence": 0.8196},
    ...
  ]
}
```

**Key Fields:**
- `success` — Whether the request was successful
- `total_people` — Total number of individuals detected
- `crowd_count` — Number of crowds identified
- `crowds` — Array of crowds with member coordinates
  - `count` — Number of people in the crowd
  - `members` — List of [x, y] centroids
- `detections` — All detected individuals
  - `bbox` — [x1, y1, x2, y2] bounding box coordinates
  - `confidence` — Detection confidence (0-1)
  - `class_name` — Always "person" for this model

---

#### More cURL Examples

**Upload from a different location:**
```bash
curl.exe -X POST http://localhost:9009/detect -F "file=@C:\path\to\image.png"
```

**Save response to file:**
```bash
curl.exe -X POST http://localhost:9009/detect -F "file=@test.jpg" > result.json
```

**Pretty-print JSON response:**
```bash
curl.exe -X POST http://localhost:9009/detect -F "file=@test.jpg" | powershell -Command "ConvertFrom-Json | ConvertTo-Json"
```

**Test with verbose output:**
```bash
curl.exe -v -X POST http://localhost:9009/detect -F "file=@test.jpg"
```
- `-v` flag shows request headers, response headers, and detailed information

---

### Using Python
```python
import requests

with open('test.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:9009/detect', files=files)
    result = response.json()
    
print(f"Total People: {result['total_people']}")
print(f"Crowds Detected: {result['crowd_count']}")
```

### Using PowerShell
```powershell
$uri = "http://localhost:9009/detect"
$filePath = "C:\path\to\test.jpg"
$form = @{ file = Get-Item -Path $filePath }
$response = Invoke-RestMethod -Uri $uri -Method Post -Form $form
$response | ConvertTo-Json
```

## Project Structure

```
crowd-detection/
├── app.py              # Flask application and API endpoints
├── detector.py         # CrowdDetector class with YOLOv8 + DBSCAN
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (optional)
├── .gitignore         # Git ignore file
├── models/            # Model weights directory (created automatically)
│   └── yolov8n.pt    # YOLOv8 nano model weights
└── README.md          # This file
```

## How It Works

1. **Image Upload** — User uploads an image via the `/detect` endpoint
2. **Person Detection** — YOLOv8n detects all people in the image
3. **Filtering** — Detections below `CONF_THRESHOLD` are filtered out
4. **Clustering** — DBSCAN groups nearby people based on `DISTANCE_THRESHOLD`
5. **Output** — Returns individual detections and identified crowds

### Crowd Detection Algorithm

The detector uses **DBSCAN (Density-Based Spatial Clustering)** to identify crowds:
- Scans each person's detection centroid
- Groups people within `DISTANCE_THRESHOLD` pixels
- Requires minimum `CROWD_THRESHOLD` people to form a valid crowd
- Ignores isolated individuals (noise points)

## Configuration Tips

### For Different Image Resolutions

- **Large images (4K)**: Increase `DISTANCE_THRESHOLD` to 200-300
- **Small images (480p)**: Decrease `DISTANCE_THRESHOLD` to 80-120
- **High-density crowds**: Decrease `CROWD_THRESHOLD` to 2-3
- **Sparse crowds**: Increase `CROWD_THRESHOLD` to 5-10

## Performance

- **Model**: YOLOv8n (nano, ~6.3M parameters, ~12ms inference)
- **Latency**: ~50-100ms per image (GPU) / ~200-500ms (CPU)
- **Memory**: ~500MB-1GB

## Troubleshooting

### No crowds detected despite many people visible
- Increase `DISTANCE_THRESHOLD` (default: 150)
- Decrease `CROWD_THRESHOLD` (default: 3)
- Check if confidence scores are above `CONF_THRESHOLD`

### Slow response
- Use GPU acceleration (CUDA)
- Reduce image resolution before uploading
- Use YOLOv8s instead of yolov8n for faster inference

### Model not loading
- Ensure `yolov8n.pt` exists in the project directory
- Check that `ultralytics` is installed: `pip install ultralytics`

## Dependencies

- **flask** — Web framework
- **ultralytics** — YOLOv8 object detection
- **scikit-learn** — DBSCAN clustering
- **torch** — Deep learning backend
- **torchvision** — Vision utilities
- **opencv-python** — Image processing
- **pillow** — Image manipulation
- **numpy** — Numerical computing
- **scipy** — Scientific computing
- **python-dotenv** — Environment variable management


## Author

Crowd Detection API - CVAPI Project
