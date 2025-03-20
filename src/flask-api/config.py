"""
Configuration settings for the application.
"""
import os

class Config:
    """Base configuration class."""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Model settings
    MODEL_PATH = os.environ.get('MODEL_PATH') or 'app/models/model.pkl'
    
    # Network flow analysis settings
    IDLE_THRESHOLD = 500000  # Microseconds (1 second) to consider a gap as "idle"
    PREDICTION_THRESHOLD = 0.05  # Probability threshold to classify as an attack