# GetOut Flutter App - Entwicklungsdokumentation

## Projektübersicht

Die GetOut Flutter App ist eine vollständige Neuentwicklung der ursprünglichen iOS GetOut App in Flutter. Sie bietet eine plattformübergreifende Lösung für soziales Event-Management.

## Architektur

### State Management
- **Provider Pattern**: Verwendet für globales State Management
- **AuthProvider**: Verwaltet Authentifizierungsstatus und Benutzerdaten
- **EventProvider**: Verwaltet Event-Daten und -Operationen
- **ChatProvider**: Verwaltet Chat-Funktionalität

### Datenmodelle
- **Event**: Repräsentiert Events mit Kategorien, Teilnehmern und Metadaten
- **UserProfile**: Benutzerprofil mit Freundeslisten und Event-Teilnahmen
- **Message**: Chat-Nachrichten zwischen Benutzern

### Services
- **AuthService**: Firebase Authentication Integration
- **EventService**: Event CRUD-Operationen mit Firestore
- **ChatService**: Echtzeit-Chat mit Firestore

## Entwicklungsrichtlinien

### Code-Stil
- Dart-Konventionen befolgen
- Aussagekräftige Variablen- und Funktionsnamen
- Dokumentation für öffentliche APIs

### Testing
- Unit Tests für Business Logic
- Widget Tests für UI-Komponenten
- Integration Tests für kritische User Flows

### CI/CD
- Automatische Tests bei Pull Requests
- Build-Validierung für Android und iOS
- Code-Qualitätsprüfungen

## Firebase-Konfiguration

### Erforderliche Services
1. **Authentication**: E-Mail/Passwort-Authentifizierung
2. **Firestore**: Datenbank für Events, Profile und Nachrichten
3. **Storage**: Bild-Uploads für Profile und Events

### Firestore-Struktur
```
users/
  {userId}/
    - email, firstName, lastName
    - profileImageUrl, bio
    - friendIds[], eventIds[]

events/
  {eventId}/
    - title, description, dateTime
    - location, creatorId, attendeeIds[]
    - category, isPublic, maxAttendees

chats/
  {chatId}/
    messages/
      {messageId}/
        - senderId, content, timestamp
        - type, isRead
```

## Nächste Entwicklungsschritte

1. **Authentifizierung implementieren**
   - Login/Register Screens
   - Firebase Auth Integration
   - Passwort-Reset-Funktionalität

2. **Event-Management**
   - Event-Liste und -Details
   - Event-Erstellung und -Bearbeitung
   - Teilnahme-Management

3. **Soziale Features**
   - Freunde-System
   - Chat-Funktionalität
   - Benachrichtigungen

4. **UI/UX Verbesserungen**
   - Responsive Design
   - Dark Mode Support
   - Animationen und Übergänge

## Deployment

### Android
- Play Store Deployment über GitHub Actions
- Signed APK Generation
- Version Management

### iOS
- App Store Deployment
- Code Signing Configuration
- TestFlight Integration
