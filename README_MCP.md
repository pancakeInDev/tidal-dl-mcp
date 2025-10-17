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

### Current Capabilities (v0.2.0)

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
- Reorder tracks within playlists
- Clear all tracks from playlists
- Merge playlists together
- Create folders for organization
- Move playlists into folders

#### ⭐ Favorites Management
- Add any media to favorites (track, album, artist, playlist, video, mix)
- Remove items from favorites
- Browse favorites by type
- Get favorites summary overview

#### 💾 Download Operations
- Download individual tracks with quality selection
- Download complete albums with folder organization
- Download playlists with optional video support
- View download settings and quality information

#### 🔍 Discovery & Details
- Get detailed track information (metadata, quality, ISRC, lyrics availability)
- Get complete album details (tracklist, release info, reviews)
- Get artist information (biography, top tracks, discography)
- Browse artist albums by type (albums, EPs/singles, compilations)
- Find similar artists for music discovery
- Get track lyrics (synced or static)
- View detailed playlist information
- Browse TIDAL genres
- Get artist radio (curated mixes based on artist style)

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

### Playlist Management (12 tools)

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

#### `reorder_playlist`
Move a track within a playlist to a new position.

**Parameters:**
- `playlist_id` (required): ID of the playlist
- `from_index` (required): Current index of the track (0-based)
- `to_position` (required): New position for the track (0-based)

**Example:**
```
reorder_playlist: playlist_id="abc123", from_index=5, to_position=0
reorder_playlist: playlist_id="abc123", from_index=0, to_position=10
```

#### `clear_playlist`
Remove all tracks from a playlist at once.

**Parameters:**
- `playlist_id` (required): ID of the playlist to clear

**Example:**
```
clear_playlist: playlist_id="abc123"
```

**Warning:** This removes ALL tracks from the playlist. This cannot be undone.

#### `merge_playlists`
Merge tracks from one playlist into another.

**Parameters:**
- `target_playlist_id` (required): ID of the playlist to merge into
- `source_playlist_id` (required): ID of the playlist to merge from
- `allow_duplicates` (optional): Allow duplicate tracks (default: false)

**Example:**
```
merge_playlists: target_playlist_id="playlist1", source_playlist_id="playlist2"
merge_playlists: target_playlist_id="main", source_playlist_id="temp", allow_duplicates=true
```

**Note:** This copies tracks from the source playlist to the target playlist. The source playlist is not modified.

#### `create_playlist_folder`
Create a new folder for organizing playlists.

**Parameters:**
- `title` (required): Folder name
- `parent_folder_id` (optional): Parent folder ID (default: "root" for top level)

**Example:**
```
create_playlist_folder: title="Workout Playlists"
create_playlist_folder: title="Rock", parent_folder_id="root"
create_playlist_folder: title="Classic Rock", parent_folder_id="abc123"
```

#### `move_playlist_to_folder`
Move a playlist into a folder or to root level.

**Parameters:**
- `playlist_id` (required): ID of the playlist to move
- `folder_id` (optional): Target folder ID (None or "root" to move to root level)

**Examples:**
```
move_playlist_to_folder: playlist_id="playlist1", folder_id="folder123"
move_playlist_to_folder: playlist_id="playlist2", folder_id="root"
move_playlist_to_folder: playlist_id="playlist3"
```

**Note:** Omitting `folder_id` or using "root" moves the playlist to the top level (no folder).

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

### Download Operations (4 tools)

#### `download_track`
Download a track from TIDAL with specified quality.

**Parameters:**
- `track_id` (required): TIDAL track ID
- `quality` (optional): Audio quality - `Low`, `HiFi`, `Lossless`, `HiRes`, `Master` (default: `HiFi`)
- `output_path` (optional): Custom output directory (default: `~/Music/TIDAL`)

**Quality Options:**
- **Low**: 320 kbps AAC
- **HiFi/Lossless**: FLAC 16-bit/44.1kHz (CD Quality)
- **HiRes/Master**: FLAC up to 24-bit/192kHz (Studio Master)

**File Organization:**
Files are saved as: `{artist}/{album}/{album_track_num} - {title}.flac`

**What's Included:**
- Full metadata (artist, album, title, date, etc.)
- Album artwork (embedded)
- Lyrics (when available)
- Replay gain information

**Examples:**
```
download_track: track_id="12345"
download_track: track_id="67890", quality="HiRes"
download_track: track_id="11111", quality="HiFi", output_path="/Users/john/Downloads"
```

**Note:** Quality depends on your TIDAL subscription:
- TIDAL HiFi: Up to HiFi quality (16-bit/44.1kHz)
- TIDAL HiFi Plus: Up to HiRes quality (24-bit/192kHz)

---

#### `download_album`
Download an entire album from TIDAL.

**Parameters:**
- `album_id` (required): TIDAL album ID
- `quality` (optional): Audio quality (default: `HiFi`)
- `output_path` (optional): Custom output directory

**File Organization:**
```
{artist}/
  {album}/
    01 - Track One.flac
    02 - Track Two.flac
    ...
    cover.jpg
    playlist.m3u
```

**What's Included:**
- All tracks with full metadata
- Album artwork
- Lyrics for all tracks (when available)
- M3U playlist file
- Proper track numbering

