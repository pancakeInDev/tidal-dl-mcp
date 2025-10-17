"""Discovery and detailed information tools for TIDAL MCP server."""

from tidal_dl_ng_mcp.utils.auth import get_tidal_instance, require_auth


@require_auth
async def get_track_details(track_id: str) -> str:
    """Get detailed information about a track.

    Args:
        track_id: TIDAL track ID.

    Returns:
        Formatted track details including metadata, quality, credits.
    """
    tidal = get_tidal_instance()

    try:
        track = tidal.session.track(track_id)

        # Get lyrics if available
        lyrics_info = ""
        try:
            lyrics = track.lyrics()
            if lyrics:
                if hasattr(lyrics, "subtitles") and lyrics.subtitles:
                    lyrics_info = f"\n✓ Synced lyrics available ({len(lyrics.subtitles)} lines)"
                elif hasattr(lyrics, "text") and lyrics.text:
                    lyrics_info = f"\n✓ Static lyrics available"
        except Exception:
            lyrics_info = "\n✗ No lyrics available"

        return f"""=== TRACK DETAILS ===

Title: {track.name}
Artist: {track.artist.name}
Album: {track.album.name}

Duration: {track.duration // 60}:{track.duration % 60:02d}
Track Number: {track.track_num if hasattr(track, "track_num") else "N/A"} / {track.album.num_tracks}
Volume Number: {track.volume_num if hasattr(track, "volume_num") else "N/A"}

Audio Quality: {track.audio_quality if hasattr(track, "audio_quality") else "N/A"}
Available: {"Yes" if track.available else "No"}
Explicit: {"Yes" if track.explicit else "No"}

ISRC: {track.isrc if hasattr(track, "isrc") else "N/A"}
Copyright: {track.copyright if hasattr(track, "copyright") else "N/A"}
Release Date: {track.album.release_date if hasattr(track.album, "release_date") else "N/A"}
{lyrics_info}

Album ID: {track.album.id}
Artist ID: {track.artist.id}
Track ID: {track.id}

TIDAL URL: https://tidal.com/browse/track/{track.id}
"""

    except Exception as e:
        return f"✗ Failed to get track details: {e!s}"


@require_auth
async def get_album_details(album_id: str) -> str:
    """Get detailed information about an album.

    Args:
        album_id: TIDAL album ID.

    Returns:
        Formatted album details including tracks, metadata, credits.
    """
    tidal = get_tidal_instance()

    try:
        album = tidal.session.album(album_id)

        # Get tracks
        tracks = album.tracks()
        track_list = "\n".join([
            f"  {i+1:2d}. {track.name} ({track.duration // 60}:{track.duration % 60:02d})"
            for i, track in enumerate(tracks[:20])  # Limit to first 20
        ])
        if len(tracks) > 20:
            track_list += f"\n  ... and {len(tracks) - 20} more tracks"

        # Get audio resolution
        resolution = ""
        try:
            audio_res = album.get_audio_resolution()
            resolution = f"\nAudio Resolution: {audio_res}"
        except Exception:
            pass

        # Get review if available
        review_info = ""
        try:
            review = album.review()
            if review:
                review_text = review[:200] + "..." if len(review) > 200 else review
                review_info = f"\n\nEditorial Review:\n{review_text}"
        except Exception:
            pass

        return f"""=== ALBUM DETAILS ===

Title: {album.name}
Artist: {album.artist.name}

Release Date: {album.release_date if hasattr(album, "release_date") else "N/A"}
Number of Tracks: {album.num_tracks}
Number of Volumes: {album.num_volumes if hasattr(album, "num_volumes") else 1}
Total Duration: {album.duration // 60} minutes

Type: {album.type if hasattr(album, "type") else "N/A"}
Explicit: {"Yes" if album.explicit else "No"}
Available: {"Yes" if album.available else "No"}

UPC: {album.upc if hasattr(album, "upc") else "N/A"}
Copyright: {album.copyright if hasattr(album, "copyright") else "N/A"}{resolution}

Tracklist:
{track_list}
{review_info}

Album ID: {album.id}
Artist ID: {album.artist.id}

TIDAL URL: https://tidal.com/browse/album/{album.id}
"""

    except Exception as e:
        return f"✗ Failed to get album details: {e!s}"


