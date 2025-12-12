from flask import Blueprint, jsonify
from app.models.patient import PatientSession
from app.utils.camera_utils import encode_frame_to_base64
from app.patient_monitor import PatientMonitor
import json
import threading
import time

main_bp = Blueprint('main', __name__)
camera_bp = Blueprint('camera', __name__, url_prefix='/api/camera')

# Global session for demo
current_session: PatientSession = None
current_frame = None
monitoring_active = False
monitor_thread = None
patient_monitor: PatientMonitor = None

def start_monitoring_thread():
    """Start the monitoring thread that processes frames continuously"""
    global monitoring_active, monitor_thread, current_session, current_frame, patient_monitor
    
    if monitoring_active:
        return
    
    monitoring_active = True
    
    def monitor():
        global current_session, current_frame, patient_monitor
        while monitoring_active:
            try:
                if patient_monitor is None:
                    patient_monitor = PatientMonitor()
                    if not patient_monitor.initialize_camera():
                        print('⚠️ Camera initialization failed')
                        break
                
                # Process frame
                result = patient_monitor.process_frame()
                if 'error' in result:
                    continue
                
                # Update global session
                current_session = patient_monitor.patient_session
                current_frame = result.get('frame')
                
                time.sleep(0.05)  # ~20 FPS
            except Exception as e:
                print(f'Monitoring error: {e}')
                time.sleep(0.1)
    
    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()
    print('✓ Monitoring thread started')

