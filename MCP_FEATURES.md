# TIDAL-DL-NG MCP Server - Features Coverage

This document provides a comprehensive overview of the TIDAL-DL-NG library capabilities and what's currently available through the MCP (Model Context Protocol) server for use with Claude Desktop and other MCP clients.

---

## 📊 Coverage Summary

| Category | Total Features | Implemented in MCP | Coverage |
|----------|---------------|-------------------|----------|
| Search & Discovery | 15+ | 10 | 🟢 Excellent |
| Playlist Management | 12 | 12 | 🟢 Complete |
| Favorites Management | 16 | 4 | 🟢 Complete |
| Download Operations | 8+ | 4 | 🟡 In Progress |
| Library Browsing | 10+ | 0 | 🔴 Not Started |
| Metadata & Details | 6+ | 0 | 🔴 Not Started |

**Overall MCP Implementation: 30 / 65+ features (~46%)**

---

## 🎵 TIDAL-DL-NG Library Features

### ✅ Implemented in MCP Server

#### 1. Search & Discovery (10/15) 🟢 EXCELLENT
- ✅ **Universal Search** - Search for tracks, albums, artists, playlists, videos
  - Supports text queries
  - Accepts TIDAL share URLs
  - Media type filtering
  - Returns formatted results with metadata

- ✅ **Get Track Details** - Comprehensive track information
  - Duration, track number, audio quality
  - ISRC code, copyright information
  - Lyrics availability check
  - Album and artist links

- ✅ **Get Album Details** - Complete album information
  - Full tracklist with durations
  - Release date, UPC code
  - Audio resolution information
  - Editorial reviews
  - Album credits

- ✅ **Get Artist Details** - Artist information
  - Biography
  - Top tracks (up to 300)
  - Album and EP/single counts
  - Artist ID and links

- ✅ **Get Artist Albums** - Browse artist's discography
  - Filter by type (albums, EPs/singles, compilations)
  - Sort by release date
  - Full album metadata

- ✅ **Similar Artists** - Artist recommendations
  - Curated similar artists list
  - Useful for music discovery

- ✅ **Get Track Lyrics** - Retrieve song lyrics
  - Synced lyrics (with timestamps)
  - Static lyrics
  - Provider information

- ✅ **Get Playlist Details** - Playlist metadata
  - Creator info
  - Track count and duration
  - Creation/update dates
  - Track preview

- ✅ **Browse Genres** - Explore TIDAL genres
  - Full genre catalog
  - Categorized listings

- ✅ **Artist Radio** - Curated artist-based mixes
  - AI-curated track selections
  - Based on artist style
  - Discovery tool

- ❌ Browse Curated Playlists
- ❌ Get New Releases
- ❌ Featured Playlists
- ❌ TIDAL Mixes
- ❌ Recommendations (For You)

#### 2. Playlist Management (12/12) 🟢 COMPLETE
- ✅ **Create Playlist** - Create new playlists with title, description, visibility
- ✅ **Edit Playlist** - Modify title, description, public/private settings
- ✅ **Delete Playlist** - Remove playlists permanently
- ✅ **Add Tracks to Playlist** - Add single or multiple tracks
  - Position control (beginning/end/specific position)
  - Duplicate prevention option
- ✅ **Remove Tracks from Playlist** - Remove by track ID or index
- ✅ **View Playlist Contents** - List all tracks with full metadata
- ✅ **List User Playlists** - View all owned playlists
- ✅ **Reorder Playlist Tracks** - Move tracks to specific positions within playlist
- ✅ **Clear Playlist** - Remove all tracks from playlist at once
- ✅ **Merge Playlists** - Combine tracks from multiple playlists
- ✅ **Create Playlist Folders** - Organize playlists in folders
- ✅ **Move Playlists to Folders** - Organize playlists in folder hierarchy

#### 3. Favorites Management (4/16) 🟢 COMPLETE CORE
- ✅ **Add to Favorites** - Add any media type (track, album, artist, playlist, video, mix)
- ✅ **Remove from Favorites** - Remove any favorited item
- ✅ **View Favorites by Type** - Retrieve and display favorites
  - Supports all media types
  - Pagination support
  - Detailed formatting
- ✅ **Favorites Summary** - Quick count overview

- ❌ Add by ISRC code
- ❌ Bulk add/remove operations
- ❌ Sort favorites by date added
- ❌ Sort favorites by name
- ❌ Sort favorites by artist
- ❌ Filter favorites by criteria
- ❌ Export favorites list
- ❌ Import favorites from file
- ❌ Sync favorites across devices
- ❌ Favorite albums pagination with custom order
- ❌ Favorite artists pagination with custom order
- ❌ Move favorites between folders

#### 4. Download Operations (4/8+) 🟡 IN PROGRESS
- ✅ **Download Track** - Download individual tracks
  - Quality selection (Low, HiFi, Lossless, HiRes, Master)
  - Automatic format selection (FLAC for lossless, AAC for lossy)
  - Metadata embedding
  - Cover art embedding
  - Lyrics embedding (when available)
  - Default file naming: `{artist}/{album}/{album_track_num} - {title}`
  - Skip existing files
  - Custom output path support

