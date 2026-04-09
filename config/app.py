"""
Application configuration for production deployment.
This file can be used by application servers like Gunicorn or uWSGI.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# WSGI application
application = get_wsgi_application()

# Application name for server configuration
app = application
