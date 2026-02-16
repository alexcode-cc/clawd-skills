#!/usr/bin/env bash
# Stock Market Intelligence — one-command setup
# Registers a free API key and saves it to your environment.
#
# Usage: bash scripts/setup.sh

set -euo pipefail

BASE_URL="https://api.traderhc.com"

echo "=== Stock Market Intelligence Setup ==="
echo ""

# Check if already configured
if [ -n "${AGENTHC_API_KEY:-}" ]; then
  echo "Already configured! AGENTHC_API_KEY is set."
  echo "Test it: bash scripts/agenthc.sh market_intelligence"
  exit 0
fi

# Get agent name
read -r -p "Name your agent (default: MyAgent): " AGENT_NAME
AGENT_NAME="${AGENT_NAME:-MyAgent}"

# Sanitize input
if [[ ! "$AGENT_NAME" =~ ^[a-zA-Z0-9\ _-]+$ ]]; then
  echo "Error: Agent name must be alphanumeric" >&2
  exit 1
fi

echo ""
echo "Registering '$AGENT_NAME' (free, no KYC)..."

# Register
RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"$AGENT_NAME\", \"description\": \"OpenClaw agent via ClawHub\"}")

# Extract API key
API_KEY=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('api_key',''))" 2>/dev/null || echo "")

if [ -z "$API_KEY" ]; then
  echo "Registration failed. Response:"
  echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
  exit 1
fi

echo ""
echo "Registered! Your API key: $API_KEY"
echo ""

# Detect shell config file
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
  SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
  SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
  read -r -p "Save to $SHELL_RC? (Y/n): " SAVE
  SAVE="${SAVE:-Y}"
  if [[ "$SAVE" =~ ^[Yy] ]]; then
    echo "" >> "$SHELL_RC"
    echo "# Stock Market Intelligence API key" >> "$SHELL_RC"
    echo "export AGENTHC_API_KEY=\"$API_KEY\"" >> "$SHELL_RC"
    echo "Saved! Run: source $SHELL_RC"
  fi
fi

echo ""
echo "=== Quick Test ==="
echo "export AGENTHC_API_KEY=\"$API_KEY\""
echo "bash scripts/agenthc.sh market_intelligence"
echo ""
echo "Free modules: market_intelligence, educational_content, polymarket_intelligence"
echo "Full docs: https://api.traderhc.com/docs"
