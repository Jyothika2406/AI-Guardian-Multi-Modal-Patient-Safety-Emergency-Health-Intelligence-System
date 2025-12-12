from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime

@dataclass
class Alert:
    """Alert data structure"""
    alert_type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict = field(default_factory=dict)

@dataclass
class HealthMetrics:
    """Health metrics for a patient"""
    heart_rate: float = 0
    breathing_rate: float = 0
    stress_level: float = 0
    tremor_score: float = 0
    skin_color_risk: str = "NORMAL"
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class SafetyMetrics:
    """Safety metrics for a patient"""
    fall_risk: float = 0
    self_harm_risk: float = 0
    aggressive_motion: float = 0
    dangerous_objects: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

class PatientSession:
    """Patient monitoring session"""
    def __init__(self, patient_id: str, patient_name: str):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.session_start = datetime.now()
        self.health_metrics_history: List[HealthMetrics] = []
        self.safety_metrics_history: List[SafetyMetrics] = []
        self.alerts_history: List[Alert] = []
        self.current_health_metrics = HealthMetrics()
        self.current_safety_metrics = SafetyMetrics()
        self.current_alerts: List[Alert] = []
        self.risk_level = "SAFE"
        
    def add_alert(self, alert: Alert):
        """Add alert to history and current alerts"""
        self.alerts_history.append(alert)
        self.current_alerts.append(alert)
        
    def update_health_metrics(self, metrics: HealthMetrics):
        """Update health metrics"""
        self.current_health_metrics = metrics
        self.health_metrics_history.append(metrics)
        
    def update_safety_metrics(self, metrics: SafetyMetrics):
        """Update safety metrics"""
        self.current_safety_metrics = metrics
        self.safety_metrics_history.append(metrics)
        
    def calculate_risk_level(self) -> str:
        """Calculate overall risk level"""
        if (self.current_safety_metrics.fall_risk > 0.8 or 
            self.current_safety_metrics.self_harm_risk > 0.8 or
            self.current_health_metrics.heart_rate > 150 or
            self.current_health_metrics.heart_rate < 40):
            return "CRITICAL"
        elif (self.current_safety_metrics.fall_risk > 0.6 or
              self.current_safety_metrics.self_harm_risk > 0.6 or
              self.current_health_metrics.tremor_score > 0.7):
            return "HIGH"
        elif (self.current_safety_metrics.fall_risk > 0.4 or
              self.current_health_metrics.tremor_score > 0.5 or
              len(self.current_safety_metrics.dangerous_objects) > 0):
            return "MEDIUM"
        elif self.current_safety_metrics.fall_risk > 0.2:
            return "LOW"
        else:
            return "SAFE"
