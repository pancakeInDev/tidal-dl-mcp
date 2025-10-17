"""
TIDAL-DL-NG MCP Server.

Main server implementation using Model Context Protocol.
"""

import asyncio
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource

from tidal_dl_ng_mcp.tools.search import search_tidal
from tidal_dl_ng_mcp.tools.playlist import (
    create_playlist,
    edit_playlist,
    delete_playlist,
    add_to_playlist,
    remove_from_playlist,
    get_playlist_items,
    get_my_playlists,
    reorder_playlist,
    clear_playlist,
    merge_playlists,
    create_playlist_folder,
    move_playlist_to_folder,
)
from tidal_dl_ng_mcp.tools.favorites import (
    add_to_favorites,
    remove_from_favorites,
    get_favorites,
    get_favorites_summary,
)
from tidal_dl_ng_mcp.tools.download import (
    download_track,
    download_album,
    download_playlist,
    get_download_settings,
)
from tidal_dl_ng_mcp.tools.discovery import (
    get_track_details,
    get_album_details,
    get_artist_details,
    get_artist_albums,
    get_similar_artists,
    get_track_lyrics,
    get_playlist_details,
    browse_genres,
    get_artist_radio,
)
from tidal_dl_ng_mcp.tools.user import (
    get_user_profile,
    get_subscription_info,
)
from tidal_dl_ng_mcp.tools.browse import (
    browse_home,
    browse_explore,
    get_mixes,
)
from tidal_dl_ng_mcp.utils.auth import get_tidal_instance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tidal-dl-ng-mcp")

