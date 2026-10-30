import sys
import os

# Add root folder to sys.path so app can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel entrypoint: app is exported as WSGI application

