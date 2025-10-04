#!/bin/bash

# GetOut FastAPI Backend - Kudu Deployment Script
# Führe diesen Command in der Kudu Bash Console aus

echo "=== GetOut FastAPI Backend Deployment ==="

# 1. Cleanup alte Installation
echo "Cleaning up old installation..."
rm -rf /home/site/wwwroot/.python_packages
mkdir -p /home/site/wwwroot/.python_packages/lib/site-packages

# 2. Navigiere zum wwwroot Verzeichnis
cd /home/site/wwwroot

# 3. Erstelle Verzeichnisstruktur falls nicht vorhanden
echo "Creating directory structure..."
mkdir -p app

# 4. Installiere Dependencies
echo "Installing Python dependencies..."
python3 -m pip install --disable-pip-version-check --no-cache-dir \
  -r requirements.txt \
  -t .python_packages/lib/site-packages

# 5. Setze PYTHONPATH
export PYTHONPATH=/home/site/wwwroot/.python_packages/lib/site-packages

# 6. Teste die Installation
echo "Testing installation..."
python3 -c "
import sys
sys.path.insert(0, '/home/site/wwwroot/.python_packages/lib/site-packages')
try:
    import fastapi
    import uvicorn
    import gunicorn
    import sqlalchemy
    import jose
    import passlib
    print('✅ All dependencies installed successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

# 7. Teste App Import
echo "Testing app import..."
python3 -c "
import sys
sys.path.insert(0, '/home/site/wwwroot/.python_packages/lib/site-packages')
sys.path.insert(0, '/home/site/wwwroot')
try:
    from app.main import app
    print('✅ App imported successfully')
except Exception as e:
    print(f'❌ App import error: {e}')
    sys.exit(1)
"

# 8. Teste Health Endpoint (falls Server läuft)
echo "Testing health endpoint..."
curl -s http://localhost:8000/health || echo "Server not running yet - this is normal"

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Next steps:"
echo "1. Set Azure App Settings:"
echo "   - SECRET_KEY=your-secret-key-here"
echo "   - WEBSITES_HEALTHCHECK_PATH=/health"
echo ""
echo "2. Configure Startup Command:"
echo "   python3 -m pip install --disable-pip-version-check --no-cache-dir -r /home/site/wwwroot/requirements.txt -t /home/site/wwwroot/.python_packages/lib/site-packages && PYTHONPATH=/home/site/wwwroot/.python_packages/lib/site-packages gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 120"
echo ""
echo "3. Test endpoints after restart:"
echo "   curl https://yourapp.azurewebsites.net/health"
echo "   curl https://yourapp.azurewebsites.net/"
echo ""
