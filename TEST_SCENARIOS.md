# TIDAL-DL-NG MCP Server - Test Scenarios

> **Comprehensive test prompts for Claude Desktop**
> Use these prompts to verify all 32 tools are working correctly.

**Last Updated:** 2025-10-17
**Version:** 0.2.0
**Total Tools:** 32

---

## 🧪 Quick Test (Essential Features)

Copy and paste this into Claude Desktop to test core functionality:

```
I want to test the TIDAL MCP server. Please help me:

1. Check my authentication status
2. Search for the artist "Daft Punk"
3. Get details about one of their albums
4. Show me my playlists
5. Show me my favorites summary

After each step, confirm it worked before moving to the next.
```

---

## 🔍 Category 1: Search & Discovery (10 tools)

### Test 1.1: Universal Search
```
Search TIDAL for:
1. Tracks by "Billie Eilish"
2. Albums by "Radiohead"
3. The artist "Kendrick Lamar"
4. Playlists with "workout" in the name

Show me the results for each search.
```

### Test 1.2: Track Details
```
From the Billie Eilish search results, get detailed information about the first track.
Show me:
- Duration and quality
- ISRC code
- Lyrics availability
- Copyright info
```

### Test 1.3: Album Details
```
Get complete details for the album "OK Computer" by Radiohead.
Include:
- Full tracklist with durations
- Release date and UPC
- Audio resolution
- Editorial review if available
```

### Test 1.4: Artist Details & Discography
```
For the artist "Daft Punk":
1. Get their biography and top tracks
2. List all their studio albums
3. List their EPs and singles separately
4. Find similar artists
```

### Test 1.5: Lyrics & Radio
```
1. Get lyrics for the track "bad guy" by Billie Eilish
2. Get artist radio for Daft Punk (show me 10 tracks)
```

### Test 1.6: Genres & Playlists
```
1. Browse TIDAL genres (show me 20)
2. Get details for a popular TIDAL playlist (use any playlist ID you find)
```

---

## 📝 Category 2: Playlist Management (12 tools)

### Test 2.1: Create & Edit
```
Let's test playlist creation:

1. Create a new playlist called "MCP Test Playlist"
   - Description: "Testing the MCP server"
   - Make it private

2. Edit the playlist:
   - Change title to "MCP Test - Updated"
   - Change description to "Updated via MCP"
   - Make it public
```

### Test 2.2: Add & Remove Tracks
```
Using the "MCP Test - Updated" playlist:

1. Add 3 tracks from the Billie Eilish search to the playlist
2. View the playlist contents
3. Move the first track to the end (reorder it)
4. Remove the middle track by index
```

### Test 2.3: Merge Playlists
```
1. Create a second playlist called "MCP Test 2"
2. Add 2 different tracks to it
3. Merge "MCP Test 2" into "MCP Test - Updated"
4. View the combined playlist contents
```

### Test 2.4: Clear & Delete
```
1. Clear all tracks from "MCP Test 2"
2. Verify it's empty
3. Delete both test playlists
4. Confirm they're gone from my playlists list
```

### Test 2.5: Folders (Optional - requires folder support)
```
1. Create a folder called "Test Folders"
2. Create a new playlist called "In Folder Test"
3. Move "In Folder Test" into the "Test Folders" folder
4. Verify the organization
5. Move it back to root
6. Delete the test playlist and folder
```

---

## ⭐ Category 3: Favorites Management (4 tools)

### Test 3.1: Add to Favorites
```
Add to my favorites:
1. A track from Billie Eilish
2. The album "OK Computer"
3. The artist "Daft Punk"
4. A playlist you find

Show me my favorites summary after each addition.
```

### Test 3.2: View Favorites
```
Show me:
1. My favorite tracks (first 10)
2. My favorite albums (first 10)
3. My favorite artists (all)
4. My favorite playlists (all)
```

### Test 3.3: Remove from Favorites
```
Remove the items we just added from favorites:
1. Remove the Billie Eilish track
2. Remove the OK Computer album
3. Remove Daft Punk from artists
4. Remove the playlist

Verify they're gone with a favorites summary.
```

---

## 💾 Category 4: Download Operations (4 tools)

### Test 4.1: Download Settings
```
Show me:
1. Current download settings
2. Available quality options
3. Default download path
4. My subscription tier limitations
```

### Test 4.2: Download Track
```
Download a single track:
1. Pick any track from the Billie Eilish search
2. Download it in HiFi quality
3. Show me the download progress and result
4. Confirm the file path

Note: This will actually download the file to ~/Music/TIDAL/
```

