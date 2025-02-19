"""
This configuration file contains many working settings tailored for the Flask application.
You can adjust these values as needed.
"""

import os

class Config:
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    TESTING = os.getenv('TESTING', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    # Model settings
    GPT_MODEL = os.getenv('GPT_MODEL', 'gpt-4')
    USE_G4F = os.getenv('USE_G4F', 'True') == 'True'
    
    # Additional application settings can be added here
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
