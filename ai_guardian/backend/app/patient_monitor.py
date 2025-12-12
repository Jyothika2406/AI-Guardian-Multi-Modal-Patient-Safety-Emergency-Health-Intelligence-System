import cv2
import numpy as np
from typing import Optional, Dict, List
from app.detectors.pose_detector import PoseDetector
from app.detectors.object_detector import ObjectDetector
from app.detectors.tremor_detector import TremorDetector
from app.detectors.heart_rate_detector import HeartRateDetector
from app.detectors.breathing_detector import BreathingDetector
from app.detectors.health_color_detector import HealthColorDetector
from app.models.patient import HealthMetrics, SafetyMetrics, PatientSession
from app.utils.alert_system import AlertSystem
from app.utils.camera_utils import CameraManager

class PatientMonitor:
    """Main monitoring system that orchestrates all detectors"""
    
    def __init__(self, patient_id: str = 'P001', patient_name: str = 'Patient'):
        self.patient_session = PatientSession(patient_id, patient_name)
        
        # Initialize detectors
        self.pose_detector = PoseDetector()
        self.object_detector = ObjectDetector()
        self.tremor_detector = TremorDetector()
        self.heart_rate_detector = HeartRateDetector()
        self.breathing_detector = BreathingDetector()
        self.health_color_detector = HealthColorDetector()
        self.alert_system = AlertSystem()
        
        # Camera manager
        self.camera_manager = CameraManager()
        
        # Frame tracking
        self.prev_pose_landmarks = None
        self.frame_count = 0
        
    def initialize_camera(self) -> bool:
        """Initialize camera"""
        return self.camera_manager.initialize()
    
    def process_frame(self, frame: Optional[np.ndarray] = None) -> Dict:
        """Process a single frame and update patient metrics"""
        
        # Read frame if not provided
        if frame is None:
            frame = self.camera_manager.read_frame()
            if frame is None:
                return {'error': 'Failed to read frame'}
        
        self.frame_count += 1
        result = {
            'frame_number': self.frame_count,
            'status': 'processing',
            'detections': {}
        }
        
        # Pose detection
        frame_pose, pose_data = self.pose_detector.detect_pose(frame)
        result['detections']['pose'] = pose_data
        
        if pose_data['landmarks']:
            # Safety analysis
            fall_risk = self.pose_detector.detect_fall_risk(pose_data['landmarks'])
            self_harm_risk = self.pose_detector.detect_self_harm_risk(pose_data['landmarks'])
            aggressive_motion = self.pose_detector.detect_aggressive_motion(
                pose_data['landmarks'], self.prev_pose_landmarks
            )
            
            self.prev_pose_landmarks = pose_data['landmarks']
            
            # Tremor detection
            tremor_data = self.tremor_detector.detect_tremor(frame)
            result['detections']['tremor'] = tremor_data
            
            # Object detection
            frame_obj, obj_data = self.object_detector.detect_objects(frame)
            result['detections']['objects'] = obj_data
            
            # Health detectors
            heart_rate_data = self.heart_rate_detector.detect_heart_rate(frame)
            result['detections']['heart_rate'] = heart_rate_data
            
            breathing_data = self.breathing_detector.detect_breathing(frame)
            result['detections']['breathing'] = breathing_data
            
            health_color_data = self.health_color_detector.detect_health_indicators(frame)
            result['detections']['health_color'] = health_color_data
            
            # Update patient metrics
            health_metrics = HealthMetrics(
                heart_rate=heart_rate_data.get('heart_rate', 0),
                breathing_rate=breathing_data.get('breathing_rate', 0),
                stress_level=heart_rate_data.get('stress_level', 0),
                tremor_score=tremor_data.get('tremor_score', 0),
                skin_color_risk=health_color_data.get('skin_color_status', 'NORMAL')
            )
            
            safety_metrics = SafetyMetrics(
                fall_risk=fall_risk,
                self_harm_risk=self_harm_risk,
                aggressive_motion=aggressive_motion,
                dangerous_objects=obj_data.get('dangerous_objects', [])
            )
            
            self.patient_session.update_health_metrics(health_metrics)
            self.patient_session.update_safety_metrics(safety_metrics)
            
            # Update risk level
            self.patient_session.risk_level = self.patient_session.calculate_risk_level()
            
            # Generate alerts
            new_alerts = self.alert_system.generate_alerts(self.patient_session)
            new_alerts = self.alert_system.filter_and_deduplicate(new_alerts)
            
            # Update current alerts (keep last 5)
            self.patient_session.current_alerts = new_alerts[-5:]
            
            # Add new alerts to history
            for alert in new_alerts:
                self.patient_session.add_alert(alert)
            
            result['status'] = 'success'
        
        # Draw visualizations
        frame = self._draw_visualizations(frame, result)
        result['frame'] = frame
        
        return result
    
    def _draw_visualizations(self, frame: np.ndarray, detection_result: Dict) -> np.ndarray:
        """Draw detection results on frame"""
        h, w = frame.shape[:2]
        
        # Draw risk level in corner
        risk_level = self.patient_session.risk_level
        color_map = {
            'CRITICAL': (0, 0, 255),
            'HIGH': (0, 165, 255),
            'MEDIUM': (0, 255, 255),
            'LOW': (0, 255, 0),
            'SAFE': (0, 255, 0)
        }
        color = color_map.get(risk_level, (255, 255, 255))
        
        cv2.rectangle(frame, (w - 200, 10), (w - 10, 60), color, -1)
        cv2.putText(frame, f"RISK: {risk_level}", (w - 190, 45),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Draw metrics
        y_offset = 30
        metrics_text = [
            f"HR: {self.patient_session.current_health_metrics.heart_rate:.0f} BPM",
            f"BR: {self.patient_session.current_health_metrics.breathing_rate:.0f} BPM",
            f"Fall: {self.patient_session.current_safety_metrics.fall_risk:.2f}",
            f"Tremor: {self.patient_session.current_health_metrics.tremor_score:.2f}"
        ]
        
        for text in metrics_text:
            cv2.putText(frame, text, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            y_offset += 25
        
        # Draw active alerts
        if self.patient_session.current_alerts:
            alert_y = y_offset + 10
            for alert in self.patient_session.current_alerts[:3]:
                alert_color = (0, 0, 255) if alert.severity == 'CRITICAL' else (0, 165, 255)
                cv2.putText(frame, f"⚠ {alert.alert_type}", (10, alert_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, alert_color, 1)
                alert_y += 20
        
        return frame
    
    def release(self):
        """Release resources"""
        self.camera_manager.release()
    
    def get_session_summary(self) -> Dict:
        """Get session summary"""
        return {
            'patient_id': self.patient_session.patient_id,
            'patient_name': self.patient_session.patient_name,
            'risk_level': self.patient_session.risk_level,
            'frames_processed': self.frame_count,
            'total_alerts': len(self.patient_session.alerts_history),
            'current_alerts': len(self.patient_session.current_alerts),
            'current_metrics': {
                'health': {
                    'heart_rate': self.patient_session.current_health_metrics.heart_rate,
                    'breathing_rate': self.patient_session.current_health_metrics.breathing_rate,
                    'stress_level': self.patient_session.current_health_metrics.stress_level,
                    'tremor_score': self.patient_session.current_health_metrics.tremor_score,
                },
                'safety': {
                    'fall_risk': self.patient_session.current_safety_metrics.fall_risk,
                    'self_harm_risk': self.patient_session.current_safety_metrics.self_harm_risk,
                    'aggressive_motion': self.patient_session.current_safety_metrics.aggressive_motion,
                    'dangerous_objects': len(self.patient_session.current_safety_metrics.dangerous_objects),
                }
            }
        }
