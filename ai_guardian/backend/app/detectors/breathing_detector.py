import cv2
import numpy as np
from typing import Dict
from collections import deque

class BreathingDetector:
    """Detects breathing patterns and sleep apnea using optical flow"""
    
    def __init__(self, window_size: int = 150, fps: int = 30):
        self.window_size = window_size
        self.fps = fps
        self.chest_motion_history = deque(maxlen=window_size)
        self.prev_frame = None
        
    def detect_breathing(self, frame: np.ndarray) -> Dict:
        """Detect breathing patterns"""
        result = {
            'breathing_rate': 0,
            'breathing_detected': False,
            'apnea_risk': 0.0,
            'chest_motion': 0.0
        }
        
        if self.prev_frame is None:
            self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return result
        
        # Calculate optical flow
        current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(
            self.prev_frame, current_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )
        
        # Extract chest region (approximate center-left area)
        h, w = flow.shape[:2]
        chest_region = flow[h//3:2*h//3, w//4:3*w//4]
        
        # Calculate motion magnitude in chest region
        motion_magnitude = np.sqrt(
            chest_region[:,:,0]**2 + chest_region[:,:,1]**2
        )
        mean_motion = np.mean(motion_magnitude)
        
        self.chest_motion_history.append(mean_motion)
        result['chest_motion'] = mean_motion
        
        # Calculate breathing rate from motion history
        if len(self.chest_motion_history) > 60:
            breathing_rate = self._calculate_breathing_rate()
            result['breathing_rate'] = breathing_rate
            result['breathing_detected'] = breathing_rate > 0
            
            # Check for apnea
            result['apnea_risk'] = self._check_apnea_risk(breathing_rate)
        
        self.prev_frame = current_gray
        return result
    
    def _calculate_breathing_rate(self) -> float:
        """Calculate breathing rate from motion history"""
        if len(self.chest_motion_history) < 60:
            return 0.0
        
        signal = np.array(list(self.chest_motion_history))
        
        # Normalize
        if np.std(signal) == 0:
            return 0.0
        
        signal = (signal - np.mean(signal)) / np.std(signal)
        
        # Simple peak detection for breathing cycles
        # Breathing typically occurs at 0.1-0.5 Hz
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1.0 / self.fps)
        
        # Get positive frequencies in breathing range
        idx = np.where((freqs > 0.1) & (freqs < 0.5))[0]
        
        if len(idx) == 0:
            return 0.0
        
        power = np.abs(fft[idx]) ** 2
        dominant_freq_idx = np.argmax(power)
        dominant_freq = freqs[idx][dominant_freq_idx]
        
        # Convert to breaths per minute
        breathing_rate = dominant_freq * 60
        
        return breathing_rate
    
    def _check_apnea_risk(self, breathing_rate: float) -> float:
        """Check for sleep apnea risk"""
        # Normal breathing rate: 12-20 breaths per minute
        
        if breathing_rate == 0:
            return 0.95  # Critical: no breathing detected
        elif breathing_rate < 8:
            return 0.85  # High risk: too slow
        elif breathing_rate > 25:
            return 0.6  # Medium risk: too fast
        elif 12 <= breathing_rate <= 20:
            return 0.0  # Normal
        else:
            return 0.3  # Low risk: slightly abnormal
