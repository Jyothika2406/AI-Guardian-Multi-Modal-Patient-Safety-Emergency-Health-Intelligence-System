from typing import List, Dict
from datetime import datetime
from app.models.patient import Alert, PatientSession

class AlertSystem:
    """Manages alert generation and filtering"""
    
    def __init__(self, max_alerts_per_type: int = 5):
        self.max_alerts_per_type = max_alerts_per_type
        self.alert_cooldown = {}  # Prevent duplicate alerts
        
    def generate_alerts(self, session: PatientSession) -> List[Alert]:
        """Generate alerts based on current metrics"""
        alerts = []
        
        # Check safety metrics
        safety_alerts = self._check_safety_metrics(session)
        alerts.extend(safety_alerts)
        
        # Check health metrics
        health_alerts = self._check_health_metrics(session)
        alerts.extend(health_alerts)
        
        return alerts
    
    def _check_safety_metrics(self, session: PatientSession) -> List[Alert]:
        """Check safety-related metrics"""
        alerts = []
        metrics = session.current_safety_metrics
        
        # Fall detection
        if metrics.fall_risk > 0.7:
            alerts.append(Alert(
                alert_type='FALL_CRITICAL',
                severity='CRITICAL',
                message='CRITICAL: Fall detected or imminent!',
                details={'fall_risk': metrics.fall_risk}
            ))
        elif metrics.fall_risk > 0.5:
            alerts.append(Alert(
                alert_type='FALL_WARNING',
                severity='HIGH',
                message='WARNING: Patient at risk of falling',
                details={'fall_risk': metrics.fall_risk}
            ))
        
        # Self-harm detection
        if metrics.self_harm_risk > 0.7:
            alerts.append(Alert(
                alert_type='SELF_HARM_CRITICAL',
                severity='CRITICAL',
                message='CRITICAL: Potential self-harm detected!',
                details={'self_harm_risk': metrics.self_harm_risk}
            ))
        elif metrics.self_harm_risk > 0.4:
            alerts.append(Alert(
                alert_type='SELF_HARM_WARNING',
                severity='HIGH',
                message='WARNING: Self-harm risk detected',
                details={'self_harm_risk': metrics.self_harm_risk}
            ))
        
        # Aggressive motion
        if metrics.aggressive_motion > 0.6:
            alerts.append(Alert(
                alert_type='AGGRESSIVE_MOTION',
                severity='HIGH',
                message='WARNING: Aggressive motion detected',
                details={'aggression_score': metrics.aggressive_motion}
            ))
        
        # Dangerous objects
        if metrics.dangerous_objects:
            alerts.append(Alert(
                alert_type='DANGEROUS_OBJECT',
                severity='CRITICAL',
                message=f'CRITICAL: Dangerous object detected: {", ".join(metrics.dangerous_objects)}',
                details={'objects': metrics.dangerous_objects}
            ))
        
        return alerts
    
    def _check_health_metrics(self, session: PatientSession) -> List[Alert]:
        """Check health-related metrics"""
        alerts = []
        metrics = session.current_health_metrics
        
        # Heart rate abnormalities
        if metrics.heart_rate > 140:
            alerts.append(Alert(
                alert_type='HIGH_HEART_RATE',
                severity='HIGH',
                message=f'WARNING: High heart rate detected: {metrics.heart_rate:.0f} BPM',
                details={'heart_rate': metrics.heart_rate}
            ))
        elif metrics.heart_rate > 0 and metrics.heart_rate < 50:
            alerts.append(Alert(
                alert_type='LOW_HEART_RATE',
                severity='HIGH',
                message=f'WARNING: Low heart rate detected: {metrics.heart_rate:.0f} BPM',
                details={'heart_rate': metrics.heart_rate}
            ))
        
        # Tremor detection (Parkinson's indication)
        if metrics.tremor_score > 0.7:
            alerts.append(Alert(
                alert_type='TREMOR_DETECTED',
                severity='MEDIUM',
                message='ALERT: Significant tremor detected (Parkinson\'s risk)',
                details={'tremor_score': metrics.tremor_score}
            ))
        
        # Stress level
        if metrics.stress_level > 0.8:
            alerts.append(Alert(
                alert_type='HIGH_STRESS',
                severity='MEDIUM',
                message='ALERT: High stress level detected',
                details={'stress_level': metrics.stress_level}
            ))
        
        return alerts
    
    def filter_and_deduplicate(self, alerts: List[Alert]) -> List[Alert]:
        """Remove duplicate/similar alerts"""
        filtered = []
        alert_types_seen = set()
        
        for alert in alerts:
            if alert.alert_type not in alert_types_seen:
                filtered.append(alert)
                alert_types_seen.add(alert.alert_type)
        
        return filtered[:self.max_alerts_per_type]
