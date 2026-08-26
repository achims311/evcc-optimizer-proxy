# EVCC Optimizer Proxy - Home Assistant Add-on

Ein HTTP-Proxy für den EVCC Optimizer, der eingehende Anfragen automatisch modifiziert, um `charge_from_grid` und `export_to_grid` auf `true` zu setzen.

## Features

- 🔄 Automatische Request-Modifikation
- 🌐 HTTP/HTTPS Proxy-Support mit NTLM-Authentifizierung
- 🪟 Windows Systemproxy-Unterstützung
- 🔧 Konfigurierbar über Home Assistant UI
- 📊 Ausführliches Logging für Debugging
- 🏥 Health Check Endpoint
- 🔐 SSL-Zertifikatsprüfung

## Installation

1. Füge das Repository zu Home Assistant hinzu:
   - Home Assistant → Einstellungen → Add-ons & Automationen → Add-on Store
   - Klicke auf die drei Punkte (⋮) → "Repositories"
   - Gib die Repository-URL ein: `https://github.com/achims311/evcc-optimizer-proxy`
   - Klicke auf "Hinzufügen"

2. Installiere das Add-on:
   - Das Add-on "EVCC Optimizer Proxy" sollte nun im Store sichtbar sein
   - Klicke auf das Add-on und dann auf "Installieren"

3. Konfiguriere das Add-on:
   - Gehe zum Add-on und klicke auf "Konfiguration"
   - Stelle die erforderlichen Parameter ein:
     - **Target URL**: Die URL des EVCC Optimizer Servers (default: `https://optimizer.evcc.io`)
     - **Proxy URL** (optional): URL deines HTTP/HTTPS Proxys (z.B. `http://proxy.example.com:8080`)
     - **Proxy Username** (optional): Benutzername für NTLM-Authentifizierung
     - **Use System Proxy**: Systemproxy verwenden (Windows/Linux/Mac)
     - **Log Level**: Logging-Level (INFO, DEBUG, WARNING, ERROR)

4. Starte das Add-on

## Konfiguration

### Grundlegende Konfiguration

Die Konfiguration erfolgt über die Home Assistant UI im Add-on-Einstellungen:

```yaml
target_url: "https://optimizer.evcc.io"
proxy_url: null
proxy_username: null
use_system_proxy: true
log_level: "INFO"
```

### Proxy-Konfiguration

#### Windows mit Systemproxy (Standard)
Setze `use_system_proxy: true`. Der Add-on nutzt automatisch den Windows-Systemproxy ohne Passworteingabe.

#### NTLM-Proxy (z.B. in Firmennetzwerken)

```yaml
proxy_url: "http://proxy.example.com:8080"
proxy_username: "DOMAIN\\username"
# Das Passwort sollte sicher in einer anderen Datei oder Umgebungsvariable gespeichert werden
```

#### Linux/Mac mit Umgebungsvariablen

```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

## API Endpoints

### Health Check
```
GET /health
```
Rückgabe: `{"status": "healthy"}`

### Proxy Endpoint
```
POST /proxy
Content-Type: application/json

{
  "batteries": [
    {
      "c_max": 5000,
      "c_min": 0,
      "charge_from_grid": true,  // Wird auf true gesetzt, falls nicht vorhanden
      "d_max": 5000,
      "p_a": 0.00018822195,
      "s_capacity": 9600,
      "s_initial": 8885.106,
      "s_max": 9600,
      "s_min": 1440
    }
  ],
  "eta_c": 0.9,
  "eta_d": 0.9,
  "grid": {},
  "strategy": {
    "charging_strategy": "attenuate_grid_peaks",
    "discharging_strategy": "discharge_before_import"
  },
  "time_series": { ... }
}
```

Die Antwort wird unverändert vom EVCC Optimizer zurückgegeben.

### Configuration Endpoint
```
GET /config        # Aktuelle Konfiguration abrufen
POST /config       # Konfiguration aktualisieren
```

## Request-Modifikation

Der Proxy modifiziert eingehende Anfragen wie folgt:

1. **charge_from_grid**: Wird automatisch auf `true` gesetzt
2. **export_to_grid**: Wird automatisch auf `true` gesetzt (neu hinzugefügt)

Dies gilt für alle Batterien im Array `batteries`.

### Beispiel

**Eingabe:**
```json
{
  "batteries": [{
    "charge_from_grid": false,
    "s_capacity": 9600
  }]
}
```

**Nach Modifikation:**
```json
{
  "batteries": [{
    "charge_from_grid": true,
    "export_to_grid": true,
    "s_capacity": 9600
  }]
}
```

## Logging

Logs können in der Home Assistant Oberfläche abgerufen werden:

1. Öffne das Add-on
2. Gehe zum Tab "Logs"
3. Stelle ggf. den Log-Level auf "DEBUG" für ausführlichere Informationen

## Troubleshooting

### Das Add-on startet nicht
- Überprüfe die Logs im "Log" Tab
- Stelle sicher, dass Port 8080 nicht belegt ist
- Überprüfe die Konfiguration auf Tippfehler

### Proxy-Verbindungsfehler
- Überprüfe die Proxy-URL und Credentials
- Teste die Verbindung manuell: `curl -x http://proxy:port https://example.com`
- Aktiviere DEBUG-Logging für ausführliche Fehlermeldungen

### NTLM-Authentifizierungsfehler
- Stelle sicher, dass der Benutzername im Format `DOMAIN\\username` angegeben ist
- Überprüfe, dass das Passwort korrekt ist
- Versuche mit einem anderen Benutzer

## Auto-Updates

Dieses Add-on unterstützt automatische Updates über das Home Assistant Add-on Repository System. Neue Versionen werden automatisch erkannt und können installiert werden.

## Entwicklung

### Lokale Tests

```bash
# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r rootfs/app/requirements.txt

# Konfiguration für Tests
export TARGET_URL="https://optimizer.evcc.io"
export LOG_LEVEL="DEBUG"

# App starten
python rootfs/app/main.py
```

### Docker Build

```bash
# Build durchführen
docker build -t evcc-optimizer-proxy .

# Container starten
docker run -p 8080:8080 -e TARGET_URL="https://optimizer.evcc.io" evcc-optimizer-proxy
```

## License

MIT

## Support

Bei Fragen oder Fehlern bitte ein Issue im Repository erstellen.
