"""
Caption Generator Module
Generates subtitles/captions using OpenAI Whisper API
"""
from openai import OpenAI
from pathlib import Path
from config import config
import json

class CaptionGenerator:
    """Generate captions/subtitles from audio"""
    
    def __init__(self):
        """Initialize caption generator"""
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    def generate(self, audio_path: str, output_path: str = None) -> str:
        """
        Generate SRT captions from audio file
        
        Args:
            audio_path: Path to audio file
            output_path: Where to save the SRT file (optional)
            
        Returns:
            Path to the SRT caption file
        """
        audio_path = Path(audio_path)
        
        if output_path is None:
            output_path = config.TEMP_DIR / "captions.srt"
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📝 Generating captions using Whisper API...")
        
        try:
            # Transcribe audio with timestamps
            with open(audio_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["word"]
                )
            
            # Convert to SRT format
            srt_content = self._create_srt(transcript)
            
            # Save SRT file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            print(f"✅ Captions generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error generating captions: {e}")
            raise
    
    def _create_srt(self, transcript) -> str:
        """Convert Whisper transcript to SRT format"""
        srt_lines = []
        
        # Group words into subtitle segments (every 3-5 words or 3 seconds)
        words = transcript.words
        segments = []
        current_segment = {
            'words': [],
            'start': 0,
            'end': 0
        }
        
        for i, word in enumerate(words):
            if not current_segment['words']:
                current_segment['start'] = word['start']
            
            current_segment['words'].append(word['word'])
            current_segment['end'] = word['end']
            
            # Create segment if we have 4 words or 3 seconds passed
            duration = current_segment['end'] - current_segment['start']
            if len(current_segment['words']) >= 4 or duration >= 3.0 or i == len(words) - 1:
                segments.append(current_segment.copy())
                current_segment = {'words': [], 'start': 0, 'end': 0}
        
        # Convert to SRT format
        for idx, segment in enumerate(segments, 1):
            start_time = self._format_timestamp(segment['start'])
            end_time = self._format_timestamp(segment['end'])
            text = ' '.join(segment['words'])
            
            srt_lines.append(f"{idx}")
            srt_lines.append(f"{start_time} --> {end_time}")
            srt_lines.append(text)
            srt_lines.append("")  # Blank line between subtitles
        
        return '\n'.join(srt_lines)
    
    def _format_timestamp(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

if __name__ == "__main__":
    # Test the caption generator
    # Note: You need an actual audio file to test this
    generator = CaptionGenerator()
    
    # Example usage (uncomment if you have an audio file):
    # audio_file = "path/to/your/audio.mp3"
    # caption_file = generator.generate(audio_file)
    # print(f"\n✨ Captions saved to: {caption_file}")
    
    print("Caption generator initialized successfully!")
    print("To test, provide an audio file path to the generate() method")
