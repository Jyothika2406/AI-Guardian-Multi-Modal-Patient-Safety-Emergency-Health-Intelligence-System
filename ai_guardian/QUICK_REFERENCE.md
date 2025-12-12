# AI Guardian - Quick Reference Card

## 🚀 Quick Start Commands

### Install & Setup
```bash
# Setup virtual environment
python setup.py

# Or manually
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r backend/requirements.txt
```

### Run System
```bash
# CLI Demo (recommended for testing)
cd backend
python demo.py

# Web Server
cd backend
python run.py
# Visit: http://localhost:5000/dashboard

# Run Examples
cd backend
python examples.py

# Run Tests
cd backend
python test.py
```

## 📊 API Reference

### Status Endpoint
```
GET http://localhost:5000/api/status

Response includes:
- Current metrics (heart rate, breathing, etc.)
- Active alerts
- Risk level
- Live video frame (base64)
```

### Camera Control
```
POST http://localhost:5000/api/camera/start
POST http://localhost:5000/api/camera/stop
```

## 🎯 Key Metrics Explained

### Heart Rate (BPM)
- Normal: 60-100
- Low: < 60
- High: > 100
- Critical: > 140

### Breathing Rate (BPM)
- Normal: 12-20
- Low: < 8
- High: > 25
- Apnea risk: 0 detected

### Stress Level (0-1 scale)
- 0.0-0.2: Relaxed
- 0.2-0.4: Normal
- 0.4-0.6: Mild stress
- 0.6-0.8: Moderate stress
- 0.8-1.0: High stress

### Fall Risk (0-1 scale)
- 0.0-0.2: Safe
- 0.2-0.4: Low risk
- 0.4-0.6: Medium risk
- 0.6-0.8: High risk
- 0.8-1.0: Critical

### Tremor Score (0-1 scale)
- 0.0-0.2: Normal
- 0.2-0.4: Low
- 0.4-0.6: Medium
- 0.6-0.8: High (Parkinson's risk)
- 0.8-1.0: Critical (Parkinson's risk)

## 🔴 Alert Severity Levels

| Level | Icon | Color | Meaning |
|-------|------|-------|---------|
| CRITICAL | 🚨 | Red | Immediate action needed |
| HIGH | ⚠️ | Orange | Significant risk detected |
| MEDIUM | ⚡ | Yellow | Monitor closely |
| LOW | ℹ️ | Green | Minor concerns |

## 🎮 Demo Controls

```
Q or q  - Quit monitoring
S or s  - Show session summary
ESC     - Exit full screen
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/run.py` | Start web server |
| `backend/demo.py` | CLI demo |
| `backend/examples.py` | Code examples |
| `backend/test.py` | Run tests |
| `frontend/index.html` | Web dashboard |
| `.env` | Configuration |
| `requirements.txt` | Dependencies |

## ⚙️ Configuration

### Edit `.env` file
```
FLASK_ENV=development
PORT=5000
CAMERA_INDEX=0
DEBUG=True
```

### Edit `app/config/settings.py` for thresholds
```python
FALL_CONFIDENCE_THRESHOLD = 0.6
TREMOR_THRESHOLD = 0.3
OBJECT_DETECTION_THRESHOLD = 0.5
HEART_RATE_MIN = 40
HEART_RATE_MAX = 150
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera not found | Try `--camera 1` in demo.py |
| Low FPS | Reduce resolution in settings.py |
| High CPU | Disable object detection in code |
| Import errors | Reinstall: `pip install -r requirements.txt` |
| NumPy error | `pip uninstall numpy && pip install numpy<2` |

## 🏥 Medical Accuracy Notes

**Remember**: This is a demonstration system
- For medical use, always verify with professionals
- Don't rely solely on AI for diagnosis
- Use FDA-approved medical devices for critical measurements
- Follow HIPAA compliance requirements
- Maintain proper patient documentation

## 📚 Documentation

| Document | Content |
|----------|---------|
| `README.md` | Project overview |
| `SETUP.md` | Installation guide |
| `ARCHITECTURE.md` | Technical architecture |
| `PROJECT_COMPLETION.md` | Completion status |

## 🔗 Useful URLs

When running locally:
- Dashboard: http://localhost:5000/dashboard
- API: http://localhost:5000/api/status
- Health Check: http://localhost:5000/

## 💻 System Requirements

- Python 3.8+
- 4GB RAM
- Webcam/USB camera
- 100MB disk space
- Modern CPU (Intel i5 equivalent or better)

## 📊 Performance Benchmarks

- **Latency**: 50-100ms
- **FPS**: 20-30
- **CPU**: 40-60% load
- **Memory**: 500MB-1GB
- **Model Size**: ~100MB

## 🔄 Common Workflows

### Test Single Detector
```python
from app.detectors.pose_detector import PoseDetector
detector = PoseDetector()
frame, data = detector.detect_pose(frame)
```

### Create Custom Alert
```python
alert = Alert(
    alert_type="CUSTOM",
    severity="HIGH",
    message="Custom message"
)
```

### Log Patient Data
```python
session = PatientSession("P001", "Patient Name")
session.update_health_metrics(health_metrics)
```

## 🚨 Critical Features

✅ Fall detection
✅ Object detection
✅ Heart rate monitoring
✅ Breathing analysis
✅ Tremor detection
✅ Stress measurement
✅ Real-time alerts
✅ Disease risk assessment

## 🎓 Learning Resources

**Code Examples**:
- Run `python examples.py` for 6 detailed examples
- Check `backend/app/` for module implementations
- Review `ARCHITECTURE.md` for technical details

**Testing**:
- Run `python test.py` to validate setup
- Review test cases for usage patterns

**Documentation**:
- Complete API docs in `ARCHITECTURE.md`
- Setup guide in `SETUP.md`
- Medical disclaimer in `README.md`

## 🔐 Security Notes

- All processing is local (no cloud upload)
- No video storage by default
- Can be air-gapped from internet
- HIPAA-compliant alert generation
- Configurable data retention

## 📞 Support

For issues:
1. Check `.env` configuration
2. Review logs in console output
3. Run `python test.py` for diagnostics
4. Check internet requirements
5. Verify camera permissions

## 🎉 You're Ready!

Your AI Guardian system is now ready to use. Start with:

```bash
cd backend
python demo.py
```

Enjoy monitoring! 🛡️

---

**Quick Reference v1.0** | AI Guardian Healthcare System
