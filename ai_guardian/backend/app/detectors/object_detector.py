import cv2
import numpy as np
from typing import List, Tuple, Dict

class ObjectDetector:
    """Detects dangerous objects using YOLO"""
    
    def __init__(self, model_path: str = None):
        try:
            from ultralytics import YOLO
            self.yolo_available = True
            # Try to load model, fallback to nano if full model not available
            try:
                self.model = YOLO(model_path or 'yolov8n.pt')
            except:
                self.model = YOLO('yolov8n.pt')
        except ImportError:
            self.yolo_available = False
            self.model = None
        
        # Dangerous objects to detect
        self.dangerous_objects = ['knife', 'scissors', 'gun', 'weapon', 'bottle']
        self.confidence_threshold = 0.5
        
    def detect_objects(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """Detect objects in frame"""
        detected_objects = {
            'dangerous_objects': [],
            'all_detections': [],
            'has_danger': False
        }
        
        if not self.yolo_available or self.model is None:
            return frame, detected_objects
        
        try:
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            if results and len(results) > 0:
                result = results[0]
                
                if result.boxes is not None:
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        class_name = result.names[class_id]
                        confidence = float(box.conf[0])
                        
                        detection = {
                            'class': class_name,
                            'confidence': confidence,
                            'bbox': box.xyxy[0].tolist()
                        }
                        
                        detected_objects['all_detections'].append(detection)
                        
                        # Check if it's a dangerous object
                        if any(danger in class_name.lower() for danger in self.dangerous_objects):
                            detected_objects['dangerous_objects'].append(detection)
                            detected_objects['has_danger'] = True
                            
            # Draw detections
            frame = self._draw_detections(frame, detected_objects)
            
        except Exception as e:
            print(f"Error in object detection: {e}")
        
        return frame, detected_objects
    
    def _draw_detections(self, frame: np.ndarray, detections: Dict) -> np.ndarray:
        """Draw detection boxes on frame"""
        # Draw dangerous objects in red
        for detection in detections['dangerous_objects']:
            bbox = detection['bbox']
            x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            label = f"{detection['class']}: {detection['confidence']:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        # Draw other objects in green
        for detection in detections['all_detections']:
            if detection not in detections['dangerous_objects']:
                bbox = detection['bbox']
                x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
        
        return frame
