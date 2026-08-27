#!/bin/bash

# Build script for EVCC Optimizer Proxy
# Usage: ./build.sh [platform] [version]

PLATFORM=${1:-linux/amd64}
VERSION=${2:-latest}
REGISTRY=${3:-ghcr.io}
USERNAME=${4:-your-username}
IMAGE_NAME="evcc-optimizer-proxy"

echo "Building $IMAGE_NAME for $PLATFORM..."
echo "Registry: $REGISTRY"
echo "Username: $USERNAME"
echo "Version: $VERSION"

# Build the Docker image
docker buildx build \
    --platform $PLATFORM \
    --tag "$REGISTRY/$USERNAME/$IMAGE_NAME:$VERSION" \
    --load \
    .

if [ $? -eq 0 ]; then
    echo "✓ Build successful!"
    echo ""
    echo "To run the image:"
    echo "  docker run -p 8080:8080 -e TARGET_URL='https://evopt.evcc.io' $REGISTRY/$USERNAME/$IMAGE_NAME:$VERSION"
else
    echo "✗ Build failed!"
    exit 1
fi
