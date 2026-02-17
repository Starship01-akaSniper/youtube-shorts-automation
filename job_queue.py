"""
Background job queue processor
Handles async video creation tasks
"""
import threading
import time
from datetime import datetime
from database import db
from modules import (
    ContentGenerator,
    TTSGenerator,
    VideoGenerator,
    CaptionGenerator,
    VideoAssembler,
    YouTubeUploader
)
from pathlib import Path

class JobQueue:
    """Background job processor for video creation"""
    
    def __init__(self):
        """Initialize job queue"""
        self.running = False
        self.worker_thread = None
        self.current_job = None
    
    def start(self):
        """Start the job queue worker"""
        if self.running:
            print("⚠️  Job queue already running")
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        print("[OK] Job queue worker started")
    
    def stop(self):
        """Stop the job queue worker"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        print("[STOP] Job queue worker stopped")
    
    def submit_job(self, video_id):
        """Submit a new job to the queue"""
        job_id = db.create_job(video_id)
        print(f"[NEW] Job {job_id} created for video {video_id}")
        return job_id
    
    def _worker(self):
        """Background worker that processes jobs"""
        print("[WORKER] Job queue worker running...")
        
        while self.running:
            # Get next pending job
            jobs = db.get_all_jobs(status='pending', limit=1)
            
            if jobs:
                job = jobs[0]
                self.current_job = job
                self._process_job(job)
                self.current_job = None
            else:
                # No jobs, sleep for a bit
                time.sleep(2)
    
    def _process_job(self, job):
        """Process a single job"""
        job_id = job['id']
        video_id = job['video_id']
        
        print(f"\n{'='*60}")
        print(f"  PROCESSING JOB {job_id} (Video {video_id})")
        print(f"{'='*60}\n")
        
        try:
            # Mark job as processing
            db.update_job(job_id, 
                status='processing',
                started_at=datetime.now(),
                current_step='Initializing',
                progress=0
            )
            
            # Get video details
            video = db.get_video(video_id)
            script = video['script']
            
            # Get API keys from database
            api_keys = self._load_api_keys()
            
            # Initialize modules with API keys
            content_gen = ContentGenerator()
            tts_gen = TTSGenerator()
            video_gen = VideoGenerator()
            caption_gen = CaptionGenerator()
            video_assembler = VideoAssembler()
            
            # Create output directory
            output_dir = Path(f"output/video_{video_id}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Step 1: Generate content metadata
            db.update_job(job_id, current_step='Generating content metadata', progress=10)
            metadata = content_gen.generate(script)
            
            # Update video with metadata
            db.update_video(video_id,
                title=metadata['title'],
                description=metadata['description'],
                tags=metadata['tags']
            )
            
            # Step 2: Generate voiceover
            db.update_job(job_id, current_step='Generating voiceover', progress=25)
            audio_path = tts_gen.generate(
                script,
                output_path=output_dir / "audio.mp3"
            )
            
            # Step 3: Generate video
            db.update_job(job_id, current_step='Generating video (2-5 min)', progress=40)
            video_prompt = f"High quality cinematic video: {script[:100]}"
            video_path = video_gen.generate(
                video_prompt,
                output_path=output_dir / "video_raw.mp4"
            )
            
            # Step 4: Generate captions
            db.update_job(job_id, current_step='Generating captions', progress=70)
            captions_path = caption_gen.generate(
                audio_path,
                output_path=output_dir / "captions.srt"
            )
            
            # Step 5: Assemble final video
            db.update_job(job_id, current_step='Assembling final video', progress=85)
            final_video_path = video_assembler.assemble(
                video_path,
                audio_path,
                captions_path,
                output_path=output_dir / "final_video.mp4"
            )
            
            # Update video record
            db.update_video(video_id,
                video_path=str(final_video_path),
                status='completed',
                completed_at=datetime.now()
            )
            
            # Mark job as completed
            db.update_job(job_id,
                status='completed',
                current_step='Completed',
                progress=100,
                completed_at=datetime.now()
            )
            
            print(f"\n[SUCCESS] Job {job_id} completed successfully!")
            
        except Exception as e:
            print(f"\n[ERROR] Job {job_id} failed: {e}")
            import traceback
            traceback.print_exc()
            
            # Mark job as failed
            db.update_job(job_id,
                status='failed',
                current_step='Failed',
                error_message=str(e),
                completed_at=datetime.now()
            )
            
            db.update_video(video_id, status='failed')
    
    def _load_api_keys(self):
        """Load API keys from database and set in environment"""
        import os
        
        keys_mapping = {
            'gemini': 'GEMINI_API_KEY',
            'openai': 'OPENAI_API_KEY',
            'luma': 'LUMA_API_KEY',
            'youtube_client_id': 'YOUTUBE_CLIENT_ID',
            'youtube_client_secret': 'YOUTUBE_CLIENT_SECRET',
        }
        
        api_keys = {}
        for service, env_var in keys_mapping.items():
            key = db.get_api_key(service)
            if key:
                os.environ[env_var] = key
                api_keys[service] = key
        
        return api_keys
    
    def get_status(self):
        """Get current worker status"""
        return {
            'running': self.running,
            'current_job': self.current_job,
            'pending_jobs': len(db.get_all_jobs(status='pending')),
            'processing_jobs': len(db.get_all_jobs(status='processing'))
        }

# Global job queue instance
job_queue = JobQueue()
