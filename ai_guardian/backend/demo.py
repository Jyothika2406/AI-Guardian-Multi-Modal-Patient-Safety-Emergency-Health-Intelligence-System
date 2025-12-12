#!/usr/bin/env python3
"""
AI Guardian - Demo Script
Demonstrates real-time patient monitoring with all detection modules
"""

import cv2
import argparse
import sys
from app.patient_monitor import PatientMonitor
from app.utils.camera_utils import CameraManager

def main():
    parser = argparse.ArgumentParser(
        description='AI Guardian - Patient Monitoring System'
    )
    parser.add_argument(
        '--camera',
        type=int,
        default=0,
        help='Camera device index (default: 0)'
    )
    parser.add_argument(
        '--patient-id',
        type=str,
        default='P001',
        help='Patient ID (default: P001)'
    )
    parser.add_argument(
        '--patient-name',
        type=str,
        default='Demo Patient',
        help='Patient name (default: Demo Patient)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=30,
        help='Target FPS (default: 30)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run without displaying video'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🛡️  AI GUARDIAN - Multi-Modal Patient Safety & Health Monitoring")
    print("=" * 70)
    
    # Initialize monitor
    print(f"\n📋 Initializing patient session...")
    monitor = PatientMonitor(
        patient_id=args.patient_id,
        patient_name=args.patient_name
    )
    
    # Initialize camera
    print(f"📷 Initializing camera (index: {args.camera})...")
    camera_manager = CameraManager(
        camera_index=args.camera,
        width=640,
        height=480,
        fps=args.fps
    )
    
    if not camera_manager.initialize():
        print("❌ Failed to initialize camera. Exiting.")
        return 1
    
    print("✅ Camera initialized successfully")
    print("\n" + "=" * 70)
    print("MONITORING ACTIVE - Press 'Q' to exit, 'S' to show summary")
    print("=" * 70 + "\n")
    
    frame_count = 0
    
    try:
        while True:
            # Read frame
            frame = camera_manager.read_frame()
            if frame is None:
                print("⚠️  Failed to read frame")
                break
            
            frame_count += 1
            
            # Create new monitor for each frame
            result = monitor.process_frame(frame)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue
            
            # Get processed frame
            processed_frame = result.get('frame', frame)
            
            # Display frame
            if not args.headless:
                cv2.imshow('AI Guardian - Patient Monitoring', processed_frame)
            
            # Print metrics every 30 frames
            if frame_count % 30 == 0:
                summary = monitor.get_session_summary()
                print(f"\n📊 Frame {frame_count} | Patient: {summary['patient_name']}")
                print(f"   Risk Level: {summary['risk_level']}")
                print(f"   Heart Rate: {summary['current_metrics']['health']['heart_rate']:.0f} BPM")
                print(f"   Breathing Rate: {summary['current_metrics']['health']['breathing_rate']:.1f} BPM")
                print(f"   Tremor Score: {summary['current_metrics']['health']['tremor_score']:.2f}")
                print(f"   Fall Risk: {summary['current_metrics']['safety']['fall_risk']:.2f}")
                print(f"   Stress Level: {summary['current_metrics']['health']['stress_level']:.2f}")
                print(f"   Active Alerts: {summary['current_alerts']}")
            
            # Print alerts
            if monitor.patient_session.current_alerts:
                for alert in monitor.patient_session.current_alerts:
                    icon = "🔴" if alert.severity == "CRITICAL" else "🟠" if alert.severity == "HIGH" else "🟡"
                    print(f"{icon} [{alert.severity}] {alert.alert_type}: {alert.message}")
            
            # Handle key press
            if not args.headless:
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    print("\n⏹️  Monitoring stopped by user")
                    break
                elif key == ord('s') or key == ord('S'):
                    summary = monitor.get_session_summary()
                    print_summary(summary)
    
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring interrupted")
    
    except Exception as e:
        print(f"\n❌ Error during monitoring: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        camera_manager.release()
        cv2.destroyAllWindows()
        
        # Print final summary
        print("\n" + "=" * 70)
        print("SESSION SUMMARY")
        print("=" * 70)
        summary = monitor.get_session_summary()
        print_summary(summary)
        
        print("\n✅ AI Guardian monitoring session completed")
        print("=" * 70)
    
    return 0

def print_summary(summary):
    """Print session summary"""
    print(f"\n📋 Patient: {summary['patient_name']} (ID: {summary['patient_id']})")
    print(f"📊 Frames Processed: {summary['frames_processed']}")
    print(f"🔴 Total Alerts: {summary['total_alerts']}")
    print(f"\n⚠️  Overall Risk Level: {summary['risk_level']}")
    
    print(f"\n❤️  Health Metrics (Latest):")
    health = summary['current_metrics']['health']
    print(f"   • Heart Rate: {health['heart_rate']:.0f} BPM")
    print(f"   • Breathing Rate: {health['breathing_rate']:.1f} BPM")
    print(f"   • Stress Level: {health['stress_level']:.2f}")
    print(f"   • Tremor Score: {health['tremor_score']:.2f}")
    
    print(f"\n🚨 Safety Metrics (Latest):")
    safety = summary['current_metrics']['safety']
    print(f"   • Fall Risk: {safety['fall_risk']:.2f}")
    print(f"   • Self-Harm Risk: {safety['self_harm_risk']:.2f}")
    print(f"   • Aggression: {safety['aggressive_motion']:.2f}")
    print(f"   • Dangerous Objects: {safety['dangerous_objects']}")

if __name__ == '__main__':
    sys.exit(main())
