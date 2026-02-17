# YouTube Shorts Automation 🎬

> **AI-Powered YouTube Shorts Creation with Web Dashboard & FREE Gemini API**

Transform your scripts into viral YouTube Shorts automatically! Features a modern web dashboard, CLI tools, and complete automation workflow.

## 🌟 Two Ways to Use

### 🌐 Web Dashboard (Recommended)
Beautiful, responsive interface with:
- API configuration through UI forms (no manual .env editing!)
- Visual video creation and management
- Real-time job monitoring
- Video library with download links
- Automated scheduling (coming soon)

### 💻 Command Line (Advanced)
Full CLI access for scripting and automation

## ✨ Features

- **🌐 Modern Web Dashboard** - Manage everything through a beautiful interface
- **🤖 AI Content Generation** - FREE Google Gemini API for titles, descriptions, tags
- **🎙️ Text-to-Speech** - Natural voiceovers (OpenAI TTS or ElevenLabs)
- **🎬 AI Video Generation** - Luma AI or Runway Gen-3 integration
- **📝 Auto-Captions** - Whisper API for professional subtitles
- **🎞️ Video Assembly** - FFmpeg-powered editing with captions
- **📤 YouTube Upload** - Direct publishing to your channel
- **💰 Cost-Effective** - ~$0.23 per video using budget setup
- **🔒 Secure** - Encrypted API key storage

## 🚀 Quick Start (Web Dashboard)

### 1. Clone & Install

```bash
git clone https://github.com/Starship01-akaSniper/youtube-shorts-automation.git
cd youtube-shorts-automation

# Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Web Server

```bash
python app.py
```

Server starts at: **http://localhost:5000** 🎉

### 3. Configure via Web UI

1. Open http://localhost:5000 in your browser
2. Click **Settings** in navigation
3. Enter your API keys in the forms
4. Click **Save Configuration**

That's it! No manual .env file editing needed! 🙌

### 4. Create Your First Video

1. Click **Create Video**
2. Enter your script (150-200 words)
3. Click **Generate Video**
4. Monitor progress on **Dashboard**
5. Download from **Library** when complete

## 🔑 API Keys Setup

Get your API keys from these providers:

### Required APIs

| Service | Cost | Link | Purpose |
|---------|------|------|---------|
| **Google Gemini** | FREE! | [ai.google.dev](https://ai.google.dev/) | Content generation |
| **OpenAI** | ~$0.03/video | [platform.openai.com](https://platform.openai.com/api-keys) | TTS & Captions |
| **Luma AI** | ~$0.20/video | [piapi.ai](https://piapi.ai/) | Video generation |

### Optional APIs

| Service | Purpose |
|---------|---------|
| **YouTube Data API** | Auto-upload to YouTube |
| **ElevenLabs** | Premium-quality voiceovers |
| **Runway Gen-3** | Higher-quality videos |

**Enter all keys through the web dashboard Settings page!**

## 💰 Cost Breakdown

**Budget Setup** - $0.23 per video:
- Gemini: $0.00 (FREE!)
- OpenAI TTS: $0.02
- Whisper Captions: $0.01
- Luma AI Video: $0.20

**Monthly (30 videos):** ~$7-14

See [youtube_shorts_automation_cost_analysis.md](https://github.com/Starship01-akaSniper/youtube-shorts-automation/blob/main/youtube_shorts_automation_cost_analysis.md) for detailed breakdown.

## 📁 Project Structure

```
youtube-shorts-automation/
├── app.py                 # Flask web server
├── database.py            # Database manager with encryption
├── job_queue.py           # Background job processor
├── config.py              # Configuration loader
├── main.py                # CLI entry point
├── modules/               # Core automation modules
│   ├── content_generator.py
│   ├── tts_generator.py
│   ├── video_generator.py
│   ├── caption_generator.py
│   ├── video_assembler.py
│   └── youtube_uploader.py
├── web/                   # Web dashboard
│   ├── index.html
│   ├── css/style.css
│   └── js/
│       ├── api.js
│       └── app.js
├── requirements.txt
└── README.md
```

## 🎯 Usage Examples

### Web Dashboard (Recommended)

1. Start server: `python app.py`
2. Open browser to http://localhost:5000
3. Use the beautiful UI to create videos!

### Command Line

```bash
# Interactive mode
python main.py --interactive

# From file
python main.py --script-file scripts/example_honey.txt

# Direct command
python main.py --script "Your amazing script here" --upload
```

## 🌐 Deploy to Cloud

Deploy your dashboard to the cloud for 24/7 access!

Supported platforms:
- **Railway** (Free tier)
- **Render** (Free tier)
- **Fly.io** (Free tier)
- **Heroku**

See [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md) for detailed deployment instructions.

## 🛠️ Advanced Configuration

### FFmpeg Installation

**Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)  
**macOS:** `brew install ffmpeg`  
**Linux:** `sudo apt-get install ffmpeg`

### Database Location

All data stored in: `data/automation.db`  
Encryption key: `data/.secret_key`

**Backup regularly!**

## 📊 Dashboard Features

- **Statistics Cards** - Total videos, completed, processing, pending
- **Video Library** - Grid view of all created videos
- **Job Monitor** - Real-time progress tracking
- **Settings Panel** - API key configuration with encrypted storage
- **Auto-Refresh** - Live updates every 5-10 seconds

## 🎬 Video Creation Workflow

The system automates these steps:

1. **Content AI** (5s) - Generate title, description, tags
2. **Text-to-Speech** (10s) - Create voiceover from script
3. **Video Generation** (2-5min) - AI-generated visuals
4. **Caption Generation** (10s) - Subtitle creation
5. **Video Assembly** (30s) - Combine everything with FFmpeg
6. **Upload** (optional) - Publish to YouTube

**Total time:** ~5-10 minutes per video

## 🐛 Troubleshooting

### Web Server Won't Start
- Check if port 5000 is in use
- Ensure all dependencies are installed
- Try: `pip install -r requirements.txt --upgrade`

### API Keys Not Saving
- Verify `data/` directory exists
- Check browser console for errors
- Ensure database has write permissions

### Jobs Not Processing
- Restart server to restart worker thread
- Check server terminal for error messages
- Verify all API keys are valid

See [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md) for more troubleshooting.

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

MIT License - feel free to use for personal or commercial projects!

## 🌟 Star This Repo!

If you find this useful, give it a star ⭐ on GitHub!

---

**Made with ❤️ for content creators**

Need help? Check the [Issues](https://github.com/Starship01-akaSniper/youtube-shorts-automation/issues) page!
