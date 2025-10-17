#!/bin/bash
# Setup script for TIDAL-DL-NG MCP Server

set -e

echo "======================================"
echo "TIDAL-DL-NG MCP Server Setup"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"
echo ""

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --quiet mcp toml requests mutagen dataclasses-json pathvalidate m3u8 coloredlogs rich typer tidalapi python-ffmpeg pycryptodome
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Authenticate with TIDAL
echo -e "${YELLOW}Authenticating with TIDAL...${NC}"
echo "You will need to:"
echo "1. Open the URL in your browser"
echo "2. Log in to TIDAL"
echo "3. Return here and press OK"
echo ""
python -m tidal_dl_ng.cli login

echo ""
echo -e "${GREEN}✓ TIDAL authentication complete${NC}"
echo ""

# Test the server
echo -e "${YELLOW}Testing MCP server...${NC}"
python -m tidal_dl_ng_mcp.server &
SERVER_PID=$!
sleep 3
if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server started successfully${NC}"
    kill $SERVER_PID 2>/dev/null || true
    wait $SERVER_PID 2>/dev/null || true
else
    echo -e "${RED}✗ Server failed to start${NC}"
    exit 1
fi
echo ""

# Get absolute path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_PATH="$SCRIPT_DIR/tidal_dl_ng_mcp/server.py"

# Configure Claude Desktop
echo -e "${YELLOW}Configuring Claude Desktop...${NC}"
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Create config directory if it doesn't exist
mkdir -p "$HOME/Library/Application Support/Claude"

# Check if config exists
if [ -f "$CLAUDE_CONFIG" ]; then
    echo "Backing up existing config..."
    cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Create or update config
cat > "$CLAUDE_CONFIG" << EOF
{
  "mcpServers": {
    "tidal-dl-ng": {
      "command": "python",
      "args": [
        "-m",
        "tidal_dl_ng_mcp.server"
      ],
      "env": {}
    }
  }
}
EOF

echo -e "${GREEN}✓ Claude Desktop configured${NC}"
echo ""
echo "Configuration file: $CLAUDE_CONFIG"
echo ""

echo "======================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Restart Claude Desktop"
echo "2. The TIDAL server will be available as 'tidal-dl-ng'"
echo "3. Try: 'Search TIDAL for Daft Punk'"
echo ""
echo "For manual testing:"
echo "  python -m tidal_dl_ng_mcp.server"
echo ""
