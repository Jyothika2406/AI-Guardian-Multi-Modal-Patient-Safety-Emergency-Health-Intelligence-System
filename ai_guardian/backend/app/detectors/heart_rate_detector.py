import cv2
import numpy as np
from typing import Dict, Tuple
from collections import deque

class HeartRateDetector:
    """Detects heart rate using rPPG (remote photoplethysmography)"""
    
    def __init__(self, window_size: int = 150, fps: int = 30):
        self.window_size = window_size
        self.fps = fps
        self.green_channel_history = deque(maxlen=window_size)
        self.last_heart_rate = 0
        self.stress_level = 0.0
        
    def detect_heart_rate(self, frame: np.ndarray, face_region: Tuple = None) -> Dict:
        """Detect heart rate from face region"""
        result = {
            'heart_rate': 0,
            'confidence': 0.0,
            'stress_level': 0.0,
            'pulse_detected': False
        }
        
        # Try to detect face if not provided
        if face_region is None:
            face_region = self._detect_face(frame)
        
        if face_region is None:
            return result
        
        # Extract face region
        x, y, w, h = face_region
        face = frame[y:y+h, x:x+w]
        
        if face.size == 0:
            return result
        
        # Extract green channel (more sensitive to blood flow)
        green_channel = face[:, :, 1]  # BGR format
        
        # Calculate mean green intensity
        mean_green = np.mean(green_channel)
        self.green_channel_history.append(mean_green)
        
        # Calculate heart rate if we have enough history
        if len(self.green_channel_history) > 60:
            heart_rate, confidence = self._calculate_heart_rate()
            result['heart_rate'] = heart_rate
            result['confidence'] = confidence
            result['pulse_detected'] = confidence > 0.5
            self.last_heart_rate = heart_rate
            
            # Calculate stress level based on heart rate deviation
            result['stress_level'] = self._calculate_stress_level(heart_rate)
        
        return result
    
    def _detect_face(self, frame: np.ndarray) -> Tuple:
        """Detect face region using cascades"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            return (x, y, w, h)
        
        return None
    
    def _calculate_heart_rate(self) -> Tuple[float, float]:
        """Calculate heart rate from green channel history"""
        if len(self.green_channel_history) < 60:
            return 0, 0.0
        
        signal = np.array(list(self.green_channel_history))
        
        # Normalize signal
        signal = (signal - np.mean(signal)) / np.std(signal)
        
        # Apply bandpass filter (0.7 Hz - 4 Hz for heart rate)
        # Simple FFT-based approach
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1.0 / self.fps)
        
        # Get positive frequencies
        idx = np.where((freqs > 0.7) & (freqs < 4.0))[0]
        
        if len(idx) == 0:
            return 0, 0.0
        
        # Find dominant frequency
        power = np.abs(fft[idx]) ** 2
        dominant_freq_idx = np.argmax(power)
        dominant_freq = freqs[idx][dominant_freq_idx]
        
        # Convert frequency to BPM
        heart_rate = dominant_freq * 60
        
        # Calculate confidence
        if len(power) > 0:
            confidence = power[dominant_freq_idx] / np.sum(power)
        else:
            confidence = 0.0
        
        return heart_rate, confidence
    
    def _calculate_stress_level(self, heart_rate: float) -> float:
        """Calculate stress level based on heart rate"""
        # Normal resting heart rate: 60-100 BPM
        if heart_rate < 60:
            stress = 0.3  # Low stress, potentially relaxed
        elif heart_rate < 80:
            stress = 0.0  # Normal
        elif heart_rate < 100:
            stress = 0.3  # Mild stress
        elif heart_rate < 120:
            stress = 0.6  # Moderate stress
        else:
            stress = 0.9  # High stress
        
        return stress
