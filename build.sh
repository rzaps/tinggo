#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Node.js is available
if command -v node &> /dev/null; then
    echo "📦 Node.js found, building Tailwind CSS..."
    # Install Node.js dependencies and build Tailwind CSS
    cd theme/static_src
    npm install
    npm run build
    cd ../..
    echo "✅ Tailwind CSS built successfully"
else
    echo "⚠️  Node.js not found, skipping Tailwind build"
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️  Running migrations..."
python manage.py migrate

echo "✅ Build completed successfully!" 