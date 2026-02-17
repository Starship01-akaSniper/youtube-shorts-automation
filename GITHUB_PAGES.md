# GitHub Pages Deployment

This repository is configured to host the web dashboard on GitHub Pages.

## Live Demo

**Frontend Demo:** https://starship01-akasniper.github.io/youtube-shorts-automation/

> **Note:** This is a UI preview only. The backend API is not hosted on GitHub Pages.

## For Full Functionality

To use the complete automation system:

### Option 1: Run Locally

```bash
git clone https://github.com/Starship01-akaSniper/youtube-shorts-automation.git
cd youtube-shorts-automation
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000

### Option 2: Deploy to Cloud

Deploy the full stack (frontend + backend) to:
- **Railway** (Free tier): [Deploy Guide](WEB_DEPLOYMENT.md#option-1-railway-recommended---free-tier)
- **Render** (Free tier): [Deploy Guide](WEB_DEPLOYMENT.md#option-2-render-free-tier)
- **Fly.io** (Free tier): [Deploy Guide](WEB_DEPLOYMENT.md#option-3-flyio-free-tier)

## What's on GitHub Pages

The GitHub Pages deployment shows:
- ✅ Modern web dashboard UI
- ✅ Navigation and layout
- ✅ Forms and interface design
- ✅ Responsive mobile design

## What Requires Backend

These features need the Flask backend running:
- ❌ API configuration saving
- ❌ Video creation
- ❌ Job monitoring
- ❌ Video library
- ❌ Statistics

## Architecture

```
Frontend (GitHub Pages)          Backend (Deploy Separately)
├── HTML/CSS/JS             →    ├── Flask API Server
├── Static Assets                ├── SQLite Database
└── UI Components                ├── Job Queue Worker
                                 └── Automation Modules
```

## GitHub Pages Setup

This repository uses the `docs/` folder for GitHub Pages deployment:

1. Frontend files copied to `docs/` folder
2. GitHub Pages serves from `docs/`
3. Access at: https://starship01-akasniper.github.io/youtube-shorts-automation/

---

For questions, see [README.md](README.md) or [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md)
