# Erste Schritte - EVCC Optimizer Proxy

Diese Anleitung hilft dir, das EVCC Optimizer Proxy Add-on schnell zum Laufen zu bringen.

## Voraussetzungen

- Home Assistant (Version 2024.1.0 oder höher)
- Git (für Repository-Setup)
- Docker (für lokale Entwicklung/Tests)

## Schnellstart

### Option 1: Installation in Home Assistant (Empfohlen)

1. **Repository hinzufügen**
   - Öffne Home Assistant
   - Gehe zu: **Einstellungen → Add-ons & Automationen → Add-on Store**
   - Klicke auf das Menü (⋮) → **Repositories**
   - Füge diese URL ein:
     ```
     https://github.com/DEIN_USERNAME/evcc-optimizer-proxy
     ```
   - Klicke **Hinzufügen**

2. **Add-on installieren**
   - Das Add-on "EVCC Optimizer Proxy" sollte nun sichtbar sein
   - Klicke darauf → **Installieren**

3. **Konfigurieren**
   - Gehe zum **Reiter "Konfiguration"**
   - Stelle die erforderlichen Werte ein
   - Klicke **Speichern**

4. **Starten**
   - Klicke auf den Reiter **Info**
   - Klicke **Starten**
   - Überprüfe die Logs im **Reiter "Logs"**

### Option 2: Lokale Entwicklung

```bash
# Repository klonen
git clone https://github.com/DEIN_USERNAME/evcc-optimizer-proxy.git
cd evcc-optimizer-proxy

# Entwicklungsumgebung starten
chmod +x run-dev.sh
./run-dev.sh

# In einem anderen Terminal: Tests durchführen
python test_client.py
```

### Option 3: Docker

```bash
# Build durchführen
docker build -t evcc-optimizer-proxy .

# Container starten
docker run -p 8080:8080 \
   -e TARGET_URL="https://optimizer.evcc.io" \
  -e LOG_LEVEL="DEBUG" \
  evcc-optimizer-proxy

# In einem anderen Terminal: Testen
python test_client.py
```

## Konfiguration

### Basis-Konfiguration (Pflichtangaben)

- **Target URL**: URL des EVCC Optimizer Servers
   - Default: `https://optimizer.evcc.io`
  - Beispiel: `https://my-evcc-server.example.com`

### Proxy-Konfiguration (Optional)

#### Windows mit Systemproxy (Einfachste Option)

Lasse die Standardeinstellungen:
- `use_system_proxy: true`
- Alle anderen Proxy-Optionen: leer/false

Der Add-on nutzt automatisch den Windows-Systemproxy ohne Passworteingabe.

#### NTLM-Proxy (Firmennetzwerk)

```
proxy_url: http://proxy.example.com:8080
proxy_username: DOMAIN\benutzername
```

Das Passwort sollte nicht in der Konfiguration gespeichert werden. Stattdessen:
- Nutze Umgebungsvariablen oder
- Speichere es in einer separaten Datei mit beschränktem Zugriff

#### Linux/Mac mit HTTP_PROXY Umgebungsvariable

```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
export NO_PROXY="localhost,127.0.0.1"
```

### Logging

- **INFO**: Standard-Logging (Produktivumgebung)
- **DEBUG**: Ausführliches Logging (Troubleshooting)
- **WARNING**: Nur Warnungen
- **ERROR**: Nur Fehler

## API Testen

### Health Check

```bash
curl http://localhost:8080/health
```

Erwartete Antwort:
```json
{"status": "healthy"}
```

### Konfiguration abrufen

```bash
curl http://localhost:8080/config
```

### Request senden

```bash
curl -X POST http://localhost:8080/proxy \
  -H "Content-Type: application/json" \
  -d @EvccOptimizerRequest.json
```

### Test-Client verwenden

```bash
python test_client.py http://localhost:8080
```

## Troubleshooting

### Add-on startet nicht

1. **Logs überprüfen:**
   - Öffne das Add-on
   - Gehe zum **Reiter "Logs"**
   - Suche nach Fehlermeldungen

2. **Port überprüfen:**
   - Port 8080 muss verfügbar sein
   - Stelle sicher, dass kein anderer Dienst den Port nutzt

3. **Konfiguration überprüfen:**
   - Speichere die Konfiguration erneut
   - Überprüfe auf Tippfehler

### Proxy-Verbindung schlägt fehl

1. **Proxy-URL überprüfen:**
   ```bash
   curl -x http://proxy:port https://optimizer.evcc.io
   ```

2. **NTLM-Authentifizierung testen:**
   - Stelle sicher, dass der Benutzername im Format `DOMAIN\username` ist
   - Überprüfe, dass das Passwort korrekt ist

3. **Firewall überprüfen:**
   - Stelle sicher, dass die Firewall den Proxy zulässt
   - Überprüfe, dass Port 443 (HTTPS) offen ist

### Logs zeigen keine Fehler, aber es funktioniert nicht

1. **Log-Level auf DEBUG stellen:**
   - Aktualisiere die Konfiguration
   - Log-Level: DEBUG
   - Speichern und Starten

2. **Wiederhole den Test:**
   ```bash
   python test_client.py
   ```

3. **Systemproxy überprüfen** (Windows):
   - Öffne: **Einstellungen → Netzwerk und Internet → Proxyeinstellungen**
   - Überprüfe, ob ein Proxy konfiguriert ist

## Docker Compose für lokale Entwicklung

```bash
# Docker Compose aufsetzen
bash setup-docker-compose.sh

# Container starten
docker-compose up -d

# Logs anschauen
docker-compose logs -f

# Container stoppen
docker-compose down
```

## Repository für Home Assistant

Um dein Add-on als Home Assistant Custom Repository zu veröffentlichen:

### GitHub Setup

1. Erstelle ein neues GitHub Repository:
   ```
   https://github.com/DEIN_USERNAME/evcc-optimizer-proxy
   ```

2. Push deine Änderungen:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/DEIN_USERNAME/evcc-optimizer-proxy.git
   git push -u origin main
   ```

3. Tags für Versionen erstellen:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

### Home Assistant Repository URL

Die Repository-URL für Home Assistant ist:
```
https://github.com/DEIN_USERNAME/evcc-optimizer-proxy
```

### Auto-Updates

Das Repository nutzt GitHub Actions für automatische Docker Image Builds:
- Bei Push zu `main`: Image wird gebaut und auf `ghcr.io` gepusht
- Bei Tag-Push (z.B. `v1.0.0`): Release wird erstellt

Home Assistant erkennt neue Versionen automatisch und bietet Updates an.

## Weiterführende Links

- [Home Assistant Add-ons Dokumentation](https://developers.home-assistant.io/docs/add-ons/)
- [EVCC Dokumentation](https://docs.evcc.io/)
- [Flask Dokumentation](https://flask.palletsprojects.com/)
- [requests-ntlm Dokumentation](https://github.com/requests/requests-ntlm)

## Support

Bei Fragen oder Problemen:
1. Überprüfe die Logs
2. Stelle sicher, dass die Konfiguration korrekt ist
3. Erstelle ein Issue im GitHub Repository

Viel Erfolg! 🎉
