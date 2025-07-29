import dotenv
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Supabase Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'your-supabase-url')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'your-supabase-anon-key')

# Email Configuration
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

# Django Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-jk*&(fo44vsa-n-ab92i53nwp1g(_#p)6bdp8jdusu9+3v2#3a')

# Debug Mode
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Allowed Hosts
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') 