# 🎉 EVCC Optimizer Proxy - Projekt erfolgreich erstellt!

Dein Home Assistant Addon für die EVCC Optimizer Request-Modifikation ist bereit.

## 📊 Projektübersicht

**Projekt:** EVCC Optimizer Proxy  
**Type:** Home Assistant Add-on (Python/Flask)  
**Sprachen:** Englisch, Deutsch  
**Version:** 1.0.0  
**Lizenz:** MIT

## ✨ Features

✅ **HTTP Proxy Server** - Empfängt GET/POST Requests  
✅ **Automatische Request-Modifikation** - Setzt `charge_from_grid` und `discharge_to_grid` auf true
✅ **NTLM Proxy-Support** - Firmennetzwerke mit Authentifizierung  
✅ **Windows Systemproxy** - Automatische Erkennung ohne Passworteingabe  
✅ **Home Assistant Integration** - Native Add-on Integration mit Auto-Updates  
✅ **Konfigurierbar via UI** - Einfache Einstellung über Home Assistant  
✅ **Mehrsprachig** - Englisch und Deutsch  
✅ **Production-Ready** - Health-Checks, Logging, Error-Handling  

## 📁 Projektstruktur

```
evcc-optimizer-proxy/
├── 📄 Konfiguration
│   ├── config.yaml             - Home Assistant Add-on Definition
│   ├── manifest.json           - Add-on Metadaten
│   └── Dockerfile              - Docker Image
│
├── 🐍 Anwendung (rootfs/app/)
│   ├── main.py                 - Flask Server & Endpoints
│   ├── proxy.py                - Request-Modifikation & Forwarding
│   ├── config_handler.py       - Konfigurationsverwaltung
│   └── requirements.txt        - Python Dependencies
│
├── 🌍 Sprachen (translations/)
│   ├── en.json                 - Englisch
│   └── de.json                 - Deutsch
│
├── ⚙️  Automatisierung (.github/workflows/)
│   ├── docker-build.yml        - Multi-Arch Docker Builds
│   └── release.yml             - Automatische Releases
│
├── 🧪 Tests & Development
│   ├── test_proxy.py           - Unit Tests
│   ├── test_client.py          - HTTP Client Tests
│   ├── run-dev.sh              - Entwicklungsumgebung
│   ├── build.sh                - Docker Build Skript
│   ├── setup-docker-compose.sh - Docker Compose Setup
│   └── quick-start.sh          - Konfigurationsassistent
│
└── 📚 Dokumentation
    ├── README.md               - Hauptdokumentation
    ├── SETUP.md                - Installationsleitfaden
    ├── PROJECT_STRUCTURE.md    - Detaillierte Struktur
    └── GETTING_STARTED.md      - Diese Datei
```

## 🚀 Schnellstart

### 1️⃣ Lokale Entwicklung (Einfachste Methode)

```bash
cd /home/achim/Downloads/EvccProxyMod

# Entwicklungsumgebung starten
chmod +x run-dev.sh
./run-dev.sh

# In anderem Terminal: Testen
python test_client.py
```

### 2️⃣ Docker Lokal Testen

```bash
docker build -t evcc-optimizer-proxy .
docker run -p 8080:8080 \
   -e TARGET_URL="https://optimizer.evcc.io" \
  -e LOG_LEVEL="DEBUG" \
  evcc-optimizer-proxy

# Test
python test_client.py
```

### 3️⃣ Interaktive Konfiguration

```bash
./quick-start.sh
```

Das Skript führt dich durch die Konfiguration und hilft bei:
- Entwicklungsumgebung Setup
- Docker Container Build
- Home Assistant Vorbereitung
- GitHub Repository Setup

## 🔧 API Endpoints

| Endpoint | Methode | Beschreibung |
|----------|---------|-------------|
| `/health` | GET | Health Check Status |
| `/proxy/<zielpfad>` | POST | Proxy-Endpoint, leitet den Zielpfad an den Optimizer weiter |
| `/config` | GET/POST | Konfigurationsverwaltung |
| `/` | GET | Root/Info Endpoint |

### Beispiel: Proxy Aufrufen

```bash
curl -X POST http://localhost:8080/proxy \
  -H "Content-Type: application/json" \
  -d @EvccOptimizerRequest.json
```

## Tests

Create and activate the project-local virtual environment, then run the isolated test suite:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r rootfs/app/requirements.txt -r requirements-dev.txt
python -m pytest -q
```

Visual Studio Code uses `.venv/bin/python` and discovers the same tests in the Testing view through `.vscode/settings.json`. Use the Testing view to run or debug individual tests.

## 📋 Konfigurationsoptionen

### Pflichtangaben
- **target_url**: EVCC Optimizer Server (default: `https://optimizer.evcc.io`)

