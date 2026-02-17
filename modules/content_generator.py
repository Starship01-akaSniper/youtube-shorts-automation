"""
Content Generator Module
Generates video titles, descriptions, and tags using AI (Google Gemini or GPT-4)
"""
import google.generativeai as genai
from openai import OpenAI
from config import config

class ContentGenerator:
    """Generate YouTube metadata from video script"""
    
    def __init__(self):
        """Initialize the content generator based on config"""
        self.service = config.CONTENT_AI_SERVICE
        
        if self.service == 'gemini':
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        elif self.service == 'gpt4':
            self.client = OpenAI(api_key=config.OPENAI_GPT_API_KEY)
    
    def generate(self, script: str) -> dict:
        """
        Generate title, description, and tags from script
        
        Args:
            script: The video script text
            
        Returns:
            dict with 'title', 'description', 'tags', and 'hashtags'
        """
        print(f"\n🤖 Generating content metadata using {self.service.upper()}...")
        
        prompt = f"""You are a YouTube Shorts optimization expert. Based on the following video script, generate:

1. A catchy, engaging title (max 100 characters) that will get clicks
2. A detailed description (2-3 sentences) optimized for SEO
3. 10 relevant tags for YouTube search
4. 5 trending hashtags

Video Script:
{script}

Return ONLY a JSON object in this exact format:
{{
    "title": "Your catchy title here",
    "description": "Your SEO-optimized description here",
    "tags": ["tag1", "tag2", "tag3", ...],
    "hashtags": ["#hashtag1", "#hashtag2", ...]
}}"""

        try:
            if self.service == 'gemini':
                response = self.model.generate_content(prompt)
                result_text = response.text
            else:  # gpt4
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                result_text = response.choices[0].message.content
            
            # Parse JSON response
            import json
            # Extract JSON from markdown code blocks if present
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            metadata = json.loads(result_text.strip())
            
            print(f"✅ Generated title: {metadata['title']}")
            print(f"✅ Generated {len(metadata['tags'])} tags")
            
            return metadata
            
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            # Return default metadata
            return {
                "title": "Interesting Fact You Need to Know",
                "description": "Check out this amazing fact! Like and subscribe for more interesting content.",
                "tags": ["shorts", "viral", "trending", "facts", "interesting"],
                "hashtags": ["#shorts", "#viral", "#trending"]
            }

if __name__ == "__main__":
    # Test the content generator
    generator = ContentGenerator()
    
    test_script = "Did you know that honey never spoils? Archaeologists have found 3000-year-old honey in Egyptian tombs that's still perfectly edible!"
    
    metadata = generator.generate(test_script)
    
    print("\n" + "="*50)
    print("Generated Metadata:")
    print("="*50)
    print(f"Title: {metadata['title']}")
    print(f"Description: {metadata['description']}")
    print(f"Tags: {', '.join(metadata['tags'])}")
    print(f"Hashtags: {' '.join(metadata['hashtags'])}")
