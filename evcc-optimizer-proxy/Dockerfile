FROM python:3.12-slim

# Install build dependencies and tools for all architectures
RUN apt-get update && apt-get install -y \
    ca-certificates \
    xz-utils \
    wget \
    build-essential \
    python3-dev \
    libffi-dev \
    libyaml-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install s6-overlay for service management (architecture-aware)
ARG S6_OVERLAY_VERSION=3.1.6.2
RUN wget https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz -O /tmp/s6-overlay-noarch.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz && \
    rm /tmp/s6-overlay-noarch.tar.xz

# Download architecture-specific s6-overlay based on build platform
RUN case "$(dpkg --print-architecture)" in \
    amd64) \
      wget https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz -O /tmp/s6-overlay-arch.tar.xz;; \
    arm64) \
      wget https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-aarch64.tar.xz -O /tmp/s6-overlay-arch.tar.xz;; \
    armhf) \
      wget https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-armhf.tar.xz -O /tmp/s6-overlay-arch.tar.xz;; \
    armel) \
      wget https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-arm.tar.xz -O /tmp/s6-overlay-arch.tar.xz;; \
    *) echo "Unsupported architecture"; exit 1;; \
  esac && \
  tar -C / -Jxpf /tmp/s6-overlay-arch.tar.xz && \
  rm /tmp/s6-overlay-arch.tar.xz

# Install Python dependencies with verbose output for debugging
WORKDIR /app
COPY rootfs/app/requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -v -r requirements.txt

# Copy application
COPY rootfs/app/*.py /app/
COPY rootfs/etc/s6-overlay/s6-rc.d/ /etc/s6-overlay/s6-rc.d/

# Set working directory
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=2)" || exit 1

# Start with s6-overlay
ENTRYPOINT ["/init"]
