"""AI adapter for Claude API integration."""

import os
from typing import Dict, List, Optional
from anthropic import Anthropic
from config.prompts import (
    get_system_prompt,
    get_scene_generation_prompt,
    get_ascii_art_prompt,
    get_opening_scene_prompt
)
from config.settings import DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE


class AIAdapter:
    """Manages AI generation for narrative content."""
    
    def __init__(self):
        """Initialize the AI adapter with API credentials."""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. "
                "Create a .env file with your API key."
            )
        
        self.client = Anthropic(api_key=api_key)
        self.model = os.getenv('MODEL_NAME', DEFAULT_MODEL)
        self.conversation_history: List[Dict] = []
        self.system_prompt = get_system_prompt()
    
    def generate_opening(self) -> Dict[str, any]:
        """Generate the opening scene of the game."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=self.system_prompt,
                messages=[{
                    "role": "user",
                    "content": get_opening_scene_prompt()
                }]
            )
            
            content = response.content[0].text
            
            # Store in conversation history
            self.conversation_history.append({
                "role": "user",
                "content": get_opening_scene_prompt()
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": content
            })
            
            return self._parse_response(content)
            
        except Exception as e:
            # Error becomes part of the narrative
            return {
                "narrative": f"[CONNECTION ERROR] ...or is it? Something doesn't want to start. {str(e)[:50]}",
                "choices": [
                    "Try again",
                    "Embrace the void",
                    "Wake up"
                ],
                "error": True
            }
    
    def generate_scene(self, context: Dict) -> Dict[str, any]:
        """Generate next scene based on current context."""
        try:
            prompt = get_scene_generation_prompt(context)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=self.system_prompt,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            content = response.content[0].text
            
            # Update conversation history (keep last 6 exchanges to manage context)
            self.conversation_history.append({
                "role": "user",
                "content": prompt
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": content
            })
            
            # Trim history if too long
            if len(self.conversation_history) > 12:
                self.conversation_history = self.conversation_history[-12:]
            
            return self._parse_response(content)
            
        except Exception as e:
            # Errors become glitches in the narrative
            return {
                "narrative": f"[S̴Y̷S̶T̸E̷M̴ ̸E̷R̶R̸O̷R̴] The narrator is having trouble remembering what happens next. ({str(e)[:40]}...)",
                "choices": [
                    "Continue anyway",
                    "Try to remember",
                    "Accept the corruption"
                ],
                "error": True
            }
    
    def generate_ascii_art(self, subject: str, mood: str, sanity_level: int) -> str:
        """Generate ASCII art for visual moments."""
        try:
            prompt = get_ascii_art_prompt(subject, mood, sanity_level)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=400,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            # Failed art generation = corrupted visual
            return """
    ▓▒░ERROR░▒▓
    [ART CORRUPTED]
    ▓▒░░░░░░░▒▓
"""
    
    def _parse_response(self, content: str) -> Dict[str, any]:
        """Parse AI response into narrative and choices."""
        # Debug: log if content is suspiciously short
        if len(content) < 50:
            print(f"[DEBUG] Short AI response: {content[:100]}")
        
        lines = content.split('\n')
        narrative = ""
        choices = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('NARRATIVE:'):
                current_section = 'narrative'
                narrative = line.replace('NARRATIVE:', '').strip()
            elif line.startswith('CHOICES:'):
                current_section = 'choices'
            elif current_section == 'narrative' and line and not line.startswith('CHOICES'):
                narrative += ' ' + line
            elif current_section == 'choices' and line:
                # Remove numbering like "1. " or "- "
                choice = line.lstrip('0123456789.-) ').strip()
                if choice and len(choice) > 2:  # Must be more than 2 chars
                    choices.append(choice)
        
        # Fallback parsing if format wasn't followed
        if not narrative or len(choices) < 2:
            # Try to split on "choices:" keyword (case insensitive)
            import re
            parts = re.split(r'(?i)choices\s*:', content)
            
            if len(parts) >= 2:
                # First part is narrative
                narrative_part = parts[0].strip()
                # Remove "NARRATIVE:" prefix if present
                narrative_part = re.sub(r'(?i)^narrative\s*:', '', narrative_part).strip()
                if narrative_part:
                    narrative = narrative_part
                
                # Second part is choices
                choice_text = parts[1].strip()
                # Extract numbered items
                for line in choice_text.split('\n'):
                    line = line.strip()
                    # Remove numbering
                    choice = re.sub(r'^[\d\.\-\)\s]+', '', line).strip()
                    if choice and len(choice) > 2 and not choice.startswith('NARRATIVE'):
                        choices.append(choice)
        
        # Even more aggressive fallback - split by newlines and find sentences
        if not narrative or len(choices) < 2:
            # Try to extract any sentences as narrative
            sentences = [line.strip() for line in lines if len(line.strip()) > 20 and not line.strip().startswith(('1.', '2.', '3.', '4.', '-'))]
            if sentences:
                narrative = ' '.join(sentences[:3])  # Take first 3 sentences
            
            # Try to extract any short lines as choices
            potential_choices = [line.strip().lstrip('0123456789.-) ').strip() 
                               for line in lines 
                               if 5 < len(line.strip()) < 100 and line.strip()[0:2].replace('.', '').replace('-', '').isdigit()]
            if len(potential_choices) >= 2:
                choices = potential_choices[:4]
        
        # Final fallback - use content as narrative
        if not narrative or len(narrative) < 20:
            narrative = content[:400] if len(content) > 20 else "The space shifts around you. Everything feels unstable."
        
        # CRITICAL: Must have valid choices or we get stuck in a loop
        if not choices or len(choices) < 2:
            # Generate contextual fallback choices based on narrative
            fallback_choices = [
                "Move forward carefully",
                "Examine your surroundings",
                "Take a moment to think",
                "Try a different approach"
            ]
            choices = fallback_choices[:3]
            print(f"[DEBUG] Using fallback choices due to parse failure")
        
        return {
            "narrative": narrative.strip(),
            "choices": choices[:4],  # Max 4 choices
            "error": False
        }
    
    def reset_conversation(self):
        """Clear conversation history (new session)."""
        self.conversation_history = []

