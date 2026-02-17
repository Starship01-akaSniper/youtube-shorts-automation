"""
Flask API Server for YouTube Shorts Automation
Provides REST API for web dashboard
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from database import db
from job_queue import job_queue
import os

app = Flask(__name__, static_folder='web', static_url_path='')
CORS(app)

# Start job queue worker
job_queue.start()

# ==================== Frontend Routes ====================

@app.route('/')
def index():
    """Serve main dashboard"""
    return send_from_directory('web', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('web', path)

# ==================== API Configuration ====================

@app.route('/api/config/status', methods=['GET'])
def get_config_status():
    """Get configuration status"""
    services = db.get_configured_services()
    
    required_services = ['gemini', 'openai', 'luma']
    optional_services = ['youtube_client_id', 'youtube_client_secret', 'elevenlabs', 'runway']
    
    configured = {s['service'] for s in services}
    
    return jsonify({
        'configured_services': services,
        'required_configured': all(s in configured for s in required_services),
        'required_services': required_services,
        'optional_services': optional_services
    })

@app.route('/api/config/save', methods=['POST'])
def save_config():
    """Save API configuration"""
    data = request.json
    
    try:
        for service, key in data.items():
            if key and key.strip():  # Only save non-empty keys
                db.save_api_key(service, key.strip())
        
        return jsonify({'success': True, 'message': 'Configuration saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== Video Management ====================

@app.route('/api/videos', methods=['GET'])
def get_videos():
    """Get all videos"""
    status = request.args.get('status')
    limit = int(request.args.get('limit', 50))
    
    videos = db.get_all_videos(status=status, limit=limit)
    return jsonify(videos)

@app.route('/api/videos/<int:video_id>', methods=['GET'])
def get_video(video_id):
    """Get specific video"""
    video = db.get_video(video_id)
    if video:
        return jsonify(video)
    return jsonify({'error': 'Video not found'}), 404

@app.route('/api/videos/create', methods=['POST'])
def create_video():
    """Create new video and start processing"""
    data = request.json
    
    script = data.get('script')
    if not script:
        return jsonify({'error': 'Script is required'}), 400
    
    try:
        # Create video record
        video_id = db.create_video(
            script=script,
            title=data.get('title'),
            description=data.get('description')
        )
        
        # Submit job to queue
        job_id = job_queue.submit_job(video_id)
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'job_id': job_id,
            'message': 'Video creation started'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/videos/<int:video_id>/download', methods=['GET'])
def download_video(video_id):
    """Download video file"""
    video = db.get_video(video_id)
    if not video or not video.get('video_path'):
        return jsonify({'error': 'Video not found or not ready'}), 404
    
    video_path = Path(video['video_path'])
    if not video_path.exists():
        return jsonify({'error': 'Video file not found'}), 404
    
    return send_from_directory(
        video_path.parent,
        video_path.name,
        as_attachment=True,
        download_name=f"{video['title']}.mp4"
    )

# ==================== Job Management ====================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs"""
    status = request.args.get('status')
    limit = int(request.args.get('limit', 50))
    
    jobs = db.get_all_jobs(status=status, limit=limit)
    return jsonify(jobs)

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get specific job"""
    job = db.get_job(job_id)
    if job:
        return jsonify(job)
    return jsonify({'error': 'Job not found'}), 404

@app.route('/api/jobs/queue/status', methods=['GET'])
def get_queue_status():
    """Get job queue status"""
    return jsonify(job_queue.get_status())

# ==================== Schedules ====================

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    """Get all schedules"""
    active_only = request.args.get('active', 'false').lower() == 'true'
    schedules = db.get_all_schedules(active_only=active_only)
    return jsonify(schedules)

@app.route('/api/schedules/create', methods=['POST'])
def create_schedule():
    """Create new schedule"""
    data = request.json
    
    try:
        schedule_id = db.create_schedule(
            name=data['name'],
            frequency=data['frequency'],
            time=data.get('time'),
            days=data.get('days'),
            script_source=data.get('script_source'),
            auto_upload=data.get('auto_upload', False)
        )
        
        return jsonify({
            'success': True,
            'schedule_id': schedule_id,
            'message': 'Schedule created successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== Statistics ====================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    all_videos = db.get_all_videos(limit=1000)
    all_jobs = db.get_all_jobs(limit=1000)
    
    stats = {
        'total_videos': len(all_videos),
        'completed_videos': len([v for v in all_videos if v['status'] == 'completed']),
        'pending_videos': len([v for v in all_videos if v['status'] == 'pending']),
        'failed_videos': len([v for v in all_videos if v['status'] == 'failed']),
        'total_jobs': len(all_jobs),
        'completed_jobs': len([j for j in all_jobs if j['status'] == 'completed']),
        'pending_jobs': len([j for j in all_jobs if j['status'] == 'pending']),
        'processing_jobs': len([j for j in all_jobs if j['status'] == 'processing']),
        'failed_jobs': len([j for j in all_jobs if j['status'] == 'failed']),
    }
    
    return jsonify(stats)

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'queue_running': job_queue.running,
        'database': 'connected'
    })

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== Main ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  YOUTUBE SHORTS AUTOMATION - WEB SERVER")
    print("="*60)
    print("\n[START] Starting server...")
    print("[URL] Dashboard: http://localhost:5000")
    print("[API] API Docs: http://localhost:5000/api/health")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
