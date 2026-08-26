#!/bin/bash

# Docker compose file for local development and testing

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  app:
    build: .
    container_name: evcc-optimizer-proxy
    ports:
      - "8080:8080"
    environment:
      - TARGET_URL=https://optimizer.evcc.io
      - LOG_LEVEL=DEBUG
      - USE_SYSTEM_PROXY=true
      # For NTLM proxy testing:
      # - PROXY_URL=http://proxy.example.com:8080
      # - PROXY_USERNAME=DOMAIN\\username
    volumes:
      - ./data:/data
      - ./rootfs/app:/app
    networks:
      - evcc-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 5s

networks:
  evcc-network:
    driver: bridge
EOF

echo "✓ docker-compose.yml created"
echo ""
echo "To use it:"
echo "  docker-compose up -d      # Start in background"
echo "  docker-compose logs -f     # View logs"
echo "  docker-compose down        # Stop containers"
