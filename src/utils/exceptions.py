"""
Custom exceptions for the OSINT Analyzer.
Provides specific error handling for different failure scenarios.
"""


class OSINTError(Exception):
    """Base exception for all OSINT analyzer errors."""
    pass


class APIError(OSINTError):
    """Raised when an API request fails."""

    def __init__(self, platform: str, message: str, status_code: int = None):
        self.platform = platform
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{platform}] API Error: {message}")


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""

    def __init__(self, platform: str, retry_after: int = None):
        self.retry_after = retry_after
        msg = f"Rate limit exceeded"
        if retry_after:
            msg += f". Retry after {retry_after} seconds"
        super().__init__(platform, msg)


class AuthenticationError(APIError):
    """Raised when API authentication fails."""

    def __init__(self, platform: str, message: str = "Authentication failed"):
        super().__init__(platform, message, status_code=401)


class DataCollectionError(OSINTError):
    """Raised when data collection fails."""

    def __init__(self, platform: str, message: str):
        self.platform = platform
        self.message = message
        super().__init__(f"[{platform}] Data Collection Error: {message}")


class NetworkError(OSINTError):
    """Raised when network connectivity issues occur."""

    def __init__(self, message: str = "Network connection failed"):
        self.message = message
        super().__init__(f"Network Error: {message}")


class InvalidSearchError(OSINTError):
    """Raised when search parameters are invalid."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid Search: {message}")


class NoDataFoundError(OSINTError):
    """Raised when no data is found for the given search."""

    def __init__(self, keyword: str, platforms: list[str]):
        self.keyword = keyword
        self.platforms = platforms
        super().__init__(
            f"No data found for keyword '{keyword}' on platforms: {', '.join(platforms)}"
        )
