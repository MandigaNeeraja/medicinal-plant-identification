import os
from backend.app import create_app

config_name = os.getenv('FLASK_ENV', 'development')
if os.getenv('RENDER'):
    config_name = 'production'

app = create_app(config_name)
