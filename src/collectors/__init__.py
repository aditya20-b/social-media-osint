"""Data collectors for different social media platforms."""

from .reddit_collector import RedditCollector
from .twitter_collector import TwitterCollector
from .news_collector import NewsCollector

__all__ = ['RedditCollector', 'TwitterCollector', 'NewsCollector']