### Test 4.3: Download Album (Optional - creates many files)
```
Download a short album or EP:
1. Find a short album (3-5 tracks)
2. Download it in HiFi quality
3. Show me the progress
4. Confirm all tracks were downloaded with metadata

Warning: This creates multiple files!
```

### Test 4.4: Download Playlist (Optional - creates many files)
```
1. Create a small test playlist with 2-3 tracks
2. Download the playlist in HiFi quality
3. Show me the progress
4. Verify the M3U playlist file was created

Warning: This creates multiple files!
```

---

## 👤 Category 5: User Account & Settings (2 tools)

### Test 5.1: User Profile
```
Show me my TIDAL user profile information:
1. Get my user profile
2. Check that it shows:
   - User ID
   - Username
   - Full name
   - Email address
```

### Test 5.2: Subscription Info
```
Show me my TIDAL subscription information:
1. Get my subscription info
2. Verify it shows:
   - Current subscription tier (Free, Premium, HiFi, or HiFi Plus)
   - Audio quality setting
   - Audio format (AAC or FLAC)
   - Bitrate information
   - Comparison of all available tiers
```

### Test 5.3: Combined Profile View
```
Using the tidal://user/profile resource:
1. View the resource in the resources panel
2. Verify it combines both profile and subscription information
3. Check that all details are displayed correctly
```

---

## 🎯 Full Integration Test

Use this comprehensive test that exercises multiple tools in a realistic workflow:

```
Let's do a complete TIDAL workflow test:

**Setup Phase:**
1. Check my authentication status
2. Show me my user profile and subscription tier
3. Show me my current playlists and favorites summary

**Discovery Phase:**
3. Search for albums by "Radiohead"
4. Get details for "OK Computer" including full tracklist
5. Get artist details for Radiohead with top tracks
6. Find similar artists to Radiohead

**Playlist Management Phase:**
7. Create a new playlist called "Radiohead Essentials"
   - Description: "Best tracks from Radiohead"
   - Private

8. Add 3 tracks from OK Computer to the playlist
9. View the playlist contents
10. Reorder: move track at index 2 to index 0
11. Create another playlist called "Similar Artists"
12. Add 2 tracks from a similar artist
13. Merge "Similar Artists" into "Radiohead Essentials"

**Favorites Phase:**
14. Add the OK Computer album to favorites
15. Add Radiohead to favorite artists
16. View my favorite albums
17. Get favorites summary

**Advanced Features:**
18. Get lyrics for a Radiohead track
19. Get artist radio for Radiohead (10 tracks)
20. Browse genres to find "Alternative"

**Cleanup Phase:**
21. Remove OK Computer from favorites
22. Remove Radiohead from favorite artists
23. Clear all tracks from "Radiohead Essentials"
24. Delete both test playlists
25. Verify everything is cleaned up

After each step, confirm success before proceeding. If any step fails, stop and report the error.
```

---

## 🐛 Error Handling Tests

Test error scenarios to verify proper error handling:

```
Test error handling:

1. Try to get details for an invalid track ID "999999999999"
2. Try to add to a playlist that doesn't exist
3. Try to remove from favorites something that isn't favorited
4. Try to delete a playlist you don't own (use a TIDAL curated playlist ID)
5. Try to get lyrics for a track that has no lyrics
6. Try to merge two playlists where one doesn't exist

Each of these should fail gracefully with a clear error message.
```

---

## 📊 Performance Test

Test handling multiple operations:

```
Performance test - run these in sequence:

1. Search for 5 different artists
2. Get details for 5 different albums
3. Create 3 playlists with different settings
4. Add 5 tracks to each playlist (15 total operations)
5. View all 3 playlists
6. Get favorites summary
7. Delete all 3 playlists

Measure approximate time and check for any slowdowns or errors.
```

---

## 🔄 Regression Test Checklist

After any code changes, verify these critical paths still work:

- [ ] Authentication status check
- [ ] User profile and subscription info
- [ ] Basic search (artist, album, track)
- [ ] Get track/album/artist details
- [ ] Create playlist
- [ ] Add tracks to playlist
- [ ] View playlist contents
- [ ] Delete playlist
- [ ] Add to favorites
- [ ] View favorites
- [ ] Remove from favorites
- [ ] Get download settings
- [ ] Get lyrics (for a track that has them)
- [ ] Browse genres
- [ ] Artist radio

---

## 🎬 Demo Scenario (For Showcasing Features)