### Optional
- **proxy_url**: HTTP/HTTPS Proxy URL
- **proxy_username**: NTLM Benutzername (Format: `DOMAIN\username`)
- **use_system_proxy**: Windows/Linux System-Proxy nutzen (default: true)
- **log_level**: DEBUG, INFO, WARNING, ERROR (default: INFO)

## 🏠 Home Assistant Installation

1. **Repository hinzufügen:**
   ```
   https://github.com/DEIN_USERNAME/evcc-optimizer-proxy
   ```

2. **Add-on installieren** aus dem Store

3. **Konfigurieren** über die UI

4. **Starten** und Logs überprüfen

## 📦 GitHub Vorbereitung

```bash
# Initialisiere Git
git init

# Füge alle Dateien hinzu
git add .

# Commit
git commit -m "Initial commit: EVCC Optimizer Proxy"

# Branch umbenennen
git branch -M main

# Remote hinzufügen (DEIN_USERNAME ersetzen!)
git remote add origin https://github.com/DEIN_USERNAME/evcc-optimizer-proxy.git

# Push
git push -u origin main

# Version taggen
git tag v1.0.0
git push origin v1.0.0
```

## 🧪 Tests durchführen

```bash
# Unit Tests
python test_proxy.py

# HTTP Client Tests (Proxy muss laufen)
python test_client.py

# Test gegen spezifische URL
python test_client.py http://192.168.1.100:8080
```

## 🛠️ Häufige Aufgaben

### Logs im Entwicklung anschauen
```bash
./run-dev.sh
```
Die Logs werden direkt in der Console angezeigt (LOG_LEVEL=DEBUG)

### Docker Compose für schnelle Tests
```bash
bash setup-docker-compose.sh
docker-compose up -d
docker-compose logs -f
```

### Änderungen Testen
```bash
# Nach Code-Änderungen in rootfs/app/:
# 1. Container neubauen
docker-compose down
docker-compose up -d

# 2. Logs checken
docker-compose logs -f

# 3. API testen
python test_client.py
```

## 📚 Weitere Ressourcen

- **[README.md](README.md)** - Umfassende Dokumentation
- **[SETUP.md](SETUP.md)** - Detaillierte Installationsanleitung
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Technische Struktur
- **[quick-start.sh](quick-start.sh)** - Interaktive Konfiguration

## 🤝 Support & Debugging

### App startet nicht
1. Logs überprüfen: `./run-dev.sh`
2. Port 8080 überprüfen: `lsof -i :8080`
3. Python Version überprüfen: `python3 --version`

### Proxy-Fehler
1. Log-Level auf DEBUG setzen
2. Proxy URL überprüfen
3. NTLM Username Format: `DOMAIN\username`
4. Firewall/Netzwerk überprüfen

### Home Assistant Probleme
1. Repository URL überprüfen
2. Docker Image Architecture überprüfen
3. Home Assistant Logs überprüfen

## ✅ Nächste Schritte

1. **Tests durchführen**
   ```bash
   python test_proxy.py
   ./run-dev.sh &
   python test_client.py
   ```

2. **Konfiguration anpassen**
   - Bearbeite `config.yaml` oder nutze die UI

3. **GitHub Setup**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/DEIN_USERNAME/evcc-optimizer-proxy.git
   git push -u origin main
   ```

4. **Home Assistant Installation**
   - Repository zum Add-on Store hinzufügen
   - Add-on installieren und konfigurieren

5. **Deployment**
   - Auf Production Server deployen
   - Mit echtem EVCC System testen
   - Monitoring einrichten

## 🎯 Technische Details

**Sprache:** Python 3.12  
**Framework:** Flask  
**Proxy-Auth:** NTLM (requests-ntlm)  
**Docker Base:** python:3.12-slim  
**Service Manager:** s6-overlay v3.1.6.2  
**Multi-Arch:** amd64, aarch64  

## 📝 Lizenz

MIT License - Frei nutzbar und modifizierbar

---

**Viel Erfolg mit deinem Projekt! 🚀**

Bei Fragen oder Problemen:
1. Schau in die Logs
2. Lese die Dokumentation
3. Aktiviere DEBUG-Logging
4. Erstelle ein GitHub Issue

Fragen? Kontaktiere den Add-on-Maintainer oder check die [Home Assistant Community](https://community.home-assistant.io/)
