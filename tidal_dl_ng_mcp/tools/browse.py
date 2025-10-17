"""Browse and discovery tools for TIDAL MCP server."""

from tidal_dl_ng_mcp.utils.auth import get_tidal_instance, require_auth


@require_auth
async def browse_home(limit: int = 50) -> str:
    """Browse TIDAL home page with personalized recommendations.

    Args:
        limit: Maximum items to show per category (default: 50).

    Returns:
        Formatted home page content with categories and items.
    """
    tidal = get_tidal_instance()

    try:
        home_page = tidal.session.home()

        if not home_page.categories:
            return "✗ No home page content available"

        output = ["=== TIDAL HOME PAGE ===\n"]

        for category in home_page.categories:
            try:
                # Add category title
                title = category.title if hasattr(category, "title") else "Unknown"
                output.append(f"\n## {title}")

                if hasattr(category, "description") and category.description:
                    output.append(f"   {category.description}")

                # Get items from category
                if hasattr(category, "items") and category.items:
                    items = category.items[:limit]

                    for i, item in enumerate(items, 1):
                        item_type = type(item).__name__

                        if item_type == "Track":
                            artist_name = item.artist.name if item.artist else "Unknown Artist"
                            output.append(f"   {i}. {item.name} - {artist_name} (Track ID: {item.id})")

                        elif item_type == "Album":
                            artist_name = item.artist.name if item.artist else "Unknown Artist"
                            output.append(f"   {i}. {item.name} - {artist_name} (Album ID: {item.id})")

                        elif item_type == "Artist":
                            output.append(f"   {i}. {item.name} (Artist ID: {item.id})")

                        elif item_type == "Playlist" or item_type == "UserPlaylist":
                            creator = getattr(item, "creator", None)
                            creator_name = creator.name if creator and hasattr(creator, "name") else "TIDAL"
                            num_tracks = getattr(item, "num_tracks", 0)
                            output.append(
                                f"   {i}. {item.name} by {creator_name} ({num_tracks} tracks, Playlist ID: {item.id})"
                            )

                        elif item_type == "Mix":
                            output.append(f"   {i}. {item.title} (Mix ID: {item.id})")

                        else:
                            # Generic item display
                            name = getattr(item, "name", getattr(item, "title", "Unknown"))
                            output.append(f"   {i}. {name} ({item_type})")

                    if len(category.items) > limit:
                        output.append(f"   ... and {len(category.items) - limit} more")

            except Exception as e:
                # Skip categories that error, but continue with others
                output.append(f"   (Error loading category: {e!s})")
                continue

        output.append(
            "\n\n💡 Tip: Use track/album/artist/playlist IDs with detail tools to learn more about any item."
        )

        return "\n".join(output)

    except Exception as e:
        return f"✗ Failed to browse home page: {e!s}"


@require_auth
async def browse_explore(limit: int = 20) -> str:
    """Browse TIDAL explore page with genres, moods, and discovery content.

    Args:
        limit: Maximum items to show per category (default: 20).

    Returns:
        Formatted explore page content with discovery categories.
    """
    tidal = get_tidal_instance()

    try:
        explore_page = tidal.session.explore()

        if not explore_page.categories:
            return "✗ No explore page content available"

        output = ["=== TIDAL EXPLORE PAGE ===\n"]
        output.append("Discover music by genre, mood, and activity.\n")

        for category in explore_page.categories:
            try:
                title = category.title if hasattr(category, "title") else "Unknown"
                output.append(f"\n## {title}")

                if hasattr(category, "description") and category.description:
                    output.append(f"   {category.description}")

                # Get items from category
                if hasattr(category, "items") and category.items:
                    items = category.items[:limit]

                    for i, item in enumerate(items, 1):
                        # Most explore items are playlists or categories
                        item_type = type(item).__name__

                        if item_type == "Playlist" or item_type == "UserPlaylist":
                            creator = getattr(item, "creator", None)
                            creator_name = creator.name if creator and hasattr(creator, "name") else "TIDAL"
                            num_tracks = getattr(item, "num_tracks", 0)
                            output.append(
                                f"   {i}. {item.name} by {creator_name} ({num_tracks} tracks, ID: {item.id})"
                            )

                        elif hasattr(item, "name"):
                            output.append(f"   {i}. {item.name}")

                        elif hasattr(item, "title"):
                            output.append(f"   {i}. {item.title}")

                        else:
                            output.append(f"   {i}. {item_type}")

                    if len(category.items) > limit:
                        output.append(f"   ... and {len(category.items) - limit} more")

            except Exception as e:
                output.append(f"   (Error loading category: {e!s})")
                continue

        output.append("\n\n💡 Tip: Use the search tool to find specific genres or moods you're interested in.")

        return "\n".join(output)

    except Exception as e:
        return f"✗ Failed to browse explore page: {e!s}"


@require_auth
async def get_mixes(limit: int = 20) -> str:
    """Get TIDAL Mixes - personalized music collections curated for you.

    Args:
        limit: Maximum mixes to return (default: 20).

    Returns:
        Formatted list of available mixes.
    """
    tidal = get_tidal_instance()

    try:
        mixes_page = tidal.session.mixes()

        if not mixes_page.categories:
            return "✗ No mixes available"

        output = ["=== TIDAL MIXES ===\n"]
        output.append("Personalized music collections curated just for you.\n")

        total_mixes = 0

        for category in mixes_page.categories:
            try:
                if hasattr(category, "items") and category.items:
                    for item in category.items[:limit]:
                        total_mixes += 1
                        mix_type = type(item).__name__

                        if mix_type == "Mix" or mix_type == "MixV2":
                            title = getattr(item, "title", "Unknown Mix")
                            subtitle = getattr(item, "sub_title", "")
                            mix_id = getattr(item, "id", "")

                            output.append(f"{total_mixes}. {title}")
                            if subtitle:
                                output.append(f"   {subtitle}")
                            if mix_id:
                                output.append(f"   Mix ID: {mix_id}")
                            output.append("")

                        if total_mixes >= limit:
                            break

            except Exception as e:
                continue

        if total_mixes == 0:
            return "✗ No mixes found"

        output.append(f"Total: {total_mixes} mixes\n")
        output.append("💡 Tip: Mixes are updated regularly based on your listening habits.")

        return "\n".join(output)

    except Exception as e:
        return f"✗ Failed to get mixes: {e!s}"
