#!/usr/bin/env python3
"""
AI Guardian - Quick Start Guide
Simple example showing how to use the system
"""

# Example 1: Basic Patient Monitoring
# ====================================

def example_basic_monitoring():
    """Simple example of patient monitoring"""
    
    from app.models.patient import PatientSession, HealthMetrics, SafetyMetrics, Alert
    
    # Create a patient session
    session = PatientSession("P001", "John Doe")
    
    # Simulate some metrics
    health_metrics = HealthMetrics(
        heart_rate=85.5,
        breathing_rate=18.2,
        stress_level=0.3,
        tremor_score=0.15
    )
    
    safety_metrics = SafetyMetrics(
        fall_risk=0.1,
        self_harm_risk=0.0,
        aggressive_motion=0.0,
        dangerous_objects=[]
    )
    
    # Update session
    session.update_health_metrics(health_metrics)
    session.update_safety_metrics(safety_metrics)
    
    # Calculate risk
    risk_level = session.calculate_risk_level()
    
    print(f"Patient: {session.patient_name}")
    print(f"Heart Rate: {health_metrics.heart_rate} BPM")
    print(f"Breathing Rate: {health_metrics.breathing_rate} BPM")
    print(f"Risk Level: {risk_level}")

# Example 2: Alert Generation
# ============================

def example_alert_generation():
    """Example of alert generation"""
    
    from app.models.patient import PatientSession, HealthMetrics, SafetyMetrics
    from app.utils.alert_system import AlertSystem
    
    # Create session with concerning metrics
    session = PatientSession("P002", "Jane Smith")
    
    # High heart rate (concerning)
    health_metrics = HealthMetrics(
        heart_rate=145,  # High!
        breathing_rate=22,
        stress_level=0.8
    )
    
    # High fall risk
    safety_metrics = SafetyMetrics(
        fall_risk=0.65,  # Medium-high risk
        dangerous_objects=['knife']  # Dangerous object detected
    )
    
    session.update_health_metrics(health_metrics)
    session.update_safety_metrics(safety_metrics)
    
    # Generate alerts
    alert_system = AlertSystem()
    alerts = alert_system.generate_alerts(session)
    
    print(f"\n🚨 Alerts for {session.patient_name}:")
    for alert in alerts:
        print(f"  [{alert.severity}] {alert.alert_type}: {alert.message}")

# Example 3: Custom Alert Rules
# ==============================

def example_custom_rules():
    """Example of custom alert rules"""
    
    from app.models.patient import Alert, PatientSession, HealthMetrics
    
    session = PatientSession("P003", "Bob Johnson")
    
    # Add custom alert
    custom_alert = Alert(
        alert_type="CUSTOM_PATIENT_ALERT",
        severity="HIGH",
        message="Patient has history of falls - enhanced monitoring",
        details={"patient_flag": "fall_history"}
    )
    
    session.add_alert(custom_alert)
    
    print(f"\nCustom Alert for {session.patient_name}:")
    print(f"  Type: {custom_alert.alert_type}")
    print(f"  Message: {custom_alert.message}")
    print(f"  Severity: {custom_alert.severity}")

# Example 4: Data Logging
# =======================

def example_data_logging():
    """Example of logging patient data"""
    
    from app.models.patient import PatientSession, HealthMetrics
    
    session = PatientSession("P004", "Alice Williams")
    
    # Log multiple readings
    readings = [
        HealthMetrics(heart_rate=75, breathing_rate=16, stress_level=0.1),
        HealthMetrics(heart_rate=78, breathing_rate=17, stress_level=0.15),
        HealthMetrics(heart_rate=82, breathing_rate=18, stress_level=0.2),
        HealthMetrics(heart_rate=88, breathing_rate=19, stress_level=0.25),
    ]
    
    for i, reading in enumerate(readings):
        session.update_health_metrics(reading)
        print(f"Reading {i+1}: HR={reading.heart_rate}, BR={reading.breathing_rate}, Stress={reading.stress_level:.2f}")
    
    print(f"\nTotal readings logged: {len(session.health_metrics_history)}")

