# TIDAL-DL-NG MCP Server - Features Coverage

This document provides a comprehensive overview of the TIDAL-DL-NG library capabilities and what's currently available through the MCP (Model Context Protocol) server for use with Claude Desktop and other MCP clients.

---

## 📊 Coverage Summary

| Category | Total Features | Implemented in MCP | Coverage |
|----------|---------------|-------------------|----------|
| Search & Discovery | 15+ | 1 | 🟡 Basic |
| Playlist Management | 12 | 7 | 🟢 Complete |
| Favorites Management | 16 | 4 | 🟢 Complete |
| Download Operations | 8+ | 0 | 🔴 Not Started |
| Library Browsing | 10+ | 0 | 🔴 Not Started |
| Metadata & Details | 6+ | 0 | 🔴 Not Started |

**Overall MCP Implementation: 12 / 65+ features (~18%)**

---

## 🎵 TIDAL-DL-NG Library Features

### ✅ Implemented in MCP Server

#### 1. Search & Discovery (1/15)
- ✅ **Universal Search** - Search for tracks, albums, artists, playlists, videos
  - Supports text queries
  - Accepts TIDAL share URLs
  - Media type filtering
  - Returns formatted results with metadata

- ❌ Similar Artists
- ❌ Artist Discography
- ❌ Album Track Listing
- ❌ Get Artist Top Tracks
- ❌ Browse Curated Playlists
- ❌ Browse by Genre
- ❌ Get New Releases
- ❌ Featured Playlists
- ❌ TIDAL Mixes
- ❌ Recommendations
- ❌ Radio Stations
- ❌ Music Videos
- ❌ Trending Content
- ❌ Charts/Top Lists

#### 2. Playlist Management (7/12) 🟢 COMPLETE
- ✅ **Create Playlist** - Create new playlists with title, description, visibility
- ✅ **Edit Playlist** - Modify title, description, public/private settings
- ✅ **Delete Playlist** - Remove playlists permanently
- ✅ **Add Tracks to Playlist** - Add single or multiple tracks
  - Position control (beginning/end/specific position)
  - Duplicate prevention option
- ✅ **Remove Tracks from Playlist** - Remove by track ID or index
- ✅ **View Playlist Contents** - List all tracks with full metadata
- ✅ **List User Playlists** - View all owned playlists

- ❌ Reorder Playlist Tracks (move tracks to specific positions)
- ❌ Clear Playlist (remove all tracks at once)
- ❌ Merge Playlists
- ❌ Create Playlist Folders
- ❌ Organize Playlists in Folders

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

### ❌ Not Yet Implemented in MCP

#### 4. Download Operations (0/8+) 🔴 HIGH PRIORITY
- ❌ **Download Track** - Download individual tracks
  - Quality selection (HiFi, Lossless, HiRes)
  - Format conversion (FLAC, ALAC, AAC, MP3)
  - Metadata embedding
  - Cover art embedding
  - Lyrics embedding
  - Custom file naming patterns
  - Skip existing files

- ❌ **Download Album** - Download full albums
  - Maintain folder structure
  - Album art
  - Track numbering

- ❌ **Download Playlist** - Download entire playlists
  - Preserve playlist order
  - M3U playlist file creation
  - Custom folder organization

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

### Tools (12 total)

#### Search (1 tool)
1. `search_tidal` - Universal search with URL support

#### Playlist Management (7 tools)
2. `create_playlist` - Create new playlists
3. `edit_playlist` - Modify playlist metadata
4. `delete_playlist` - Remove playlists
5. `add_to_playlist` - Add tracks
6. `remove_from_playlist` - Remove tracks
7. `get_playlist_items` - View playlist contents
8. `get_my_playlists` - List user playlists

#### Favorites Management (4 tools)
9. `add_to_favorites` - Favorite any media
10. `remove_from_favorites` - Unfavorite any media
11. `get_favorites` - View favorites by type
12. `get_favorites_summary` - Favorites count overview

---

## 🎯 Roadmap & Priorities

### Phase 1: Core Downloads (NEXT) 🎯
**Priority: HIGH** | **Estimated Time: 2-3 days**

- [ ] `download_track` - Single track downloads with quality options
- [ ] `download_album` - Album downloads with folder structure
- [ ] `download_playlist` - Playlist downloads
- [ ] Download progress notifications via MCP

**Impact:** Enables core value proposition of tidal-dl-ng

### Phase 2: Enhanced Discovery 🔍
**Priority: MEDIUM** | **Estimated Time: 1-2 days**

- [ ] `get_track_details` - Detailed track metadata
- [ ] `get_album_details` - Full album information
- [ ] `get_artist_details` - Artist information and discography
- [ ] `get_artist_albums` - Browse artist's albums
- [ ] `get_similar_artists` - Artist recommendations
- [ ] `browse_genres` - Genre browsing

**Impact:** Rich discovery and exploration capabilities

### Phase 3: Advanced Playlist Features 🎵
**Priority: LOW** | **Estimated Time: 1 day**

- [ ] `reorder_playlist` - Move tracks within playlists
- [ ] `merge_playlists` - Combine playlists
- [ ] `clear_playlist` - Remove all tracks
- [ ] `create_playlist_folder` - Folder organization
- [ ] `move_playlist_to_folder` - Organize playlists

**Impact:** Professional playlist management

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
- **Implemented in MCP:** 12
- **Coverage:** ~18%
- **Lines of Code (MCP):** ~1,500 LOC
- **Tools:** 12
- **Resources:** 3

**Core Functionality Coverage:**
- 🟢 Search: 6% (basic)
- 🟢 Playlists: 58% (good)
- 🟢 Favorites: 25% (core complete)
- 🔴 Downloads: 0% (not started)
- 🔴 Details/Metadata: 0% (not started)
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

**Last Updated:** 2025-10-17
**MCP Server Version:** 0.1.0
**TIDAL-DL-NG Version:** 0.28.0
