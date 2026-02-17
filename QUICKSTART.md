# Quick Start Guide - YouTube Shorts Automation

Follow these steps to get your first video created in minutes!

## Step 1: Install Python & FFmpeg

### Python 3.8+
- Download from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### FFmpeg
- **Windows**: Download from https://ffmpeg.org/download.html and add to PATH
- **macOS**: Run `brew install ffmpeg`
- **Linux**: Run `sudo apt-get install ffmpeg`

## Step 2: Setup Project

```bash
# Navigate to project directory
cd youtube-shorts-automation

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure API Keys

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your API keys:

### Get Google Gemini API (FREE)
1. Go to: https://ai.google.dev/
2. Click "Get API key in Google AI Studio"
3. Create a new project
4. Generate API key
5. Add to `.env`: `GEMINI_API_KEY=your_key_here`

### Get OpenAI API
1. Go to: https://platform.openai.com/api-keys
2. Create account and generate API key
3. Add $5-10 credit
4. Add to `.env`: `OPENAI_API_KEY=your_key_here`

### Get Luma AI API
1. Go to: https://lumaapi.com/ or https://piapi.ai/
2. Sign up for API access
3. Add to `.env`: `LUMA_API_KEY=your_key_here`

### Get YouTube API
1. Go to: https://console.cloud.google.com/
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials
5. Add Client ID and Secret to `.env`

## Step 4: Run Your First Video!

### Interactive Mode (Easiest)
```bash
python main.py --interactive
```

Then:
1. Paste your script
2. Press Ctrl+D (or Ctrl+Z on Windows) when done
3. Choose whether to upload
4. Wait for magic! ✨

### Command Line Mode
```bash
python main.py --script "Your amazing script here" --upload
```

### From File
```bash
python main.py --script-file scripts/example_honey.txt
```

## Step 5: Check Your Output

Your video will be saved in the `output/` directory!

If you chose to upload, check YouTube Studio for your new video (it will be PRIVATE by default).

## Common Issues

### "FFmpeg not found"
- Make sure FFmpeg is installed and in your PATH
- Restart your terminal after installation
- Test with: `ffmpeg -version`

### "API key not valid"
- Double-check your `.env` file for typos
- Make sure there are no extra spaces
- Verify keys are active in respective platforms

### "YouTube authentication failed"
- Make sure you have OAuth 2.0 credentials, not just API key
- Check that YouTube Data API v3 is enabled in Google Cloud Console

## Tips for Best Results

1. **Scripts**: Keep them 150-200 words for 60-second videos
2. **Video Prompts**: Be descriptive but concise
3. **Cost Saving**: Use Gemini (free) + Luma AI ($0.20/video)
4. **Quality**: Use Runway + ElevenLabs for premium content

## Need Help?

Check the main README.md for detailed documentation and troubleshooting!

Happy creating! 🎥✨
