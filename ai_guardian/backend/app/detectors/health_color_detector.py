import cv2
import numpy as np
from typing import Dict, Tuple

class HealthColorDetector:
    """Detects health conditions through face color analysis"""
    
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
    def detect_health_indicators(self, frame: np.ndarray) -> Dict:
        """Detect health indicators from face color"""
        result = {
            'diabetes_risk': 0.0,
            'bp_risk': 0.0,
            'skin_color_status': 'NORMAL',
            'face_detected': False
        }
        
        # Detect face
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return result
        
        result['face_detected'] = True
        x, y, w, h = faces[0]
        face_roi = frame[y:y+h, x:x+w]
        
        # Convert to HSV for better color analysis
        hsv_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
        
        # Analyze color
        diabetes_risk, bp_risk, color_status = self._analyze_face_color(hsv_face)
        
        result['diabetes_risk'] = diabetes_risk
        result['bp_risk'] = bp_risk
        result['skin_color_status'] = color_status
        
        return result
    
    def _analyze_face_color(self, hsv_image: np.ndarray) -> Tuple[float, float, str]:
        """Analyze HSV image for health indicators"""
        
        # Extract color channels
        h, s, v = cv2.split(hsv_image)
        
        # Analyze saturation (skin color intensity)
        mean_saturation = np.mean(s)
        mean_value = np.mean(v)
        
        # Analyze hue distribution
        mean_hue = np.mean(h)
        
        diabetes_risk = 0.0
        bp_risk = 0.0
        color_status = 'NORMAL'
        
        # High saturation and value might indicate fever/high blood pressure
        if mean_value > 200 and mean_saturation > 100:
            bp_risk = 0.7
            color_status = 'FLUSH - High BP Risk'
        
        # Low value might indicate anemia or low BP
        elif mean_value < 100:
            bp_risk = 0.6
            diabetes_risk = 0.4
            color_status = 'PALE - Low BP Risk'
        
        # Yellowish tint (high hue in red range, specific saturation)
        elif 10 < mean_hue < 30 and mean_saturation > 120:
            diabetes_risk = 0.7
            color_status = 'YELLOW_TINT - Diabetes/Liver Risk'
        
        # Bluish tint might indicate respiratory issues
        elif mean_hue > 100 or mean_hue < 10:
            color_status = 'CYANOTIC - Respiratory Risk'
        
        # Add random variation for demonstration
        diabetes_risk += np.random.normal(0, 0.05)
        bp_risk += np.random.normal(0, 0.05)
        
        diabetes_risk = np.clip(diabetes_risk, 0, 1)
        bp_risk = np.clip(bp_risk, 0, 1)
        
        return diabetes_risk, bp_risk, color_status
