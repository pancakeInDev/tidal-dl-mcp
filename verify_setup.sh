#!/bin/bash
# Verification script for TIDAL-DL-NG MCP Server

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "======================================"
echo "TIDAL-DL-NG MCP Server Verification"
echo "======================================"
echo ""

PASS=0
FAIL=0

# Test 1: Python modules
echo -n "Checking Python modules... "
if python -c "import tidal_dl_ng_mcp, mcp, tidalapi" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
    ((PASS++))
else
    echo -e "${RED}✗${NC}"
    ((FAIL++))
fi

# Test 2: TIDAL authentication
echo -n "Checking TIDAL authentication... "
if [ -f "$HOME/Library/Application Support/tidal-dl-ng/token.json" ] || [ -f "$HOME/.config/tidal-dl-ng/token.json" ]; then
    echo -e "${GREEN}✓${NC}"
    ((PASS++))
else
    echo -e "${RED}✗${NC}"
    echo "  Run: python -m tidal_dl_ng.cli login"
    ((FAIL++))
fi

# Test 3: MCP Server starts
echo -n "Testing MCP server startup... "
python -m tidal_dl_ng_mcp.server &
SERVER_PID=$!
sleep 2
if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
    kill $SERVER_PID 2>/dev/null || true
    wait $SERVER_PID 2>/dev/null || true
    ((PASS++))
else
    echo -e "${RED}✗${NC}"
    ((FAIL++))
fi

# Test 4: Claude Desktop config
echo -n "Checking Claude Desktop config... "
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [ -f "$CLAUDE_CONFIG" ]; then
    if python -m json.tool "$CLAUDE_CONFIG" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
        ((PASS++))
    else
        echo -e "${RED}✗ (Invalid JSON)${NC}"
        ((FAIL++))
    fi
else
    echo -e "${RED}✗ (Not found)${NC}"
    ((FAIL++))
fi

# Test 5: Search tool available
echo -n "Checking search tool... "
if python -c "from tidal_dl_ng_mcp.tools.search import search_tidal" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
    ((PASS++))
else
    echo -e "${RED}✗${NC}"
    ((FAIL++))
fi

echo ""
echo "======================================"
echo "Results: ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC}"
echo "======================================"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Restart Claude Desktop"
    echo "2. Try: 'Search TIDAL for Daft Punk'"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some checks failed${NC}"
    echo ""
    echo "Please review the errors above."
    exit 1
fi
