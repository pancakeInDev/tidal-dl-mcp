"""Download tools for TIDAL MCP server."""

import pathlib
import logging
from threading import Event
from typing import List

from rich.progress import Progress
from tidalapi.media import Quality

from tidal_dl_ng.download import Download
from tidal_dl_ng.constants import MediaType, QualityVideo
from tidal_dl_ng.helper.wrapper import LoggerWrapped
from tidal_dl_ng_mcp.utils.auth import get_tidal_instance, require_auth


# Configure logger
logger = logging.getLogger("tidal-dl-ng-mcp")


class ProgressCollector:
    """Collects progress messages without writing to stdout."""

    def __init__(self):
        self.messages: List[str] = []
        self.downloads_completed = 0

    def log(self, message: str) -> None:
        """Collect a progress message."""
        self.messages.append(message)
        # Count completed downloads
        if "Downloaded item" in message:
            self.downloads_completed += 1

    def get_summary(self) -> str:
        """Get a summary of progress."""
        if not self.messages:
            return ""

        summary_lines = []

        # Show download count if multiple items
        if self.downloads_completed > 1:
            summary_lines.append(f"  ✓ Downloaded {self.downloads_completed} items")

        # Show last few messages (excluding FFmpeg warnings)
        relevant_messages = [
            msg for msg in self.messages
            if "Downloaded item" in msg and "FFmpeg" not in msg
        ]

        # Show last 3 downloads
        for msg in relevant_messages[-3:]:
            # Clean up the message
            if "Downloaded item" in msg:
                item_name = msg.replace("Downloaded item", "").strip(" '.\"")
                summary_lines.append(f"  • {item_name}")

        return "\n".join(summary_lines) if summary_lines else ""


@require_auth
async def download_track(
    track_id: str,
    quality: str = "HiFi",
    output_path: str | None = None,
) -> str:
    """Download a track from TIDAL.

    Args:
        track_id: TIDAL track ID.
        quality: Audio quality (HiFi, Lossless, HiRes, Master, default: HiFi).
        output_path: Custom output path (optional, uses default if not provided).

    Returns:
        Success message with file path or error message.
    """
    tidal = get_tidal_instance()

    try:
        # Map quality string to Quality enum
        quality_map = {
            "Low": Quality.low_320k,
            "High": Quality.high_lossless,
            "HiFi": Quality.high_lossless,
            "Lossless": Quality.high_lossless,
            "HiRes": Quality.hi_res_lossless,
            "Master": Quality.hi_res_lossless,
        }

        quality_audio = quality_map.get(quality, Quality.high_lossless)

        # Determine output path
        if output_path:
            path_base = output_path
        else:
            # Use user's home directory by default
            path_base = str(pathlib.Path.home() / "Music" / "TIDAL")

        # Create progress collector to gather download info
        progress_collector = ProgressCollector()

        # Create logger wrapper that collects progress without stdout pollution
        fn_logger = LoggerWrapped(progress_collector.log)

        # Create progress bar (completely disabled for MCP - no output allowed)
        progress = Progress(disable=True)

        # Create abort and run events
        event_abort = Event()
        event_run = Event()
        event_run.set()  # Start immediately

        # Create Download instance
        downloader = Download(
            session=tidal.session,
            path_base=path_base,
            fn_logger=fn_logger,
            skip_existing=True,
            progress=progress,
            event_abort=event_abort,
            event_run=event_run,
        )

        # Use proper template variables from settings
        file_template = "Tracks/{artist_name} - {track_title}{track_explicit}"

        # Download the track
        success, result_path = downloader.item(
            file_template=file_template,
            media_id=track_id,
            media_type=MediaType.TRACK,
            quality_audio=quality_audio,
        )

        # Progress already disabled, no need to stop

        # Get progress summary
        progress_summary = progress_collector.get_summary()
        progress_section = f"\n\nDownload Progress:\n{progress_summary}" if progress_summary else ""

        if success and result_path:
            return f"""✓ Track downloaded successfully!

File: {result_path}
Quality: {quality}
Location: {path_base}

The track has been saved with full metadata, cover art, and lyrics (if available).{progress_section}"""
        else:
            return "✗ Failed to download track (track may not be available or invalid ID)"

    except Exception as e:
        return f"✗ Download failed: {e!s}"