@require_auth
async def get_artist_details(artist_id: str, include_top_tracks: bool = True) -> str:
    """Get detailed information about an artist.

    Args:
        artist_id: TIDAL artist ID.
        include_top_tracks: Include top tracks (default: True).

    Returns:
        Formatted artist details including bio, top tracks, albums.
    """
    tidal = get_tidal_instance()

    try:
        artist = tidal.session.artist(artist_id)

        # Get bio
        bio_text = ""
        try:
            bio = artist.get_bio()
            if bio and hasattr(bio, "text") and bio.text:
                bio_text = bio.text[:500]
                if len(bio.text) > 500:
                    bio_text += "..."
                bio_text = f"\nBiography:\n{bio_text}\n"
        except Exception:
            pass

        # Get top tracks
        top_tracks_text = ""
        if include_top_tracks:
            try:
                top_tracks = artist.get_top_tracks(limit=10)
                if top_tracks:
                    tracks_list = "\n".join([
                        f"  {i+1:2d}. {track.name} - {track.album.name if hasattr(track, 'album') else 'Unknown Album'}"
                        for i, track in enumerate(top_tracks[:10])
                    ])
                    top_tracks_text = f"\nTop Tracks:\n{tracks_list}\n"
            except Exception:
                pass

        # Get album counts
        albums_count = 0
        eps_count = 0
        try:
            albums = artist.get_albums()
            albums_count = len(albums) if albums else 0
        except Exception:
            pass

        try:
            eps = artist.get_ep_singles()
            eps_count = len(eps) if eps else 0
        except Exception:
            pass

        return f"""=== ARTIST DETAILS ===

Name: {artist.name}
Artist ID: {artist.id}
{bio_text}
Discography:
  Albums: {albums_count}
  EPs & Singles: {eps_count}
{top_tracks_text}
TIDAL URL: https://tidal.com/browse/artist/{artist.id}
"""

    except Exception as e:
        return f"✗ Failed to get artist details: {e!s}"


@require_auth
async def get_artist_albums(
    artist_id: str,
    album_type: str = "all",
    limit: int = 50,
) -> str:
    """Get albums by an artist.

    Args:
        artist_id: TIDAL artist ID.
        album_type: Type of albums ('all', 'albums', 'eps_singles', 'other').
        limit: Maximum albums to return (default: 50).

    Returns:
        Formatted list of artist's albums.
    """
    tidal = get_tidal_instance()

    try:
        artist = tidal.session.artist(artist_id)

        # Get albums based on type
        if album_type == "albums":
            albums = artist.get_albums(limit=limit)
            type_label = "Albums"
        elif album_type == "eps_singles":
            albums = artist.get_ep_singles(limit=limit)
            type_label = "EPs & Singles"
        elif album_type == "other":
            albums = artist.get_other(limit=limit)
            type_label = "Compilations & Other"
        else:  # all
            albums_list = artist.get_albums(limit=limit) or []
            eps_list = artist.get_ep_singles(limit=limit) or []
            albums = albums_list + eps_list
            type_label = "All Releases"

        if not albums:
            return f"✗ No {type_label.lower()} found for {artist.name}"

        albums_text = "\n".join([
            f"{i+1:3d}. {album.name} ({album.release_date.year if hasattr(album, 'release_date') and album.release_date else 'N/A'})"
            f"\n     {album.num_tracks} tracks | ID: {album.id}"
            for i, album in enumerate(albums[:limit])
        ])

        return f"""=== {type_label.upper()} BY {artist.name.upper()} ===

Total: {len(albums)} releases

{albums_text}
"""

    except Exception as e:
        return f"✗ Failed to get artist albums: {e!s}"


@require_auth
async def get_similar_artists(artist_id: str, limit: int = 10) -> str:
    """Get similar artists.

    Args:
        artist_id: TIDAL artist ID.
        limit: Maximum artists to return (default: 10).

    Returns:
        Formatted list of similar artists.
    """
    tidal = get_tidal_instance()

    try:
        artist = tidal.session.artist(artist_id)
        similar = artist.get_similar()

        if not similar:
            return f"✗ No similar artists found for {artist.name}"

        similar_text = "\n".join([
            f"{i+1:2d}. {sim_artist.name} (ID: {sim_artist.id})"
            for i, sim_artist in enumerate(similar[:limit])
        ])

        return f"""=== SIMILAR TO {artist.name.upper()} ===

{similar_text}

Tip: Use get_artist_details with any of these artist IDs to learn more!
"""

    except Exception as e:
        return f"✗ Failed to get similar artists: {e!s}"


