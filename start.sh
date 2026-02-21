#!/bin/bash

echo "🎥 YouTube Downloader API - Startup Script"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null

# Build and start
echo "🔨 Building and starting containers..."
docker-compose up -d --build

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 5

# Check if containers are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ YouTube Downloader API is running!"
    echo ""
    echo "📍 Access URLs:"
    echo "   - Web Interface: http://localhost:8080"
    echo "   - API Docs: http://localhost:8080/docs"
    echo "   - Traefik (if configured): http://youtube-downloader.traefik.me"
    echo "   - Traefik Dashboard: http://localhost:8081"
    echo ""
    echo "📝 Useful commands:"
    echo "   - View logs: docker-compose logs -f"
    echo "   - Stop: docker-compose down"
    echo "   - Restart: docker-compose restart"
    echo ""
else
    echo ""
    echo "❌ Failed to start containers. Check logs with: docker-compose logs"
    exit 1
fi
