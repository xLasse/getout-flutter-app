# Kudu Bash Commands für GetOut Backend

## One-Liner Deployment Command

Kopiere und führe diesen Command in der Kudu Bash Console aus:

```bash
cd /home/site/wwwroot && rm -rf .python_packages && mkdir -p .python_packages/lib/site-packages && python3 -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt -t .python_packages/lib/site-packages && export PYTHONPATH=/home/site/wwwroot/.python_packages/lib/site-packages && python3 -c "import sys; sys.path.insert(0, '/home/site/wwwroot/.python_packages/lib/site-packages'); import fastapi, uvicorn, gunicorn, sqlalchemy, jose, passlib; print('✅ Dependencies OK')" && python3 -c "import sys; sys.path.insert(0, '/home/site/wwwroot/.python_packages/lib/site-packages'); sys.path.insert(0, '/home/site/wwwroot'); from app.main import app; print('✅ App import OK')" && echo "🚀 Deployment successful!"
```

## Schritt-für-Schritt Commands

Falls der One-Liner nicht funktioniert, führe diese Commands einzeln aus:

### 1. Cleanup und Setup
```bash
cd /home/site/wwwroot
rm -rf .python_packages
mkdir -p .python_packages/lib/site-packages
```

### 2. Dependencies installieren
```bash
python3 -m pip install --disable-pip-version-check --no-cache-dir \
  -r requirements.txt \
  -t .python_packages/lib/site-packages
```

### 3. PYTHONPATH setzen
```bash
export PYTHONPATH=/home/site/wwwroot/.python_packages/lib/site-packages
```

### 4. Dependencies testen
```bash
python3 -c "
import sys
sys.path.insert(0, '/home/site/wwwroot/.python_packages/lib/site-packages')
import fastapi, uvicorn, gunicorn, sqlalchemy, jose, passlib
print('✅ All dependencies installed successfully')
"
```

### 5. App Import testen
```bash
python3 -c "
import sys
sys.path.insert(0, '/home/site/wwwroot/.python_packages/lib/site-packages')
sys.path.insert(0, '/home/site/wwwroot')
from app.main import app
print('✅ App imported successfully')
"
```

## Azure App Settings

Setze diese Environment Variables in Azure Portal:

```
SECRET_KEY = "your-super-secret-jwt-key-change-this-in-production"
WEBSITES_HEALTHCHECK_PATH = "/health"
APP_VERSION = "1.0.0"
LOG_LEVEL = "INFO"
ACCESS_TOKEN_EXPIRE_MINUTES = "30"
CORS_ORIGINS = "*"
```

## Azure Startup Command

Setze diesen Startup Command in Azure App Service:

```bash
python3 -m pip install --disable-pip-version-check --no-cache-dir -r /home/site/wwwroot/requirements.txt -t /home/site/wwwroot/.python_packages/lib/site-packages && PYTHONPATH=/home/site/wwwroot/.python_packages/lib/site-packages gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 120
```

## Test Commands

Nach dem Deployment teste diese Endpoints:

### Health Check
```bash
curl -sSf https://yourapp.azurewebsites.net/health
# Expected: {"status":"ok"}
```

### Service Info
```bash
curl -sSf https://yourapp.azurewebsites.net/
# Expected: {"service":"GetOut API","version":"1.0.0","status":"running"}
```

### User Signup
```bash
curl -X POST https://yourapp.azurewebsites.net/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPassword123!"}'
```

### User Login
```bash
curl -X POST https://yourapp.azurewebsites.net/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=test@example.com&password=TestPassword123!'
```

## Troubleshooting

### Häufige Fehler und Lösungen

**ModuleNotFoundError:**
```bash
# Prüfe PYTHONPATH
echo $PYTHONPATH
# Prüfe installierte Pakete
ls -la .python_packages/lib/site-packages/
```

**App Import Fehler:**
```bash
# Prüfe Dateistruktur
ls -la app/
# Prüfe Python Path
python3 -c "import sys; print(sys.path)"
```

**Database Fehler:**
```bash
# App verwendet SQLite Fallback, sollte funktionieren
# Prüfe Logs in Azure Portal
```

## Kudu Console Zugriff

1. Gehe zu: `https://yourapp.scm.azurewebsites.net`
2. Klicke auf "Debug console" → "Bash"
3. Navigiere zu `/home/site/wwwroot`
4. Führe die Commands aus
