#!/usr/bin/env python3
"""
Quick setup script for Terminal Story Engine.
Helps you configure your API key and test the installation.
"""

import os
import sys

def main():
    print("\n" + "="*60)
    print("  Terminal Story Engine - Setup")
    print("="*60 + "\n")
    
    # Check if .env exists
    if os.path.exists('.env'):
        print("✓ .env file already exists")
        response = input("  Do you want to reconfigure it? (y/N): ").strip().lower()
        if response != 'y':
            print("\nKeeping existing .env file.")
            test_imports()
            return
    
    # Get API key
    print("\nYou need an Anthropic API key to run this game.")
    print("Get one at: https://console.anthropic.com/\n")
    
    api_key = input("Enter your ANTHROPIC_API_KEY (or press Enter to skip): ").strip()
    
    if not api_key:
        print("\n⚠ No API key provided. You can add it to .env later.")
        print("  The game won't run without it, but you can test visuals with:")
        print("  python3 test_visuals.py\n")
        create_env_template()
    else:
        create_env_file(api_key)
        print("\n✓ .env file created successfully!")
    
    test_imports()
    
    print("\n" + "="*60)
    print("Setup complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Test visual effects: python3 test_visuals.py")
    if api_key:
        print("  2. Start the game: python3 main.py")
    else:
        print("  2. Add your API key to .env file")
        print("  3. Start the game: python3 main.py")
    print("\n")

def create_env_file(api_key):
    """Create .env file with API key."""
    with open('.env', 'w') as f:
        f.write(f"# Terminal Story Engine Configuration\n")
        f.write(f"ANTHROPIC_API_KEY={api_key}\n")
        f.write(f"\n# Optional: Model configuration\n")
        f.write(f"MODEL_NAME=claude-3-5-sonnet-20241022\n")

def create_env_template():
    """Create empty .env template."""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(f"# Terminal Story Engine Configuration\n")
            f.write(f"ANTHROPIC_API_KEY=your_api_key_here\n")
            f.write(f"\n# Optional: Model configuration\n")
            f.write(f"MODEL_NAME=claude-3-5-sonnet-20241022\n")

def test_imports():
    """Test that all required modules can be imported."""
    print("\nTesting imports...")
    try:
        import rich
        print("  ✓ rich")
        import anthropic
        print("  ✓ anthropic")
        import dotenv
        print("  ✓ python-dotenv")
        
        from engine.story_engine import StoryEngine
        print("  ✓ story_engine")
        from engine.renderer import Renderer
        print("  ✓ renderer")
        from engine.typography import TypographyEngine
        print("  ✓ typography")
        
        print("\n✓ All dependencies installed correctly!")
        return True
        
    except ImportError as e:
        print(f"\n✗ Import error: {e}")
        print("\nPlease install dependencies:")
        print("  pip3 install -r requirements.txt\n")
        return False

if __name__ == "__main__":
    main()

