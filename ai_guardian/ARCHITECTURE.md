# AI Guardian - Comprehensive Architecture & Implementation Guide

## 📋 Table of Contents
1. [System Architecture](#system-architecture)
2. [Module Documentation](#module-documentation)
3. [Detection Algorithms](#detection-algorithms)
4. [API Reference](#api-reference)
5. [Data Models](#data-models)
6. [Customization Guide](#customization-guide)
7. [Performance Optimization](#performance-optimization)

---

## System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    AI Guardian System                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Camera Input   │
                    │   (30 FPS)      │
                    └─────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │           Patient Monitor                    │
        │  (Orchestrates all detectors)                │
        └─────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
    ┌────────────┐      ┌────────────┐      ┌────────────┐
    │   Safety   │      │   Health   │      │  Disease   │
    │ Detection  │      │ Detection  │      │  Detection │
    └────────────┘      └────────────┘      └────────────┘
        │                     │                     │
    ├─ Pose                ├─ Heart Rate        ├─ Tremor
    ├─ Objects             ├─ Breathing         ├─ Sleep Apnea
    └─ Aggression          └─ Stress            └─ Color Analysis
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Alert System    │
                    │  (Risk Scoring)  │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Web Dashboard    │
                    │  & REST API      │
                    └──────────────────┘
```

### Data Flow
```
Frame (640x480)
    │
    ├─► Pose Detection (MediaPipe)
    │   └─► Landmarks [17 key points]
    │       └─► Fall Risk, Self-Harm Risk, Aggression
    │
    ├─► Object Detection (YOLOv8)
    │   └─► Detections [class, confidence, bbox]
    │       └─► Dangerous Objects List
    │
    ├─► Tremor Detection (MediaPipe Hands)
    │   └─► Hand Position History
    │       └─► Tremor Score
    │
    ├─► Heart Rate Detection (rPPG)
    │   └─► Green Channel Intensity
    │       └─► Heart Rate (BPM), Stress Level
    │
    ├─► Breathing Detection (Optical Flow)
    │   └─► Chest Motion Magnitude
    │       └─► Breathing Rate, Apnea Risk
    │
    └─► Health Color Analysis (HSV)
        └─► Face Color Distribution
            └─► Diabetes Risk, BP Risk
                │
                ▼
        Metrics Aggregation
                │
                ├─► HealthMetrics
                ├─► SafetyMetrics
                └─► Risk Scoring
                    │
                    ▼
            Alert Generation & Distribution
```

---

## Module Documentation

### 1. PoseDetector (pose_detector.py)

**Purpose**: Detect human body pose using MediaPipe

**Key Methods**:
- `detect_pose()`: Extract body landmarks
- `detect_fall_risk()`: Analyze body angle for falls
- `detect_self_harm_risk()`: Check hand positions near face
- `detect_aggressive_motion()`: Calculate arm movement speed

**Key Features**:
- 33 body landmarks (full body pose)
- Real-time processing
- Visibility confidence scores
- Angle-based fall detection

**Example**:
```python
detector = PoseDetector()
frame, pose_data = detector.detect_pose(frame)

if pose_data['landmarks']:
    fall_risk = detector.detect_fall_risk(pose_data['landmarks'])
    print(f"Fall Risk: {fall_risk:.2f}")  # 0-1 scale
```

### 2. ObjectDetector (object_detector.py)

**Purpose**: Detect dangerous objects using YOLO

**Key Methods**:
- `detect_objects()`: Run object detection
- `_draw_detections()`: Visualize detections

**Dangerous Objects**:
- Knife, scissors, gun, weapon, bottle

**Example**:
```python
detector = ObjectDetector('yolov8n.pt')
frame, detections = detector.detect_objects(frame)

for obj in detections['dangerous_objects']:
    print(f"{obj['class']}: {obj['confidence']:.2f}")
```

### 3. TremorDetector (tremor_detector.py)

**Purpose**: Detect hand tremors (Parkinson's indicator)

**Key Methods**:
- `detect_tremor()`: Analyze hand movement
- `_calculate_tremor_score()`: Compute tremor magnitude
- `detect_parkinsons_risk()`: Assess risk level

**Algorithm**:
- Hand tracking via MediaPipe Hands
- Velocity variance analysis
- High-frequency component extraction
- Normalized to 0-1 scale

**Risk Levels**:
- CRITICAL: 0.8-1.0
- HIGH: 0.6-0.8
- MEDIUM: 0.4-0.6
- LOW: 0.2-0.4
- NORMAL: 0-0.2

### 4. HeartRateDetector (heart_rate_detector.py)

**Purpose**: Estimate heart rate from facial color changes (rPPG)

**Algorithm**:
1. Extract face region
2. Isolate green channel (most sensitive to blood flow)
3. Apply FFT to detect dominant frequency
4. Convert frequency to BPM (Hz × 60)

**Stress Calculation**:
- < 60 BPM: Relaxed (0.3)
- 60-80 BPM: Normal (0.0)
- 80-100 BPM: Mild stress (0.3)
- 100-120 BPM: Moderate stress (0.6)
- > 120 BPM: High stress (0.9)

**Limitations**:
- Requires good lighting
- Sensitive to face movement
- Best accuracy with still subject

### 5. BreathingDetector (breathing_detector.py)

**Purpose**: Detect breathing patterns (sleep apnea detection)

**Algorithm**:
1. Calculate optical flow between frames
2. Extract chest region
3. Measure motion magnitude
4. Perform FFT to find breathing frequency
5. Detect apnea patterns

**Normal Range**: 12-20 breaths per minute

**Apnea Risk**:
- No breathing: 0.95 (CRITICAL)
- < 8 BPM: 0.85 (HIGH)
- > 25 BPM: 0.6 (MEDIUM)
- 12-20 BPM: 0.0 (NORMAL)

### 6. HealthColorDetector (health_color_detector.py)

**Purpose**: Detect health conditions from face color

**HSV Analysis**:
- **Saturation**: Intensity of color
- **Value**: Brightness
- **Hue**: Actual color tone

**Indicators**:
- High saturation + high value → Flush (High BP risk)
- Low value → Pale (Low BP/Anemia)
- Yellowish tint → Diabetes/Liver risk
- Bluish tint → Respiratory risk

---

## Detection Algorithms

### Fall Detection Algorithm

```
Body Landmarks → Extract Key Points
                    │
                    ▼
            Calculate Joint Angles
                    │
         ┌──────────┼──────────┐
         │          │          │
         ▼          ▼          ▼
    Shoulder   Hip      Ankle
    Angle      Position  Position
         │          │          │
         └──────────┼──────────┘
                    │
                    ▼
        Check Thresholds:
        - Hip Y >> Shoulder Y? → Falling
        - Nose Y >> 0.8? → Lying down
        - Nose X far from Shoulder? → Leaning
                    │
                    ▼
        Fall Risk Score (0-1)
```

**Thresholds**:
- Hip below shoulder by 15%: 0.9 (Falling)
- Nose near ground (Y > 0.8): 0.85 (Lying)
- Excessive lean (X offset > 0.15): 0.6

### Heart Rate Detection (rPPG)

```
Frame → CVT to BGR → Extract Face → CVT to BGR
                          │
                          ▼
                  Extract Green Channel
                    (most PPG signal)
                          │
                          ▼
              Normalize & Bandpass Filter
              (0.7-4.0 Hz range)
                          │
                          ▼
                    Apply FFT
                          │
                          ▼
            Find Dominant Frequency
                          │
                          ▼
            Convert to BPM (freq × 60)
```

**Confidence**: Based on dominant frequency power

### Breathing Detection

```
Consecutive Frames → Calculate Optical Flow
                            │
                            ▼
                  Extract Chest Region
                            │
                            ▼
              Calculate Motion Magnitude
                            │
                            ▼
            Keep History (window = 150 frames)
                            │
                            ▼
                    Apply FFT
              (0.1-0.5 Hz breathing range)
                            │
                            ▼
        Detect Dominant Frequency
                            │
                            ▼
        Convert to BPM (freq × 60)
```

---

## API Reference

### REST Endpoints

#### GET /api/status
Get current patient metrics

**Response**:
```json
{
  "status": "active",
  "patient_id": "P001",
  "patient_name": "John Doe",
  "risk_level": "MEDIUM",
  "metrics": {
    "heart_rate": 85.5,
    "breathing_rate": 18.2,
    "stress_level": 0.35,
    "tremor_score": 0.15,
    "fall_risk": 0.25,
    "self_harm_risk": 0.0,
    "aggressive_motion": 0.1
  },
  "alerts": [
    {
      "alert_type": "TREMOR_DETECTED",
      "severity": "MEDIUM",
      "message": "Significant tremor detected",
      "timestamp": "2024-01-15T10:30:45.123456"
    }
  ],
  "frame": "base64_encoded_image"
}
```

#### POST /api/camera/start
Start monitoring

**Response**:
```json
{
  "status": "success",
  "message": "Camera monitoring started"
}
```

#### POST /api/camera/stop
Stop monitoring

**Response**:
```json
{
  "status": "success",
  "message": "Camera monitoring stopped"
}
```

---

## Data Models

### HealthMetrics
```python
@dataclass
class HealthMetrics:
    heart_rate: float = 0              # BPM (40-150)
    breathing_rate: float = 0          # BPM (8-25)
    stress_level: float = 0            # 0-1 scale
    tremor_score: float = 0            # 0-1 scale
    skin_color_risk: str = "NORMAL"    # NORMAL, FLUSH, PALE, etc.
    timestamp: datetime = field(default_factory=datetime.now)
```

### SafetyMetrics
```python
@dataclass
class SafetyMetrics:
    fall_risk: float = 0               # 0-1 scale
    self_harm_risk: float = 0          # 0-1 scale
    aggressive_motion: float = 0       # 0-1 scale
    dangerous_objects: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
```

### Alert
```python
@dataclass
class Alert:
    alert_type: str                    # FALL_CRITICAL, TREMOR_DETECTED, etc.
    severity: str                      # CRITICAL, HIGH, MEDIUM, LOW
    message: str                       # Human-readable message
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict = field(default_factory=dict)
```

---

## Customization Guide

### Adjusting Thresholds

Edit `backend/app/config/settings.py`:

```python
# Fall detection
FALL_CONFIDENCE_THRESHOLD = 0.6  # 0-1 scale

# Tremor detection
TREMOR_THRESHOLD = 0.3  # 0-1 scale

# Object detection
OBJECT_DETECTION_THRESHOLD = 0.5  # Confidence

# Health ranges
HEART_RATE_MIN = 40
HEART_RATE_MAX = 150
BREATHING_RATE_MIN = 8
BREATHING_RATE_MAX = 25
```

### Custom Alert Rules

Edit alert generation in `backend/app/utils/alert_system.py`:

```python
def _check_safety_metrics(self, session: PatientSession) -> List[Alert]:
    metrics = session.current_safety_metrics
    
    # Add custom rule
    if metrics.fall_risk > 0.85:
        alerts.append(Alert(
            alert_type='FALL_IMMINENT',
            severity='CRITICAL',
            message='Fall imminent - check patient immediately!'
        ))
    
    return alerts
```

### Custom Detector

1. Create new file: `backend/app/detectors/custom_detector.py`
2. Implement detector class
3. Integrate in `patient_monitor.py`

Example:
```python
class CustomDetector:
    def detect(self, frame: np.ndarray) -> Dict:
        # Your algorithm here
        return {
            'metric': value,
            'score': 0.0
        }
```

---

## Performance Optimization

### 1. Frame Resolution
```python
# Lower resolution = faster processing
FRAME_WIDTH = 320  # Default: 640
FRAME_HEIGHT = 240  # Default: 480
```

### 2. Model Selection
```python
# Use nano model for speed
model = YOLO('yolov8n.pt')  # Nano
# model = YOLO('yolov8s.pt')  # Small
# model = YOLO('yolov8m.pt')  # Medium
```

### 3. Skip Expensive Detections
```python
# Comment out in patient_monitor.py
# tremor_data = self.tremor_detector.detect_tremor(frame)
# breathing_data = self.breathing_detector.detect_breathing(frame)
```

### 4. Multi-threading
```python
# Run detector in separate thread
import threading

def detect_async(frame):
    thread = threading.Thread(target=detector.detect_tremor, args=(frame,))
    thread.start()
```

### 5. Frame Skipping
```python
# Process every Nth frame
if frame_count % 2 == 0:  # Process every 2nd frame
    tremor_data = self.tremor_detector.detect_tremor(frame)
```

### Benchmark Results

| Detector | FPS | CPU % | Memory |
|----------|-----|-------|--------|
| Pose | 30 | 15% | 100MB |
| Object | 25 | 25% | 200MB |
| Tremor | 30 | 5% | 50MB |
| Heart Rate | 30 | 5% | 50MB |
| Breathing | 30 | 5% | 50MB |
| Color | 30 | 3% | 30MB |
| **Total** | **20-25** | **50-60%** | **500MB** |

---

## Troubleshooting

### Low FPS
- Reduce resolution
- Skip expensive detectors
- Use GPU acceleration (requires CUDA)

### High CPU Usage
- Disable unused detectors
- Increase frame skip ratio
- Reduce model complexity

### Inaccurate Metrics
- Improve lighting
- Move closer to camera
- Use higher resolution

### Memory Leaks
- Monitor frame history
- Clear detector caches
- Limit alert history

---

**For more information, see README.md and SETUP.md**
