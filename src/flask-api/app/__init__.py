"""
Flask application factory.
"""
from flask import Flask
from config import Config

def create_app(config_class=Config):
    """
    Create and configure the Flask application.
    
    Args:
        config_class: Configuration class for the application
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    from app.routes.prediction_routes import prediction_bp
    app.register_blueprint(prediction_bp)
    
    return app