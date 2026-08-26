#!/usr/bin/env bash

# EVCC Optimizer Proxy - Quick Start Guide
# Dieses Skript führt dich durch die ersten Schritte

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     EVCC Optimizer Proxy - Konfigurationsassistent         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Funktion für Ja/Nein Fragen
ask_yes_no() {
    local prompt="$1"
    local response
    while true; do
        read -p "$prompt (j/n): " response
        case "$response" in
            [jJ]) return 0 ;;
            [nN]) return 1 ;;
            *) echo "Bitte antworte mit 'j' oder 'n'" ;;
        esac
    done
}

# Schritt 1: Umgebung überprüfen
echo "📋 Schritt 1: Systemüberprüfung"
echo "=================================="

# Python überprüfen
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python gefunden: $python_version"
else
    echo "✗ Python3 nicht gefunden"
    exit 1
fi

# Docker überprüfen
if command -v docker &> /dev/null; then
    echo "✓ Docker gefunden: $(docker --version)"
else
    echo "⚠ Docker nicht gefunden (optional für Container-Tests)"
fi

# Git überprüfen
if command -v git &> /dev/null; then
    echo "✓ Git gefunden: $(git --version)"
else
    echo "⚠ Git nicht gefunden (für Repository-Upload nötig)"
fi

echo ""

# Schritt 2: Was möchte der Benutzer tun?
echo "🎯 Schritt 2: Was möchtest du tun?"
echo "===================================="
echo ""
echo "1) Lokal in Entwicklungsumgebung testen"
echo "2) Docker Container bauen und testen"
echo "3) Für Home Assistant vorbereiten"
echo "4) GitHub Repository einrichten"
echo "0) Abbrechen"
echo ""

read -p "Auswahl (0-4): " choice

case $choice in
    1)
        echo ""
        echo "🐍 Entwicklungsumgebung einrichten..."
        echo "========================================"
        
        if [ ! -d "venv" ]; then
            echo "Erstelle virtuelle Umgebung..."
            python3 -m venv venv
        fi
        
        echo "Aktiviere virtuelle Umgebung..."
        source venv/bin/activate
        
        echo "Installiere Dependencies..."
        pip install -r rootfs/app/requirements.txt
        
        echo ""
        echo "✓ Entwicklungsumgebung fertig!"
        echo ""
        echo "Um die App zu starten:"
        echo "  chmod +x run-dev.sh"
        echo "  ./run-dev.sh"
        echo ""
        echo "In einem anderen Terminal:"
        echo "  python test_client.py"
        ;;
    
    2)
        echo ""
        echo "🐋 Docker Container vorbereiten..."
        echo "===================================="
        
        if ! command -v docker &> /dev/null; then
            echo "✗ Docker ist nicht installiert!"
            exit 1
        fi
        
        echo "Überprüfe Dockerfile..."
        if [ ! -f "Dockerfile" ]; then
            echo "✗ Dockerfile nicht gefunden!"
            exit 1
        fi
        
        echo "✓ Build mit: docker build -t evcc-optimizer-proxy ."
        echo "✓ Start mit:  docker run -p 8080:8080 evcc-optimizer-proxy"
        echo ""
        
        if ask_yes_no "Soll der Build jetzt gestartet werden?"; then
            docker build -t evcc-optimizer-proxy .
            echo ""
            echo "✓ Docker Image erstellt!"
        fi
        ;;
    
    3)
        echo ""
        echo "🏠 Home Assistant Vorbereitung"
        echo "=============================="
        echo ""
        echo "Überprüfe notwendige Dateien..."
        
        required_files=("addon.yaml" "Dockerfile" "rootfs/app/main.py")
        all_exist=true
        
        for file in "${required_files[@]}"; do
            if [ -f "$file" ]; then
                echo "✓ $file"
            else
                echo "✗ $file nicht gefunden"
                all_exist=false
            fi
        done
        
        echo ""
        if [ "$all_exist" = true ]; then
            echo "✓ Alle notwendigen Dateien vorhanden!"
            echo ""
            echo "Nächste Schritte:"
            echo "1. Repository auf GitHub hochladen"
            echo "2. In Home Assistant: Einstellungen → Add-ons → Repository"
            echo "3. Diese URL hinzufügen: https://github.com/DEIN_USERNAME/evcc-optimizer-proxy"
            echo "4. Add-on suchen und installieren"
        else
            echo "✗ Einige Dateien fehlen"
        fi
        ;;
    
    4)
        echo ""
        echo "📦 GitHub Repository Setup"
        echo "=========================="
        echo ""
        
        if ! command -v git &> /dev/null; then
            echo "✗ Git ist nicht installiert!"
            exit 1
        fi
        
        echo "Git Konfiguration:"
        git_name=$(git config user.name)
        git_email=$(git config user.email)
        
        echo "  Name: $git_name"
        echo "  Email: $git_email"
        
        if [ -z "$git_name" ] || [ -z "$git_email" ]; then
            echo ""
            echo "⚠ Git ist nicht konfiguriert!"
            echo "Bitte führe aus:"
            echo "  git config --global user.name 'Dein Name'"
            echo "  git config --global user.email 'deine.email@example.com'"
            exit 1
        fi
        
        echo ""
        if ask_yes_no "Git Repository in diesem Verzeichnis initialisieren?"; then
            if [ -d ".git" ]; then
                echo "✓ Repository existiert bereits"
            else
                git init
                git add .
                git commit -m "Initial commit: EVCC Optimizer Proxy"
                git branch -M main
                echo ""
                echo "✓ Repository initialisiert!"
                echo ""
                echo "Um zu GitHub zu pushen:"
                echo "  git remote add origin https://github.com/DEIN_USERNAME/evcc-optimizer-proxy.git"
                echo "  git push -u origin main"
            fi
        fi
        ;;
    
    0)
        echo "Abbrechen"
        exit 0
        ;;
    
    *)
        echo "Ungültige Auswahl"
        exit 1
        ;;
esac

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  Weitere Informationen                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📖 Dokumentation:"
echo "  - README.md           - Allgemeine Dokumentation"
echo "  - SETUP.md            - Installationsleitfaden"
echo "  - PROJECT_STRUCTURE.md - Projektstruktur"
echo ""
echo "🧪 Tests:"
echo "  - python test_proxy.py      - Unit Tests"
echo "  - python test_client.py     - HTTP Client Tests"
echo ""
echo "🛠️  Entwicklung:"
echo "  - ./run-dev.sh         - Entwicklungsserver starten"
echo "  - ./build.sh           - Docker Image bauen"
echo "  - ./setup-docker-compose.sh - Docker Compose aufsetzen"
echo ""
echo "📝 Konfiguration:"
echo "  - config.yaml          - Standardkonfiguration"
echo "  - addon.yaml           - Home Assistant Add-on Definition"
echo ""
echo "Weitere Hilfe? Lese die README.md oder SETUP.md!"
echo ""
