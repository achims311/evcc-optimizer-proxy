FROM python:3.12-slim

# amd64/aarch64 have prebuilt manylinux wheels for all deps, no compiler needed
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /app
COPY rootfs/app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY rootfs/app/*.py /app/

# Set working directory
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=2)" || exit 1

# Start the Flask app directly (single-process add-on, no init system needed)
CMD ["python", "main.py"]
