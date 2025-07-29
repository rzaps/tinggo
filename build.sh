#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies and build Tailwind CSS
cd theme/static_src
npm install
npm run build
cd ../..

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Make sure the script is executable
chmod +x build.sh 