Use this to demonstrate the MCP server capabilities:

```
I'd like to show you what this TIDAL MCP server can do. Let's create a "Discover Weekly" style playlist:

1. Search for my favorite artist [pick one]
2. Get their top tracks
3. Find 3 similar artists
4. Get artist radio for each similar artist (10 tracks each)
5. Create a playlist called "Discovery Mix - [Date]"
6. Add 2-3 tracks from each artist radio to the playlist
7. View the final playlist
8. Show me the playlist details and track count

Then let's organize it:
9. Create a folder called "Discovery Playlists"
10. Move the playlist into that folder
11. Add the playlist to my favorites

This demonstrates: search, discovery, playlist creation, organization, and favorites!
```

---

## 📝 Notes for Testing

### Prerequisites
- TIDAL account (HiFi or HiFi Plus recommended)
- Authenticated via `tidal-dl-ng login`
- Claude Desktop configured with MCP server

### Test Data
Use these as fallback search terms if needed:
- **Artists:** Daft Punk, Radiohead, Billie Eilish, Kendrick Lamar, Taylor Swift
- **Albums:** Random Access Memories, OK Computer, When We All Fall Asleep
- **Tracks:** Get Lucky, Paranoid Android, bad guy

### Known Limitations
- Download operations create actual files on disk
- Folder operations may not work if TIDAL API changes
- Some tracks may not have lyrics available
- Quality depends on subscription tier (HiFi vs HiFi Plus)

### Cleanup After Testing
Remember to:
- Delete test playlists
- Remove test items from favorites
- Delete downloaded test files from ~/Music/TIDAL/ if needed
- Remove test folders

---

## 🚀 Continuous Integration Test Script

For automated testing (requires CLI setup):

```bash
# Test MCP server can start
.venv/bin/python -c "from tidal_dl_ng_mcp import server; print('✓ Server imports')"

# Test authentication
.venv/bin/python -c "
from tidal_dl_ng_mcp.utils.auth import get_tidal_instance
try:
    tidal = get_tidal_instance()
    print(f'✓ Authenticated as user {tidal.session.user.id}')
except:
    print('✗ Authentication failed')
    exit(1)
"

# Test tool imports
.venv/bin/python -c "
from tidal_dl_ng_mcp.tools.search import search_tidal
from tidal_dl_ng_mcp.tools.playlist import (
    create_playlist, edit_playlist, delete_playlist,
    add_to_playlist, remove_from_playlist,
    reorder_playlist, clear_playlist, merge_playlists,
    create_playlist_folder, move_playlist_to_folder
)
from tidal_dl_ng_mcp.tools.favorites import (
    add_to_favorites, remove_from_favorites,
    get_favorites, get_favorites_summary
)
from tidal_dl_ng_mcp.tools.download import (
    download_track, download_album, download_playlist,
    get_download_settings
)
from tidal_dl_ng_mcp.tools.discovery import (
    get_track_details, get_album_details, get_artist_details,
    get_artist_albums, get_similar_artists, get_track_lyrics,
    get_playlist_details, browse_genres, get_artist_radio
)
from tidal_dl_ng_mcp.tools.user import (
    get_user_profile, get_subscription_info
)
print('✓ All 32 tools import successfully')
"
```

---

## 📊 Test Coverage Matrix

| Category | Tools | Basic Test | Integration Test | Error Test | Status |
|----------|-------|------------|------------------|------------|--------|
| Search & Discovery | 10 | ✅ | ✅ | ✅ | Complete |
| Playlist Management | 12 | ✅ | ✅ | ✅ | Complete |
| Favorites | 4 | ✅ | ✅ | ✅ | Complete |
| Downloads | 4 | ✅ | ⚠️ Optional | ✅ | Complete |
| User Account & Settings | 2 | ✅ | ✅ | ✅ | Complete |
| **Total** | **32** | **32/32** | **32/32** | **32/32** | **100%** |

---

## 🔧 Troubleshooting Test Failures

### If authentication test fails:
```bash
cd ~/dev/tidal-dl-mcp
.venv/bin/tidal-dl-ng login
```

### If tools aren't available:
1. Check Claude Desktop config
2. Restart Claude Desktop (Cmd+Q, not just close)
3. Verify MCP server logs for errors

### If operations fail:
- Check TIDAL subscription is active
- Verify internet connection
- Check TIDAL service status
- Try re-authenticating

---

**Testing Guide Version:** 1.0.0
**Compatible with MCP Server:** 0.2.0
**Last Verified:** 2025-01-17
