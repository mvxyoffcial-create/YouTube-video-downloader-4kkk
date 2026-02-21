# 🎥 YouTube Downloader API

A high-performance YouTube downloader API built with FastAPI, yt-dlp, and Docker. Supports all video qualities and audio formats with Traefik integration.

## ✨ Features

- **Multiple Video Formats**: 144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 4K
- **Multiple Audio Formats**: MP3, M4A, WEBM, AAC, FLAC, OPUS, OGG, WAV
- **Fast Downloads**: Multi-worker uvicorn server
- **Web Interface**: Built-in responsive UI
- **REST API**: Easy integration with other applications
- **Docker Support**: Containerized deployment
- **Traefik Integration**: Ready for reverse proxy
- **CORS Enabled**: Works with any frontend

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd youtube-downloader

# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f
```

Access the application:
- **Web UI**: http://localhost:8080
- **With Traefik**: http://youtube-downloader.traefik.me
- **Traefik Dashboard**: http://localhost:8081

### Using Docker Only

```bash
# Build the image
docker build -t youtube-downloader .

# Run the container
docker run -d -p 8080:8080 --name youtube-downloader youtube-downloader

# View logs
docker logs -f youtube-downloader
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Install ffmpeg (required for audio conversion)
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Run the application
python app.py
# or
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

## 📚 API Documentation

### Interactive API Docs
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

### Endpoints

#### 1. Download Video/Audio
**POST** `/download`

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "format": "1080p"
}
```

**Format Options:**
- Video: `144p`, `240p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `4k`
- Audio: `mp3`, `m4a`, `webm`, `aac`, `flac`, `opus`, `ogg`, `wav`

**Response**: File download

**cURL Example:**
```bash
curl -X POST "http://localhost:8080/download" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","format":"720p"}' \
  -o video.mp4
```

#### 2. Get Video Info
**GET** `/info?url=VIDEO_URL`

```bash
curl "http://localhost:8080/info?url=https://www.youtube.com/watch?v=VIDEO_ID"
```

**Response:**
```json
{
  "title": "Video Title",
  "duration": 240,
  "thumbnail": "https://...",
  "uploader": "Channel Name",
  "view_count": 1000000,
  "formats": [...]
}
```

#### 3. Health Check
**GET** `/health`

```bash
curl "http://localhost:8080/health"
```

## 🌐 Traefik Configuration

The included `docker-compose.yml` sets up Traefik automatically. Access your API via:

```
http://youtube-downloader.traefik.me
```

### Custom Domain

Edit `docker-compose.yml` to use your own domain:

```yaml
labels:
  - "traefik.http.routers.youtube-downloader.rule=Host(`yourdomain.com`)"
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# Port
PORT=8080

# Workers
WORKERS=4

# Download directory
DOWNLOAD_DIR=/tmp/downloads
```

### Docker Compose Override

Create `docker-compose.override.yml`:

```yaml
version: '3.8'

services:
  youtube-downloader:
    environment:
      - WORKERS=8
    ports:
      - "9090:8080"
```

## 📱 Usage Examples

### Python
```python
import requests

# Download video
response = requests.post(
    "http://localhost:8080/download",
    json={"url": "https://youtube.com/watch?v=...", "format": "1080p"}
)

with open("video.mp4", "wb") as f:
    f.write(response.content)
```

### JavaScript
```javascript
async function downloadVideo(url, format) {
    const response = await fetch('http://localhost:8080/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, format })
    });
    
    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = 'video.mp4';
    a.click();
}
```

### cURL
```bash
# Download 1080p video
curl -X POST http://localhost:8080/download \
  -H "Content-Type: application/json" \
  -d '{"url":"https://youtube.com/watch?v=...","format":"1080p"}' \
  -o video.mp4

# Download MP3 audio
curl -X POST http://localhost:8080/download \
  -H "Content-Type: application/json" \
  -d '{"url":"https://youtube.com/watch?v=...","format":"mp3"}' \
  -o audio.mp3
```

## 🛠️ Development

### Project Structure
```
youtube-downloader/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── README.md            # Documentation
└── .gitignore           # Git ignore rules
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🐛 Troubleshooting

### Download Fails
- Check if the video is available and not region-locked
- Verify ffmpeg is installed (for audio conversion)
- Check Docker logs: `docker-compose logs youtube-downloader`

### Port Already in Use
```bash
# Change port in docker-compose.yml
ports:
  - "9090:8080"  # Use port 9090 instead
```

### Traefik Not Working
- Ensure port 80 is not in use
- Check Traefik logs: `docker-compose logs traefik`
- Verify traefik.me resolves to 127.0.0.1

## 📊 Performance

- **Workers**: 4 uvicorn workers by default
- **Concurrent Downloads**: Supports multiple simultaneous downloads
- **Speed**: Limited by your internet connection and YouTube throttling
- **Formats**: All formats supported by yt-dlp

## 🔒 Security Notes

- This API has CORS enabled for all origins
- No authentication by default - add your own if exposing publicly
- Files are automatically cleaned up after download
- Consider rate limiting for production use

## 📝 License

MIT License - feel free to use in your projects

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## ⚠️ Disclaimer

This tool is for educational purposes. Respect copyright laws and YouTube's Terms of Service. Only download content you have permission to download.

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions

## 🎉 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube download engine
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Traefik](https://traefik.io/) - Reverse proxy
- [FFmpeg](https://ffmpeg.org/) - Media processing

---

Made with ❤️ for the community
