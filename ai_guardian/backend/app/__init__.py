from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)
    CORS(app)
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Register blueprints
    from app.routes import main_bp, camera_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(camera_bp)
    
    return app, socketio

app, socketio = create_app()
