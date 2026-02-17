# YouTube Shorts Automation

An AI-powered automation system that generates YouTube Shorts from scripts. Simply provide a script, and the system will automatically create a professional video with voiceover, captions, music, and publish it to YouTube.

## 🎯 Features

- **Video Generation**: AI-powered video creation from text prompts
- **Text-to-Speech**: Professional voiceover generation
- **Auto-Captions**: Automatic subtitle generation
- **Content Generation**: AI-generated titles, descriptions, and tags
- **YouTube Upload**: Automatic publishing to YouTube

## 💰 Cost Per Video

Using the recommended FREE/budget setup:
- **Video Generation**: $0.20 (Luma AI)
- **Text-to-Speech**: $0.02 (OpenAI TTS)
- **Content AI**: $0.00 (Google Gemini FREE API)
- **Captions**: $0.01 (Whisper)
- **Total**: ~$0.23 per video

## 📋 Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system
- API keys for the services you want to use

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd youtube-shorts-automation
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys (see Configuration section below).

### 3. Run Your First Video

```bash
python main.py
```

Follow the prompts to:
1. Enter your video script
2. Choose your preferences
3. Watch as the system creates and uploads your video!

## ⚙️ Configuration

### Required API Keys

Edit the `.env` file and add your API keys:

```env
# === FREE OPTION (Recommended for starting) ===
# Google Gemini API - FREE (1,000 requests/day)
GEMINI_API_KEY=your_gemini_api_key_here

# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Luma AI API
LUMA_API_KEY=your_luma_api_key_here

# YouTube Data API v3
YOUTUBE_API_KEY=your_youtube_api_key_here
YOUTUBE_CLIENT_ID=your_client_id_here
YOUTUBE_CLIENT_SECRET=your_client_secret_here
```

### How to Get API Keys

1. **Google Gemini API** (FREE - Recommended)
   - Visit: https://ai.google.dev/
   - Click "Get API key in Google AI Studio"
   - Create a new project and generate an API key
   - Free tier: 1,000 requests per day

2. **OpenAI API**
   - Visit: https://platform.openai.com/api-keys
   - Create an account and generate an API key
   - Add $5-10 credit to start

3. **Luma AI API**
   - Visit: https://lumaapi.com/ or https://piapi.ai/
   - Sign up for API access
   - Pay-as-you-go: $0.20 per video

4. **YouTube Data API v3**
   - Visit: https://console.cloud.google.com/
   - Create a new project
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials

## 📁 Project Structure

```
youtube-shorts-automation/
├── main.py                 # Main entry point
├── config.py              # Configuration loader
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment file
├── .env                  # Your API keys (do not commit!)
├── modules/
│   ├── video_generator.py    # Video generation (Luma AI)
│   ├── tts_generator.py      # Text-to-speech (OpenAI)
│   ├── content_generator.py  # Titles/descriptions (Gemini)
│   ├── caption_generator.py  # Auto-captions (Whisper)
│   ├── video_assembler.py    # FFmpeg video assembly
│   └── youtube_uploader.py   # YouTube upload
├── output/               # Generated videos
└── scripts/             # Example video scripts
```

## 🎬 Usage Examples

### Simple Mode (Interactive)
```bash
python main.py
```

### Advanced Mode (Programmatic)
```python
from modules import VideoGenerator, TTSGenerator, ContentGenerator

# Your script
script = "Did you know that honey never spoils? Archaeologists have found 3000-year-old honey in Egyptian tombs that's still edible!"

# Generate video
video = VideoGenerator.create(script)
audio = TTSGenerator.generate(script)
metadata = ContentGenerator.generate(script)

# Upload to YouTube
YouTubeUploader.upload(video, audio, metadata)
```

## 🔧 Customization

### Change Video Service
Edit `config.py` to switch between Luma AI and Runway:

```python
VIDEO_SERVICE = "luma"  # Options: "luma", "runway"
```

### Change TTS Service
```python
TTS_SERVICE = "openai"  # Options: "openai", "elevenlabs"
```

### Change Content AI
```python
CONTENT_AI = "gemini"  # Options: "gemini", "gpt4", "claude"
```

## 📊 Cost Optimization

- **FREE Option**: Use Google Gemini API (free up to 1,000 requests/day)
- **Budget**: Luma AI ($0.20) + OpenAI TTS ($0.02) + Gemini (free) = $0.23/video
- **Quality**: Runway ($3.00) + ElevenLabs ($0.30) + GPT-4 ($0.01) = $3.31/video

## 🐛 Troubleshooting

### FFmpeg Not Found
Install FFmpeg:
- **Windows**: Download from https://ffmpeg.org/download.html
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

### API Rate Limits
- Gemini: 1,000 requests/day (free tier)
- YouTube: 6 uploads/day (new channels)
- Adjust frequency in config if you hit limits

### Video Generation Fails
- Check your API key validity
- Ensure you have sufficient credits
- Check service status pages

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This tool is for educational purposes. Ensure you comply with:
- YouTube's Terms of Service
- Each API provider's terms
- Copyright laws for any content you generate

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Made with ❤️ for content creators**