# Example 5: Multi-Metric Analysis
# =================================

def example_multi_metric_analysis():
    """Example of analyzing multiple metrics together"""
    
    from app.models.patient import PatientSession, HealthMetrics, SafetyMetrics
    
    session = PatientSession("P005", "Charlie Brown")
    
    # Scenario: Patient with Parkinson's symptoms
    health_metrics = HealthMetrics(
        heart_rate=72,
        breathing_rate=16,
        tremor_score=0.65,  # High tremor = Parkinson's risk
        stress_level=0.4
    )
    
    safety_metrics = SafetyMetrics(
        fall_risk=0.4,  # Higher fall risk with tremor
        aggressive_motion=0.0
    )
    
    session.update_health_metrics(health_metrics)
    session.update_safety_metrics(safety_metrics)
    
    risk_level = session.calculate_risk_level()
    
    print(f"\n🏥 Clinical Analysis for {session.patient_name}:")
    print(f"  Tremor Score: {health_metrics.tremor_score:.2f} (Parkinson's indicator)")
    print(f"  Fall Risk: {safety_metrics.fall_risk:.2f} (elevated)")
    print(f"  Overall Risk: {risk_level}")
    
    # Interpretation
    if health_metrics.tremor_score > 0.6:
        print(f"  → Recommendation: Neurological assessment suggested")
    if safety_metrics.fall_risk > 0.3:
        print(f"  → Recommendation: Fall prevention measures advised")

# Example 6: Dashboard Data Preparation
# ======================================

def example_dashboard_data():
    """Example of preparing data for dashboard display"""
    
    from app.models.patient import PatientSession, HealthMetrics, SafetyMetrics
    import json
    
    session = PatientSession("P006", "Diana Prince")
    
    health_metrics = HealthMetrics(
        heart_rate=80,
        breathing_rate=17,
        stress_level=0.2,
        tremor_score=0.1
    )
    
    safety_metrics = SafetyMetrics(
        fall_risk=0.15,
        self_harm_risk=0.0,
        aggressive_motion=0.0,
        dangerous_objects=[]
    )
    
    session.update_health_metrics(health_metrics)
    session.update_safety_metrics(safety_metrics)
    
    # Prepare for dashboard
    dashboard_data = {
        'patient_id': session.patient_id,
        'patient_name': session.patient_name,
        'risk_level': session.calculate_risk_level(),
        'metrics': {
            'heart_rate': health_metrics.heart_rate,
            'breathing_rate': health_metrics.breathing_rate,
            'stress_level': health_metrics.stress_level,
            'tremor_score': health_metrics.tremor_score,
            'fall_risk': safety_metrics.fall_risk,
            'self_harm_risk': safety_metrics.self_harm_risk,
            'dangerous_objects_count': len(safety_metrics.dangerous_objects)
        },
        'timestamp': health_metrics.timestamp.isoformat()
    }
    
    print(f"\n📊 Dashboard Data:")
    print(json.dumps(dashboard_data, indent=2))

# Main
# ====

if __name__ == '__main__':
    print("=" * 70)
    print("🛡️  AI Guardian - Quick Start Examples")
    print("=" * 70)
    
    examples = [
        ("Basic Monitoring", example_basic_monitoring),
        ("Alert Generation", example_alert_generation),
        ("Custom Rules", example_custom_rules),
        ("Data Logging", example_data_logging),
        ("Multi-Metric Analysis", example_multi_metric_analysis),
        ("Dashboard Data", example_dashboard_data),
    ]
    
    for title, example_func in examples:
        print(f"\n{'=' * 70}")
        print(f"Example: {title}")
        print("=" * 70)
        try:
            example_func()
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'=' * 70}")
    print("✅ Examples completed!")
    print("=" * 70)
