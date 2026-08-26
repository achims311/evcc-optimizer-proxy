# EVCC Optimizer Proxy - Projektstruktur

```
evcc-optimizer-proxy/
├── addon.yaml                          # Home Assistant Add-on Konfiguration
├── config.yaml                         # Standard-Konfigurationsdatei
├── manifest.json                       # Add-on Manifest
├── Dockerfile                          # Docker-Image Definition
├── .gitignore                          # Git Ignore Rules
│
├── README.md                           # Hauptdokumentation
├── SETUP.md                            # Installationsleitfaden
├── PROJECT_STRUCTURE.md                # Diese Datei
│
├── rootfs/
│   ├── app/
│   │   ├── main.py                     # Hauptanwendung (Flask Server)
│   │   ├── proxy.py                    # Proxy-Logik und NTLM Support
│   │   ├── config_handler.py           # Konfigurationsverwaltung
│   │   └── requirements.txt            # Python Dependencies
│   │
│   └── etc/s6-overlay/
│       └── s6-rc.d/
│           ├── app/
│           │   ├── type                # Service-Typ
│           │   └── contents            # Service-Definition
│           └── python-app/
│               ├── type                # Startup-Typ
│               └── up                  # Startup-Skript
│
├── translations/
│   ├── en.json                         # Englische Übersetzungen
│   └── de.json                         # Deutsche Übersetzungen
│
├── .github/workflows/
│   ├── docker-build.yml                # Auto-Build für Docker Images
│   └── release.yml                     # Release-Automation
│
├── build.sh                            # Lokales Build-Skript
├── run-dev.sh                          # Entwicklungsumgebung
├── setup-docker-compose.sh             # Docker Compose Setup
├── test_proxy.py                       # Unit Tests
└── test_client.py                      # HTTP Client für Tests
```

## Wichtige Dateien

### addon.yaml
- Konfiguriert das Add-on für Home Assistant
- Definiert Ports, Umgebungsvariablen, Konfigurationsoptionen
- Angabe der Docker-Image-Architektur

### Dockerfile
- Definiert das Docker-Image
- Installiert Python 3.12 und Dependencies
- Nutzt s6-overlay für Service-Management
- Konfiguriert Health-Check

### rootfs/app/main.py
- Flask Web-Server
- Definiert API-Endpoints:
  - `/health` - Health Check
  - `/proxy` - Haupt-Proxy-Endpoint
  - `/config` - Konfigurationsverwaltung
  - `/` - Root-Endpoint

### rootfs/app/proxy.py
- Hauptlogik für Request-Modifikation
- NTLM-Proxy-Support
- Systemproxy-Integration
- Fehlerbehandlung und Logging

### rootfs/app/config_handler.py
- Konfiguration aus Home Assistant oder Umgebungsvariablen laden
- Sichere Verwaltung von Passwörtern
- Konfigurationsvalidierung

### translations/
- Mehrsprachige UI-Texte für Home Assistant
- Unterstützt mindestens: Englisch, Deutsch
- Alle Add-on-Konfigurationsoptionen übersetzt

### .github/workflows/
- Automatische Docker-Image-Builds
- Multi-Architektur-Support (amd64, aarch64, armhf, armv7, i386)
- Auto-Release bei Git-Tags

## Abhängigkeiten

### Python Packages (requirements.txt)
- `Flask` - Web-Framework
- `requests` - HTTP-Client
- `requests-ntlm` - NTLM-Authentifizierung
- `python-dotenv` - Umgebungsvariablen
- `pyyaml` - YAML-Parsing

### System-Dependencies
- Python 3.12
- s6-overlay - Service-Management in Docker
- ca-certificates - SSL-Zertifikate

## API-Schnittstellen

### GET /health
Status des Proxy überprüfen.

**Antwort:**
```json
{"status": "healthy"}
```

### POST /proxy
Proxy-Endpoint für EVCC Optimizer Requests.

**Request:**
```json
{
  "batteries": [{...}],
  "strategy": {...},
  "time_series": {...}
}
```

**Modifikation:**
- Setzt `charge_from_grid: true` für alle Batterien
- Setzt `export_to_grid: true` für alle Batterien
- Leitet modifizierten Request an `target_url` weiter
- Gibt Antwort unverändert zurück

### GET /config
Aktuelle Konfiguration abrufen.

**Antwort:**
```json
{
  "target_url": "https://optimizer.evcc.io",
  "proxy_url": null,
  "use_system_proxy": true,
  "log_level": "INFO"
}
```

### POST /config
Konfiguration aktualisieren.

**Request:**
```json
{
  "target_url": "https://new-url.com",
  "log_level": "DEBUG"
}
```

## Workflow für Entwicklung

### 1. Lokale Entwicklung

```bash
chmod +x run-dev.sh
./run-dev.sh
```

Dann in anderem Terminal:
```bash
python test_client.py
```

### 2. Docker-Test

```bash
docker build -t evcc-optimizer-proxy .
docker run -p 8080:8080 evcc-optimizer-proxy
```

### 3. Git & GitHub

```bash
git add .
git commit -m "Beschreibung der Änderung"
git push origin main

# Für Releases:
git tag v1.0.1
git push origin v1.0.1
```

### 4. Home Assistant Installation

Nach Push zu GitHub:
1. Repository zu Home Assistant hinzufügen
2. Add-on wird automatisch erkannt
3. Installation und Updates funktionieren automatisch

## Sicherheitsaspekte

- Passwörter werden NICHT in Logs ausgegeben
- Konfiguration mit sensiblen Daten ist mit `/data/options.json` geschützt
- SSL-Zertifikate werden immer überprüft
- NTLM-Authentifizierung unterstützt ohne Passwortspeicherung
- Eingabevalidierung für Konfiguration

## Performance & Ressourcen

- Leichtes Python-Image (slim variant)
- Flask mit minimalem Overhead
- s6-overlay für schnelle Service-Verwaltung
- Health-Check alle 30 Sekunden
- Timeout von 30 Sekunden für externe Requests

## Erweiterungen für die Zukunft

Mögliche Verbesserungen:
- [ ] Caching von Responses
- [ ] Rate-Limiting
- [ ] Request-Signing
- [ ] Metrics/Telemetrie
- [ ] WebUI Dashboard
- [ ] Multiple Target-URLs
- [ ] Request-Logging-Database
