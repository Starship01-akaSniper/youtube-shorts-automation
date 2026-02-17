"""
Configuration loader for YouTube Shorts Automation
Loads API keys and settings from environment variables
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API keys and settings"""
    
    # ===============================
    # API KEYS
    # ===============================
    
    # Content Generation
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    OPENAI_GPT_API_KEY = os.getenv('OPENAI_GPT_API_KEY', '')
    
    # Text-to-Speech
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')
    
    # Video Generation
    LUMA_API_KEY = os.getenv('LUMA_API_KEY', '')
    RUNWAY_API_KEY = os.getenv('RUNWAY_API_KEY', '')
    
    # YouTube Upload
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID', '')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET', '')
    
    # Optional Services
    MUBERT_API_KEY = os.getenv('MUBERT_API_KEY', '')
    
    # ===============================
    # SERVICE PREFERENCES
    # ===============================
    
    VIDEO_SERVICE = os.getenv('VIDEO_SERVICE', 'luma')  # 'luma' or 'runway'
    TTS_SERVICE = os.getenv('TTS_SERVICE', 'openai')    # 'openai' or 'elevenlabs'
    CONTENT_AI_SERVICE = os.getenv('CONTENT_AI_SERVICE', 'gemini')  # 'gemini' or 'gpt4'
    MUSIC_SERVICE = os.getenv('MUSIC_SERVICE', 'none')   # 'none' or 'mubert'
    
    # ===============================
    # VIDEO SETTINGS
    # ===============================
    
    VIDEO_FORMAT = os.getenv('VIDEO_FORMAT', 'vertical')
    VIDEO_WIDTH = int(os.getenv('VIDEO_WIDTH', 1080))
    VIDEO_HEIGHT = int(os.getenv('VIDEO_HEIGHT', 1920))
    VIDEO_FPS = int(os.getenv('VIDEO_FPS', 30))
    
    # ===============================
    # DIRECTORIES
    # ===============================
    
    OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', './output'))
    TEMP_DIR = OUTPUT_DIR / 'temp'
    SCRIPTS_DIR = Path('./scripts')
    
    # ===============================
    # API SETTINGS
    # ===============================
    
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 5))
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Validate that required API keys are present"""
        errors = []
        
        # Check content AI
        if cls.CONTENT_AI_SERVICE == 'gemini' and not cls.GEMINI_API_KEY:
            errors.append("❌ GEMINI_API_KEY is required (set in .env file)")
        elif cls.CONTENT_AI_SERVICE == 'gpt4' and not cls.OPENAI_GPT_API_KEY:
            errors.append("❌ OPENAI_GPT_API_KEY is required (set in .env file)")
        
        # Check TTS
        if cls.TTS_SERVICE == 'openai' and not cls.OPENAI_API_KEY:
            errors.append("❌ OPENAI_API_KEY is required (set in .env file)")
        elif cls.TTS_SERVICE == 'elevenlabs' and not cls.ELEVENLABS_API_KEY:
            errors.append("❌ ELEVENLABS_API_KEY is required (set in .env file)")
        
        # Check video generation
        if cls.VIDEO_SERVICE == 'luma' and not cls.LUMA_API_KEY:
            errors.append("❌ LUMA_API_KEY is required (set in .env file)")
        elif cls.VIDEO_SERVICE == 'runway' and not cls.RUNWAY_API_KEY:
            errors.append("❌ RUNWAY_API_KEY is required (set in .env file)")
        
        # Check YouTube
        if not cls.YOUTUBE_CLIENT_ID or not cls.YOUTUBE_CLIENT_SECRET:
            errors.append("❌ YouTube credentials required (YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET)")
        
        if errors:
            print("\n🔴 Configuration Errors:\n")
            for error in errors:
                print(f"  {error}")
            print("\n💡 Please check your .env file and add the required API keys.")
            print("   See .env.example for reference.\n")
            return False
        
        print("✅ Configuration validated successfully!")
        return True
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.TEMP_DIR.mkdir(parents=True, exist_ok=True)
        cls.SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directories created/verified")
    
    @classmethod
    def print_config(cls):
        """Print current configuration (without exposing full API keys)"""
        print("\n" + "="*50)
        print("  YOUTUBE SHORTS AUTOMATION - CONFIGURATION")
        print("="*50)
        
        print(f"\n📹 Video Service: {cls.VIDEO_SERVICE.upper()}")
        print(f"🎤 TTS Service: {cls.TTS_SERVICE.upper()}")
        print(f"🤖 Content AI: {cls.CONTENT_AI_SERVICE.upper()}")
        print(f"🎵 Music Service: {cls.MUSIC_SERVICE.upper()}")
        
        print(f"\n📐 Video Settings:")
        print(f"   Format: {cls.VIDEO_FORMAT}")
        print(f"   Resolution: {cls.VIDEO_WIDTH}x{cls.VIDEO_HEIGHT}")
        print(f"   FPS: {cls.VIDEO_FPS}")
        
        print(f"\n📁 Output Directory: {cls.OUTPUT_DIR}")
        
        # Show masked API keys
        def mask_key(key):
            if not key or len(key) < 8:
                return "❌ NOT SET"
            return f"✅ {key[:4]}...{key[-4:]}"
        
        print(f"\n🔑 API Keys Status:")
        if cls.CONTENT_AI_SERVICE == 'gemini':
            print(f"   Gemini API: {mask_key(cls.GEMINI_API_KEY)}")
        if cls.TTS_SERVICE == 'openai':
            print(f"   OpenAI API: {mask_key(cls.OPENAI_API_KEY)}")
        if cls.VIDEO_SERVICE == 'luma':
            print(f"   Luma AI API: {mask_key(cls.LUMA_API_KEY)}")
        print(f"   YouTube Client ID: {mask_key(cls.YOUTUBE_CLIENT_ID)}")
        
        print("\n" + "="*50 + "\n")

# Initialize configuration on import
config = Config()
