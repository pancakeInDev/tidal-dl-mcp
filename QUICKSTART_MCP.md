# TIDAL-DL-NG MCP Server - Quick Start

> **5-minute setup guide** for using TIDAL with Claude Desktop

---

## ⚡ Quick Setup

### 1. Clone & Install (2 min)

```bash
cd ~/dev
git clone https://github.com/exislow/tidal-dl-ng.git tidal-dl-mcp
cd tidal-dl-mcp
python3.12 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e .
```

### 2. Authenticate with TIDAL (1 min)

```bash
.venv/bin/tidal-dl-ng login
# Follow the browser prompts to log in
```

### 3. Configure Claude Desktop (2 min)

**Edit:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

**Add:**
```json
{
  "mcpServers": {
    "tidal-dl-ng": {
      "command": "/Users/YOUR_USERNAME/dev/tidal-dl-mcp/.venv/bin/python",
      "args": ["-m", "tidal_dl_ng_mcp.server"],
      "cwd": "/Users/YOUR_USERNAME/dev/tidal-dl-mcp"
    }
  }
}
```

**Replace** `/Users/YOUR_USERNAME/` with your actual path!

Find your path:
```bash
cd ~/dev/tidal-dl-mcp && pwd
```

### 4. Restart Claude Desktop

Quit completely (Cmd+Q), then reopen.

---

## ✅ Verify It Works

In Claude Desktop, try:

```
Search for tracks by Daft Punk
```

or

```
Show me my playlists
```

---

## 🎵 What You Can Do

- **Search:** "Find albums by Radiohead"
- **Details:** "Show me details for this track"
- **Discovery:** "Find similar artists to MF DOOM"
- **Lyrics:** "Get the lyrics for this song"
- **Playlists:** "Create a playlist called 'Workout Mix'"
- **Add Tracks:** "Add this track to my playlist"
- **Favorites:** "Show me my favorite albums"
- **Downloads:** "Download this track in HiRes quality"
- **Explore:** "Show me artist radio for Daft Punk"

---

## 🐛 Not Working?

**Problem: "spawn python ENOENT"**
- Fix: Check the `command` path in config points to `.venv/bin/python`
- Run: `ls /path/to/.venv/bin/python` to verify

**Problem: "Authentication required"**
- Fix: Re-run authentication
- Run: `.venv/bin/tidal-dl-ng login`
- Then restart Claude Desktop

**Problem: Tools not showing**
- Fix: Ensure you quit Claude Desktop completely (Cmd+Q)
- Check config file is valid JSON (no trailing commas)

---

## 📚 Full Documentation

- **Complete Setup Guide:** [README_MCP.md](README_MCP.md)
- **All Features:** [MCP_FEATURES.md](MCP_FEATURES.md)
- **Troubleshooting:** [README_MCP.md#troubleshooting](README_MCP.md#troubleshooting)

---

## 🚀 Available Tools (30)

### Search & Discovery (10)
- `search_tidal` - Find music content
- `get_track_details` - Track information
- `get_album_details` - Album information
- `get_artist_details` - Artist bio & top tracks
- `get_artist_albums` - Browse discography
- `get_similar_artists` - Find similar artists
- `get_track_lyrics` - Get song lyrics
- `get_playlist_details` - Playlist information
- `browse_genres` - Explore genres
- `get_artist_radio` - Artist radio mixes

### Playlists (12)
- `create_playlist` - Make new playlists
- `edit_playlist` - Modify playlist info
- `delete_playlist` - Remove playlists
- `add_to_playlist` - Add tracks
- `remove_from_playlist` - Remove tracks
- `get_playlist_items` - View tracks
- `get_my_playlists` - List playlists
- `reorder_playlist` - Reorder tracks
- `clear_playlist` - Remove all tracks
- `merge_playlists` - Combine playlists
- `create_playlist_folder` - Create folders
- `move_playlist_to_folder` - Organize playlists

### Favorites (4)
- `add_to_favorites` - Favorite items
- `remove_from_favorites` - Unfavorite
- `get_favorites` - View favorites
- `get_favorites_summary` - Count overview

### Downloads (4)
- `download_track` - Download tracks with quality options
- `download_album` - Download complete albums
- `download_playlist` - Download playlists
- `get_download_settings` - View download config

---

**Need help?** See [README_MCP.md](README_MCP.md) for detailed instructions!

**Issues?** https://github.com/exislow/tidal-dl-ng/issues

---

*Setup time: ~5 minutes | Version: 0.1.0*
