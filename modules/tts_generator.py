"""
Text-to-Speech Generator Module
Converts scripts to audio using OpenAI TTS or ElevenLabs
"""
from openai import OpenAI
import requests
from pathlib import Path
from config import config

class TTSGenerator:
    """Generate voiceover audio from text"""
    
    def __init__(self):
        """Initialize TTS generator based on config"""
        self.service = config.TTS_SERVICE
        
        if self.service == 'openai':
            self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        elif self.service == 'elevenlabs':
            self.api_key = config.ELEVENLABS_API_KEY
    
    def generate(self, text: str, output_path: str = None) -> str:
        """
        Generate speech audio from text
        
        Args:
            text: The script text to convert to speech
            output_path: Where to save the audio file (optional)
            
        Returns:
            Path to the generated audio file
        """
        if output_path is None:
            output_path = config.TEMP_DIR / "voiceover.mp3"
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🎤 Generating voiceover using {self.service.upper()}...")
        
        try:
            if self.service == 'openai':
                return self._generate_openai(text, output_path)
            elif self.service == 'elevenlabs':
                return self._generate_elevenlabs(text, output_path)
        except Exception as e:
            print(f"❌ Error generating TTS: {e}")
            raise
    
    def _generate_openai(self, text: str, output_path: Path) -> str:
        """Generate using OpenAI TTS"""
        response = self.client.audio.speech.create(
            model="tts-1",  # Use "tts-1-hd" for higher quality
            voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
            input=text,
            speed=1.0
        )
        
        response.stream_to_file(str(output_path))
        
        print(f"✅ Voiceover generated: {output_path}")
        return str(output_path)
    
    def _generate_elevenlabs(self, text: str, output_path: Path) -> str:
        """Generate using ElevenLabs"""
        VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Default voice (Rachel)
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Voiceover generated: {output_path}")
        return str(output_path)

if __name__ == "__main__":
    # Test the TTS generator
    generator = TTSGenerator()
    
    test_text = "Did you know that honey never spoils? Archaeologists have found 3000-year-old honey in Egyptian tombs that's still perfectly edible!"
    
    audio_file = generator.generate(test_text)
    print(f"\n✨ Audio saved to: {audio_file}")
