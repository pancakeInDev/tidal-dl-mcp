"""Playlist management tools for TIDAL MCP server."""

from tidalapi.playlist import UserPlaylist

from tidal_dl_ng_mcp.utils.auth import get_tidal_instance, require_auth


@require_auth
async def create_playlist(title: str, description: str = "", public: bool = False) -> str:
    """Create a new TIDAL playlist.

    Args:
        title: Playlist title.
        description: Playlist description (optional).
        public: Whether the playlist should be public (default: False).

    Returns:
        Success message with playlist ID and URL.
    """
    tidal = get_tidal_instance()

    try:
        # Create the playlist
        playlist: UserPlaylist = tidal.session.user.create_playlist(title=title, description=description)

        # Set visibility
        if public:
            playlist.set_playlist_public()
        else:
            playlist.set_playlist_private()

        return f"""✓ Playlist created successfully!

Title: {playlist.name}
Description: {playlist.description or '(none)'}
Visibility: {'Public' if public else 'Private'}
Playlist ID: {playlist.id}
URL: {playlist.share_url}

You can now add tracks using the add_to_playlist tool."""

    except Exception as e:
        return f"✗ Failed to create playlist: {e!s}"


@require_auth
async def edit_playlist(
    playlist_id: str, title: str | None = None, description: str | None = None, public: bool | None = None
) -> str:
    """Edit an existing playlist's metadata.

    Args:
        playlist_id: ID of the playlist to edit.
        title: New title (optional, keeps existing if not provided).
        description: New description (optional, keeps existing if not provided).
        public: New visibility setting (optional, keeps existing if not provided).

    Returns:
        Success message.
    """
    tidal = get_tidal_instance()

    try:
        # Get the playlist
        playlist: UserPlaylist = tidal.session.playlist(playlist_id)

        if not isinstance(playlist, UserPlaylist):
            return f"✗ Playlist {playlist_id} is not a user playlist (cannot edit playlists you don't own)"

        # Update metadata if provided
        if title is not None or description is not None:
            playlist.edit(title=title, description=description)

        # Update visibility if provided
        if public is not None:
            if public:
                playlist.set_playlist_public()
            else:
                playlist.set_playlist_private()

        return f"""✓ Playlist updated successfully!

Title: {playlist.name}
Description: {playlist.description or '(none)'}
URL: {playlist.share_url}"""

    except Exception as e:
        return f"✗ Failed to edit playlist: {e!s}"


@require_auth
async def delete_playlist(playlist_id: str) -> str:
    """Delete a playlist.

    Args:
        playlist_id: ID of the playlist to delete.

    Returns:
        Success message.
    """
    tidal = get_tidal_instance()

    try:
        # Get the playlist
        playlist: UserPlaylist = tidal.session.playlist(playlist_id)

        if not isinstance(playlist, UserPlaylist):
            return f"✗ Playlist {playlist_id} is not a user playlist (cannot delete playlists you don't own)"

        playlist_name = playlist.name

        # Delete it
        success = playlist.delete()

        if success:
            return f"✓ Playlist '{playlist_name}' deleted successfully"
        else:
            return "✗ Failed to delete playlist (unknown error)"

    except Exception as e:
        return f"✗ Failed to delete playlist: {e!s}"


@require_auth
async def add_to_playlist(
    playlist_id: str, track_ids: list[str], position: int = -1, allow_duplicates: bool = False
) -> str:
    """Add tracks to a playlist.

    Args:
        playlist_id: ID of the playlist.
        track_ids: List of track IDs to add.
        position: Position to insert tracks (-1 for end, 0 for beginning).
        allow_duplicates: Whether to allow duplicate tracks.

    Returns:
        Success message with added track count.
    """
    tidal = get_tidal_instance()

    try:
        # Get the playlist
        playlist: UserPlaylist = tidal.session.playlist(playlist_id)

        if not isinstance(playlist, UserPlaylist):
            return f"✗ Playlist {playlist_id} is not a user playlist (cannot edit playlists you don't own)"

        # Add tracks
        result_indices = playlist.add(media_ids=track_ids, allow_duplicates=allow_duplicates, position=position)

        added_count = len(result_indices)

        return f"""✓ Successfully added {added_count} track(s) to '{playlist.name}'

Playlist URL: {playlist.share_url}
Total tracks in playlist: {playlist.num_tracks}"""

    except Exception as e:
        return f"✗ Failed to add tracks to playlist: {e!s}"


