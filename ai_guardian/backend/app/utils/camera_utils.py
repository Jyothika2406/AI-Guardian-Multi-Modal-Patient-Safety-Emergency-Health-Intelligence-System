import cv2
import numpy as np
from typing import Optional, Tuple, Dict

class CameraManager:
    """Manages camera input and frame processing"""
    
    def __init__(self, camera_index: int = 0, width: int = 640, height: int = 480, fps: int = 30):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None
        self.is_running = False
        
    def initialize(self) -> bool:
        """Initialize camera"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                return False
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            self.is_running = True
            return True
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def read_frame(self) -> Optional[np.ndarray]:
        """Read frame from camera"""
        if self.cap is None or not self.is_running:
            return None
        
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None
    
    def release(self):
        """Release camera"""
        if self.cap is not None:
            self.cap.release()
            self.is_running = False
    
    def get_frame_info(self) -> Dict:
        """Get current frame information"""
        if self.cap is None:
            return {}
        
        return {
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': self.cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        }

def resize_frame(frame: np.ndarray, width: int = 640, height: int = 480) -> np.ndarray:
    """Resize frame to specified dimensions"""
    return cv2.resize(frame, (width, height))

def add_text_to_frame(frame: np.ndarray, text: str, position: Tuple = (10, 30),
                     font_scale: float = 1, color: Tuple = (255, 255, 255),
                     thickness: int = 2) -> np.ndarray:
    """Add text to frame"""
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX,
               font_scale, color, thickness)
    return frame

def encode_frame_to_base64(frame: np.ndarray) -> str:
    """Encode frame to base64 for web transmission"""
    import base64
    ret, buffer = cv2.imencode('.jpg', frame)
    frame_data = base64.b64encode(buffer).decode('utf-8')
    return frame_data
