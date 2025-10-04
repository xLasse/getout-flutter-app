# GetOut Backend API

FastAPI-basiertes Backend für die GetOut Flutter App mit JWT-Authentifizierung und Azure App Service Unterstützung.

## Features

- **JWT Authentication**: Sichere Benutzerauthentifizierung mit Access- und Refresh-Tokens
- **User Management**: Benutzerregistrierung, Login und Profilverwaltung
- **Event Management**: CRUD-Operationen für soziale Events
- **Social Features**: Freundschaftssystem und Chat-Funktionalität
- **Health Checks**: Umfassende Health- und Readiness-Probes
- **Rate Limiting**: Schutz vor Brute-Force-Angriffen
- **Azure Ready**: Optimiert für Azure App Service Deployment

## API Endpoints

### Authentication
- `POST /auth/signup` - Benutzerregistrierung
- `POST /auth/login` - Benutzeranmeldung
- `POST /auth/refresh` - Token-Erneuerung
- `GET /auth/me` - Aktueller Benutzer
- `POST /auth/logout` - Abmeldung
- `POST /auth/revoke-all-tokens` - Alle Tokens widerrufen

### Health & Monitoring
- `GET /` - Service-Informationen
- `GET /health` - Health Check
- `GET /livez` - Liveness Probe
- `GET /readyz` - Readiness Probe

### Protected Routes
- `GET /users/me` - Benutzerprofil
- `GET /admin/ping` - Admin-Zugriff (Beispiel)

## Lokale Entwicklung

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Umgebungsvariablen
```bash
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="sqlite:///./app.db"  # Optional
export LOG_LEVEL="DEBUG"
```

### Server starten
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Dokumentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Datenbank

### Modelle
- **User**: Benutzerkonten und Profile
- **RefreshToken**: JWT Refresh Token Management
- **Event**: Soziale Events und Veranstaltungen
- **EventAttendee**: Event-Teilnahme-Beziehungen
- **Friendship**: Freundschaftsbeziehungen
- **ChatMessage**: Chat-Nachrichten zwischen Benutzern

### Migration
Das System erstellt automatisch alle Tabellen beim Start. Für Produktionsumgebungen wird Alembic für Migrationen empfohlen.

## Sicherheit

### Passwort-Hashing
- Bcrypt-Hashing für alle Passwörter
- Keine Klartext-Passwörter in der Datenbank

### JWT-Token
- HS256 Algorithmus
- Konfigurierbare Ablaufzeiten
- Refresh-Token für sichere Token-Erneuerung

### Rate Limiting
- 5 Login-Versuche pro Minute pro IP
- Schutz vor Brute-Force-Angriffen

## Deployment

Siehe [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) für detaillierte Azure App Service Deployment-Anweisungen.

## Testing

### Manueller Test mit curl
```bash
# Health Check
curl http://localhost:8000/health

# Signup
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPassword123!"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=test@example.com&password=TestPassword123!'

# Get Profile (mit Token)
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Architektur

Das Backend folgt einer modularen Architektur mit klarer Trennung von Verantwortlichkeiten:

- **main.py**: FastAPI App-Konfiguration und Routing
- **auth.py**: Authentifizierungs-Endpoints
- **security.py**: JWT und Passwort-Handling
- **models.py**: SQLAlchemy Datenmodelle
- **schemas.py**: Pydantic Request/Response Schemas
- **db.py**: Datenbankverbindung und Session Management
