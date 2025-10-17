"""Search tool for TIDAL MCP server."""

from tidalapi import Album, Artist, Mix, Playlist, Track, Video

from tidal_dl_ng.helper.tidal import (
    get_tidal_media_id,
    get_tidal_media_type,
    instantiate_media,
    name_builder_artist,
    name_builder_title,
    search_results_all,
    url_ending_clean,
)
from tidal_dl_ng_mcp.utils.auth import get_tidal_instance, require_auth


def _format_track(track: Track, index: int) -> str:
    """Format a track for display.

    Args:
        track: Track object.
        index: Index in results.

    Returns:
        Formatted track string.
    """
    artist = name_builder_artist(track)
    title = name_builder_title(track)
    album = track.album.name if track.album else "Unknown Album"
    duration_min = track.duration // 60
    duration_sec = track.duration % 60
    explicit = " [EXPLICIT]" if track.explicit else ""

    return f"{index}. {artist} - {title} ({album}) [{duration_min}:{duration_sec:02d}]{explicit}\n   URL: {track.share_url}"


def _format_album(album: Album, index: int) -> str:
    """Format an album for display.

    Args:
        album: Album object.
        index: Index in results.

    Returns:
        Formatted album string.
    """
    artist = name_builder_artist(album)
    explicit = " [EXPLICIT]" if album.explicit else ""
    num_tracks = album.num_tracks if hasattr(album, "num_tracks") else "?"

    return f"{index}. {artist} - {album.name} ({num_tracks} tracks){explicit}\n   URL: {album.share_url}"


def _format_artist(artist: Artist, index: int) -> str:
    """Format an artist for display.

    Args:
        artist: Artist object.
        index: Index in results.

    Returns:
        Formatted artist string.
    """
    return f"{index}. {artist.name}\n   URL: {artist.share_url}"


def _format_playlist(playlist: Playlist, index: int) -> str:
    """Format a playlist for display.

    Args:
        playlist: Playlist object.
        index: Index in results.

    Returns:
        Formatted playlist string.
    """
    num_items = (playlist.num_tracks + playlist.num_videos) if hasattr(playlist, "num_tracks") else "?"
    creator = playlist.creator.name if hasattr(playlist, "creator") and playlist.creator else "Unknown"

    return f"{index}. {playlist.name} by {creator} ({num_items} items)\n   {playlist.description or ''}\n   URL: {playlist.share_url}"


def _format_video(video: Video, index: int) -> str:
    """Format a video for display.

    Args:
        video: Video object.
        index: Index in results.

    Returns:
        Formatted video string.
    """
    artist = name_builder_artist(video)
    title = name_builder_title(video)
    duration_min = video.duration // 60
    duration_sec = video.duration % 60
    explicit = " [EXPLICIT]" if video.explicit else ""

    return f"{index}. {artist} - {title} [{duration_min}:{duration_sec:02d}]{explicit}\n   URL: {video.share_url}"


def _format_mix(mix: Mix, index: int) -> str:
    """Format a mix for display.

    Args:
        mix: Mix object.
        index: Index in results.

    Returns:
        Formatted mix string.
    """
    return f"{index}. {mix.title}\n   {mix.sub_title}\n   URL: {mix.share_url}"


def format_search_results(results: dict[str, list]) -> str:
    """Format search results for display.

    Args:
        results: Dictionary of search results by type.

    Returns:
        Formatted results string.
    """
    output_lines = []

    for media_type, items in results.items():
        # Skip empty or non-list results
        if not items or not isinstance(items, list):
            continue

        # Add section header
        output_lines.append(f"\n=== {media_type.upper()} ===")

        for idx, item in enumerate(items[:10], 1):  # Limit to 10 results per type
            if isinstance(item, Track):
                output_lines.append(_format_track(item, idx))
            elif isinstance(item, Album):
                output_lines.append(_format_album(item, idx))
            elif isinstance(item, Artist):
                output_lines.append(_format_artist(item, idx))
            elif isinstance(item, Playlist):
                output_lines.append(_format_playlist(item, idx))
            elif isinstance(item, Video):
                output_lines.append(_format_video(item, idx))
            elif isinstance(item, Mix):
                output_lines.append(_format_mix(item, idx))

        if len(items) > 10:
            output_lines.append(f"\n... and {len(items) - 10} more results")

    return "\n".join(output_lines) if output_lines else "No results found."


@require_auth
async def search_tidal(query: str, media_type: str | None = None) -> str:
    """Search TIDAL for media.

    Args:
        query: Search query string or TIDAL URL.
        media_type: Optional filter (track, album, artist, playlist, video).

    Returns:
        Formatted search results as string.
    """
    tidal = get_tidal_instance()

    # Check if query is a URL
    if "http" in query:
        try:
            url_clean = url_ending_clean(query)
            detected_type = get_tidal_media_type(url_clean)
            media_id = get_tidal_media_id(url_clean)

            # Instantiate the media directly
            media = instantiate_media(tidal.session, detected_type, media_id)

            # Format as single result
            if isinstance(media, Track):
                result_text = f"Found track:\n{_format_track(media, 1)}"
            elif isinstance(media, Album):
                result_text = f"Found album:\n{_format_album(media, 1)}"
            elif isinstance(media, Artist):
                result_text = f"Found artist:\n{_format_artist(media, 1)}"
            elif isinstance(media, Playlist):
                result_text = f"Found playlist:\n{_format_playlist(media, 1)}"
            elif isinstance(media, Video):
                result_text = f"Found video:\n{_format_video(media, 1)}"
            else:
                result_text = f"Found: {media}"

            return result_text

        except Exception as e:
            return f"Error parsing URL: {e!s}"

    # Regular search
    types_map = {
        "track": [Track],
        "album": [Album],
        "artist": [Artist],
        "playlist": [Playlist],
        "video": [Video],
    }

    search_types = types_map.get(media_type.lower()) if media_type else None

    results = search_results_all(session=tidal.session, needle=query, types_media=search_types)

    return format_search_results(results)
