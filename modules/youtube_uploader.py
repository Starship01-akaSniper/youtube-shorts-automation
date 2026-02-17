"""
YouTube Uploader Module
Uploads videos to YouTube using YouTube Data API v3
"""
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
from pathlib import Path
from config import config

class YouTubeUploader:
    """Upload videos to YouTube"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self):
        """Initialize YouTube uploader"""
        self.credentials = None
        self.youtube = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with YouTube API"""
        token_file = Path('token.pickle')
        creds_file = Path('client_secrets.json')
        
        # Load existing credentials
        if token_file.exists():
            with open(token_file, 'rb') as token:
                self.credentials = pickle.load(token)
        
        # Refresh or get new credentials
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                print("🔄 Refreshing YouTube credentials...")
                self.credentials.refresh(Request())
            else:
                # Create client_secrets.json if it doesn't exist
                if not creds_file.exists():
                    self._create_client_secrets()
                
                print("🔐 Authenticating with YouTube...")
                print("   A browser window will open for authorization...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(creds_file), self.SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_file, 'wb') as token:
                pickle.dump(self.credentials, token)
            
            print("✅ YouTube authentication successful")
        
        # Build YouTube API client
        self.youtube = build('youtube', 'v3', credentials=self.credentials)
    
    def _create_client_secrets(self):
        """Create client_secrets.json from environment variables"""
        import json
        
        client_secrets = {
            "installed": {
                "client_id": config.YOUTUBE_CLIENT_ID,
                "client_secret": config.YOUTUBE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": ["http://localhost"]
            }
        }
        
        with open('client_secrets.json', 'w') as f:
            json.dump(client_secrets, f, indent=2)
        
        print("✅ Created client_secrets.json from environment variables")
    
    def upload(self, video_path: str, title: str, description: str, 
               tags: list = None, category: str = "22") -> str:
        """
        Upload video to YouTube
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags (optional)
            category: YouTube category ID (22 = People & Blogs)
            
        Returns:
            Video ID of uploaded video
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        print(f"\n📤 Uploading to YouTube...")
        print(f"   Title: {title}")
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category
            },
            'status': {
                'privacyStatus': 'private',  # Options: 'private', 'unlisted', 'public'
                'selfDeclaredMadeForKids': False,
            }
        }
        
        # Create media upload
        media = MediaFileUpload(
            str(video_path),
            chunksize=-1,  # Upload in a single request
            resumable=True,
            mimetype='video/mp4'
        )
        
        try:
            # Execute upload
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            print("   ⏳ Uploading...")
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"   📊 Upload progress: {progress}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"✅ Video uploaded successfully!")
            print(f"   Video ID: {video_id}")
            print(f"   URL: {video_url}")
            print(f"   ⚠️  Status: PRIVATE (change in YouTube Studio)")
            
            return video_id
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            raise

if __name__ == "__main__":
    # Test the YouTube uploader (requires authentication)
    uploader = YouTubeUploader()
    print("✅ YouTube uploader initialized")
    print("To test, provide video_path, title, and description to the upload() method")
