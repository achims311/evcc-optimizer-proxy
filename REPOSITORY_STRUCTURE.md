# Repository-Struktur für Home Assistant

Dieses Repository ist ein Home Assistant Add-on Repository.

## Verzeichnisstruktur

```
.
├── repository.yaml          # Home Assistant Repository Definition
├── README.md                # Überblick und Installationsanleitung
├── evcc-optimizer-proxy/    # Das Add-on Verzeichnis
│   ├── config.yaml          # Add-on Manifest für Home Assistant
│   ├── Dockerfile           # Docker Image Definition
│   ├── rootfs/              # Dateien für das Container Image
│   │   ├── app/             # Python Anwendung
│   │   │   ├── main.py
│   │   │   ├── proxy.py
│   │   │   ├── config_handler.py
│   │   │   └── requirements.txt
│   │   └── etc/s6-overlay/  # Service Management
│   ├── translations/        # Mehrsprachige UI Texte
│   ├── SETUP.md             # Detaillierter Installationsleitfaden
│   ├── GETTING_STARTED.md   # Erste Schritte
│   ├── PROJECT_STRUCTURE.md # Technische Struktur
│   ├── test_client.py       # HTTP Test Client
│   ├── test_proxy.py        # Unit Tests
│   ├── run-dev.sh           # Entwicklungsumgebung
│   ├── build.sh             # Docker Build Skript
│   └── quick-start.sh       # Interaktiver Setup-Assistent
├── .github/workflows/       # GitHub Actions CI/CD
│   ├── docker-build.yml     # Auto Docker Build
│   └── release.yml          # Auto Release
└── .gitignore              # Git Ignore Rules
```

## Installation in Home Assistant

1. **Repository hinzufügen:**
   - Home Assistant → Settings → Add-ons & Automations → Add-on Store
   - Klick auf Menü (⋮) → "Repositories"
   - Füge diese URL ein: `https://github.com/achims311/evcc-optimizer-proxy`

2. **Add-on installieren:**
   - Das Add-on sollte im Store sichtbar sein
   - Installiere es und konfiguriere die Optionen

## Was ist dieses Add-on?

Der EVCC Optimizer Proxy ist ein HTTP-Proxy, der:
- HTTP/HTTPS Anfragen empfängt
- Automatisch `charge_from_grid` und `export_to_grid` auf `true` setzt
- Die Anfragen an einen konfigurierbaren EVCC Optimizer Server weiterleitet
- NTLM-Proxy-Support für Firmennetzwerke bietet
- Windows Systemproxy ohne Passworteingabe nutzen kann

## Dokumentation

- [README.md](README.md) - Überblick
- [evcc-optimizer-proxy/SETUP.md](evcc-optimizer-proxy/SETUP.md) - Installationsleitfaden
- [evcc-optimizer-proxy/GETTING_STARTED.md](evcc-optimizer-proxy/GETTING_STARTED.md) - Erste Schritte
- [evcc-optimizer-proxy/PROJECT_STRUCTURE.md](evcc-optimizer-proxy/PROJECT_STRUCTURE.md) - Technische Struktur

## Lokale Entwicklung

```bash
cd evcc-optimizer-proxy
./run-dev.sh          # Entwicklungsserver starten
python test_client.py # Tests durchführen
```

## Support

Bei Fragen oder Problemen: https://github.com/achims311/evcc-optimizer-proxy/issues
