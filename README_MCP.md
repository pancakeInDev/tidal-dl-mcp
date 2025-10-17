# TIDAL-DL-NG MCP Server

> **Model Context Protocol server for TIDAL-DL-NG** - Bring TIDAL music library management to Claude Desktop and other MCP clients.

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.18.0-green.svg)](https://modelcontextprotocol.io/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

---

## 📋 Table of Contents

- [What is This?](#what-is-this)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Tools](#available-tools)
- [Resources](#resources)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)

---

## 🎯 What is This?

The **TIDAL-DL-NG MCP Server** is a [Model Context Protocol](https://modelcontextprotocol.io/) server that exposes TIDAL music streaming service capabilities to AI assistants like Claude. It allows you to:

- 🔍 Search for music (tracks, albums, artists, playlists, videos)
- 📝 Create and manage playlists
- ⭐ Manage your favorites (tracks, albums, artists, playlists, videos)
- 🎵 Organize your TIDAL library through natural language conversation

This transforms Claude Desktop (or any MCP client) into a powerful interface for managing your TIDAL music library!

---

## ✨ Features

### Current Capabilities (v0.1.0)

#### 🔍 Search & Discovery
- Universal search across all TIDAL content types
- Support for TIDAL share URLs
- Filter by media type (track, album, artist, playlist, video)
- Formatted results with full metadata

#### 📝 Playlist Management
- Create playlists with custom titles and descriptions
- Edit playlist metadata (title, description, visibility)
- Delete playlists
- Add/remove tracks with position control
- View playlist contents with full details
- List all your playlists
- Public/private visibility settings

#### ⭐ Favorites Management
- Add any media to favorites (track, album, artist, playlist, video, mix)
- Remove items from favorites
- Browse favorites by type
- Get favorites summary overview

#### 📊 Resources
- Authentication status checking
- Quick view of playlists
- Favorites summary dashboard

**[See full feature comparison →](MCP_FEATURES.md)**

---

## 📦 Prerequisites

Before installing, ensure you have:

1. **Python 3.12** (required by tidal-dl-ng)
   ```bash
   python3.12 --version  # Should show Python 3.12.x
   ```

2. **TIDAL Account** (HiFi or HiFi Plus subscription recommended)
   - Free accounts have limited access
   - Sign up at [tidal.com](https://tidal.com)

3. **Claude Desktop** (for using with Claude AI)
   - Download from [claude.ai/download](https://claude.ai/download)
   - Or use any MCP-compatible client

4. **Git** (for cloning the repository)
   ```bash
   git --version
   ```

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
cd ~/dev  # Or your preferred directory
git clone https://github.com/exislow/tidal-dl-ng.git tidal-dl-mcp
cd tidal-dl-mcp
```

### Step 2: Create Python Virtual Environment

The project requires **Python 3.12**. Create a virtual environment:

```bash
python3.12 -m venv .venv
```

> **Note:** If you don't have Python 3.12, install it first:
> - **macOS:** `brew install python@3.12`
> - **Linux:** `sudo apt install python3.12 python3.12-venv`
> - **Windows:** Download from [python.org](https://www.python.org/downloads/)

### Step 3: Install Dependencies

```bash
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e .
```

This installs:
- `tidal-dl-ng` and all its dependencies
- MCP SDK (`mcp>=1.1.2`)
- TIDAL API client (`tidalapi`)
- All required libraries

### Step 4: Verify Installation

```bash
.venv/bin/python -c "import tidal_dl_ng_mcp; print('✓ MCP server installed successfully')"
```

You should see: `✓ MCP server installed successfully`

---

## 🔐 Authentication

### Authenticate with TIDAL

Before using the MCP server, you must authenticate with TIDAL:

```bash
cd ~/dev/tidal-dl-mcp  # Use your actual path
.venv/bin/tidal-dl-ng login
```

**The authentication process:**

1. You'll be prompted to choose a login method (usually OAuth/Device Login)
2. A URL will be displayed - open it in your browser
3. Log in to your TIDAL account
4. Enter the code shown in the browser
5. Authentication token will be saved locally

**Where tokens are stored:**
- **macOS:** `~/Library/Application Support/tidal-dl-ng/`
- **Linux:** `~/.config/tidal-dl-ng/`
- **Windows:** `%APPDATA%\tidal-dl-ng\`

> **Security Note:** Tokens are stored locally and never transmitted. The MCP server uses the same authentication as the tidal-dl-ng CLI.

---

## ⚙️ Configuration

### Configure Claude Desktop

Edit Claude Desktop's MCP configuration file:

**Configuration file location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Add this configuration:**

```json
{
  "mcpServers": {
    "tidal-dl-ng": {
      "command": "/Users/YOUR_USERNAME/dev/tidal-dl-mcp/.venv/bin/python",
      "args": [
        "-m",
        "tidal_dl_ng_mcp.server"
      ],
      "cwd": "/Users/YOUR_USERNAME/dev/tidal-dl-mcp"
    }
  }
}
```

**⚠️ Important: Replace `/Users/YOUR_USERNAME/` with your actual path!**

To find your path:
```bash
cd ~/dev/tidal-dl-mcp
pwd  # Copy this output
```

### Example Configurations

#### macOS Example
```json
{
  "mcpServers": {
    "tidal-dl-ng": {
      "command": "/Users/john/dev/tidal-dl-mcp/.venv/bin/python",
      "args": ["-m", "tidal_dl_ng_mcp.server"],
      "cwd": "/Users/john/dev/tidal-dl-mcp"
    }
  }
}
```

#### Linux Example
```json
{
  "mcpServers": {
    "tidal-dl-ng": {
      "command": "/home/john/dev/tidal-dl-mcp/.venv/bin/python",
      "args": ["-m", "tidal_dl_ng_mcp.server"],
      "cwd": "/home/john/dev/tidal-dl-mcp"
    }
  }
}
```

#### Windows Example
```json
{
  "mcpServers": {
    "tidal-dl-ng": {
      "command": "C:\\Users\\John\\dev\\tidal-dl-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "tidal_dl_ng_mcp.server"],
      "cwd": "C:\\Users\\John\\dev\\tidal-dl-mcp"
    }
  }
}
```

### Restart Claude Desktop

After editing the configuration:

1. **Quit Claude Desktop completely** (don't just close the window)
   - macOS: `Cmd+Q`
   - Windows/Linux: Right-click system tray icon → Quit

2. **Reopen Claude Desktop**

3. **Verify connection** - In a new chat, you should see the TIDAL tools available

---

## 💬 Usage

### Starting a Conversation

Once configured, start using TIDAL tools naturally in Claude Desktop:

**Example prompts:**

```
Search for tracks by Daft Punk

Create a new playlist called "Workout Mix"

Add this track to my playlist: [track URL]

Show me my favorite albums

What are my playlists?

Search for the album "Random Access Memories"
```

### Check Authentication Status

View the **Authentication Status** resource in Claude Desktop's resources panel, or ask:

```
Check my TIDAL authentication status
```

### View Resources

Claude Desktop provides quick access to:
- **Authentication Status** - Check if you're logged in
- **My Playlists** - Quick view of all playlists
- **Favorites Summary** - Overview of favorites counts

---

## 🛠️ Available Tools

### Search (1 tool)

#### `search_tidal`
Search for music content on TIDAL.

**Parameters:**
- `query` (required): Search query or TIDAL share URL
- `media_type` (optional): Filter by type (`track`, `album`, `artist`, `playlist`, `video`)

**Examples:**
```
search_tidal: query="Billie Eilish"
search_tidal: query="https://tidal.com/browse/track/12345"
search_tidal: query="jazz", media_type="playlist"
```

---

### Playlist Management (7 tools)

#### `create_playlist`
Create a new TIDAL playlist.

**Parameters:**
- `title` (required): Playlist title
- `description` (optional): Playlist description
- `public` (optional): Make playlist public (default: false)

**Example:**
```
create_playlist: title="My Chill Mix", description="Relaxing vibes", public=true
```

#### `edit_playlist`
Edit an existing playlist's metadata.

**Parameters:**
- `playlist_id` (required): ID of the playlist
- `title` (optional): New title
- `description` (optional): New description
- `public` (optional): New visibility setting

**Example:**
```
edit_playlist: playlist_id="abc123", title="Updated Title", public=false
```

#### `delete_playlist`
Delete a playlist permanently.

**Parameters:**
- `playlist_id` (required): ID of the playlist to delete

**Example:**
```
delete_playlist: playlist_id="abc123"
```

#### `add_to_playlist`
Add tracks to a playlist.

**Parameters:**
- `playlist_id` (required): ID of the playlist
- `track_ids` (required): List of track IDs to add
- `position` (optional): Position to insert (-1 for end, 0 for beginning)
- `allow_duplicates` (optional): Allow duplicate tracks (default: false)

**Example:**
```
add_to_playlist: playlist_id="abc123", track_ids=["track1", "track2"]
add_to_playlist: playlist_id="abc123", track_ids=["track3"], position=0
```

#### `remove_from_playlist`
Remove a track from a playlist.

**Parameters:**
- `playlist_id` (required): ID of the playlist
- `track_id` (optional): ID of the track to remove
- `index` (optional): Index of track to remove (0-based)

**Note:** Provide either `track_id` OR `index`, not both.

**Examples:**
```
remove_from_playlist: playlist_id="abc123", track_id="track1"
remove_from_playlist: playlist_id="abc123", index=5
```

#### `get_playlist_items`
Get the tracks/videos in a playlist.

**Parameters:**
- `playlist_id` (required): ID of the playlist
- `limit` (optional): Maximum items to return (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Example:**
```
get_playlist_items: playlist_id="abc123", limit=100
```

#### `get_my_playlists`
Get a list of your playlists.

**Parameters:**
- `limit` (optional): Maximum playlists to return (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Example:**
```
get_my_playlists: limit=20
```

---

### Favorites Management (4 tools)

#### `add_to_favorites`
Add a track, album, artist, playlist, video, or mix to your favorites.

**Parameters:**
- `media_id` (required): ID of the media item
- `media_type` (required): Type of media (`track`, `album`, `artist`, `playlist`, `video`, `mix`)

**Example:**
```
add_to_favorites: media_id="12345", media_type="track"
add_to_favorites: media_id="67890", media_type="album"
```

#### `remove_from_favorites`
Remove an item from your favorites.

**Parameters:**
- `media_id` (required): ID of the media item
- `media_type` (required): Type of media

**Example:**
```
remove_from_favorites: media_id="12345", media_type="track"
```

#### `get_favorites`
Get your favorite tracks, albums, artists, playlists, videos, or mixes.

**Parameters:**
- `media_type` (required): Type of favorites (`track`, `album`, `artist`, `playlist`, `video`, `mix`)
- `limit` (optional): Maximum items to return (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Example:**
```
get_favorites: media_type="track", limit=20
get_favorites: media_type="album"
```

#### `get_favorites_summary`
Get a summary count of all your favorites by type.

**No parameters required.**

**Example:**
```
get_favorites_summary
```

---

## 📊 Resources

MCP Resources provide quick, read-only access to information:

### `tidal://auth/status`
**Authentication Status** - Check if you're logged in to TIDAL and get setup instructions if needed.

### `tidal://user/playlists`
**My Playlists** - Quick view of all your playlists with IDs, track counts, and URLs.

### `tidal://user/favorites`
**Favorites Summary** - Count of all your favorites by type (tracks, albums, artists, playlists).

---

## 🐛 Troubleshooting

### Server Won't Start

**Error:** `spawn python ENOENT` or "Failed to connect"

**Solution:**
1. Verify Python path is correct in config:
   ```bash
   ls -la /path/to/tidal-dl-mcp/.venv/bin/python
   ```
2. Ensure path is absolute (not relative)
3. Check virtual environment exists
4. Restart Claude Desktop completely

---

### Authentication Issues

**Error:** "TIDAL authentication required" or "400 Bad Request"

**Solution:**
1. Re-authenticate:
   ```bash
   cd ~/dev/tidal-dl-mcp
   .venv/bin/tidal-dl-ng login
   ```
2. Verify token files exist:
   - macOS: `ls ~/Library/Application\ Support/tidal-dl-ng/`
3. Check TIDAL subscription is active
4. Restart Claude Desktop after authenticating

---

### Tools Not Showing Up

**Problem:** TIDAL tools don't appear in Claude Desktop

**Solution:**
1. Check Claude Desktop config file syntax (valid JSON)
2. Verify paths are correct (no typos)
3. Ensure Claude Desktop was fully restarted (quit, not just closed)
4. Check MCP server logs in Claude Desktop:
   - Open Claude Desktop
   - Check for error messages in logs

---

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'tidal_dl_ng_mcp'`

**Solution:**
1. Reinstall in virtual environment:
   ```bash
   cd ~/dev/tidal-dl-mcp
   .venv/bin/pip install -e .
   ```
2. Verify installation:
   ```bash
   .venv/bin/python -c "import tidal_dl_ng_mcp"
   ```

---

### Python Version Issues

**Error:** "Package 'tidal-dl-ng' requires a different Python: 3.13.x not in '<3.13,>=3.12'"

**Solution:**
Must use Python 3.12 (not 3.13+):
```bash
# Remove wrong version
rm -rf .venv

# Create with Python 3.12
python3.12 -m venv .venv
.venv/bin/pip install -e .
```

Update Claude Desktop config to use `.venv/bin/python` (Python 3.12).

---

### Permission Errors

**Error:** "Permission denied" when running commands

**Solution:**
```bash
chmod +x .venv/bin/python
chmod +x .venv/bin/tidal-dl-ng
```

---

### Getting Help

If you're still having issues:

1. **Check Logs:**
   - Claude Desktop shows MCP server logs when tools fail
   - Look for error messages in the conversation

2. **Verify Setup:**
   ```bash
   # From the tidal-dl-mcp directory
   .venv/bin/python -m tidal_dl_ng_mcp.server
   ```
   Should start the server (Ctrl+C to stop)

3. **Test Authentication:**
   ```bash
   .venv/bin/python -c "
   from tidal_dl_ng.config import Settings, Tidal
   settings = Settings()
   tidal = Tidal(settings)
   if tidal.login_token():
       print('✓ Authentication works')
   else:
       print('✗ Authentication failed')
   "
   ```

4. **Open an Issue:**
   - Visit: https://github.com/exislow/tidal-dl-ng/issues
   - Include: error messages, Python version, OS, configuration (remove sensitive info)

---

## 🔧 Development

### Project Structure

```
tidal-dl-mcp/
├── tidal_dl_ng/              # Main tidal-dl-ng library
│   ├── cli.py                # CLI interface
│   ├── download.py           # Download engine
│   ├── config.py             # Configuration
│   └── ...
├── tidal_dl_ng_mcp/          # MCP server implementation
│   ├── server.py             # MCP server entry point
│   ├── tools/
│   │   ├── search.py         # Search tool
│   │   ├── playlist.py       # Playlist management tools
│   │   └── favorites.py      # Favorites management tools
│   └── utils/
│       └── auth.py           # Authentication utilities
├── pyproject.toml            # Project configuration
├── README.md                 # Main documentation
├── README_MCP.md             # This file
└── MCP_FEATURES.md           # Feature coverage documentation
```

### Running Tests

```bash
# Install dev dependencies
.venv/bin/pip install -e ".[dev]"

# Run tests
.venv/bin/pytest

# Run with coverage
.venv/bin/pytest --cov=tidal_dl_ng_mcp
```

### Code Style

This project follows the tidal-dl-ng coding standards:

```bash
# Run linters
.venv/bin/ruff check .
.venv/bin/black --check .

# Auto-format
.venv/bin/black .
.venv/bin/ruff check --fix .
```

### Adding New Tools

1. Create tool function in `tidal_dl_ng_mcp/tools/`
2. Use `@require_auth` decorator for auth
3. Register tool in `server.py`:
   - Add to imports
   - Add to `list_tools()`
   - Add handler in `call_tool()`
4. Test thoroughly
5. Update documentation

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**See also:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See [LICENSE](LICENSE) for full details.

---

## 🙏 Acknowledgments

- **tidal-dl-ng** - Original project by [Robert Honz](https://github.com/exislow)
- **tidalapi** - TIDAL API Python client
- **Anthropic** - MCP protocol and Claude Desktop
- **TIDAL** - Music streaming service

---

## 🔗 Links

- **Main Repository:** https://github.com/exislow/tidal-dl-ng
- **MCP Documentation:** https://modelcontextprotocol.io
- **Claude Desktop:** https://claude.ai/download
- **TIDAL:** https://tidal.com
- **Feature Coverage:** [MCP_FEATURES.md](MCP_FEATURES.md)

---

**Questions? Issues? Feedback?**

Open an issue on GitHub: https://github.com/exislow/tidal-dl-ng/issues

---

*Last Updated: 2025-10-17 | Version: 0.1.0*
