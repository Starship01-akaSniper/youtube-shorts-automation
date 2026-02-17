"""
Video Generator Module
Creates AI-generated videos using Luma AI or Runway
"""
import requests
import time
from pathlib import Path
from config import config

class VideoGenerator:
    """Generate video from text prompts"""
    
    def __init__(self):
        """Initialize video generator based on config"""
        self.service = config.VIDEO_SERVICE
        
        if self.service == 'luma':
            self.api_key = config.LUMA_API_KEY
            self.base_url = "https://api.piapi.ai/api/luma"  # Third-party API endpoint
        elif self.service == 'runway':
            self.api_key = config.RUNWAY_API_KEY
            self.base_url = "https://api.runwayml.com/v1"
    
    def generate(self, prompt: str, duration: int = 5, output_path: str = None) -> str:
        """
        Generate video from text prompt
        
        Args:
            prompt: Text description of the video
            duration: Video duration in seconds (default: 5)
            output_path: Where to save the video file
            
        Returns:
            Path to the generated video file
        """
        if output_path is None:
            output_path = config.TEMP_DIR / "generated_video.mp4"
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🎬 Generating video using {self.service.upper()}...")
        print(f"   Prompt: {prompt}")
        
        try:
            if self.service == 'luma':
                return self._generate_luma(prompt, output_path)
            elif self.service == 'runway':
                return self._generate_runway(prompt, duration, output_path)
        except Exception as e:
            print(f"❌ Error generating video: {e}")
            raise
    
    def _generate_luma(self, prompt: str, output_path: Path) -> str:
        """Generate video using Luma AI"""
        
        # Step 1: Create generation task
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "aspect_ratio": "9:16",  # Vertical for Shorts
            "expand_prompt": True
        }
        
        print("   📤 Submitting video generation request...")
        response = requests.post(
            f"{self.base_url}/generations",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        task_id = response.json()['id']
        print(f"   ⏳ Task ID: {task_id}")
        print("   ⏳ Waiting for video generation (this may take 2-5 minutes)...")
        
        # Step 2: Poll for completion
        max_attempts = 60  # 10 minutes max
        for attempt in range(max_attempts):
            time.sleep(10)  # Check every 10 seconds
            
            status_response = requests.get(
                f"{self.base_url}/generations/{task_id}",
                headers=headers
            )
            status_response.raise_for_status()
            
            result = status_response.json()
            state = result.get('state')
            
            print(f"   ⏳ Status: {state} ({attempt + 1}/{max_attempts})")
            
            if state == 'completed':
                video_url = result['video']['url']
                
                # Step 3: Download video
                print("   📥 Downloading video...")
                video_data = requests.get(video_url)
                video_data.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(video_data.content)
                
                print(f"✅ Video generated: {output_path}")
                return str(output_path)
            
            elif state == 'failed':
                raise Exception(f"Video generation failed: {result.get('failure_reason')}")
        
        raise TimeoutError("Video generation timed out")
    
    def _generate_runway(self, prompt: str, duration: int, output_path: Path) -> str:
        """Generate video using Runway Gen-3"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gen3a_turbo",  # or "gen3a" for higher quality
            "prompt": prompt,
            "duration": duration,
            "ratio": "9:16"  # Vertical for Shorts
        }
        
        print("   📤 Submitting video generation request...")
        response = requests.post(
            f"{self.base_url}/video/generate",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        task_id = response.json()['id']
        print(f"   ⏳ Task ID: {task_id}")
        print("   ⏳ Waiting for video generation...")
        
        # Poll for completion
        max_attempts = 60
        for attempt in range(max_attempts):
            time.sleep(10)
            
            status_response = requests.get(
                f"{self.base_url}/tasks/{task_id}",
                headers=headers
            )
            status_response.raise_for_status()
            
            result = status_response.json()
            status = result.get('status')
            
            print(f"   ⏳ Status: {status} ({attempt + 1}/{max_attempts})")
            
            if status == 'SUCCEEDED':
                video_url = result['output'][0]
                
                # Download video
                print("   📥 Downloading video...")
                video_data = requests.get(video_url)
                video_data.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(video_data.content)
                
                print(f"✅ Video generated: {output_path}")
                return str(output_path)
            
            elif status == 'FAILED':
                raise Exception(f"Video generation failed: {result.get('failure')}")
        
        raise TimeoutError("Video generation timed out")

if __name__ == "__main__":
    # Test the video generator
    generator = VideoGenerator()
    
    test_prompt = "A jar of golden honey sitting on an ancient Egyptian tomb, cinematic lighting, high quality"
    
    video_file = generator.generate(test_prompt, duration=5)
    print(f"\n✨ Video saved to: {video_file}")
