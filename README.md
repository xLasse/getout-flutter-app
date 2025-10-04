# GetOut Flutter App

Eine soziale Event-Management-Anwendung, die es Benutzern ermöglicht, Events zu erstellen, zu verwalten und mit Freunden zu interagieren.

## Features

- **Authentifizierung**: Benutzerregistrierung und -anmeldung mit Firebase Auth
- **Event-Management**: Events erstellen, bearbeiten und verwalten
- **Soziale Funktionen**: Freunde hinzufügen und mit ihnen chatten
- **Profilverwaltung**: Benutzerprofile anpassen und verwalten
- **Responsive Design**: Optimiert für verschiedene Bildschirmgrößen

## Technologie-Stack

- **Frontend**: Flutter/Dart
- **Backend**: Firebase (Auth, Firestore, Storage)
- **State Management**: Provider
- **Navigation**: GoRouter
- **UI**: Material Design 3 mit Google Fonts

## Projektstruktur

```
lib/
├── models/          # Datenmodelle
├── providers/       # State Management
├── screens/         # UI-Bildschirme
├── widgets/         # Wiederverwendbare Widgets
├── services/        # API und Backend-Services
└── utils/           # Hilfsfunktionen und Konstanten
```

## Installation

1. Flutter SDK installieren
2. Dependencies installieren: `flutter pub get`
3. Firebase-Projekt konfigurieren
4. App starten: `flutter run`

## Basiert auf

Dieses Projekt ist eine Flutter-Portierung der ursprünglichen iOS GetOut App.
