"""
Main orchestrator for YouTube Shorts automation
"""
import sys
from pathlib import Path
from datetime import datetime
from config import config
from modules import (
    ContentGenerator,
    TTSGenerator,
    VideoGenerator,
    CaptionGenerator,
    VideoAssembler,
    YouTubeUploader
)

class YouTubeShortsAutomation:
    """Main automation orchestrator"""
    
    def __init__(self):
        """Initialize all components"""
        print("\n" + "="*60)
        print("  YOUTUBE SHORTS AUTOMATION")
        print("="*60)
        
        # Validate configuration
        if not config.validate():
            sys.exit(1)
        
        # Create directories
        config.create_directories()
        
        # Print configuration
        config.print_config()
        
        # Initialize modules
        print("🔧 Initializing modules...")
        try:
            self.content_gen = ContentGenerator()
            self.tts_gen = TTSGenerator()
            self.video_gen = VideoGenerator()
            self.caption_gen = CaptionGenerator()
            self.video_assembler = VideoAssembler()
            self.youtube_uploader = YouTubeUploader()
            print("✅ All modules initialized\n")
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            sys.exit(1)
    
    def create_video(self, script: str, video_prompt: str = None, 
                    auto_upload: bool = False) -> dict:
        """
        Create a complete YouTube Short from a script
        
        Args:
            script: The video script text
            video_prompt: Custom prompt for video generation (optional)
            auto_upload: Automatically upload to YouTube (default: False)
            
        Returns:
            dict with paths to generated files and metadata
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("\n" + "="*60)
        print(f"  CREATING VIDEO - {timestamp}")
        print("="*60)
        print(f"\n📝 Script:\n{script}\n")
        
        result = {
            'timestamp': timestamp,
            'script': script,
            'success': False
        }
        
        try:
            # Step 1: Generate content metadata
            print("\n[STEP 1/6] Generating content metadata...")
            metadata = self.content_gen.generate(script)
            result['metadata'] = metadata
            
            # Step 2: Generate voiceover
            print("\n[STEP 2/6] Generating voiceover...")
            audio_path = self.tts_gen.generate(
                script,
                output_path=config.TEMP_DIR / f"audio_{timestamp}.mp3"
            )
            result['audio'] = audio_path
            
            # Step 3: Generate video
            print("\n[STEP 3/6] Generating video...")
            if video_prompt is None:
                video_prompt = f"High quality cinematic video of: {script[:100]}"
            
            video_path = self.video_gen.generate(
                video_prompt,
                output_path=config.TEMP_DIR / f"video_{timestamp}.mp4"
            )
            result['video_raw'] = video_path
            
            # Step 4: Generate captions
            print("\n[STEP 4/6] Generating captions...")
            captions_path = self.caption_gen.generate(
                audio_path,
                output_path=config.TEMP_DIR / f"captions_{timestamp}.srt"
            )
            result['captions'] = captions_path
            
            # Step 5: Assemble final video
            print("\n[STEP 5/6] Assembling final video...")
            final_video_path = self.video_assembler.assemble(
                video_path,
                audio_path,
                captions_path,
                output_path=config.OUTPUT_DIR / f"youtube_short_{timestamp}.mp4"
            )
            result['final_video'] = final_video_path
            
            # Step 6: Upload to YouTube (if requested)
            if auto_upload:
                print("\n[STEP 6/6] Uploading to YouTube...")
                video_id = self.youtube_uploader.upload(
                    final_video_path,
                    title=metadata['title'],
                    description=metadata['description'] + '\n\n' + ' '.join(metadata['hashtags']),
                    tags=metadata['tags']
                )
                result['video_id'] = video_id
                result['youtube_url'] = f"https://www.youtube.com/watch?v={video_id}"
            else:
                print("\n[STEP 6/6] Skipping YouTube upload (auto_upload=False)")
                print("   You can upload manually later using the YouTube upload module")
            
            result['success'] = True
            
            # Print summary
            print("\n" + "="*60)
            print("  ✅ VIDEO CREATION COMPLETE!")
            print("="*60)
            print(f"\n📹 Final Video: {final_video_path}")
            print(f"📊 Title: {metadata['title']}")
            print(f"📝 Description: {metadata['description']}")
            print(f"🏷️  Tags: {', '.join(metadata['tags'][:5])}...")
            
            if auto_upload:
                print(f"🔗 YouTube URL: {result['youtube_url']}")
                print("   ⚠️  Status: PRIVATE (change in YouTube Studio)")
            
            print("\n" + "="*60 + "\n")
            
            return result
            
        except Exception as e:
            print(f"\n❌ Error during video creation: {e}")
            import traceback
            traceback.print_exc()
            result['error'] = str(e)
            return result

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YouTube Shorts Automation')
    parser.add_argument('--script', type=str, help='Video script text')
    parser.add_argument('--script-file', type=str, help='Path to script file')
    parser.add_argument('--video-prompt', type=str, help='Custom video generation prompt')
    parser.add_argument('--upload', action='store_true', help='Auto-upload to YouTube')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    # Initialize automation
    automation = YouTubeShortsAutomation()
    
    # Get script
    if args.script_file:
        with open(args.script_file, 'r', encoding='utf-8') as f:
            script = f.read()
    elif args.script:
        script = args.script
    elif args.interactive or len(sys.argv) == 1:
        # Interactive mode
        print("📝 Enter your video script (press Ctrl+D or Ctrl+Z when done):")
        print("-" * 60)
        script_lines = []
        try:
            while True:
                line = input()
                script_lines.append(line)
        except EOFError:
            pass
        script = '\n'.join(script_lines).strip()
        
        if not script:
            print("❌ No script provided!")
            return
        
        # Ask about upload
        upload_choice = input("\n🔼 Upload to YouTube? (y/N): ").lower().strip()
        args.upload = upload_choice == 'y'
    else:
        print("❌ Please provide a script using --script or --script-file")
        parser.print_help()
        return
    
    # Create video
    result = automation.create_video(
        script=script,
        video_prompt=args.video_prompt,
        auto_upload=args.upload
    )
    
    if result['success']:
        print("🎉 All done! Your YouTube Short is ready!")
    else:
        print("😞 Video creation failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