@require_auth
async def download_album(
    album_id: str,
    quality: str = "HiFi",
    output_path: str | None = None,
) -> str:
    """Download an album from TIDAL.

    Args:
        album_id: TIDAL album ID.
        quality: Audio quality (HiFi, Lossless, HiRes, Master, default: HiFi).
        output_path: Custom output path (optional, uses default if not provided).

    Returns:
        Success message with details or error message.
    """
    tidal = get_tidal_instance()

    try:
        # Map quality string to Quality enum
        quality_map = {
            "Low": Quality.low_320k,
            "High": Quality.high_lossless,
            "HiFi": Quality.high_lossless,
            "Lossless": Quality.high_lossless,
            "HiRes": Quality.hi_res_lossless,
            "Master": Quality.hi_res_lossless,
        }

        quality_audio = quality_map.get(quality, Quality.high_lossless)

        # Determine output path
        if output_path:
            path_base = output_path
        else:
            path_base = str(pathlib.Path.home() / "Music" / "TIDAL")

        # Create progress collector to gather download info
        progress_collector = ProgressCollector()

        # Create logger wrapper that collects progress without stdout pollution
        fn_logger = LoggerWrapped(progress_collector.log)

        # Create progress bar (completely disabled for MCP - no output allowed)
        progress = Progress(disable=True)

        # Create abort and run events
        event_abort = Event()
        event_run = Event()
        event_run.set()

        # Create Download instance
        downloader = Download(
            session=tidal.session,
            path_base=path_base,
            fn_logger=fn_logger,
            skip_existing=True,
            progress=progress,
            event_abort=event_abort,
            event_run=event_run,
        )

        # Get album info for display
        album = tidal.session.album(album_id)
        album_name = album.name
        artist_name = album.artist.name if album.artist else "Unknown Artist"
        track_count = album.num_tracks

        # Use proper template variables from settings for album
        file_template = "Albums/{album_artist} - {album_title}{album_explicit}/{track_volume_num_optional}{album_track_num}. {artist_name} - {track_title}{album_explicit}"

        # Download the album
        downloader.items(
            file_template=file_template,
            media_id=album_id,
            media_type=MediaType.ALBUM,
            quality_audio=quality_audio,
            download_delay=True,
        )

        # Progress already disabled, no need to stop

        # Get progress summary
        progress_summary = progress_collector.get_summary()
        progress_section = f"\n\nDownload Progress:\n{progress_summary}" if progress_summary else ""

        return f"""✓ Album downloaded successfully!

Album: {album_name}
Artist: {artist_name}
Tracks: {track_count}
Quality: {quality}
Location: {path_base}/{artist_name}/{album_name}/

All tracks have been saved with full metadata, cover art, and lyrics (if available).
A playlist file has been created for the album.{progress_section}"""

    except Exception as e:
        return f"✗ Download failed: {e!s}"


