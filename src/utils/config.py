"""
Configuration management for the OSINT Analyzer.
Handles environment variables and application settings.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Centralized configuration management."""

    # Reddit API Configuration
    REDDIT_CLIENT_ID: str = os.getenv('REDDIT_CLIENT_ID', '')
    REDDIT_CLIENT_SECRET: str = os.getenv('REDDIT_CLIENT_SECRET', '')
    REDDIT_USER_AGENT: str = os.getenv('REDDIT_USER_AGENT', 'python:osint-analyzer:v1.0')

    # Twitter/X API Configuration
    TWITTER_BEARER_TOKEN: str = os.getenv('TWITTER_BEARER_TOKEN', '')
    TWITTER_API_KEY: str = os.getenv('TWITTER_API_KEY', '')
    TWITTER_API_SECRET: str = os.getenv('TWITTER_API_SECRET', '')
    TWITTER_ACCESS_TOKEN: str = os.getenv('TWITTER_ACCESS_TOKEN', '')
    TWITTER_ACCESS_SECRET: str = os.getenv('TWITTER_ACCESS_SECRET', '')

    # News API Configuration
    NEWS_API_KEY: str = os.getenv('NEWS_API_KEY', '')

    # Application Settings
    MAX_POSTS_PER_PLATFORM: int = int(os.getenv('MAX_POSTS_PER_PLATFORM', '100'))
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', '30'))
    CACHE_ENABLED: bool = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    CACHE_EXPIRY_HOURS: int = int(os.getenv('CACHE_EXPIRY_HOURS', '24'))

    # Output Settings
    REPORT_FORMAT: str = os.getenv('REPORT_FORMAT', 'json,html')
    SAVE_RAW_DATA: bool = os.getenv('SAVE_RAW_DATA', 'true').lower() == 'true'
    OUTPUT_DIRECTORY: Path = Path(os.getenv('OUTPUT_DIRECTORY', './output/reports'))

    @classmethod
    def validate_reddit_config(cls) -> bool:
        """Validate Reddit API credentials."""
        return bool(cls.REDDIT_CLIENT_ID and cls.REDDIT_CLIENT_SECRET)

    @classmethod
    def validate_twitter_config(cls) -> bool:
        """Validate Twitter API credentials."""
        return bool(cls.TWITTER_BEARER_TOKEN or
                   (cls.TWITTER_API_KEY and cls.TWITTER_API_SECRET))

    @classmethod
    def get_enabled_platforms(cls) -> list[str]:
        """Return list of platforms with valid credentials."""
        platforms = []
        if cls.validate_reddit_config():
            platforms.append('reddit')
        if cls.validate_twitter_config():
            platforms.append('twitter')
        # News scraping doesn't require credentials
        platforms.append('news')
        return platforms

    @classmethod
    def ensure_output_directory(cls) -> None:
        """Create output directory if it doesn't exist."""
        cls.OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)


# Initialize configuration on module import
Config.ensure_output_directory()
