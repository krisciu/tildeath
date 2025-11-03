# Security

## API Key Required

This game requires an Anthropic API key to run. No key is included in the repository.

Get your own key at: https://console.anthropic.com/

## Setting Your Key

**Option 1: Environment Variable (Temporary)**
```bash
export ANTHROPIC_API_KEY='your-key-here'
tildeath
```

**Option 2: .env File (Persistent)**
```bash
echo "ANTHROPIC_API_KEY=your-key-here" > ~/.ATH/.env
tildeath
```

## Sharing Keys

If you want to share a key with friends:
- Share it privately (Discord, text, etc.)
- Set usage limits in Anthropic console
- Monitor usage regularly
- Revoke if abused

## Cost Estimates

Each playthrough costs approximately:
- Short (5-10 choices): $0.05-0.10
- Medium (10-20 choices): $0.10-0.20
- Long (20+ choices): $0.20+

