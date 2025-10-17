"""Favorites management tools for TIDAL MCP server."""

from tidal_dl_ng_mcp.utils.auth import get_tidal_instance, require_auth


@require_auth
async def add_to_favorites(media_id: str, media_type: str) -> str:
    """Add a track, album, artist, playlist, or video to favorites.

    Args:
        media_id: ID of the media item.
        media_type: Type of media (track, album, artist, playlist, video, mix).

    Returns:
        Success message.
    """
    tidal = get_tidal_instance()

    try:
        favorites = tidal.session.user.favorites

        # Add to appropriate favorites category
        success = False
        if media_type == "track":
            success = favorites.add_track(media_id)
        elif media_type == "album":
            success = favorites.add_album(media_id)
        elif media_type == "artist":
            success = favorites.add_artist(media_id)
        elif media_type == "playlist":
            success = favorites.add_playlist(media_id)
        elif media_type == "video":
            success = favorites.add_video(media_id)
        elif media_type == "mix":
            success = favorites.add_mixes(media_id)
        else:
            return f"✗ Invalid media type: {media_type}. Must be one of: track, album, artist, playlist, video, mix"

        if success:
            return f"✓ Added {media_type} (ID: {media_id}) to your favorites"
        else:
            return f"✗ Failed to add {media_type} to favorites (may already be favorited or invalid ID)"

    except Exception as e:
        return f"✗ Failed to add to favorites: {e!s}"


@require_auth
async def remove_from_favorites(media_id: str, media_type: str) -> str:
    """Remove a track, album, artist, playlist, or video from favorites.

    Args:
        media_id: ID of the media item.
        media_type: Type of media (track, album, artist, playlist, video, mix).

    Returns:
        Success message.
    """
    tidal = get_tidal_instance()

    try:
        favorites = tidal.session.user.favorites

        # Remove from appropriate favorites category
        success = False
        if media_type == "track":
            success = favorites.remove_track(media_id)
        elif media_type == "album":
            success = favorites.remove_album(media_id)
        elif media_type == "artist":
            success = favorites.remove_artist(media_id)
        elif media_type == "playlist":
            success = favorites.remove_playlist(media_id)
        elif media_type == "video":
            success = favorites.remove_video(media_id)
        elif media_type == "mix":
            success = favorites.remove_mixes(media_id)
        else:
            return f"✗ Invalid media type: {media_type}. Must be one of: track, album, artist, playlist, video, mix"

        if success:
            return f"✓ Removed {media_type} (ID: {media_id}) from your favorites"
        else:
            return f"✗ Failed to remove {media_type} from favorites (may not be in favorites or invalid ID)"

    except Exception as e:
        return f"✗ Failed to remove from favorites: {e!s}"


