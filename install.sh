#!/bin/bash
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "~ATH Installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 required"
    exit 1
fi

# Clone or update repo
if [ -d "$HOME/.ATH" ]; then
    echo "Existing installation found. Updating..."
    echo ""
    
    # Preserve API key if it exists
    API_KEY_BACKUP=""
    if [ -f "$HOME/.ATH/.env" ]; then
        API_KEY_BACKUP=$(cat "$HOME/.ATH/.env")
        echo "✓ Preserving your API key"
    fi
    
    # Update from git
    cd "$HOME/.ATH"
    git fetch origin
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})
    
    if [ "$LOCAL" = "$REMOTE" ]; then
        echo "✓ Already up to date"
    else
        echo "Pulling latest changes..."
        git pull origin main
        echo "✓ Updated to latest version"
    fi
    
    # Restore API key
    if [ -n "$API_KEY_BACKUP" ]; then
        echo "$API_KEY_BACKUP" > "$HOME/.ATH/.env"
    fi
    echo ""
else
    echo "Installing ~ATH for the first time..."
    echo ""
    git clone https://github.com/krisciu/tildeath.git "$HOME/.ATH"
    echo "✓ Repository cloned"
    echo ""
fi

# Install dependencies
cd "$HOME/.ATH"
pip3 install -q -r requirements.txt

# Prompt for API key if not already set
if [ ! -f "$HOME/.ATH/.env" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "API Key Setup"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "~ATH requires an Anthropic API key to run."
    echo "Get one at: https://console.anthropic.com/"
    echo ""
    echo "Options:"
    echo "  1. Enter your API key now (saved to ~/.ATH/.env)"
    echo "  2. Skip (you'll need to set it manually later)"
    echo ""
    read -p "Enter your choice (1 or 2): " choice
    
    if [ "$choice" = "1" ]; then
        echo ""
        read -p "Paste your API key: " api_key
        if [ -n "$api_key" ]; then
            echo "ANTHROPIC_API_KEY=$api_key" > "$HOME/.ATH/.env"
            echo "✓ API key saved to ~/.ATH/.env"
        else
            echo "⚠ No key entered. You'll need to set it manually."
        fi
    else
        echo ""
        echo "⚠ Skipped API key setup."
        echo "To set it later, run:"
        echo "  echo \"ANTHROPIC_API_KEY=your-key-here\" > ~/.ATH/.env"
    fi
    echo ""
fi

# Create launcher directory if needed
mkdir -p "$HOME/.local/bin"

# Create launcher
cat > "$HOME/.local/bin/tildeath" << 'LAUNCHER'
#!/bin/bash
cd "$HOME/.ATH" && python3 main.py "$@"
LAUNCHER
chmod +x "$HOME/.local/bin/tildeath"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ Installation complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Run: tildeath"
echo ""
if [ ! -f "$HOME/.ATH/.env" ]; then
    echo "⚠ Remember to set your API key before running!"
    echo "  echo \"ANTHROPIC_API_KEY=your-key-here\" > ~/.ATH/.env"
    echo ""
fi
echo "If 'tildeath' command not found, add to PATH:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "To update ~ATH in the future, just run this script again:"
echo "  curl -fsSL https://raw.githubusercontent.com/krisciu/tildeath/main/install.sh | bash"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

