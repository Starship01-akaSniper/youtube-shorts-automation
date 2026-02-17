"""
Test script to verify each module works independently
Run this BEFORE running the full automation
"""
import sys
from pathlib import Path

print("="*60)
print("  YOUTUBE SHORTS AUTOMATION - MODULE TESTS")
print("="*60)

# Test 1: Configuration
print("\n[TEST 1/5] Testing configuration...")
try:
    from config import config
    if config.validate():
        print("✅ Configuration valid!")
    else:
        print("❌ Configuration failed. Check your .env file.")
        sys.exit(1)
except Exception as e:
    print(f"❌ Config error: {e}")
    sys.exit(1)

# Test 2: Content Generator (Gemini)
print("\n[TEST 2/5] Testing content generator...")
try:
    from modules import ContentGenerator
    gen = ContentGenerator()
    
    test_script = "Honey never spoils. It lasts forever!"
    metadata = gen.generate(test_script)
    
    print(f"✅ Title: {metadata['title']}")
    print(f"✅ Generated {len(metadata['tags'])} tags")
except Exception as e:
    print(f"❌ Content generator error: {e}")
    print("   Check your GEMINI_API_KEY in .env")

# Test 3: Text-to-Speech
print("\n[TEST 3/5] Testing TTS generator...")
try:
    from modules import TTSGenerator
    gen = TTSGenerator()
    
    test_text = "This is a test. Hello world!"
    audio_path = gen.generate(test_text, output_path="test_audio.mp3")
    
    if Path(audio_path).exists():
        print(f"✅ Audio generated: {audio_path}")
        print(f"   Size: {Path(audio_path).stat().st_size / 1024:.1f} KB")
    else:
        print("❌ Audio file not created")
except Exception as e:
    print(f"❌ TTS error: {e}")
    print("   Check your OPENAI_API_KEY in .env")

# Test 4: FFmpeg (Video Assembler)
print("\n[TEST 4/5] Testing FFmpeg installation...")
try:
    from modules import VideoAssembler
    assembler = VideoAssembler()
    print("✅ FFmpeg is installed and working!")
except Exception as e:
    print(f"❌ FFmpeg error: {e}")
    print("   Install FFmpeg: https://ffmpeg.org/download.html")

# Test 5: Video Generator (This will take 2-5 minutes!)
print("\n[TEST 5/5] Testing video generator...")
response = input("⚠️  This will cost ~$0.20 and take 2-5 minutes. Continue? (y/N): ")

if response.lower() == 'y':
    try:
        from modules import VideoGenerator
        gen = VideoGenerator()
        
        test_prompt = "A golden jar of honey on a wooden table, warm lighting"
        video_path = gen.generate(test_prompt, output_path="test_video.mp4")
        
        if Path(video_path).exists():
            print(f"✅ Video generated: {video_path}")
            print(f"   Size: {Path(video_path).stat().st_size / (1024*1024):.1f} MB")
        else:
            print("❌ Video file not created")
    except Exception as e:
        print(f"❌ Video generator error: {e}")
        print("   Check your LUMA_API_KEY in .env")
else:
    print("⏭️  Skipped video generation test")

print("\n" + "="*60)
print("  MODULE TESTS COMPLETE!")
print("="*60)
print("\n✨ If all tests passed, you're ready to run:")
print("   python main.py --interactive")
print("\n💡 Or test with an example script:")
print("   python main.py --script-file scripts/example_honey.txt")