# Create MCP server instance
app = Server("tidal-dl-ng")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources.

    Returns:
        List of available MCP resources.
    """
    return [
        Resource(
            uri="tidal://auth/status",
            name="Authentication Status",
            mimeType="text/plain",
            description="Check TIDAL authentication status and get setup instructions",
        ),
        Resource(
            uri="tidal://user/profile",
            name="User Profile",
            mimeType="text/plain",
            description="View your TIDAL user profile and subscription information",
        ),
        Resource(
            uri="tidal://user/playlists",
            name="My Playlists",
            mimeType="text/plain",
            description="View all your TIDAL playlists",
        ),
        Resource(
            uri="tidal://user/favorites",
            name="Favorites Summary",
            mimeType="text/plain",
            description="Summary of your TIDAL favorites (tracks, albums, artists, playlists)",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read resource content.

    Args:
        uri: Resource URI to read.

    Returns:
        Resource content as string.
    """
    if uri == "tidal://auth/status":
        try:
            tidal = get_tidal_instance()
            return f"""✓ Authenticated with TIDAL

User ID: {tidal.session.user.id}
Session: Active

You can now use the search_tidal tool to search for music on TIDAL!
"""
        except RuntimeError:
            return """✗ Not authenticated with TIDAL

To authenticate, run the following command in your terminal:

    cd /Users/ghubert/dev/tidal-dl-mcp
    .venv/bin/tidal-dl-ng login

This will guide you through the TIDAL login process. After logging in,
restart Claude Desktop to use the TIDAL MCP server.
"""

    elif uri == "tidal://user/profile":
        try:
            profile = await get_user_profile()
            subscription = await get_subscription_info()
            return f"{profile}\n\n{'=' * 50}\n\n{subscription}"
        except Exception as e:
            return f"✗ Failed to get user profile: {e!s}"

    elif uri == "tidal://user/playlists":
        try:
            result = await get_my_playlists(limit=100)
            return result
        except Exception as e:
            return f"✗ Failed to get playlists: {e!s}"

    elif uri == "tidal://user/favorites":
        try:
            result = await get_favorites_summary()
            return result
        except Exception as e:
            return f"✗ Failed to get favorites summary: {e!s}"

    else:
        return f"Unknown resource: {uri}"


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available TIDAL tools.

    Returns:
        List of available MCP tools.
    """
    return [
        # Search
        Tool(
            name="search_tidal",
            description=(
                "Search TIDAL for music content. Can search for tracks, albums, artists, playlists, or videos. "
                "Also accepts TIDAL share URLs to get direct information about specific items."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query or TIDAL share URL (e.g., 'Daft Punk' or 'https://tidal.com/browse/track/12345')",
                    },
                    "media_type": {
                        "type": "string",
                        "description": "Optional filter for type of media to search",
                        "enum": ["track", "album", "artist", "playlist", "video"],
                    },
                },
                "required": ["query"],
            },
        ),
        # Playlist Management
        Tool(
            name="create_playlist",
            description="Create a new TIDAL playlist.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Playlist title"},
                    "description": {"type": "string", "description": "Playlist description (optional)"},
                    "public": {"type": "boolean", "description": "Make playlist public (default: false)"},
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="edit_playlist",
            description="Edit an existing playlist's metadata (title, description, visibility).",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {"type": "string", "description": "ID of the playlist to edit"},
                    "title": {"type": "string", "description": "New title (optional)"},
                    "description": {"type": "string", "description": "New description (optional)"},
                    "public": {"type": "boolean", "description": "New visibility setting (optional)"},
                },
                "required": ["playlist_id"],
            },
        ),
        Tool(
            name="delete_playlist",
            description="Delete a playlist permanently.",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {"type": "string", "description": "ID of the playlist to delete"},
                },
                "required": ["playlist_id"],
            },
        ),
        Tool(
            name="add_to_playlist",
            description="Add tracks to a playlist.",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {"type": "string", "description": "ID of the playlist"},
                    "track_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of track IDs to add",
                    },
                    "position": {
                        "type": "integer",
                        "description": "Position to insert tracks (-1 for end, 0 for beginning, default: -1)",
                    },
                    "allow_duplicates": {"type": "boolean", "description": "Allow duplicate tracks (default: false)"},
                },
                "required": ["playlist_id", "track_ids"],
            },
        ),
        Tool(
            name="remove_from_playlist",
            description="Remove a track from a playlist by ID or index.",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {"type": "string", "description": "ID of the playlist"},
                    "track_id": {"type": "string", "description": "ID of the track to remove (optional if index provided)"},
                    "index": {"type": "integer", "description": "Index of track to remove (optional if track_id provided)"},
                },
                "required": ["playlist_id"],
            },
        ),
        Tool(
            name="get_playlist_items",
            description="Get the tracks/videos in a playlist.",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {"type": "string", "description": "ID of the playlist"},
                    "limit": {"type": "integer", "description": "Maximum items to return (default: 50)"},
                    "offset": {"type": "integer", "description": "Pagination offset (default: 0)"},
                },
                "required": ["playlist_id"],
            },
        ),
        Tool(
            name="get_my_playlists",
            description="Get a list of your playlists.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum playlists to return (default: 50)"},
                    "offset": {"type": "integer", "description": "Pagination offset (default: 0)"},
                },
            },
        ),
        Tool(
            name="reorder_playlist",
            description="Move a track within a playlist to a new position (reorder tracks).",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {"type": "string", "description": "ID of the playlist"},
                    "from_index": {"type": "integer", "description": "Current index of the track (0-based)"},
                    "to_position": {"type": "integer", "description": "New position for the track (0-based)"},
                },
                "required": ["playlist_id", "from_index", "to_position"],
            },
        ),
        Tool(
            name="clear_playlist",
            description="Remove all tracks from a playlist (clear the playlist).",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {"type": "string", "description": "ID of the playlist to clear"},
                },
                "required": ["playlist_id"],
            },
        ),
        Tool(
            name="merge_playlists",
            description="Merge tracks from one playlist into another.",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_playlist_id": {"type": "string", "description": "ID of the playlist to merge into"},
                    "source_playlist_id": {"type": "string", "description": "ID of the playlist to merge from"},
                    "allow_duplicates": {
                        "type": "boolean",
                        "description": "Allow duplicate tracks (default: false)",
                    },
                },
                "required": ["target_playlist_id", "source_playlist_id"],
            },
        ),
        Tool(
            name="create_playlist_folder",
            description="Create a new folder for organizing playlists.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Folder name"},
                    "parent_folder_id": {
                        "type": "string",
                        "description": "Parent folder ID (default: 'root' for top level)",
                    },
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="move_playlist_to_folder",
            description="Move a playlist into a folder or to root level.",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {"type": "string", "description": "ID of the playlist to move"},
                    "folder_id": {
                        "type": "string",
                        "description": "Target folder ID (None or 'root' to move to root level)",
                    },
                },
                "required": ["playlist_id"],
            },
        ),
        # Favorites Management
        Tool(
            name="add_to_favorites",
            description="Add a track, album, artist, playlist, video, or mix to your favorites.",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_id": {"type": "string", "description": "ID of the media item"},
                    "media_type": {
                        "type": "string",
                        "enum": ["track", "album", "artist", "playlist", "video", "mix"],
                        "description": "Type of media",
                    },
                },
                "required": ["media_id", "media_type"],
            },
        ),
        Tool(
            name="remove_from_favorites",
            description="Remove a track, album, artist, playlist, video, or mix from your favorites.",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_id": {"type": "string", "description": "ID of the media item"},
                    "media_type": {
                        "type": "string",
                        "enum": ["track", "album", "artist", "playlist", "video", "mix"],
                        "description": "Type of media",
                    },
                },
                "required": ["media_id", "media_type"],
            },
        ),
        Tool(
            name="get_favorites",
            description="Get your favorite tracks, albums, artists, playlists, videos, or mixes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_type": {
                        "type": "string",
                        "enum": ["track", "album", "artist", "playlist", "video", "mix"],
                        "description": "Type of favorites to retrieve",
                    },
                    "limit": {"type": "integer", "description": "Maximum items to return (default: 50)"},
                    "offset": {"type": "integer", "description": "Pagination offset (default: 0)"},
                },
                "required": ["media_type"],
            },
        ),
        Tool(
            name="get_favorites_summary",
            description="Get a summary count of all your favorites by type.",
            inputSchema={"type": "object", "properties": {}},
        ),
        # Downloads
        Tool(
            name="download_track",
            description="Download a track from TIDAL with specified quality.",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_id": {"type": "string", "description": "TIDAL track ID"},
                    "quality": {
                        "type": "string",
                        "enum": ["Low", "HiFi", "Lossless", "HiRes", "Master"],
                        "description": "Audio quality (default: HiFi)",
                    },
                    "output_path": {"type": "string", "description": "Custom output path (optional)"},
                },
                "required": ["track_id"],
            },
        ),
        Tool(
            name="download_album",
            description="Download an entire album from TIDAL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "album_id": {"type": "string", "description": "TIDAL album ID"},
                    "quality": {
                        "type": "string",
                        "enum": ["Low", "HiFi", "Lossless", "HiRes", "Master"],
                        "description": "Audio quality (default: HiFi)",
                    },
                    "output_path": {"type": "string", "description": "Custom output path (optional)"},
                },
                "required": ["album_id"],
            },
        ),
        Tool(
            name="download_playlist",
            description="Download a playlist from TIDAL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {"type": "string", "description": "TIDAL playlist ID"},
                    "quality": {
                        "type": "string",
                        "enum": ["Low", "HiFi", "Lossless", "HiRes", "Master"],
                        "description": "Audio quality (default: HiFi)",
                    },
                    "output_path": {"type": "string", "description": "Custom output path (optional)"},
                    "include_videos": {"type": "boolean", "description": "Include videos (default: false)"},
                },
                "required": ["playlist_id"],
            },
        ),
        Tool(
            name="get_download_settings",
            description="Get current download settings and quality information.",
            inputSchema={"type": "object", "properties": {}},
        ),
        # Discovery & Details
        Tool(
            name="get_track_details",
            description="Get detailed information about a track including metadata, quality, ISRC, copyright, and lyrics availability.",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_id": {"type": "string", "description": "TIDAL track ID"},
                },
                "required": ["track_id"],
            },
        ),
        Tool(
            name="get_album_details",
            description="Get detailed information about an album including tracks, release date, UPC, credits, and editorial review.",
            inputSchema={
                "type": "object",
                "properties": {
                    "album_id": {"type": "string", "description": "TIDAL album ID"},
                },
                "required": ["album_id"],
            },
        ),
        Tool(
            name="get_artist_details",
            description="Get detailed information about an artist including biography, top tracks, and discography counts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "artist_id": {"type": "string", "description": "TIDAL artist ID"},
                    "include_top_tracks": {"type": "boolean", "description": "Include top tracks (default: true)"},
                },
                "required": ["artist_id"],
            },
        ),
        Tool(
            name="get_artist_albums",
            description="Get albums by an artist, filterable by type (albums, EPs/singles, compilations).",
            inputSchema={
                "type": "object",
                "properties": {
                    "artist_id": {"type": "string", "description": "TIDAL artist ID"},
                    "album_type": {
                        "type": "string",
                        "enum": ["all", "albums", "eps_singles", "other"],
                        "description": "Type of albums to retrieve (default: all)",
                    },
                    "limit": {"type": "integer", "description": "Maximum albums to return (default: 50)"},
                },
                "required": ["artist_id"],
            },
        ),
        Tool(
            name="get_similar_artists",
            description="Get artists similar to a given artist.",
            inputSchema={
                "type": "object",
                "properties": {
                    "artist_id": {"type": "string", "description": "TIDAL artist ID"},
                    "limit": {"type": "integer", "description": "Maximum artists to return (default: 10)"},
                },
                "required": ["artist_id"],
            },
        ),
        Tool(
            name="get_track_lyrics",
            description="Get lyrics for a track (synced or static).",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_id": {"type": "string", "description": "TIDAL track ID"},
                },
                "required": ["track_id"],
            },
        ),
        Tool(
            name="get_playlist_details",
            description="Get detailed information about a playlist including creator, tracks, duration, and metadata.",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {"type": "string", "description": "TIDAL playlist ID"},
                },
                "required": ["playlist_id"],
            },
        ),
        Tool(
            name="browse_genres",
            description="Browse available music genres on TIDAL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum genres to return (default: 50)"},
                },
            },
        ),
        Tool(
            name="get_artist_radio",
            description="Get artist radio - a curated mix of tracks inspired by an artist's style.",
            inputSchema={
                "type": "object",
                "properties": {
                    "artist_id": {"type": "string", "description": "TIDAL artist ID"},
                    "limit": {"type": "integer", "description": "Maximum tracks to return (default: 50)"},
                },
                "required": ["artist_id"],
            },
        ),
        Tool(
            name="browse_home",
            description="Browse TIDAL home page with personalized recommendations, new releases, and featured content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum items per category (default: 50)"},
                },
            },
        ),
        Tool(
            name="browse_explore",
            description="Browse TIDAL explore page with genres, moods, activities, and discovery playlists.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum items per category (default: 20)"},
                },
            },
        ),
        Tool(
            name="get_mixes",
            description="Get TIDAL Mixes - personalized music collections curated based on your listening habits.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum mixes to return (default: 20)"},
                },
            },
        ),
        # User Account
        Tool(
            name="get_user_profile",
            description="Get your TIDAL user profile information including username, email, and account details.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_subscription_info",
            description="Get your TIDAL subscription tier and audio quality information.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution requests.

    Args:
        name: Name of the tool to execute.
        arguments: Arguments passed to the tool.

    Returns:
        List of text content responses.

    Raises:
        ValueError: If tool name is unknown.
    """
    try:
        # Search
        if name == "search_tidal":
            result = await search_tidal(arguments.get("query", ""), arguments.get("media_type"))
            return [TextContent(type="text", text=result)]

        # Playlist Management
        elif name == "create_playlist":
            result = await create_playlist(
                arguments.get("title", ""),
                arguments.get("description", ""),
                arguments.get("public", False),
            )
            return [TextContent(type="text", text=result)]

        elif name == "edit_playlist":
            result = await edit_playlist(
                arguments.get("playlist_id", ""),
                arguments.get("title"),
                arguments.get("description"),
                arguments.get("public"),
            )
            return [TextContent(type="text", text=result)]

        elif name == "delete_playlist":
            result = await delete_playlist(arguments.get("playlist_id", ""))
            return [TextContent(type="text", text=result)]

        elif name == "add_to_playlist":
            result = await add_to_playlist(
                arguments.get("playlist_id", ""),
                arguments.get("track_ids", []),
                arguments.get("position", -1),
                arguments.get("allow_duplicates", False),
            )
            return [TextContent(type="text", text=result)]

        elif name == "remove_from_playlist":
            result = await remove_from_playlist(
                arguments.get("playlist_id", ""),
                arguments.get("track_id"),
                arguments.get("index"),
            )
            return [TextContent(type="text", text=result)]

        elif name == "get_playlist_items":
            result = await get_playlist_items(
                arguments.get("playlist_id", ""),
                arguments.get("limit", 50),
                arguments.get("offset", 0),
            )
            return [TextContent(type="text", text=result)]

        elif name == "get_my_playlists":
            result = await get_my_playlists(
                arguments.get("limit", 50),
                arguments.get("offset", 0),
            )
            return [TextContent(type="text", text=result)]

        elif name == "reorder_playlist":
            result = await reorder_playlist(
                arguments.get("playlist_id", ""),
                arguments.get("from_index", 0),
                arguments.get("to_position", 0),
            )
            return [TextContent(type="text", text=result)]

        elif name == "clear_playlist":
            result = await clear_playlist(arguments.get("playlist_id", ""))
            return [TextContent(type="text", text=result)]

        elif name == "merge_playlists":
            result = await merge_playlists(
                arguments.get("target_playlist_id", ""),
                arguments.get("source_playlist_id", ""),
                arguments.get("allow_duplicates", False),
            )
            return [TextContent(type="text", text=result)]

        elif name == "create_playlist_folder":
            result = await create_playlist_folder(
                arguments.get("title", ""),
                arguments.get("parent_folder_id", "root"),
            )
            return [TextContent(type="text", text=result)]

        elif name == "move_playlist_to_folder":
            result = await move_playlist_to_folder(
                arguments.get("playlist_id", ""),
                arguments.get("folder_id"),
            )
            return [TextContent(type="text", text=result)]

        # Favorites Management
        elif name == "add_to_favorites":
            result = await add_to_favorites(
                arguments.get("media_id", ""),
                arguments.get("media_type", ""),
            )
            return [TextContent(type="text", text=result)]

        elif name == "remove_from_favorites":
            result = await remove_from_favorites(
                arguments.get("media_id", ""),
                arguments.get("media_type", ""),
            )
            return [TextContent(type="text", text=result)]

        elif name == "get_favorites":
            result = await get_favorites(
                arguments.get("media_type", ""),
                arguments.get("limit", 50),
                arguments.get("offset", 0),
            )
            return [TextContent(type="text", text=result)]

        elif name == "get_favorites_summary":
            result = await get_favorites_summary()
            return [TextContent(type="text", text=result)]

        # Downloads
        elif name == "download_track":
            result = await download_track(
                arguments.get("track_id", ""),
                arguments.get("quality", "HiFi"),
                arguments.get("output_path"),
            )
            return [TextContent(type="text", text=result)]

        elif name == "download_album":
            result = await download_album(
                arguments.get("album_id", ""),
                arguments.get("quality", "HiFi"),
                arguments.get("output_path"),
            )
            return [TextContent(type="text", text=result)]

        elif name == "download_playlist":
            result = await download_playlist(
                arguments.get("playlist_id", ""),
                arguments.get("quality", "HiFi"),
                arguments.get("output_path"),
                arguments.get("include_videos", False),
            )
            return [TextContent(type="text", text=result)]

        elif name == "get_download_settings":
            result = await get_download_settings()
            return [TextContent(type="text", text=result)]

        # Discovery & Details
        elif name == "get_track_details":
            result = await get_track_details(arguments.get("track_id", ""))
            return [TextContent(type="text", text=result)]

        elif name == "get_album_details":
            result = await get_album_details(arguments.get("album_id", ""))
            return [TextContent(type="text", text=result)]

        elif name == "get_artist_details":
            result = await get_artist_details(
                arguments.get("artist_id", ""),
                arguments.get("include_top_tracks", True),
            )
            return [TextContent(type="text", text=result)]

        elif name == "get_artist_albums":
            result = await get_artist_albums(
                arguments.get("artist_id", ""),
                arguments.get("album_type", "all"),
                arguments.get("limit", 50),
            )
            return [TextContent(type="text", text=result)]

        elif name == "get_similar_artists":
            result = await get_similar_artists(
                arguments.get("artist_id", ""),
                arguments.get("limit", 10),
            )
            return [TextContent(type="text", text=result)]

        elif name == "get_track_lyrics":
            result = await get_track_lyrics(arguments.get("track_id", ""))
            return [TextContent(type="text", text=result)]

        elif name == "get_playlist_details":
            result = await get_playlist_details(arguments.get("playlist_id", ""))
            return [TextContent(type="text", text=result)]

        elif name == "browse_genres":
            result = await browse_genres(arguments.get("limit", 50))
            return [TextContent(type="text", text=result)]

        elif name == "get_artist_radio":
            result = await get_artist_radio(
                arguments.get("artist_id", ""),
                arguments.get("limit", 50),
            )
            return [TextContent(type="text", text=result)]

        elif name == "browse_home":
            result = await browse_home(arguments.get("limit", 50))
            return [TextContent(type="text", text=result)]

        elif name == "browse_explore":
            result = await browse_explore(arguments.get("limit", 20))
            return [TextContent(type="text", text=result)]

        elif name == "get_mixes":
            result = await get_mixes(arguments.get("limit", 20))
            return [TextContent(type="text", text=result)]

        # User Account
        elif name == "get_user_profile":
            result = await get_user_profile()
            return [TextContent(type="text", text=result)]

        elif name == "get_subscription_info":
            result = await get_subscription_info()
            return [TextContent(type="text", text=result)]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except RuntimeError as e:
        # Authentication or other runtime errors
        error_msg = f"Error: {e!s}"
        logger.error(error_msg)
        return [TextContent(type="text", text=error_msg)]

    except Exception as e:
        # Unexpected errors
        error_msg = f"Unexpected error: {e!s}"
        logger.exception("Tool execution failed")
        return [TextContent(type="text", text=error_msg)]


async def run_server():
    """Run the MCP server with stdio transport."""
    logger.info("Starting TIDAL-DL-NG MCP server...")

    # Check authentication status but don't fail on startup
    try:
        tidal = get_tidal_instance()
        logger.info(f"✓ Authenticated with TIDAL as user: {tidal.session.user.id}")
    except RuntimeError as e:
        logger.warning(f"⚠ Not authenticated with TIDAL: {e}")
        logger.warning("Run 'tidal-dl-ng login' to authenticate. Server will start but tools will require authentication.")

    # Start the server
    async with stdio_server() as (read_stream, write_stream):
        logger.info("✓ MCP server running on stdio")
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main():
    """Main entry point for the MCP server."""
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