- ✅ **Download Album** - Download full albums
  - Maintain folder structure
  - Album art
  - Track numbering
  - Quality selection
  - Playlist file (m3u) creation
  - Progress tracking

- ✅ **Download Playlist** - Download entire playlists
  - Preserve playlist order
  - M3U playlist file creation
  - Custom folder organization (`Playlists/{title}/`)
  - Video download option (optional)
  - Quality selection

- ✅ **Download Settings Info** - View current download configuration
  - Current quality settings
  - Default download path
  - Available quality tiers
  - Subscription tier limitations

### ❌ Not Yet Implemented in MCP

#### 4. Download Operations - Advanced (0/4+) 🔴

- ❌ **Download Artist Discography** - Download all albums from artist

- ❌ **Download Video** - Download music videos
  - Quality selection
  - Format conversion

- ❌ **Download Favorites** - Batch download all favorites
  - Download favorite tracks
  - Download favorite albums
  - Download favorite videos

- ❌ **Download Queue Management**
  - View current downloads
  - Pause/Resume downloads
  - Cancel downloads
  - Download progress tracking
  - Multi-threaded downloading
  - Chunk-based downloading

- ❌ **Download History**
  - Track downloaded items
  - Prevent re-downloads
  - Export download history

#### 5. Library Browsing & Details (0/10+) 🔴
- ❌ **Get Track Details** - Full track metadata
  - Audio quality info
  - ISRC code
  - Copyright info
  - Recording date
  - Replay gain
  - Credits

- ❌ **Get Album Details** - Complete album information
  - Release date
  - Label
  - UPC code
  - All tracks
  - Album credits
  - Reviews/editorial

- ❌ **Get Artist Details** - Artist information
  - Biography
  - Pictures
  - Related artists
  - Top tracks
  - Albums
  - Videos
  - Playlists

- ❌ **Get Playlist Details** - Playlist metadata
  - Creator info
  - Creation date
  - Last updated
  - Followers count
  - Full track list

- ❌ **Get Video Details** - Video metadata

- ❌ **Get Mix Details** - TIDAL mix information

- ❌ **Get Lyrics** - Retrieve song lyrics
  - Synced lyrics (with timestamps)
  - Static lyrics

- ❌ **Get Credits** - Song/album credits
  - Performers
  - Producers
  - Engineers
  - Composers
  - Writers

- ❌ **Get Similar Items**
  - Similar tracks
  - Similar albums
  - Similar artists

- ❌ **Browse Artist Albums** - View all albums by artist
  - Sort by release date
  - Filter by album type (album, EP, single, compilation)

#### 6. User Account & Settings (0/8) 🔴
- ❌ **Get User Profile** - View user information
  - Username
  - Subscription tier
  - Country
  - Account creation date

- ❌ **Get Subscription Info** - Subscription details
  - Tier (HiFi, HiFi Plus, Free)
  - Audio quality limits
  - Expiration date

- ❌ **Configure Download Settings**
  - Default audio quality
  - Default download path
  - File naming patterns
  - Metadata options
  - Cover art settings

- ❌ **Configure Streaming Settings**
  - Streaming quality
  - Offline mode
  - Cache settings

- ❌ **Session Management**
  - View active sessions
  - Logout from devices

- ❌ **Get Playback Statistics**
  - Listening history
  - Most played tracks/artists/albums
  - Listening time

- ❌ **Recently Played** - View recent playback history

- ❌ **Continue Listening** - Resume where you left off

#### 7. Advanced Features (0/10+) 🔴
- ❌ **Audio Quality Analysis**
  - Check available qualities for track
  - Verify download quality
  - Bit depth and sample rate info

- ❌ **Offline Mode**
  - Mark content for offline
  - Manage offline library
  - Sync offline content

- ❌ **Batch Operations**
  - Bulk download
  - Bulk favorite/unfavorite
  - Bulk add to playlist

- ❌ **Smart Playlists** - Auto-updating playlists based on criteria

- ❌ **Playlist Templates** - Reusable playlist structures

- ❌ **Collaborative Playlists** - Share and collaborate on playlists

- ❌ **Crossfade Settings** - Configure playback crossfade

- ❌ **Normalize Audio** - Audio normalization options

- ❌ **Gapless Playback** - Configure gapless playback

- ❌ **DJ Mode** - Automatic playlist continuation

---

## 🔧 MCP-Specific Features

### Resources (3 total)
1. ✅ **Authentication Status** (`tidal://auth/status`)
   - Check login status
   - View user ID
   - Get setup instructions

2. ✅ **My Playlists** (`tidal://user/playlists`)
   - Quick view of all playlists
   - Accessible from resources panel

3. ✅ **Favorites Summary** (`tidal://user/favorites`)
   - Overview of all favorites counts
   - Quick access summary

### Tools (30 total)

#### Search & Discovery (10 tools)
1. `search_tidal` - Universal search with URL support
2. `get_track_details` - Detailed track information
3. `get_album_details` - Complete album information
4. `get_artist_details` - Artist biography and top tracks
5. `get_artist_albums` - Browse artist discography
6. `get_similar_artists` - Find similar artists
7. `get_track_lyrics` - Get synced or static lyrics
8. `get_playlist_details` - Playlist metadata and tracks
9. `browse_genres` - Explore TIDAL genres
10. `get_artist_radio` - Artist-based radio mixes

