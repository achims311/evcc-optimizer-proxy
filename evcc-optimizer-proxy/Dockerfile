FROM python:3.12-slim

# Install s6-overlay for service management
ARG S6_OVERLAY_VERSION=3.1.6.2
RUN apt-get update && apt-get install -y \
    ca-certificates \
    xz-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz -O /tmp/s6-overlay-noarch.tar.xz && \
    wget https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz -O /tmp/s6-overlay-x86_64.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz && \
    rm /tmp/s6-overlay-*.tar.xz

# Install Python dependencies
WORKDIR /app
COPY rootfs/app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY rootfs/app/*.py /app/
COPY rootfs/etc/s6-overlay/s6-rc.d/ /etc/s6-overlay/s6-rc.d/

# Set working directory
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=2)"

# Start with s6-overlay
ENTRYPOINT ["/init"]
