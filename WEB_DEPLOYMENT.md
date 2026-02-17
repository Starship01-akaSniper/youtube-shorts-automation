# Web Dashboard Deployment Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd youtube-shorts-automation
pip install -r requirements.txt
```

### 2. Start the Web Server

```bash
python app.py
```

The server will start on: **http://localhost:5000**

### 3. Access the Dashboard

Open your browser and navigate to: **http://localhost:5000**

---

## 📋 First-Time Setup

### Step 1: Configure API Keys

1. Click **Settings** in the navigation
2. Enter your API keys:
   - **Google Gemini** (FREE, required)
   - **OpenAI** (required) 
   - **Luma AI** (required)
   - **YouTube** (optional, for uploads)
3. Click **Save Configuration**

### Step 2: Create Your First Video

1. Click **Create Video** in the navigation
2. Enter your video script (150-200 words recommended)
3. Optionally add a title and description
4. Click **Generate Video**

### Step 3: Monitor Progress

1. Return to **Dashboard**
2. Watch the job progress in real-time
3. Once complete, download from the **Library**

---

## 🌐 Deploying to Cloud

### Option 1: Railway (Recommended - Free Tier)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Deploy:**
   ```bash
   railway init
   railway up
   ```

4. **Set Environment (if needed):**
   ```bash
   railway variables set FLASK_ENV=production
   ```

5. **Get URL:**
   ```bash
   railway open
   ```

### Option 2: Render (Free Tier)

1. Create account at https://render.com
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
5. Click **Create Web Service**

### Option 3: Fly.io (Free Tier)

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Launch:**
   ```bash
   fly launch
   ```

4. **Deploy:**
   ```bash
   fly deploy
   ```

### Option 4: Heroku

1. **Install Heroku CLI**
2. **Create app:**
   ```bash
   heroku create your-app-name
   ```

3. **Add Procfile:**
   ```
   web: python app.py
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

---

## 🔧 Configuration

### Environment Variables (Optional)

While the web UI handles API key configuration, you can also set environment variables:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### Database Location

The database is stored at: `data/automation.db`

API keys are encrypted using: `data/.secret_key`

**Important:** Back up these files regularly!

---

## 🔒 Security

### API Key Storage

- API keys entered via web UI are **encrypted** before storage
- Encryption key is stored separately in `data/.secret_key`
- Never commit `data/` directory to version control

### Production Security

For production deployments:

1. **Use HTTPS** (most cloud providers handle this automatically)
2. **Set strong passwords** for any authentication you add
3. **Backup database regularly**
4. **Monitor API usage** to avoid unexpected charges

---

## 📊 Monitoring

### Real-Time Status

The dashboard automatically refreshes:
- **Statistics:** Every 10 seconds
- **Active Jobs:** Every 5 seconds

### API Health Check

Check server health:
```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "queue_running": true,
  "database": "connected"
}
```

---

## 🎯 Production Optimization

### 1. Use Production WSGI Server

Instead of Flask's built-in server, use Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2. Enable Logging

Add logging configuration in `app.py`:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 3. Set Up Reverse Proxy

Use Nginx for better performance:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🐛 Troubleshooting

### Server Won't Start

**Error:** `Address already in use`

**Solution:** 
```bash
# Find process on port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process and restart
```

### Database Errors

**Error:** `database is locked`

**Solution:** Only one process should run at a time. Stop all instances and restart.

### API Keys Not Saving

**Error:** Configuration not persisting

**Solution:** 
1. Check `data/` directory exists and is writable
2. Verify `data/.secret_key` was created
3. Check browser console for JavaScript errors

### Jobs Not Processing

**Error:** Videos stuck in pending state

**Solution:**
1. Check job queue status: `curl http://localhost:5000/api/jobs/queue/status`
2. Restart server to restart worker thread
3. Check server logs for errors

---

## 📱 Mobile Access

The dashboard is fully responsive and works on mobile devices. Access from any device on your local network using your computer's IP address:

```
http://YOUR_LOCAL_IP:5000
```

Find your IP:
- **Windows:** `ipconfig`
- **macOS/Linux:** `ifconfig` or `ip addr`

---

## 🔄 Updating

To update the application:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
python app.py
```

---

## 💡 Tips

1. **Keep server running:** Use `screen` or `tmux` for persistent sessions
2. **Monitor costs:** Check your API usage dashboards regularly
3. **Backup database:** Copy `data/` directory before major updates
4. **Test locally first:** Always test new features locally before deploying

---

## 🆘 Support

- Check logs in terminal where `app.py` is running
- Review browser console for frontend errors
- Ensure all API keys are valid and have sufficient credits

---

## 🎉 You're Ready!

Your YouTube Shorts automation web application is now deployed and ready to use. Create amazing content effortlessly! 🚀
