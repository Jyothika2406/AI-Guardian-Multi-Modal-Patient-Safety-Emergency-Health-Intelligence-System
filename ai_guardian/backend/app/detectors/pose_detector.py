import cv2
import numpy as np
import mediapipe as mp
from typing import Tuple, Dict, List

class PoseDetector:
    """Detects human pose using MediaPipe"""
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def detect_pose(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """Detect pose landmarks in frame"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        landmarks = []
        if results.pose_landmarks:
            for landmark in results.pose_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z,
                    'visibility': landmark.visibility
                })
        
        return frame, {
            'landmarks': landmarks,
            'has_person': len(landmarks) > 0
        }
    
    def draw_pose(self, frame: np.ndarray, pose_data: Dict) -> np.ndarray:
        """Draw pose landmarks on frame"""
        if not pose_data['landmarks']:
            return frame
        
        # Reconstruct landmarks for drawing
        class LandmarkData:
            def __init__(self, x, y, z, visibility):
                self.x = x
                self.y = y
                self.z = z
                self.visibility = visibility
        
        h, w, c = frame.shape
        landmarks_proto = mp.framework.formats.landmark_pb2.NormalizedLandmarkList()
        
        for landmark_dict in pose_data['landmarks']:
            landmark = landmarks_proto.landmark.add()
            landmark.x = landmark_dict['x']
            landmark.y = landmark_dict['y']
            landmark.z = landmark_dict['z']
            landmark.visibility = landmark_dict['visibility']
        
        self.mp_drawing.draw_landmarks(
            frame,
            landmarks_proto,
            self.mp_pose.POSE_CONNECTIONS
        )
        
        return frame
    
    def calculate_angle(self, point1: Dict, point2: Dict, point3: Dict) -> float:
        """Calculate angle between three points"""
        x1, y1 = point1['x'], point1['y']
        x2, y2 = point2['x'], point2['y']
        x3, y3 = point3['x'], point3['y']
        
        angle = np.arctan2(y3 - y2, x3 - x2) - np.arctan2(y1 - y2, x1 - x2)
        return np.abs(np.degrees(angle))
    
    def detect_fall_risk(self, landmarks: List[Dict]) -> float:
        """Detect fall risk based on pose"""
        if len(landmarks) < 32:
            return 0.0
        
        # Get key joints
        nose = landmarks[0]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_hip = landmarks[23]
        right_hip = landmarks[24]
        left_ankle = landmarks[27]
        right_ankle = landmarks[28]
        
        # Calculate body angle
        shoulder_y = (left_shoulder['y'] + right_shoulder['y']) / 2
        hip_y = (left_hip['y'] + right_hip['y']) / 2
        ankle_y = (left_ankle['y'] + right_ankle['y']) / 2
        
        # If hip is below shoulders significantly, person is falling
        if hip_y > shoulder_y + 0.15:
            return 0.9
        
        # If lying down (nose close to ground)
        if nose['y'] > 0.8:
            return 0.85
        
        # Check if leaning forward excessively
        nose_x = nose['x']
        shoulder_x = (left_shoulder['x'] + right_shoulder['x']) / 2
        if abs(nose_x - shoulder_x) > 0.15:
            return 0.6
        
        return 0.0
    
    def detect_self_harm_risk(self, landmarks: List[Dict]) -> float:
        """Detect potential self-harm actions"""
        if len(landmarks) < 32:
            return 0.0
        
        nose = landmarks[0]
        left_wrist = landmarks[15]
        right_wrist = landmarks[16]
        left_hand = landmarks[19]
        right_hand = landmarks[20]
        
        # Check if hands are near face/neck
        face_region = nose['y'] - 0.1
        
        hands_near_face = 0
        if left_wrist['y'] < face_region and left_wrist['visibility'] > 0.5:
            hands_near_face += 1
        if right_wrist['y'] < face_region and right_wrist['visibility'] > 0.5:
            hands_near_face += 1
        
        return min(0.5 * hands_near_face, 1.0)
    
    def detect_aggressive_motion(self, landmarks: List[Dict], prev_landmarks: List[Dict]) -> float:
        """Detect aggressive or violent motions"""
        if not prev_landmarks or len(landmarks) < 32:
            return 0.0
        
        # Calculate motion in arms
        left_shoulder = landmarks[11]
        left_wrist = landmarks[15]
        prev_left_wrist = prev_landmarks[15] if len(prev_landmarks) > 15 else None
        
        if not prev_left_wrist:
            return 0.0
        
        # Calculate motion speed
        motion_x = abs(left_wrist['x'] - prev_left_wrist['x'])
        motion_y = abs(left_wrist['y'] - prev_left_wrist['y'])
        motion_speed = np.sqrt(motion_x**2 + motion_y**2)
        
        # High speed arm movement could indicate aggression
        if motion_speed > 0.1:
            return 0.7
        
        return 0.0
