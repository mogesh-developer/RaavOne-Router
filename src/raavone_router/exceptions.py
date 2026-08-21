class RouterError(Exception):
    """Base exception for RaavOne Router."""


class InvalidRouteError(RouterError):
    """Raised when a route is invalid."""


class RouterLLMError(RouterError):
    """Raised when LLM-based routing fails."""
