# 🚀 Quick Start Guide - YouTube Downloader API

## 📦 What's Included

This package contains a complete YouTube downloader API with:
- ✅ All video formats (144p to 4K)
- ✅ All audio formats (MP3, M4A, FLAC, WAV, etc.)
- ✅ Web interface
- ✅ REST API
- ✅ Docker support
- ✅ Traefik integration
- ✅ CORS enabled

## 🎯 Quick Setup (3 Steps)

### Step 1: Extract Files
```bash
tar -xzf youtube-downloader.tar.gz
cd youtube-downloader
```

### Step 2: Start the Application
```bash
# Option A: Using the startup script (recommended)
./start.sh

# Option B: Manual Docker Compose
docker-compose up -d --build
```

### Step 3: Access the Application
- **Web Interface**: http://localhost:8080
- **API Documentation**: http://localhost:8080/docs
- **With Traefik**: http://youtube-downloader.traefik.me
- **Traefik Dashboard**: http://localhost:8081

## 📁 Files Included

```
youtube-downloader/
├── app.py                    # Main FastAPI application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container setup
├── start.sh                 # Easy startup script
├── README.md                # Full documentation
├── .gitignore              # Git ignore rules
└── .env.example            # Environment variables template
```

## 🐙 Upload to GitHub

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: YouTube Downloader API"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/youtube-downloader.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🔧 Basic Usage

### Download Video (1080p)
```bash
curl -X POST http://localhost:8080/download \
  -H "Content-Type: application/json" \
  -d '{"url":"https://youtube.com/watch?v=VIDEO_ID","format":"1080p"}' \
  -o video.mp4
```

### Download Audio (MP3)
```bash
curl -X POST http://localhost:8080/download \
  -H "Content-Type: application/json" \
  -d '{"url":"https://youtube.com/watch?v=VIDEO_ID","format":"mp3"}' \
  -o audio.mp3
```

### Get Video Information
```bash
curl "http://localhost:8080/info?url=https://youtube.com/watch?v=VIDEO_ID"
```

## 📋 Available Formats

**Video Formats:**
- 144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 4k

**Audio Formats:**
- mp3, m4a, webm, aac, flac, opus, ogg, wav

## 🛠️ Management Commands

```bash
# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# Rebuild after changes
docker-compose up -d --build

# Remove everything
docker-compose down -v
```

## 🌐 Access via Traefik

The application is pre-configured for Traefik. After starting:
- Main App: http://youtube-downloader.traefik.me
- Dashboard: http://localhost:8081

## 📝 Customize

Edit `docker-compose.yml` to:
- Change ports
- Add custom domain
- Adjust worker count
- Configure environment variables

## ⚠️ Requirements

- Docker
- Docker Compose
- Internet connection

## 🆘 Troubleshooting

**Port 8080 already in use?**
Edit `docker-compose.yml`:
```yaml
ports:
  - "9090:8080"  # Change to port 9090
```

**Traefik not working?**
- Check port 80 is available
- Verify traefik.me resolves to 127.0.0.1

**Download fails?**
- Check video availability
- Verify ffmpeg is installed in container
- Check logs: `docker-compose logs youtube-downloader`

## 💡 Tips

1. **Performance**: Increase workers in Dockerfile for better performance
2. **Security**: Add authentication if exposing publicly
3. **Storage**: Monitor `/tmp/downloads` - files auto-delete after sending
4. **Updates**: Pull latest yt-dlp: `docker-compose build --no-cache`

## 📚 Full Documentation

See `README.md` for complete documentation, API reference, and advanced usage.

---

**Need Help?** Open an issue on GitHub or check the full README.md