@require_auth
async def remove_from_playlist(playlist_id: str, track_id: str | None = None, index: int | None = None) -> str:
    """Remove a track from a playlist.

    Args:
        playlist_id: ID of the playlist.
        track_id: ID of the track to remove (optional if index is provided).
        index: Index of the track to remove (optional if track_id is provided).

    Returns:
        Success message.
    """
    tidal = get_tidal_instance()

    try:
        # Get the playlist
        playlist: UserPlaylist = tidal.session.playlist(playlist_id)

        if not isinstance(playlist, UserPlaylist):
            return f"✗ Playlist {playlist_id} is not a user playlist (cannot edit playlists you don't own)"

        # Remove by ID or index
        if track_id is not None:
            success = playlist.remove_by_id(media_id=track_id)
            identifier = f"track ID {track_id}"
        elif index is not None:
            success = playlist.remove_by_index(index=index)
            identifier = f"index {index}"
        else:
            return "✗ Must provide either track_id or index"

        if success:
            return f"""✓ Successfully removed {identifier} from '{playlist.name}'

Total tracks remaining: {playlist.num_tracks}
Playlist URL: {playlist.share_url}"""
        else:
            return f"✗ Failed to remove {identifier} (track not found or other error)"

    except Exception as e:
        return f"✗ Failed to remove track from playlist: {e!s}"


@require_auth
async def get_playlist_items(playlist_id: str, limit: int = 50, offset: int = 0) -> str:
    """Get items in a playlist.

    Args:
        playlist_id: ID of the playlist.
        limit: Maximum number of items to return (default: 50).
        offset: Offset for pagination (default: 0).

    Returns:
        Formatted list of playlist items.
    """
    tidal = get_tidal_instance()

    try:
        # Get the playlist
        playlist = tidal.session.playlist(playlist_id)

        # Get items
        items = playlist.items(limit=limit, offset=offset)
        total_count = playlist.num_tracks + playlist.num_videos

        output_lines = [
            f"Playlist: {playlist.name}",
            f"By: {playlist.creator.name if hasattr(playlist, 'creator') and playlist.creator else 'Unknown'}",
            f"Total items: {total_count}",
            f"Description: {playlist.description or '(none)'}",
            f"URL: {playlist.share_url}",
            "",
            "=== TRACKS ===",
        ]

        for idx, item in enumerate(items, start=offset + 1):
            # Format based on item type
            if hasattr(item, "artist"):  # Track
                artist = item.artist.name if item.artist else "Unknown Artist"
                title = item.name
                duration_min = item.duration // 60
                duration_sec = item.duration % 60
                explicit = " [EXPLICIT]" if item.explicit else ""

                output_lines.append(
                    f"{idx}. {artist} - {title} [{duration_min}:{duration_sec:02d}]{explicit}"
                )
            else:  # Video or other
                output_lines.append(f"{idx}. {item.name}")

        if total_count > offset + limit:
            output_lines.append(f"\n... and {total_count - offset - limit} more items")

        return "\n".join(output_lines)

    except Exception as e:
        return f"✗ Failed to get playlist items: {e!s}"


@require_auth
async def get_my_playlists(limit: int = 50, offset: int = 0) -> str:
    """Get user's playlists.

    Args:
        limit: Maximum number of playlists to return (default: 50).
        offset: Offset for pagination (default: 0).

    Returns:
        Formatted list of user's playlists.
    """
    tidal = get_tidal_instance()

    try:
        # Get user's playlists
        playlists = tidal.session.user.playlists()

        if not playlists:
            return "You don't have any playlists yet. Create one with create_playlist!"

        output_lines = ["=== YOUR PLAYLISTS ===", ""]

        for idx, playlist in enumerate(playlists[offset : offset + limit], start=offset + 1):
            num_items = playlist.num_tracks + (playlist.num_videos if hasattr(playlist, "num_videos") else 0)
            visibility = "Public" if getattr(playlist, "public", False) else "Private"

            output_lines.append(f"{idx}. {playlist.name}")
            output_lines.append(f"   Items: {num_items} | {visibility}")
            output_lines.append(f"   ID: {playlist.id}")
            output_lines.append(f"   URL: {playlist.share_url}")
            if playlist.description:
                output_lines.append(f"   Description: {playlist.description}")
            output_lines.append("")

        if len(playlists) > offset + limit:
            output_lines.append(f"... and {len(playlists) - offset - limit} more playlists")

        return "\n".join(output_lines)

    except Exception as e:
        return f"✗ Failed to get playlists: {e!s}"
