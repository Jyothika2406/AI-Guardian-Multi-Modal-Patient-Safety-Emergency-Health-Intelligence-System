import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    
    # Camera settings
    CAMERA_INDEX = 0
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    FPS = 30
    
    # Alert thresholds
    FALL_CONFIDENCE_THRESHOLD = 0.6
    TREMOR_THRESHOLD = 0.3
    OBJECT_DETECTION_THRESHOLD = 0.5
    HEART_RATE_MIN = 40
    HEART_RATE_MAX = 150
    BREATHING_RATE_MIN = 8
    BREATHING_RATE_MAX = 25
    
    # Model paths
    YOLO_MODEL_PATH = 'models/yolov8n.pt'
    
    # Alert levels
    ALERT_LEVELS = {
        'CRITICAL': 0,
        'HIGH': 1,
        'MEDIUM': 2,
        'LOW': 3,
        'SAFE': 4
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
