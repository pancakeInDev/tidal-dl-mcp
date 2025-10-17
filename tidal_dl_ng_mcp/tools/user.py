"""User account and profile tools for TIDAL MCP server."""

from tidalapi.media import Quality

from tidal_dl_ng_mcp.utils.auth import get_tidal_instance, require_auth


@require_auth
async def get_user_profile() -> str:
    """Get user profile information.

    Returns:
        Formatted user profile information.
    """
    tidal = get_tidal_instance()

    try:
        user = tidal.session.user

        # Get available user attributes
        user_id = user.id if hasattr(user, "id") else "N/A"
        username = user.username if hasattr(user, "username") else "N/A"
        first_name = user.first_name if hasattr(user, "first_name") else ""
        last_name = user.last_name if hasattr(user, "last_name") else ""
        email = user.email if hasattr(user, "email") else "N/A"

        # Construct full name
        full_name = f"{first_name} {last_name}".strip() if first_name or last_name else "N/A"

        return f"""=== TIDAL USER PROFILE ===

User ID: {user_id}
Username: {username}
Name: {full_name}
Email: {email}

This profile information is retrieved from your TIDAL account.
For subscription details, use the get_subscription_info tool."""

    except Exception as e:
        return f"✗ Failed to get user profile: {e!s}"


@require_auth
async def get_subscription_info() -> str:
    """Get subscription and audio quality information.

    Returns:
        Formatted subscription information including tier and quality limits.
    """
    tidal = get_tidal_instance()

    try:
        # Get audio quality setting
        audio_quality = tidal.session.audio_quality

        # Map quality to tier and description
        quality_info = {
            Quality.low_96k: {
                "tier": "Free / Basic",
                "description": "Low Quality (96 kbps AAC)",
                "format": "AAC",
                "bitrate": "96 kbps",
            },
            Quality.low_320k: {
                "tier": "TIDAL Premium",
                "description": "High Quality (320 kbps AAC)",
                "format": "AAC",
                "bitrate": "320 kbps",
            },
            Quality.high_lossless: {
                "tier": "TIDAL HiFi",
                "description": "HiFi / Lossless (FLAC 16-bit/44.1kHz)",
                "format": "FLAC",
                "bitrate": "1411 kbps (CD Quality)",
            },
            Quality.hi_res_lossless: {
                "tier": "TIDAL HiFi Plus",
                "description": "HiRes / Master (FLAC up to 24-bit/192kHz)",
                "format": "FLAC",
                "bitrate": "Up to 9216 kbps (Studio Master)",
            },
        }

        current = quality_info.get(
            audio_quality,
            {
                "tier": "Unknown",
                "description": "Unknown quality",
                "format": "Unknown",
                "bitrate": "Unknown",
            },
        )

        return f"""=== TIDAL SUBSCRIPTION INFO ===

Subscription Tier: {current['tier']}
Current Audio Quality: {current['description']}
Audio Format: {current['format']}
Bitrate: {current['bitrate']}

=== Available Tiers ===

1. TIDAL Free/Basic
   - Quality: Up to 320 kbps AAC
   - Format: AAC (lossy)
   - Ads: Yes (Free tier)

2. TIDAL Premium (Not available in all regions)
   - Quality: Up to 320 kbps AAC
   - Format: AAC (lossy)
   - Ads: No

3. TIDAL HiFi
   - Quality: 16-bit/44.1kHz (CD Quality)
   - Format: FLAC (lossless)
   - Bitrate: 1411 kbps
   - Ads: No
   - Offline: Yes

4. TIDAL HiFi Plus
   - Quality: Up to 24-bit/192kHz (Studio Master)
   - Format: FLAC (lossless)
   - Bitrate: Up to 9216 kbps
   - Ads: No
   - Offline: Yes
   - Exclusive content: Yes

Your current tier is: {current['tier']}

Note: To change your subscription, visit https://tidal.com/account"""

    except Exception as e:
        return f"✗ Failed to get subscription info: {e!s}"
