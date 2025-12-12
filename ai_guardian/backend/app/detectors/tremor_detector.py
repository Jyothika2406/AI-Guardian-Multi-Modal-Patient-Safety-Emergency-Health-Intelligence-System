import cv2
import numpy as np
import mediapipe as mp
from typing import Dict, List
from collections import deque

class TremorDetector:
    """Detects tremors (Parkinson's symptoms) using hand tracking"""
    
    def __init__(self, window_size: int = 30):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=1
        )
        self.window_size = window_size
        self.hand_position_history = deque(maxlen=window_size)
        
    def detect_tremor(self, frame: np.ndarray) -> Dict:
        """Detect tremors in hand movements"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        tremor_data = {
            'tremor_score': 0.0,
            'left_hand_tremor': 0.0,
            'right_hand_tremor': 0.0,
            'is_tremor_detected': False,
            'hand_positions': []
        }
        
        if not results.multi_hand_landmarks:
            return tremor_data
        
        for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get wrist position
            wrist = hand_landmarks.landmark[0]
            position = np.array([wrist.x, wrist.y])
            
            self.hand_position_history.append(position)
            
            # Calculate tremor score based on velocity variance
            if len(self.hand_position_history) > 5:
                tremor_score = self._calculate_tremor_score(
                    list(self.hand_position_history)
                )
                
                if hand_idx == 0:
                    tremor_data['right_hand_tremor'] = tremor_score
                else:
                    tremor_data['left_hand_tremor'] = tremor_score
                
                tremor_data['hand_positions'].append({
                    'hand': 'right' if hand_idx == 0 else 'left',
                    'x': wrist.x,
                    'y': wrist.y,
                    'tremor': tremor_score
                })
        
        # Overall tremor score
        tremor_data['tremor_score'] = max(
            tremor_data['left_hand_tremor'],
            tremor_data['right_hand_tremor']
        )
        tremor_data['is_tremor_detected'] = tremor_data['tremor_score'] > 0.5
        
        return tremor_data
    
    def _calculate_tremor_score(self, positions: List[np.ndarray]) -> float:
        """Calculate tremor score from position history"""
        if len(positions) < 3:
            return 0.0
        
        positions = np.array(positions)
        
        # Calculate velocities
        velocities = np.diff(positions, axis=0)
        
        # Calculate velocity magnitudes
        vel_magnitudes = np.linalg.norm(velocities, axis=1)
        
        # Calculate high-frequency components (tremor)
        # High variance in small time windows indicates tremor
        high_freq_variance = np.var(vel_magnitudes[-5:]) if len(vel_magnitudes) >= 5 else 0
        
        # Normalize to 0-1 range
        tremor_score = min(high_freq_variance * 100, 1.0)
        
        return tremor_score
    
    def detect_parkinsons_risk(self, tremor_data: Dict) -> str:
        """Assess Parkinson's risk based on tremor"""
        tremor_score = tremor_data['tremor_score']
        
        if tremor_score > 0.8:
            return "CRITICAL"
        elif tremor_score > 0.6:
            return "HIGH"
        elif tremor_score > 0.4:
            return "MEDIUM"
        elif tremor_score > 0.2:
            return "LOW"
        else:
            return "NORMAL"