@require_auth
async def download_playlist(
    playlist_id: str,
    quality: str = "HiFi",
    output_path: str | None = None,
    include_videos: bool = False,
) -> str:
    """Download a playlist from TIDAL.

    Args:
        playlist_id: TIDAL playlist ID.
        quality: Audio quality (HiFi, Lossless, HiRes, Master, default: HiFi).
        output_path: Custom output path (optional, uses default if not provided).
        include_videos: Whether to include videos (default: False).

    Returns:
        Success message with details or error message.
    """
    tidal = get_tidal_instance()

    try:
        # Map quality string to Quality enum
        quality_map = {
            "Low": Quality.low_320k,
            "High": Quality.high_lossless,
            "HiFi": Quality.high_lossless,
            "Lossless": Quality.high_lossless,
            "HiRes": Quality.hi_res_lossless,
            "Master": Quality.hi_res_lossless,
        }

        quality_audio = quality_map.get(quality, Quality.high_lossless)

        # Determine output path
        if output_path:
            path_base = output_path
        else:
            path_base = str(pathlib.Path.home() / "Music" / "TIDAL")

        # Create progress collector to gather download info
        progress_collector = ProgressCollector()

        # Create logger wrapper that collects progress without stdout pollution
        fn_logger = LoggerWrapped(progress_collector.log)

        # Create progress bar (completely disabled for MCP - no output allowed)
        progress = Progress(disable=True)

        # Create abort and run events
        event_abort = Event()
        event_run = Event()
        event_run.set()

        # Create Download instance
        downloader = Download(
            session=tidal.session,
            path_base=path_base,
            fn_logger=fn_logger,
            skip_existing=True,
            progress=progress,
            event_abort=event_abort,
            event_run=event_run,
        )

        # Get playlist info for display
        playlist = tidal.session.playlist(playlist_id)
        playlist_name = playlist.name
        creator_name = playlist.creator.name if hasattr(playlist, "creator") and playlist.creator else "Unknown"
        item_count = playlist.num_tracks + (playlist.num_videos if hasattr(playlist, "num_videos") else 0)

        # Use proper template variables from settings for playlist
        file_template = "Playlists/{playlist_name}/{list_pos}. {artist_name} - {track_title}"

        # Download the playlist
        downloader.items(
            file_template=file_template,
            media_id=playlist_id,
            media_type=MediaType.PLAYLIST,
            quality_audio=quality_audio,
            video_download=include_videos,
            download_delay=True,
        )

        # Progress already disabled, no need to stop

        # Get progress summary
        progress_summary = progress_collector.get_summary()
        progress_section = f"\n\nDownload Progress:\n{progress_summary}" if progress_summary else ""

        return f"""✓ Playlist downloaded successfully!

Playlist: {playlist_name}
Creator: {creator_name}
Items: {item_count}
Quality: {quality}
Location: {path_base}/Playlists/{playlist_name}/

All tracks have been saved with full metadata.
A playlist file (m3u) has been created.{progress_section}"""

    except Exception as e:
        return f"✗ Download failed: {e!s}"


@require_auth
async def get_download_settings() -> str:
    """Get current download settings and quality information.

    Returns:
        Formatted settings information.
    """
    tidal = get_tidal_instance()

    try:
        # Get current session quality
        quality_audio = tidal.session.audio_quality
        quality_name = {
            Quality.low_96k: "Low (96 kbps AAC)",
            Quality.low_320k: "Low (320 kbps AAC)",
            Quality.high_lossless: "HiFi / Lossless (FLAC 16-bit/44.1kHz)",
            Quality.hi_res_lossless: "HiRes / Master (FLAC up to 24-bit/192kHz)",
        }.get(quality_audio, "Unknown")

        # Get default download path
        default_path = str(pathlib.Path.home() / "Music" / "TIDAL")

        return f"""=== TIDAL DOWNLOAD SETTINGS ===

Current Quality: {quality_name}
Default Location: {default_path}

Available Quality Options:
- Low: 320 kbps AAC
- HiFi/Lossless: FLAC 16-bit/44.1kHz (CD Quality)
- HiRes/Master: FLAC up to 24-bit/192kHz (Studio Master)

Note: Actual quality depends on your TIDAL subscription tier.
- TIDAL HiFi: Up to 'HiFi' quality (16-bit/44.1kHz)
- TIDAL HiFi Plus: Up to 'HiRes' quality (24-bit/192kHz)

Downloads include:
✓ Full metadata (artist, album, title, etc.)
✓ Album artwork
✓ Lyrics (when available)
✓ Playlist files (m3u)
✓ Proper folder organization"""

    except Exception as e:
        return f"✗ Failed to get settings: {e!s}"
