"""
Database manager for YouTube Shorts Automation
Handles API keys, videos, jobs, and schedules
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
import os

class Database:
    """Database manager with encryption for API keys"""
    
    def __init__(self, db_path="data/automation.db"):
        """Initialize database"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get or create encryption key
        self.key = self._get_encryption_key()
        self.cipher = Fernet(self.key)
        
        self._init_db()
    
    def _get_encryption_key(self):
        """Get or create encryption key for API keys"""
        key_file = Path("data/.secret_key")
        key_file.parent.mkdir(parents=True, exist_ok=True)
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            # Set file permissions to read-only for owner
            os.chmod(key_file, 0o600)
            return key
    
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # API Keys table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT UNIQUE NOT NULL,
                key_value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Videos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                script TEXT NOT NULL,
                video_path TEXT,
                thumbnail_path TEXT,
                youtube_id TEXT,
                youtube_url TEXT,
                status TEXT DEFAULT 'pending',
                tags TEXT,
                duration INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        # Jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                status TEXT DEFAULT 'pending',
                progress INTEGER DEFAULT 0,
                current_step TEXT,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos (id)
            )
        ''')
        
        # Schedules table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                frequency TEXT NOT NULL,
                time TEXT,
                days TEXT,
                script_source TEXT,
                auto_upload BOOLEAN DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                last_run TIMESTAMP,
                next_run TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ==================== API Keys ====================
    
    def save_api_key(self, service, key_value):
        """Save encrypted API key"""
        encrypted = self.cipher.encrypt(key_value.encode())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO api_keys (service, key_value, updated_at)
            VALUES (?, ?, ?)
        ''', (service, encrypted.decode(), datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_api_key(self, service):
        """Get decrypted API key"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT key_value FROM api_keys WHERE service = ?', (service,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            encrypted = result[0].encode()
            return self.cipher.decrypt(encrypted).decode()
        return None
    
    def get_configured_services(self):
        """Get list of configured services"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT service, updated_at FROM api_keys')
        results = cursor.fetchall()
        conn.close()
        
        return [{'service': r[0], 'updated_at': r[1]} for r in results]
    
    # ==================== Videos ====================
    
    def create_video(self, script, title=None, description=None):
        """Create new video record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO videos (script, title, description, status)
            VALUES (?, ?, ?, 'pending')
        ''', (script, title or 'Untitled Video', description or ''))
        
        video_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return video_id
    
    def update_video(self, video_id, **kwargs):
        """Update video record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fields = []
        values = []
        for key, value in kwargs.items():
            if key == 'tags' and isinstance(value, list):
                value = json.dumps(value)
            fields.append(f"{key} = ?")
            values.append(value)
        
        values.append(video_id)
        query = f"UPDATE videos SET {', '.join(fields)} WHERE id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    
    def get_video(self, video_id):
        """Get video by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM videos WHERE id = ?', (video_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            video = dict(result)
            if video.get('tags'):
                video['tags'] = json.loads(video['tags'])
            return video
        return None
    
    def get_all_videos(self, status=None, limit=50):
        """Get all videos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT * FROM videos WHERE status = ?
                ORDER BY created_at DESC LIMIT ?
            ''', (status, limit))
        else:
            cursor.execute('''
                SELECT * FROM videos
                ORDER BY created_at DESC LIMIT ?
            ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        videos = []
        for r in results:
            video = dict(r)
            if video.get('tags'):
                video['tags'] = json.loads(video['tags'])
            videos.append(video)
        
        return videos
    
    # ==================== Jobs ====================
    
    def create_job(self, video_id):
        """Create new job"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO jobs (video_id, status, current_step)
            VALUES (?, 'pending', 'Queued')
        ''', (video_id,))
        
        job_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return job_id
    
    def update_job(self, job_id, **kwargs):
        """Update job record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            values.append(value)
        
        values.append(job_id)
        query = f"UPDATE jobs SET {', '.join(fields)} WHERE id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    
    def get_job(self, job_id):
        """Get job by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT j.*, v.script, v.title
            FROM jobs j
            LEFT JOIN videos v ON j.video_id = v.id
            WHERE j.id = ?
        ''', (job_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return dict(result) if result else None
    
    def get_all_jobs(self, status=None, limit=50):
        """Get all jobs"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT j.*, v.title, v.script
                FROM jobs j
                LEFT JOIN videos v ON j.video_id = v.id
                WHERE j.status = ?
                ORDER BY j.created_at DESC LIMIT ?
            ''', (status, limit))
        else:
            cursor.execute('''
                SELECT j.*, v.title, v.script
                FROM jobs j
                LEFT JOIN videos v ON j.video_id = v.id
                ORDER BY j.created_at DESC LIMIT ?
            ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [dict(r) for r in results]
    
    # ==================== Schedules ====================
    
    def create_schedule(self, name, frequency, **kwargs):
        """Create new schedule"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO schedules (name, frequency, time, days, script_source, auto_upload, active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            name,
            frequency,
            kwargs.get('time'),
            kwargs.get('days'),
            kwargs.get('script_source'),
            kwargs.get('auto_upload', False),
            kwargs.get('active', True)
        ))
        
        schedule_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return schedule_id
    
    def get_all_schedules(self, active_only=False):
        """Get all schedules"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if active_only:
            cursor.execute('SELECT * FROM schedules WHERE active = 1 ORDER BY created_at DESC')
        else:
            cursor.execute('SELECT * FROM schedules ORDER BY created_at DESC')
        
        results = cursor.fetchall()
        conn.close()
        
        return [dict(r) for r in results]

# Initialize global database instance
db = Database()
