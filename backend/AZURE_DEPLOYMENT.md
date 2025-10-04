# Azure App Service Deployment Guide

## Azure Startup Command

Verwenden Sie folgenden Startup Command in Azure App Service:

```bash
python3 -m pip install --disable-pip-version-check --no-cache-dir -r /home/site/wwwroot/requirements.txt -t /home/site/wwwroot/.python_packages/lib/site-packages && PYTHONPATH=/home/site/wwwroot/.python_packages/lib/site-packages gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 120
```

## Azure App Settings

Konfigurieren Sie folgende Environment Variables in Azure App Service:

### Erforderliche Settings
- `SECRET_KEY`: JWT Secret Key (generieren Sie einen sicheren Schlüssel)
- `WEBSITES_HEALTHCHECK_PATH`: `/health`

### Optionale Settings
- `APP_VERSION`: `1.0.0` (oder aktuelle Version)
- `LOG_LEVEL`: `INFO`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
- `REFRESH_TOKEN_EXPIRE_DAYS`: `7`
- `DATABASE_URL`: PostgreSQL/MySQL Connection String (optional, SQLite Fallback)
- `CORS_ORIGINS`: `https://yourapp.com,https://www.yourapp.com`
- `TRUSTED_HOSTS`: `yourapp.azurewebsites.net,yourapp.com`

## Verzeichnisstruktur für Azure

```
/home/site/wwwroot/
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
```

## Test Commands

### 1. Health Check
```bash
curl -sSf https://yourapp.azurewebsites.net/health
# Expected: {"status":"ok"}
```

### 2. User Signup
```bash
curl -sSf -X POST https://yourapp.azurewebsites.net/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"StrongPassword123!"}'
```

### 3. User Login
```bash
curl -sSf -X POST https://yourapp.azurewebsites.net/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=test@example.com&password=StrongPassword123!'
```

### 4. Get Current User (with token)
```bash
curl -sSf https://yourapp.azurewebsites.net/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Deployment Checklist

1. ✅ Upload alle Dateien nach `/home/site/wwwroot/`
2. ✅ Setze Azure App Settings (besonders SECRET_KEY)
3. ✅ Konfiguriere Startup Command
4. ✅ Setze WEBSITES_HEALTHCHECK_PATH auf `/health`
5. ✅ Teste Health Endpoint
6. ✅ Teste Authentication Flow
7. ✅ Überprüfe Logs in Azure Portal

## Troubleshooting

### Häufige Probleme
- **ModuleNotFoundError**: Überprüfe requirements.txt und Startup Command
- **Database Connection**: Überprüfe DATABASE_URL oder verwende SQLite Fallback
- **JWT Errors**: Stelle sicher, dass SECRET_KEY gesetzt ist
- **CORS Errors**: Konfiguriere CORS_ORIGINS richtig

### Log-Überwachung
- Azure Portal → App Service → Log Stream
- Kudu Console: `https://yourapp.scm.azurewebsites.net`
- Application Insights für erweiterte Überwachung