@require_auth
async def get_favorites(media_type: str, limit: int = 50, offset: int = 0) -> str:
    """Get user's favorite tracks, albums, artists, playlists, videos, or mixes.

    Args:
        media_type: Type of favorites to retrieve (track, album, artist, playlist, video, mix).
        limit: Maximum number of items to return (default: 50).
        offset: Offset for pagination (default: 0).

    Returns:
        Formatted list of favorites.
    """
    tidal = get_tidal_instance()

    try:
        favorites = tidal.session.user.favorites

        # Get appropriate favorites
        items = []
        total_count = 0

        if media_type == "track":
            items = favorites.tracks(limit=limit, offset=offset)
            total_count = favorites.get_tracks_count()
        elif media_type == "album":
            items = favorites.albums(limit=limit, offset=offset)
            total_count = favorites.get_albums_count()
        elif media_type == "artist":
            items = favorites.artists(limit=limit, offset=offset)
            total_count = favorites.get_artists_count()
        elif media_type == "playlist":
            items = favorites.playlists(limit=limit, offset=offset)
            total_count = favorites.get_playlists_count()
        elif media_type == "video":
            items = favorites.videos(limit=limit, offset=offset)
            # Note: videos don't have a count method
            total_count = len(items) if offset == 0 else "?"
        elif media_type == "mix":
            items = favorites.mixes(limit=limit, offset=offset)
            total_count = len(items) if offset == 0 else "?"
        else:
            return f"✗ Invalid media type: {media_type}. Must be one of: track, album, artist, playlist, video, mix"

        if not items:
            return f"You don't have any favorite {media_type}s yet!"

        output_lines = [f"=== YOUR FAVORITE {media_type.upper()}S ===", f"Total: {total_count}", ""]

        for idx, item in enumerate(items, start=offset + 1):
            if media_type == "track":
                artist = item.artist.name if item.artist else "Unknown Artist"
                title = item.name
                album = item.album.name if item.album else "Unknown Album"
                duration_min = item.duration // 60
                duration_sec = item.duration % 60
                explicit = " [EXPLICIT]" if item.explicit else ""

                output_lines.append(f"{idx}. {artist} - {title}")
                output_lines.append(f"   Album: {album} | Duration: {duration_min}:{duration_sec:02d}{explicit}")
                output_lines.append(f"   ID: {item.id} | URL: {item.share_url}")

            elif media_type == "album":
                artist = item.artist.name if item.artist else "Unknown Artist"
                num_tracks = item.num_tracks if hasattr(item, "num_tracks") else "?"
                explicit = " [EXPLICIT]" if item.explicit else ""

                output_lines.append(f"{idx}. {artist} - {item.name}")
                output_lines.append(f"   Tracks: {num_tracks}{explicit}")
                output_lines.append(f"   ID: {item.id} | URL: {item.share_url}")

            elif media_type == "artist":
                output_lines.append(f"{idx}. {item.name}")
                output_lines.append(f"   ID: {item.id} | URL: {item.share_url}")

            elif media_type == "playlist":
                creator = item.creator.name if hasattr(item, "creator") and item.creator else "Unknown"
                num_items = item.num_tracks + (item.num_videos if hasattr(item, "num_videos") else 0)

                output_lines.append(f"{idx}. {item.name} by {creator}")
                output_lines.append(f"   Items: {num_items}")
                output_lines.append(f"   ID: {item.id} | URL: {item.share_url}")

            elif media_type == "video":
                artist = item.artist.name if hasattr(item, "artist") and item.artist else "Unknown Artist"
                duration_min = item.duration // 60
                duration_sec = item.duration % 60
                explicit = " [EXPLICIT]" if item.explicit else ""

                output_lines.append(f"{idx}. {artist} - {item.name}")
                output_lines.append(f"   Duration: {duration_min}:{duration_sec:02d}{explicit}")
                output_lines.append(f"   ID: {item.id} | URL: {item.share_url}")

            elif media_type == "mix":
                output_lines.append(f"{idx}. {item.title}")
                output_lines.append(f"   {item.sub_title}")
                output_lines.append(f"   URL: {item.share_url}")

            output_lines.append("")

        if isinstance(total_count, int) and total_count > offset + limit:
            output_lines.append(f"... and {total_count - offset - limit} more {media_type}s")

        return "\n".join(output_lines)

    except Exception as e:
        return f"✗ Failed to get favorites: {e!s}"


@require_auth
async def get_favorites_summary() -> str:
    """Get a summary of all favorites counts.

    Returns:
        Summary of favorites by type.
    """
    tidal = get_tidal_instance()

    try:
        favorites = tidal.session.user.favorites

        tracks_count = favorites.get_tracks_count()
        albums_count = favorites.get_albums_count()
        artists_count = favorites.get_artists_count()
        playlists_count = favorites.get_playlists_count()

        return f"""=== YOUR FAVORITES SUMMARY ===

Tracks: {tracks_count}
Albums: {albums_count}
Artists: {artists_count}
Playlists: {playlists_count}

Use get_favorites to view items in each category."""

    except Exception as e:
        return f"✗ Failed to get favorites summary: {e!s}"
