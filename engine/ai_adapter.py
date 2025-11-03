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
        # Try environment variable first
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Try .env file if not in environment
        if not api_key:
            try:
                from dotenv import load_dotenv
                load_dotenv()
                api_key = os.getenv('ANTHROPIC_API_KEY')
            except ImportError:
                pass
        
        # If still no key, show helpful error
        if not api_key:
            raise ValueError(
                "\n\nNo API key found. Get one at: https://console.anthropic.com/\n"
                "Then set it with:\n"
                "  export ANTHROPIC_API_KEY='your-key-here'\n"
                "Or create ~/.ATH/.env with:\n"
                "  ANTHROPIC_API_KEY=your-key-here\n"
            )
        
        self.client = Anthropic(api_key=api_key)
        self.model = os.getenv('MODEL_NAME', DEFAULT_MODEL)
        self.conversation_history: List[Dict] = []
        self.system_prompt = get_system_prompt()
        self.art_cache: Dict[str, str] = {}  # Cache generated art
    
    def generate_opening(self, scenario_data=None) -> Dict[str, any]:
        """Generate the opening scene of the game."""
        try:
            opening_prompt = get_opening_scene_prompt(scenario_data)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=self.system_prompt,
                messages=[{
                    "role": "user",
                    "content": opening_prompt
                }]
            )
            
            content = response.content[0].text
            
            # Store in conversation history
            self.conversation_history.append({
                "role": "user",
                "content": opening_prompt
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
        """Parse AI response into narrative, consequences, and choices."""
        # Debug: log if content is suspiciously short
        if len(content) < 50:
            print(f"[DEBUG] Short AI response: {content[:100]}")
        
        lines = content.split('\n')
        narrative = ""
        choices = []
        consequences = {'health': 0, 'sanity': 0, 'courage': 0}
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('NARRATIVE:'):
                current_section = 'narrative'
                narrative = line.replace('NARRATIVE:', '').strip()
            elif line.startswith('CONSEQUENCES:'):
                current_section = 'consequences'
            elif line.startswith('CHOICES:'):
                current_section = 'choices'
            elif current_section == 'narrative' and line and not line.startswith(('CONSEQUENCES', 'CHOICES')):
                narrative += ' ' + line
            elif current_section == 'consequences' and line:
                # Parse consequence lines like "health: -15"
                if ':' in line:
                    stat, value = line.split(':', 1)
                    stat = stat.strip().lower()
                    try:
                        value = int(value.strip())
                        if stat in consequences:
                            consequences[stat] = value
                    except ValueError:
                        pass  # Ignore malformed consequence lines
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
            "consequences": consequences,
            "error": False
        }
    
    def should_generate_art(self, context: Dict) -> bool:
        """Check if art should be generated at this moment."""
        choice_count = context['choice_count']
        char_stats = context['character_stats']
        hidden_stats = context['hidden_stats']
        revelation_level = context.get('revelation_level', 0)
        
        # Milestone choices (every 5 choices)
        if choice_count > 0 and choice_count % 5 == 0:
            return True
        
        # Critical health (<30%)
        if char_stats['health'] < 30:
            return True
        
        # Critical sanity
        if hidden_stats['sanity'] < 3:
            return True
        
        # Revelation moments
        if revelation_level >= 3 and choice_count > 15:
            return True
        
        return False
    
    def get_art_subject(self, context: Dict) -> tuple[str, str]:
        """
        Get subject and mood for art generation based on context.
        Returns (subject, mood) tuple - now more specific and contextual.
        """
        char_stats = context['character_stats']
        hidden_stats = context['hidden_stats']
        revelation_level = context.get('revelation_level', 0)
        choice_count = context['choice_count']
        recent_narrative = context.get('recent_narrative', '')
        
        # Extract concrete nouns from recent narrative for context
        narrative_lower = recent_narrative.lower()
        
        # Context-specific art from narrative keywords
        if 'hand' in narrative_lower or 'fingers' in narrative_lower:
            if 'too many' in narrative_lower or 'extra' in narrative_lower:
                return ("hand with seven fingers reaching toward viewer, extra joints visible", "body horror")
            return ("reaching hand with five distinct fingers, palm forward", "unsettling")
        
        if 'eye' in narrative_lower or 'staring' in narrative_lower or 'watching' in narrative_lower:
            if 'multiple' in narrative_lower or 'many' in narrative_lower:
                return ("seven eyes arranged in circular pattern, all pupils following viewer", "watching")
            return ("two eyes with dilated pupils, bloodshot, unblinking", "paranoia")
        
        if 'mirror' in narrative_lower or 'reflection' in narrative_lower:
            return ("cracked mirror with distorted face reflection, wrong number of eyes", "uncanny")
        
        if 'door' in narrative_lower or 'doorway' in narrative_lower or 'threshold' in narrative_lower:
            return ("doorway with impossible perspective, shadow figure standing in frame", "liminal")
        
        if 'mouth' in narrative_lower or 'teeth' in narrative_lower:
            return ("mouth with too many teeth, rows of sharp incisors visible", "devouring")
        
        if 'flesh' in narrative_lower or 'skin' in narrative_lower:
            return ("pulsing organic mass, veins visible through translucent skin", "visceral")
        
        # Critical health - death approaching
        if char_stats['health'] < 20:
            return ("skeletal figure draped in torn cloth, hollow eye sockets, bony hands reaching", "death")
        
        # Critical health but not dying yet
        if char_stats['health'] < 30:
            return ("wounded figure with visible injuries, blood dripping, bandaged limbs", "pain")
        
        # Critical sanity - breakdown
        if hidden_stats['sanity'] < 2:
            return ("face split vertically down middle, each half showing different expression", "fractured")
        
        # Low sanity
        if hidden_stats['sanity'] < 3:
            return ("figure melting like wax, features sliding down face", "dissolution")
        
        # High revelation - IHNMAIMS truth
        if revelation_level >= 4:
            return ("human figure transformed into soft shapeless mass, machine tendrils embedded", "hate")
        
        if revelation_level >= 3:
            return ("same doorway repeated infinitely in recursive loop, figure trapped inside", "eternal")
        
        # Milestones - but still specific
        if choice_count % 5 == 0:
            milestone_subjects = [
                ("twisted staircase spiraling into darkness, no visible end", "descent"),
                ("window showing impossible geometry outside, angles that shouldn't exist", "wrongness"),
                ("figure made entirely of writhing tendrils, vaguely humanoid shape", "alien"),
                ("mechanical skull with exposed gears and wires, one eye glowing", "machine"),
            ]
            return random.choice(milestone_subjects)
        
        # Default - specific, not abstract
        default_subjects = [
            ("doorway with shadow figure in threshold, impossible to see face clearly", "eerie"),
            ("pair of hands emerging from darkness, too-long fingers spread wide", "reaching"),
            ("geometric shape that hurts to look at, angles wrong", "incomprehensible"),
            ("face with features in wrong positions, mouth where eyes should be", "wrongness"),
        ]
        return random.choice(default_subjects)
    
    def generate_ending_narrative(self, ending, context: Dict) -> Dict[str, str]:
        """
        Generate AI-driven ending narrative with final ASCII art.
        Returns: {'narrative': str, 'ascii_art': str}
        """
        from config.prompts import get_ending_generation_prompt
        
        prompt = get_ending_generation_prompt(ending, context)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,  # Longer for endings
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text.strip()
            narrative = content
            
            # Generate final ASCII art
            art_subject = self._get_ending_art_subject(ending, context)
            ascii_art = self.generate_ascii_art(art_subject[0], art_subject[1], 
                                                context['hidden_stats']['sanity'])
            
            return {
                'narrative': narrative,
                'ascii_art': ascii_art
            }
            
        except Exception as e:
            # Fallback to basic ending
            return {
                'narrative': ending.ai_seed if hasattr(ending, 'ai_seed') else "The story ends here.",
                'ascii_art': self._get_fallback_ending_art(ending.ending_category if hasattr(ending, 'ending_category') else 'death')
            }
    
    def _get_ending_art_subject(self, ending, context: Dict) -> tuple[str, str]:
        """Get appropriate ASCII art subject for ending type."""
        category = ending.ending_category if hasattr(ending, 'ending_category') else 'death'
        
        art_map = {
            'death': ("skeletal figure reaching toward viewer, death personified", "finality"),
            'sanity_loss': ("face fragmenting into pieces, mind shattering visually", "dissolution"),
            'victory': ("figure ascending or transcending, triumphant pose", "triumph"),
            'transformation': ("human form becoming something else, mid-change", "metamorphosis"),
            'loop': ("infinite spiral or recursive pattern, no escape", "eternal"),
        }
        return art_map.get(category, ("abstract void, ending", "conclusion"))
    
    def _get_fallback_ending_art(self, category: str) -> str:
        """Get fallback ASCII art for endings."""
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        
        art_types = {
            'death': 'skull',
            'sanity_loss': 'split_face',
            'victory': 'spiral',
            'transformation': 'melting',
            'loop': 'void',
        }
        
        art_type = art_types.get(category, 'void')
        return typo.get_creepy_ascii_art(art_type)
    
    def generate_art_for_context(self, context: Dict) -> Optional[str]:
        """
        Generate ASCII art if conditions are met.
        Uses caching to avoid regenerating same concepts.
        """
        if not self.should_generate_art(context):
            return None
        
        subject, mood = self.get_art_subject(context)
        
        # Check cache first
        cache_key = f"{subject[:30]}_{mood}_{context['choice_count']}"
        if cache_key in self.art_cache:
            return self.art_cache[cache_key]
        
        # Generate new art
        art = self.generate_ascii_art(
            subject, 
            mood, 
            context['hidden_stats']['sanity']
        )
        
        # Cache it
        self.art_cache[cache_key] = art
        
        return art
    
    def reset_conversation(self):
        """Clear conversation history (new session)."""
        self.conversation_history = []