**Examples:**
```
download_album: album_id="98765"
download_album: album_id="54321", quality="HiRes"
```

---

#### `download_playlist`
Download a playlist from TIDAL.

**Parameters:**
- `playlist_id` (required): TIDAL playlist ID
- `quality` (optional): Audio quality (default: `HiFi`)
- `output_path` (optional): Custom output directory
- `include_videos` (optional): Include videos in download (default: `false`)

**File Organization:**
```
Playlists/
  {playlist_name}/
    01 - Artist - Track.flac
    02 - Artist - Track.flac
    ...
    playlist.m3u
```

**What's Included:**
- All tracks in playlist order
- Full metadata for each track
- M3U playlist file preserving order
- Videos (if `include_videos=true`)

**Examples:**
```
download_playlist: playlist_id="abc-123"
download_playlist: playlist_id="def-456", quality="HiFi", include_videos=true
```

---

#### `get_download_settings`
View current download configuration and quality information.

**No parameters required.**

**Returns:**
- Current quality setting
- Default download path
- Available quality options
- Subscription tier limitations

**Example:**
```
get_download_settings
```

---

### Discovery & Details (9 tools)

#### `get_track_details`
Get detailed information about a track.

**Parameters:**
- `track_id` (required): TIDAL track ID

**Returns:**
- Track name, artist, album
- Duration, track number, volume number
- Audio quality, availability
- ISRC code, copyright
- Lyrics availability (synced/static/none)
- TIDAL URL

**Example:**
```
get_track_details: track_id="108043415"
```

---

#### `get_album_details`
Get detailed information about an album.

**Parameters:**
- `album_id` (required): TIDAL album ID

**Returns:**
- Album name, artist, release date
- Complete tracklist with durations
- Number of tracks and volumes
- UPC code, copyright
- Audio resolution
- Editorial review (if available)
- TIDAL URL

**Example:**
```
get_album_details: album_id="108043414"
```

---

#### `get_artist_details`
Get detailed information about an artist.

**Parameters:**
- `artist_id` (required): TIDAL artist ID
- `include_top_tracks` (optional): Include top tracks list (default: `true`)

**Returns:**
- Artist name and ID
- Biography
- Album and EP/single counts
- Top tracks (up to 10)
- TIDAL URL

**Example:**
```
get_artist_details: artist_id="3503597"
get_artist_details: artist_id="3503597", include_top_tracks=false
```

---

#### `get_artist_albums`
Get albums by an artist, filterable by type.

**Parameters:**
- `artist_id` (required): TIDAL artist ID
- `album_type` (optional): Type filter - `all`, `albums`, `eps_singles`, `other` (default: `all`)
- `limit` (optional): Maximum albums to return (default: 50)

**Album Types:**
- **all**: All releases (albums + EPs/singles)
- **albums**: Studio albums only
- **eps_singles**: EPs and singles
- **other**: Compilations and other releases

**Example:**
```
get_artist_albums: artist_id="3503597"
get_artist_albums: artist_id="3503597", album_type="albums"
get_artist_albums: artist_id="3503597", album_type="eps_singles", limit=20
```

---

#### `get_similar_artists`
Find artists similar to a given artist.

**Parameters:**
- `artist_id` (required): TIDAL artist ID
- `limit` (optional): Maximum artists to return (default: 10)

**Returns:**
- List of similar artists with names and IDs
- Useful for music discovery

**Example:**
```
get_similar_artists: artist_id="3503597"
get_similar_artists: artist_id="3503597", limit=20
```

---

#### `get_track_lyrics`
Get lyrics for a track.

**Parameters:**
- `track_id` (required): TIDAL track ID

**Returns:**
- **Synced lyrics**: Timestamped lyrics with `[MM:SS]` format
- **Static lyrics**: Plain text lyrics without timestamps
- Provider information

**Example:**
```
get_track_lyrics: track_id="108043415"
```

**Note:** Not all tracks have lyrics available. Returns error message if no lyrics found.

---

#### `get_playlist_details`
Get detailed information about a playlist.

**Parameters:**
- `playlist_id` (required): TIDAL playlist ID

**Returns:**
- Playlist name, creator, description
- Track count and total duration
- Creation and last updated dates
- Public/private status
- Preview of tracks (first 15)
- TIDAL URL

**Example:**
```
get_playlist_details: playlist_id="abc-123-def"
```

---

#### `browse_genres`
Browse available music genres on TIDAL.

**Parameters:**
- `limit` (optional): Maximum genres to return (default: 50)

**Returns:**
- List of TIDAL genres
- Categorized listings

**Example:**
```
browse_genres
browse_genres: limit=20
```

---

#### `get_artist_radio`
Get artist radio - a curated mix of tracks inspired by an artist.

**Parameters:**
- `artist_id` (required): TIDAL artist ID
- `limit` (optional): Maximum tracks to return (default: 50)

**Returns:**
- Curated tracklist inspired by the artist's style
- Mix of tracks from the artist and similar artists
- Useful for discovery

**Example:**
```
get_artist_radio: artist_id="3503597"
get_artist_radio: artist_id="3503597", limit=30
```

**Tip:** Artist radio is AI-curated and provides a great way to discover new music similar to your favorite artists!

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

*Last Updated: 2025-01-17 | Version: 0.2.0*
