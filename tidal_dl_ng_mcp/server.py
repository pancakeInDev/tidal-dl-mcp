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
)
from tidal_dl_ng_mcp.tools.favorites import (
    add_to_favorites,
    remove_from_favorites,
    get_favorites,
    get_favorites_summary,
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
