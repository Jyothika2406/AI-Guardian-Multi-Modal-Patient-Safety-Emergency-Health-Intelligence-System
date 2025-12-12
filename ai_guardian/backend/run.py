import os
import sys
from dotenv import load_dotenv

load_dotenv()

from app import app, socketio
from app.config.settings import DevelopmentConfig, ProductionConfig

# Set configuration
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig())
else:
    app.config.from_object(DevelopmentConfig())

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = app.config['DEBUG']
    
    print(f"🛡️  AI Guardian Starting on port {port}...")
    print(f"Dashboard: http://localhost:{port}/dashboard")
    print(f"API: http://localhost:{port}/")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