@main_bp.route('/')
def home():
    """Home page"""
    return jsonify({
        'message': 'AI Guardian API',
        'version': '1.0',
        'endpoints': {
            'dashboard': '/dashboard',
            'api': {
                'status': '/api/status',
                'session': '/api/session',
                'alerts': '/api/alerts',
                'metrics': '/api/metrics'
            }
        }
    })

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Guardian Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1a1a; color: #fff; }
            .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            .header h1 { font-size: 2.5em; color: #00d4ff; margin-bottom: 10px; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .card { background: #2a2a2a; border: 2px solid #00d4ff; border-radius: 10px; padding: 20px; }
            .card h2 { color: #00d4ff; margin-bottom: 15px; font-size: 1.3em; }
            .video-container { position: relative; width: 100%; padding-bottom: 75%; background: #000; border-radius: 5px; overflow: hidden; }
            .video-container img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }
            .metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
            .metric { background: #1a1a1a; padding: 10px; border-radius: 5px; border-left: 3px solid #00d4ff; }
            .metric-label { font-size: 0.85em; color: #aaa; }
            .metric-value { font-size: 1.5em; font-weight: bold; color: #00d4ff; margin-top: 5px; }
            .alert { background: #1a1a1a; padding: 10px; margin: 5px 0; border-left: 3px solid #ff4444; border-radius: 3px; }
            .alert.high { border-left-color: #ff8800; }
            .alert.medium { border-left-color: #ffff00; }
            .alert.low { border-left-color: #00ff00; }
            .risk-badge { display: inline-block; padding: 5px 10px; border-radius: 20px; font-weight: bold; }
            .risk-critical { background: #ff0000; }
            .risk-high { background: #ff8800; }
            .risk-medium { background: #ffff00; color: #000; }
            .risk-low { background: #00ff00; color: #000; }
            .risk-safe { background: #00aa00; }
            @media (max-width: 1024px) { .grid { grid-template-columns: 1fr; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ AI Guardian</h1>
                <p>Multi-Modal Patient Safety & Health Monitoring System</p>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h2>Live Feed</h2>
                    <div class="video-container">
                        <img id="videoFeed" src="" alt="Live Feed">
                    </div>
                </div>
                
                <div class="card">
                    <h2>Health Metrics</h2>
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-label">Heart Rate</div>
                            <div class="metric-value" id="heartRate">-- BPM</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Breathing Rate</div>
                            <div class="metric-value" id="breathingRate">-- BPM</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Stress Level</div>
                            <div class="metric-value" id="stressLevel">--</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Tremor Score</div>
                            <div class="metric-value" id="tremorScore">--</div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>Safety Metrics</h2>
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-label">Fall Risk</div>
                            <div class="metric-value" id="fallRisk">--</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Self-Harm Risk</div>
                            <div class="metric-value" id="selfHarmRisk">--</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Aggression</div>
                            <div class="metric-value" id="aggression">--</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Risk Level</div>
                            <div class="metric-value" id="riskLevel">SAFE</div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>Active Alerts</h2>
                    <div id="alertsList"></div>
                </div>
            </div>
        </div>
        
        <script>
            function updateDashboard() {
                fetch('/api/status')
                    .then(r => r.json())
                    .then(data => {
                        if (data.frame) {
                            document.getElementById('videoFeed').src = 'data:image/jpeg;base64,' + data.frame;
                        }
                        if (data.metrics) {
                            const m = data.metrics;
                            document.getElementById('heartRate').textContent = (m.heart_rate || 0).toFixed(0) + ' BPM';
                            document.getElementById('breathingRate').textContent = (m.breathing_rate || 0).toFixed(0) + ' BPM';
                            document.getElementById('stressLevel').textContent = (m.stress_level || 0).toFixed(2);
                            document.getElementById('tremorScore').textContent = (m.tremor_score || 0).toFixed(2);
                            document.getElementById('fallRisk').textContent = (m.fall_risk || 0).toFixed(2);
                            document.getElementById('selfHarmRisk').textContent = (m.self_harm_risk || 0).toFixed(2);
                            document.getElementById('aggression').textContent = (m.aggressive_motion || 0).toFixed(2);
                            
                            const riskLevel = data.risk_level || 'SAFE';
                            const riskBadge = document.getElementById('riskLevel');
                            riskBadge.textContent = riskLevel;
                            riskBadge.className = 'metric-value risk-badge risk-' + riskLevel.toLowerCase();
                        }
                        if (data.alerts) {
                            const alertsList = document.getElementById('alertsList');
                            alertsList.innerHTML = data.alerts.length > 0 
                                ? data.alerts.map(a => `<div class="alert ${a.severity.toLowerCase()}">
                                    <strong>${a.alert_type}:</strong> ${a.message}
                                  </div>`).join('')
                                : '<div style="color: #00ff00;">✓ No active alerts</div>';
                        }
                    });
            }
            
            // Auto-start camera on page load
            fetch('/api/camera/start', { method: 'POST' })
                .then(r => r.json())
                .then(d => console.log('Camera started:', d))
                .catch(e => console.error('Camera start error:', e));
            
            // Update dashboard every 200ms for real-time view
            setInterval(updateDashboard, 200);
            updateDashboard();
        </script>
    </body>
    </html>
    '''

@main_bp.route('/api/status')
def get_status():
    """Get current system status"""
    global current_session, current_frame
    
    if current_session is None:
        return jsonify({
            'status': 'offline',
            'message': 'No active session'
        })
    
    frame_base64 = None
    if current_frame is not None:
        try:
            frame_base64 = encode_frame_to_base64(current_frame)
        except:
            frame_base64 = None
    
    return jsonify({
        'status': 'active',
        'patient_id': current_session.patient_id,
        'patient_name': current_session.patient_name,
        'risk_level': current_session.risk_level,
        'metrics': {
            'heart_rate': current_session.current_health_metrics.heart_rate,
            'breathing_rate': current_session.current_health_metrics.breathing_rate,
            'stress_level': current_session.current_health_metrics.stress_level,
            'tremor_score': current_session.current_health_metrics.tremor_score,
            'fall_risk': current_session.current_safety_metrics.fall_risk,
            'self_harm_risk': current_session.current_safety_metrics.self_harm_risk,
            'aggressive_motion': current_session.current_safety_metrics.aggressive_motion,
        },
        'alerts': [
            {
                'alert_type': a.alert_type,
                'severity': a.severity,
                'message': a.message,
                'timestamp': a.timestamp.isoformat()
            } for a in current_session.current_alerts
        ],
        'frame': frame_base64
    })

@camera_bp.route('/start', methods=['POST'])
def start_camera():
    """Start camera monitoring"""
    global current_session, patient_monitor, monitoring_active
    
    if not monitoring_active:
        start_monitoring_thread()
    
    return jsonify({'status': 'success', 'message': 'Camera monitoring started'})

@camera_bp.route('/stop', methods=['POST'])
def stop_camera():
    """Stop camera monitoring"""
    global current_session, monitoring_active, patient_monitor
    monitoring_active = False
    current_session = None
    if patient_monitor:
        patient_monitor.camera_manager.release()
    
    return jsonify({'status': 'success', 'message': 'Camera monitoring stopped'})
