"""Authentication utilities for TIDAL MCP server."""

from functools import wraps
from typing import Callable

from tidal_dl_ng.config import Settings, Tidal


# Global TIDAL instance (singleton pattern)
_tidal_instance: Tidal | None = None


def get_tidal_instance() -> Tidal:
    """Get or create the TIDAL session instance.

    Returns:
        Tidal: Authenticated TIDAL session instance.

    Raises:
        RuntimeError: If authentication fails.
    """
    global _tidal_instance

    if _tidal_instance is None:
        settings = Settings()
        _tidal_instance = Tidal(settings)

        # Try token-based login first
        if not _tidal_instance.login_token():
            raise RuntimeError(
                "TIDAL authentication required. Please run 'tidal-dl-ng login' first to authenticate."
            )

    return _tidal_instance


def require_auth(func: Callable) -> Callable:
    """Decorator to ensure TIDAL authentication before function execution.

    Args:
        func: Async function to wrap with authentication check.

    Returns:
        Wrapped async function.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        """Wrapper function that ensures authentication."""
        get_tidal_instance()  # Will raise if not authenticated
        return await func(*args, **kwargs)

    return wrapper