@require_auth
async def get_track_lyrics(track_id: str) -> str:
    """Get lyrics for a track.

    Args:
        track_id: TIDAL track ID.

    Returns:
        Formatted lyrics (synced or static).
    """
    tidal = get_tidal_instance()

    try:
        track = tidal.session.track(track_id)
        lyrics = track.lyrics()

        if not lyrics:
            return f"✗ No lyrics available for '{track.name}' by {track.artist.name}"

        # Check for synced lyrics
        if hasattr(lyrics, "subtitles") and lyrics.subtitles:
            lyrics_text = "\n".join([
                f"[{sub.start // 1000 // 60:02d}:{(sub.start // 1000) % 60:02d}] {sub.text}"
                for sub in lyrics.subtitles[:100]  # Limit to first 100 lines
            ])
            if len(lyrics.subtitles) > 100:
                lyrics_text += f"\n... and {len(lyrics.subtitles) - 100} more lines"
            lyrics_type = "Synced Lyrics"
        elif hasattr(lyrics, "text") and lyrics.text:
            lyrics_text = lyrics.text[:2000]
            if len(lyrics.text) > 2000:
                lyrics_text += "\n\n... (truncated)"
            lyrics_type = "Static Lyrics"
        else:
            return f"✗ Lyrics data available but in unknown format for '{track.name}'"

        return f"""=== {lyrics_type.upper()}: {track.name} ===
Artist: {track.artist.name}
Album: {track.album.name}

{lyrics_text}

Provider: {lyrics.provider if hasattr(lyrics, "provider") else "TIDAL"}
"""

    except Exception as e:
        return f"✗ Failed to get lyrics: {e!s}"


@require_auth
async def get_playlist_details(playlist_id: str) -> str:
    """Get detailed information about a playlist.

    Args:
        playlist_id: TIDAL playlist ID.

    Returns:
        Formatted playlist details.
    """
    tidal = get_tidal_instance()

    try:
        playlist = tidal.session.playlist(playlist_id)

        # Get creator info
        creator_name = "Unknown"
        if hasattr(playlist, "creator") and playlist.creator:
            creator_name = playlist.creator.name

        # Get tracks preview
        tracks = playlist.items()
        track_list = "\n".join([
            f"  {i+1:3d}. {track.name} - {track.artist.name if hasattr(track, 'artist') else 'Unknown'}"
            for i, track in enumerate(tracks[:15])
        ])
        if len(tracks) > 15:
            track_list += f"\n  ... and {len(tracks) - 15} more tracks"

        # Calculate duration
        total_duration = sum(t.duration for t in tracks if hasattr(t, "duration"))
        hours = total_duration // 3600
        minutes = (total_duration % 3600) // 60

        return f"""=== PLAYLIST DETAILS ===

Title: {playlist.name}
Creator: {creator_name}
Description: {playlist.description if hasattr(playlist, "description") and playlist.description else "No description"}

Number of Tracks: {playlist.num_tracks}
Duration: {hours}h {minutes}m
Public: {"Yes" if hasattr(playlist, "public") and playlist.public else "No"}
Type: {playlist.type if hasattr(playlist, "type") else "N/A"}

Created: {playlist.created if hasattr(playlist, "created") else "N/A"}
Last Updated: {playlist.last_updated if hasattr(playlist, "last_updated") else "N/A"}

Preview Tracks:
{track_list}

Playlist ID: {playlist.id}
TIDAL URL: https://tidal.com/browse/playlist/{playlist.id}
"""

    except Exception as e:
        return f"✗ Failed to get playlist details: {e!s}"


@require_auth
async def browse_genres(limit: int = 50) -> str:
    """Browse available music genres on TIDAL.

    Args:
        limit: Maximum genres to return (default: 50).

    Returns:
        Formatted list of genres.
    """
    tidal = get_tidal_instance()

    try:
        genres_page = tidal.session.genres()

        if not genres_page or not hasattr(genres_page, "categories"):
            return "✗ No genres available"

        # Extract genre items from page
        genres = []
        for category in genres_page.categories:
            if hasattr(category, "items"):
                genres.extend(category.items)

        if not genres:
            return "✗ No genres found"

        genres_text = "\n".join([
            f"{i+1:2d}. {genre.name if hasattr(genre, 'name') else str(genre)}"
            for i, genre in enumerate(genres[:limit])
        ])

        return f"""=== TIDAL GENRES ===

Total genres: {len(genres)}

{genres_text}
"""

    except Exception as e:
        return f"✗ Failed to browse genres: {e!s}"


@require_auth
async def get_artist_radio(artist_id: str, limit: int = 50) -> str:
    """Get artist radio - a mix of tracks inspired by an artist.

    Args:
        artist_id: TIDAL artist ID.
        limit: Maximum tracks to return (default: 50).

    Returns:
        Formatted radio tracklist.
    """
    tidal = get_tidal_instance()

    try:
        artist = tidal.session.artist(artist_id)
        radio = artist.get_radio()

        if not radio:
            return f"✗ No radio available for {artist.name}"

        tracks_text = "\n".join([
            f"{i+1:2d}. {track.name} - {track.artist.name}"
            for i, track in enumerate(radio[:limit])
        ])

        return f"""=== {artist.name.upper()} RADIO ===

Mix of tracks inspired by {artist.name}
Total tracks: {len(radio)}

{tracks_text}

Tip: These are curated tracks similar to {artist.name}'s style!
"""

    except Exception as e:
        return f"✗ Failed to get artist radio: {e!s}"
