# AI Guardian - Multi-Modal Patient Safety & Health Monitoring System

An advanced AI-powered healthcare system that monitors patient safety and health using vision-based AI with a single camera. It detects falls, self-harm attempts, health risks, and disease indicators in real-time.

## 🎯 Project Overview

AI Guardian combines multiple AI models to provide comprehensive patient monitoring:
- **Safety Monitoring**: Fall detection, self-harm detection, aggressive motion, dangerous objects
- **Health Monitoring**: Heart rate, breathing patterns, stress levels, tremor analysis
- **Disease Prediction**: Early indicators for Parkinson's, sleep apnea, diabetes, BP abnormalities
- **Real-time Alerts**: Severity-based alert system with live notifications
- **Dashboard**: Comprehensive web-based monitoring dashboard

## 🏗️ Architecture

### Backend Stack
- **Framework**: Flask + Flask-SocketIO (Python)
- **AI Models**:
  - MediaPipe (Pose, Hands detection)
  - YOLOv8 Nano (Object detection)
  - rPPG (Heart rate from video)
  - Optical Flow (Breathing analysis)
  - Custom algorithms (Tremor, health indicators)

### Frontend Stack
- **Dashboard**: HTML5 + CSS3 + JavaScript
- **Features**: Real-time metrics, live video feed, alert system

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam/Camera
- 4GB RAM minimum

### Installation

1. **Clone the project**
```bash
cd ai_guardian
```

2. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Run the backend**
```bash
python run.py
```

4. **Open dashboard**
Open `frontend/index.html` in a web browser:
```
http://localhost:5000/dashboard
```

## 📊 Features

### Safety Monitoring
- **Fall Detection**: Analyzes body posture and position to detect falls or high-risk situations
- **Self-Harm Detection**: Tracks hand positions relative to face/neck area
- **Aggressive Motion**: Detects rapid arm movements indicating potential violence
- **Dangerous Objects**: Uses YOLOv8 to identify knives, scissors, and other weapons

### Health Monitoring
- **Heart Rate**: rPPG analysis from facial skin color changes (40-150 BPM)
- **Breathing Rate**: Optical flow analysis of chest movements (8-25 breaths/min)
- **Stress Level**: Calculated from heart rate and breathing patterns (0-1 scale)
- **Tremor Analysis**: Detects hand/arm tremors indicating neurological conditions

### Disease Risk Assessment
- **Parkinson's Risk**: Hand tremor frequency and amplitude analysis
- **Sleep Apnea Risk**: Abnormal breathing pattern detection
- **Diabetes Risk**: Face color analysis for early indicators
- **Blood Pressure Risk**: Skin color and facial flushing analysis

### Alert System
Risk Levels:
- 🔴 **CRITICAL** (0.8-1.0): Immediate intervention required
- 🟠 **HIGH** (0.6-0.8): Significant risk detected
- 🟡 **MEDIUM** (0.4-0.6): Monitor closely
- 🟢 **LOW** (0.2-0.4): Minor concerns
- ✅ **SAFE** (0-0.2): No immediate concerns

## 🔧 Configuration

Edit `backend/.env` to customize:
```
FLASK_ENV=development      # development or production
PORT=5000                  # API port
CAMERA_INDEX=0             # Camera device index
DEBUG=True                 # Debug mode
```

Edit `backend/app/config/settings.py` for thresholds and model paths.

## 📁 Project Structure

```
ai_guardian/
├── backend/                 # Python Flask backend
│   ├── app/
│   │   ├── config/         # Configuration files
│   │   ├── detectors/      # AI detection modules
│   │   │   ├── pose_detector.py
│   │   │   ├── object_detector.py
│   │   │   ├── tremor_detector.py
│   │   │   ├── heart_rate_detector.py
│   │   │   ├── breathing_detector.py
│   │   │   └── health_color_detector.py
│   │   ├── models/         # Data models
│   │   ├── utils/          # Utilities
│   │   └── routes.py       # API endpoints
│   ├── run.py             # Entry point
│   └── requirements.txt    # Dependencies
├── frontend/              # Web dashboard
│   └── index.html         # Main dashboard UI
└── README.md             # This file
```

## 🔌 API Endpoints

### Main Endpoints
- `GET /` - API information
- `GET /dashboard` - Web dashboard
- `GET /api/status` - Current system status and metrics

### Camera Control
- `POST /api/camera/start` - Start monitoring
- `POST /api/camera/stop` - Stop monitoring

## 🎨 Dashboard Features

- **Live Video Feed**: Real-time camera feed with pose skeleton overlay
- **Health Metrics Panel**: Heart rate, breathing, stress, tremor
- **Safety Metrics Panel**: Fall risk, self-harm risk, aggression, dangerous objects
- **Disease Risk Panel**: Parkinson's, sleep apnea, diabetes, BP risks
- **Alert Panel**: Real-time alerts with severity indicators
- **Overall Risk Level**: Color-coded risk assessment

## 🔄 Data Flow

1. **Camera Input** → Capture frames at 30 FPS
2. **Pose Detection** → Extract body landmarks using MediaPipe
3. **Safety Analysis** → Calculate fall, self-harm, aggression risks
4. **Object Detection** → Identify dangerous objects using YOLO
5. **Health Analysis** → Extract heart rate, breathing, tremor
6. **Risk Assessment** → Combine metrics to calculate overall risk
7. **Alert Generation** → Create alerts for abnormal conditions
8. **Dashboard Update** → Stream results to web interface

## 📈 Performance

- **Latency**: ~50-100ms per frame (30 FPS capable)
- **CPU Usage**: ~40-60% on modern processors
- **Memory**: ~500MB-1GB runtime
- **Storage**: ~100MB for models

## 🔮 Future Enhancements

1. **Multi-Patient Support**
   - Multiple camera streams
   - Centralized monitoring server
   - Hospital-wide dashboard

2. **Advanced Features**
   - Audio distress detection ("Help!", crying)
   - Doctor mobile app notifications
   - Integration with hospital databases
   - Predictive health analytics
   - ML-based risk prediction

3. **Improvements**
   - Facial recognition for patient identification
   - Wearable sensor integration (heart rate, BP)
   - Integration with electronic medical records
   - 3D pose estimation for better fall detection
   - Thermal imaging for additional health insights

## 🛡️ Safety & Privacy

- All processing happens locally on the device
- No cloud storage of video by default
- HIPAA-compliant alert generation
- Configurable data retention policies
- Encryption for data in transit (optional)

## 📝 Model References

- **MediaPipe**: https://mediapipe.dev/
- **YOLOv8**: https://github.com/ultralytics/ultralytics
- **rPPG**: Remote Photoplethysmography for heart rate
- **Optical Flow**: Lucas-Kanade method for motion analysis

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Enhanced disease prediction models
- Multi-camera support
- Mobile app development
- Cloud integration
- Performance optimization

## 📄 License

This project is provided as-is for healthcare research and development purposes.

## ⚕️ Medical Disclaimer

**IMPORTANT**: This system is intended as a supplementary monitoring tool and should NOT replace professional medical care. Always consult with qualified healthcare professionals for medical advice and diagnosis.

## 🆘 Support & Issues

For issues, questions, or suggestions:
1. Check existing documentation
2. Review configuration settings
3. Test with different cameras/lighting
4. Enable debug mode for troubleshooting

## 🎓 Educational Use

This project serves as an educational example of:
- Real-time AI/ML in healthcare
- Computer vision applications
- Flask web application development
- IoT and edge computing
- Healthcare data processing

---

**AI Guardian v1.0** | Healthcare Innovation Lab | 2024
