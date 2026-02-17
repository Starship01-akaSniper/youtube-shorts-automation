"""
Video Assembler Module
Combines video, audio, and captions using FFmpeg
"""
import subprocess
from pathlib import Path
from config import config

class VideoAssembler:
    """Assemble final video from components"""
    
    def __init__(self):
        """Initialize video assembler"""
        self._check_ffmpeg()
    
    def _check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "FFmpeg not found! Please install FFmpeg:\n"
                "  Windows: Download from https://ffmpeg.org/download.html\n"
                "  macOS: brew install ffmpeg\n"
                "  Linux: sudo apt-get install ffmpeg"
            )
    
    def assemble(self, video_path: str, audio_path: str, captions_path: str = None, 
                 output_path: str = None) -> str:
        """
        Combine video, audio, and optionally captions into final video
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            captions_path: Path to SRT caption file (optional)
            output_path: Where to save final video
            
        Returns:
            Path to the assembled video
        """
        video_path = Path(video_path)
        audio_path = Path(audio_path)
        
        if output_path is None:
            output_path = config.OUTPUT_DIR / "final_video.mp4"
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🎞️ Assembling final video...")
        
        # Build FFmpeg command
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output file
            '-i', str(video_path),  # Input video
            '-i', str(audio_path),  # Input audio
        ]
        
        # Add subtitle filter if captions provided
        if captions_path and Path(captions_path).exists():
            print("   📝 Adding captions...")
            # Escape the subtitle path for FFmpeg
            srt_path = str(Path(captions_path)).replace('\\', '/').replace(':', '\\:')
            
            cmd.extend([
                '-vf', f"subtitles='{srt_path}':force_style='FontName=Arial Bold,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=2,Shadow=1,Alignment=2'",
            ])
        
        # Output settings
        cmd.extend([
            '-c:v', 'libx264',  # Video codec
            '-preset', 'medium',  # Encoding speed/quality tradeoff
            '-crf', '23',  # Quality (lower = better, 18-28 typical)
            '-c:a', 'aac',  # Audio codec
            '-b:a', '192k',  # Audio bitrate
            '-ar', '44100',  # Audio sample rate
            '-shortest',  # Match duration to shortest input
            '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
            '-movflags', '+faststart',  # Enable streaming
            str(output_path)
        ])
        
        try:
            print("   🔧 Running FFmpeg...")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            print(f"✅ Final video assembled: {output_path}")
            print(f"   Size: {output_path.stat().st_size / (1024*1024):.2f} MB")
            
            return str(output_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ FFmpeg error: {e.stderr}")
            raise

if __name__ == "__main__":
    # Test the video assembler
    assembler = VideoAssembler()
    print("✅ Video assembler initialized (FFmpeg found)")
    print("To test, provide video_path and audio_path to the assemble() method")