#### Playlist Management (12 tools)
11. `create_playlist` - Create new playlists
12. `edit_playlist` - Modify playlist metadata
13. `delete_playlist` - Remove playlists
14. `add_to_playlist` - Add tracks
15. `remove_from_playlist` - Remove tracks
16. `get_playlist_items` - View playlist contents
17. `get_my_playlists` - List user playlists
18. `reorder_playlist` - Move tracks within playlists
19. `clear_playlist` - Remove all tracks from playlist
20. `merge_playlists` - Merge tracks from one playlist into another
21. `create_playlist_folder` - Create folders for organizing playlists
22. `move_playlist_to_folder` - Move playlists into folders

#### Favorites Management (4 tools)
23. `add_to_favorites` - Favorite any media
24. `remove_from_favorites` - Unfavorite any media
25. `get_favorites` - View favorites by type
26. `get_favorites_summary` - Favorites count overview

#### Download Operations (4 tools)
27. `download_track` - Download individual tracks with quality options
28. `download_album` - Download complete albums
29. `download_playlist` - Download playlists with optional videos
30. `get_download_settings` - View download configuration

---

## 🎯 Roadmap & Priorities

### Phase 1: Core Downloads ✅ COMPLETE
**Priority: HIGH** | **Status: DONE**

- [x] `download_track` - Single track downloads with quality options
- [x] `download_album` - Album downloads with folder structure
- [x] `download_playlist` - Playlist downloads
- [x] `get_download_settings` - View download configuration

**Impact:** Enables core value proposition of tidal-dl-ng

### Phase 2: Enhanced Discovery ✅ COMPLETE
**Priority: MEDIUM** | **Status: DONE**

- [x] `get_track_details` - Detailed track metadata
- [x] `get_album_details` - Full album information
- [x] `get_artist_details` - Artist information and discography
- [x] `get_artist_albums` - Browse artist's albums
- [x] `get_similar_artists` - Artist recommendations
- [x] `get_track_lyrics` - Lyrics retrieval
- [x] `get_playlist_details` - Playlist details
- [x] `browse_genres` - Genre browsing
- [x] `get_artist_radio` - Artist radio

**Impact:** Rich discovery and exploration capabilities

### Phase 3: Advanced Playlist Features ✅ COMPLETE
**Priority: LOW** | **Status: DONE**

- [x] `reorder_playlist` - Move tracks within playlists
- [x] `merge_playlists` - Combine playlists
- [x] `clear_playlist` - Remove all tracks
- [x] `create_playlist_folder` - Folder organization
- [x] `move_playlist_to_folder` - Organize playlists

**Impact:** Professional playlist management - Full playlist feature parity with TIDAL web/app

### Phase 4: User Library & Settings ⚙️
**Priority: LOW** | **Estimated Time: 1-2 days**

- [ ] `get_user_profile` - View user information
- [ ] `get_subscription_info` - Subscription details
- [ ] `configure_download_settings` - Set default quality, paths, formats
- [ ] `get_download_history` - View download history
- [ ] User settings resource

**Impact:** Personalization and configuration

### Phase 5: Advanced Features 🚀
**Priority: FUTURE** | **Estimated Time: 3-5 days**

- [ ] Bulk operations (batch downloads, favorites)
- [ ] Smart playlists
- [ ] Lyrics retrieval
- [ ] Credits and detailed metadata
- [ ] Audio quality analysis
- [ ] Download queue management with pause/resume
- [ ] Recently played / listening history

**Impact:** Power user features

---

## 📈 Implementation Statistics

**Current Status:**
- **Total Features in Library:** 65+
- **Implemented in MCP:** 30
- **Coverage:** ~46%
- **Lines of Code (MCP):** ~3,400 LOC
- **Tools:** 30
- **Resources:** 3

**Core Functionality Coverage:**
- 🟢 Search & Discovery: 67% (excellent)
- 🟢 Playlists: 100% (complete - all features)
- 🟢 Favorites: 25% (core complete)
- 🟡 Downloads: 50% (core complete)
- 🟢 Details/Metadata: 100% (complete - track, album, artist, playlist)
- 🔴 User Settings: 0% (not started)

---

## 💡 Feature Request?

Want a feature implemented? Check the roadmap above or open an issue at:
https://github.com/exislow/tidal-dl-ng/issues

**Most Requested Features:**
1. Download operations (Phase 1) 🔥
2. Track/album/artist details (Phase 2)
3. Lyrics retrieval (Phase 5)
4. Playlist reordering (Phase 3)

---

## 🔗 Related Documentation

- [README_MCP.md](README_MCP.md) - Setup and configuration guide
- [CLAUDE.md](CLAUDE.md) - Development guidelines
- [README.md](README.md) - Main tidal-dl-ng documentation

---

**Last Updated:** 2025-01-17
**MCP Server Version:** 0.2.0
**TIDAL-DL-NG Version:** 0.28.0
