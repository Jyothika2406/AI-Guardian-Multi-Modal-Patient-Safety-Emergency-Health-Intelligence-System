# AI Guardian Setup & Deployment Guide

## Quick Start

### Option 1: Command Line Demo
```bash
cd backend
python demo.py
```

Options:
```bash
python demo.py --help
python demo.py --camera 0 --patient-id P001 --patient-name "John Doe"
python demo.py --headless  # Run without display
```

### Option 2: Web Dashboard
```bash
cd backend
python run.py
```
Then open: `http://localhost:5000/dashboard`

## Installation Steps

### 1. Prerequisites
- Python 3.8+
- pip
- Webcam/USB camera
- Minimum 4GB RAM

### 2. Setup Python Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Download YOLO Model (Optional)
The system will auto-download YOLOv8n model on first use.
Pre-download with:
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## Running the System

### Demo Mode (Recommended for Testing)
```bash
cd backend
python demo.py --patient-name "Test Patient"
```

### Web Dashboard (Production)
```bash
cd backend
python run.py
```
Visit: http://localhost:5000

### Configuration
Edit `backend/.env`:
```
FLASK_ENV=development
PORT=5000
CAMERA_INDEX=0
DEBUG=True
```

Edit `backend/app/config/settings.py` for thresholds.

## Features Overview

### Safety Monitoring
- Fall detection (body angle analysis)
- Self-harm detection (hand position tracking)
- Aggressive motion detection
- Dangerous object detection (knife, scissors, etc.)

### Health Monitoring
- Heart rate estimation (rPPG)
- Breathing rate analysis (optical flow)
- Stress level calculation
- Tremor detection (Parkinson's screening)

### Disease Risk Assessment
- Parkinson's risk (tremor analysis)
- Sleep apnea risk (breathing abnormalities)
- Diabetes risk (face color analysis)
- Blood pressure risk (facial flushing detection)

## Troubleshooting

### Camera Not Detected
```bash
# List available cameras
python -c "import cv2; print(cv2.getBuildInformation())"

# Try different camera index
python demo.py --camera 1
```

### Low Performance
- Reduce resolution in settings.py
- Skip object detection if not needed
- Close other applications
- Use headless mode: `python demo.py --headless`

### Import Errors
Reinstall missing packages:
```bash
pip install --upgrade -r requirements.txt
```

### YOLO Model Issues
```bash
# Clear cache and redownload
rm -rf ~/.ultralytics/
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## API Endpoints

### Status
```
GET http://localhost:5000/api/status
```

### Camera Control
```
POST http://localhost:5000/api/camera/start
POST http://localhost:5000/api/camera/stop
```

### Dashboard
```
GET http://localhost:5000/dashboard
```

## Docker Deployment

### Build Image
```bash
docker build -t ai-guardian .
```

### Run Container
```bash
docker run --device /dev/video0 -p 5000:5000 ai-guardian
```

## Performance Metrics

- **Latency**: 50-100ms per frame (30 FPS)
- **CPU**: 40-60% on modern processors
- **Memory**: 500MB-1GB
- **Storage**: 100MB for models

## Advanced Configuration

### Custom Alert Thresholds
Edit `backend/app/config/settings.py`:
```python
FALL_CONFIDENCE_THRESHOLD = 0.6
TREMOR_THRESHOLD = 0.3
OBJECT_DETECTION_THRESHOLD = 0.5
HEART_RATE_MIN = 40
HEART_RATE_MAX = 150
```

### Logging
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Multi-Patient Support (Future)
Current version supports single patient. For multiple:
1. Create multiple PatientMonitor instances
2. Run separate camera threads
3. Aggregate metrics in dashboard

## Medical Accuracy Notes

**DISCLAIMER**: This is a demonstration system. For medical use:
- Always verify with qualified healthcare professionals
- Use FDA-approved devices for health measurements
- Don't rely solely on AI for diagnoses
- Maintain proper patient documentation
- Follow HIPAA compliance requirements

## Support

For issues:
1. Check error logs
2. Review configuration
3. Test with sample videos
4. Enable debug mode
5. Check camera permissions

## Future Enhancements

- [ ] Multi-patient dashboard
- [ ] Mobile app integration
- [ ] Hospital database integration
- [ ] Advanced ML models
- [ ] Cloud deployment
- [ ] Thermal imaging support
- [ ] Wearable sensor integration
