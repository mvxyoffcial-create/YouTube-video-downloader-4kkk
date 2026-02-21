from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import os
import uuid
from pathlib import Path
import asyncio
from typing import Optional

app = FastAPI(title="YouTube Downloader API", version="1.0.0")

# CORS middleware - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins including traefik.me
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)

# Download directory
DOWNLOAD_DIR = Path("/tmp/downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

class DownloadRequest(BaseModel):
    url: str
    format: str  # e.g., "144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "4k", "mp3", "m4a", "webm", "aac", "flac", "opus", "ogg", "wav"

class VideoInfo(BaseModel):
    title: str
    duration: int
    thumbnail: str
    formats: list

def get_format_selector(format_type: str) -> str:
    """Convert format type to yt-dlp format selector"""
    format_map = {
        # Video formats
        "144p": "bestvideo[height<=144]+bestaudio/best[height<=144]",
        "240p": "bestvideo[height<=240]+bestaudio/best[height<=240]",
        "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "1440p": "bestvideo[height<=1440]+bestaudio/best[height<=1440]",
        "4k": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",
        # Audio formats
        "mp3": "bestaudio/best",
        "m4a": "bestaudio[ext=m4a]/bestaudio/best",
        "webm": "bestaudio[ext=webm]/bestaudio/best",
        "aac": "bestaudio/best",
        "flac": "bestaudio/best",
        "opus": "bestaudio[ext=opus]/bestaudio/best",
        "ogg": "bestaudio[ext=ogg]/bestaudio/best",
        "wav": "bestaudio/best",
    }
    return format_map.get(format_type.lower(), "best")

def get_audio_format(format_type: str) -> Optional[str]:
    """Get the audio format for post-processing"""
    audio_formats = {
        "mp3": "mp3",
        "m4a": "m4a",
        "aac": "aac",
        "flac": "flac",
        "opus": "opus",
        "ogg": "vorbis",
        "wav": "wav",
    }
    return audio_formats.get(format_type.lower())

@app.get("/", response_class=HTMLResponse)
async def home():
    """Simple web interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>YouTube Downloader</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            input, select, button {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
                font-size: 14px;
            }
            button {
                background: #ff0000;
                color: white;
                border: none;
                cursor: pointer;
                font-weight: bold;
            }
            button:hover {
                background: #cc0000;
            }
            #status {
                margin-top: 20px;
                padding: 15px;
                border-radius: 5px;
                display: none;
            }
            .success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .loading {
                background: #d1ecf1;
                color: #0c5460;
                border: 1px solid #bee5eb;
            }
            .formats {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            .format-section {
                margin: 10px 0;
            }
            .format-section h3 {
                margin: 10px 0 5px 0;
                color: #555;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎥 YouTube Downloader</h1>
            <input type="text" id="url" placeholder="Enter YouTube URL..." />
            
            <div class="format-section">
                <h3>📹 Video Quality</h3>
                <select id="format">
                    <option value="1440p">MP4 (1440p) - 2K</option>
                    <option value="1080p">MP4 (1080p) - Full HD</option>
                    <option value="720p">MP4 (720p) - HD</option>
                    <option value="480p">MP4 (480p)</option>
                    <option value="360p">MP4 (360p)</option>
                    <option value="240p">MP4 (240p)</option>
                    <option value="144p">MP4 (144p)</option>
                    <option value="4k">WEBM (4K)</option>
                </select>
            </div>
            
            <div class="format-section">
                <h3>🎵 Audio Only</h3>
                <select id="audioFormat" style="display:none;">
                    <option value="mp3">MP3</option>
                    <option value="m4a">M4A</option>
                    <option value="webm">WEBM</option>
                    <option value="aac">AAC</option>
                    <option value="flac">FLAC</option>
                    <option value="opus">OPUS</option>
                    <option value="ogg">OGG</option>
                    <option value="wav">WAV</option>
                </select>
            </div>
            
            <label>
                <input type="checkbox" id="audioOnly" /> Download Audio Only
            </label>
            
            <button onclick="downloadVideo()">Download</button>
            <div id="status"></div>
        </div>

        <script>
            const audioOnlyCheckbox = document.getElementById('audioOnly');
            const formatSelect = document.getElementById('format');
            const audioFormatSelect = document.getElementById('audioFormat');

            audioOnlyCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    formatSelect.style.display = 'none';
                    audioFormatSelect.style.display = 'block';
                } else {
                    formatSelect.style.display = 'block';
                    audioFormatSelect.style.display = 'none';
                }
            });

            async function downloadVideo() {
                const url = document.getElementById('url').value;
                const audioOnly = document.getElementById('audioOnly').checked;
                const format = audioOnly ? 
                    document.getElementById('audioFormat').value : 
                    document.getElementById('format').value;
                const status = document.getElementById('status');

                if (!url) {
                    status.className = 'error';
                    status.style.display = 'block';
                    status.textContent = 'Please enter a YouTube URL';
                    return;
                }

                status.className = 'loading';
                status.style.display = 'block';
                status.textContent = '⏳ Downloading... Please wait...';

                try {
                    const response = await fetch('/download', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ url, format })
                    });

                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail || 'Download failed');
                    }

                    // Get filename from header
                    const contentDisposition = response.headers.get('content-disposition');
                    const filename = contentDisposition 
                        ? contentDisposition.split('filename=')[1].replace(/"/g, '')
                        : 'download';

                    // Download file
                    const blob = await response.blob();
                    const downloadUrl = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = downloadUrl;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(downloadUrl);
                    document.body.removeChild(a);

                    status.className = 'success';
                    status.textContent = '✅ Download complete!';
                } catch (error) {
                    status.className = 'error';
                    status.textContent = '❌ Error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/download")
async def download_video(request: DownloadRequest, background_tasks: BackgroundTasks):
    """Download video/audio in specified format"""
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        
        # Determine if audio format
        audio_format = get_audio_format(request.format)
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': get_format_selector(request.format),
            'outtmpl': str(DOWNLOAD_DIR / f'{file_id}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        # Add audio conversion if needed
        if audio_format:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '320' if audio_format == 'mp3' else '0',
            }]
        
        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=True)
            title = info.get('title', 'video')
            
            # Find the downloaded file
            downloaded_files = list(DOWNLOAD_DIR.glob(f'{file_id}.*'))
            if not downloaded_files:
                raise HTTPException(status_code=500, detail="Download failed")
            
            file_path = downloaded_files[0]
            
            # Clean filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            ext = file_path.suffix
            
            # Schedule file deletion after sending
            background_tasks.add_task(cleanup_file, file_path)
            
            return FileResponse(
                path=file_path,
                filename=f"{safe_title}{ext}",
                media_type='application/octet-stream'
            )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info")
async def get_video_info(url: str):
    """Get video information without downloading"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                "title": info.get('title'),
                "duration": info.get('duration'),
                "thumbnail": info.get('thumbnail'),
                "uploader": info.get('uploader'),
                "view_count": info.get('view_count'),
                "formats": [
                    {
                        "format_id": f.get('format_id'),
                        "ext": f.get('ext'),
                        "quality": f.get('format_note'),
                        "filesize": f.get('filesize'),
                    }
                    for f in info.get('formats', [])
                ]
            }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def cleanup_file(file_path: Path):
    """Delete downloaded file after sending"""
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception:
        pass

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
