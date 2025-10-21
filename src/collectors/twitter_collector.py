"""
Twitter/X data collector using tweepy.
Collects tweets based on keywords/hashtags.
"""

import tweepy
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import sys
from pathlib import Path

# Add src to path for absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import Config
from utils.exceptions import (
    AuthenticationError,
    RateLimitError,
    DataCollectionError,
    NetworkError
)


class TwitterCollector:
    """Collect data from Twitter/X using the tweepy library."""

    def __init__(self):
        """Initialize Twitter API client."""
        if not Config.validate_twitter_config():
            raise AuthenticationError(
                'twitter',
                'Missing Twitter API credentials. Check your .env file.'
            )

        try:
            # Try using Bearer Token (API v2) first
            if Config.TWITTER_BEARER_TOKEN:
                self.client = tweepy.Client(
                    bearer_token=Config.TWITTER_BEARER_TOKEN,
                    wait_on_rate_limit=True
                )
            else:
                # Fallback to OAuth 1.0a (API v1.1)
                auth = tweepy.OAuth1UserHandler(
                    Config.TWITTER_API_KEY,
                    Config.TWITTER_API_SECRET,
                    Config.TWITTER_ACCESS_TOKEN,
                    Config.TWITTER_ACCESS_SECRET
                )
                api = tweepy.API(auth, wait_on_rate_limit=True)
                self.client = tweepy.Client(
                    consumer_key=Config.TWITTER_API_KEY,
                    consumer_secret=Config.TWITTER_API_SECRET,
                    access_token=Config.TWITTER_ACCESS_TOKEN,
                    access_token_secret=Config.TWITTER_ACCESS_SECRET,
                    wait_on_rate_limit=True
                )

        except tweepy.TweepyException as e:
            raise AuthenticationError('twitter', str(e))
        except Exception as e:
            raise NetworkError(f"Failed to connect to Twitter: {str(e)}")

    def search_tweets(
        self,
        keyword: str,
        limit: int = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Search for tweets containing the keyword.

        Args:
            keyword: Search term or hashtag
            limit: Maximum number of tweets to retrieve
            start_time: Start of time range (default: 7 days ago)
            end_time: End of time range (default: now)

        Returns:
            List of tweet dictionaries with relevant data
        """
        if limit is None:
            limit = Config.MAX_POSTS_PER_PLATFORM

        if start_time is None:
            start_time = datetime.utcnow() - timedelta(days=7)

        tweets = []
        try:
            # Search recent tweets (last 7 days for free tier)
            response = self.client.search_recent_tweets(
                query=keyword,
                max_results=min(limit, 100),  # API limit per request
                tweet_fields=['created_at', 'public_metrics', 'author_id', 'lang'],
                expansions=['author_id'],
                start_time=start_time,
                end_time=end_time
            )

            if not response.data:
                return tweets

            # Create a map of user IDs to usernames
            users = {}
            if response.includes and 'users' in response.includes:
                users = {user.id: user.username for user in response.includes['users']}

            for tweet in response.data:
                metrics = tweet.public_metrics

                tweet_data = {
                    'platform': 'twitter',
                    'id': tweet.id,
                    'text': tweet.text,
                    'author_id': tweet.author_id,
                    'author': users.get(tweet.author_id, 'unknown'),
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else None,
                    'retweet_count': metrics.get('retweet_count', 0),
                    'reply_count': metrics.get('reply_count', 0),
                    'like_count': metrics.get('like_count', 0),
                    'quote_count': metrics.get('quote_count', 0),
                    'impression_count': metrics.get('impression_count', 0),
                    'language': tweet.lang if hasattr(tweet, 'lang') else 'unknown',
                    'url': f"https://twitter.com/i/web/status/{tweet.id}",
                    'full_text': tweet.text
                }

                tweets.append(tweet_data)

                # Small delay to avoid hitting rate limits
                time.sleep(0.05)

        except tweepy.TweepyException as e:
            error_str = str(e)
            if 'rate limit' in error_str.lower():
                raise RateLimitError('twitter')
            elif '401' in error_str or 'unauthorized' in error_str.lower():
                raise AuthenticationError('twitter', 'Invalid credentials or expired token')
            else:
                raise DataCollectionError('twitter', error_str)
        except Exception as e:
            raise DataCollectionError('twitter', f"Failed to search tweets: {str(e)}")

        return tweets

    def search_by_hashtag(
        self,
        hashtag: str,
        limit: int = None,
        start_time: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Search tweets by hashtag.

        Args:
            hashtag: Hashtag to search (with or without #)
            limit: Maximum number of tweets
            start_time: Start of time range

        Returns:
            List of tweets containing the hashtag
        """
        if not hashtag.startswith('#'):
            hashtag = f'#{hashtag}'

        return self.search_tweets(hashtag, limit=limit, start_time=start_time)

    def get_user_tweets(self, username: str, limit: int = 50) -> List[Dict]:
        """
        Get recent tweets from a specific user.

        Args:
            username: Twitter username (without @)
            limit: Number of tweets to retrieve

        Returns:
            List of user's tweets
        """
        tweets = []
        try:
            # Get user ID from username
            user = self.client.get_user(username=username)
            if not user.data:
                raise DataCollectionError('twitter', f"User {username} not found")

            user_id = user.data.id

            # Get user's tweets
            response = self.client.get_users_tweets(
                id=user_id,
                max_results=min(limit, 100),
                tweet_fields=['created_at', 'public_metrics', 'lang']
            )

            if not response.data:
                return tweets

            for tweet in response.data:
                metrics = tweet.public_metrics

                tweet_data = {
                    'platform': 'twitter',
                    'id': tweet.id,
                    'text': tweet.text,
                    'author': username,
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else None,
                    'retweet_count': metrics.get('retweet_count', 0),
                    'reply_count': metrics.get('reply_count', 0),
                    'like_count': metrics.get('like_count', 0),
                    'language': tweet.lang if hasattr(tweet, 'lang') else 'unknown',
                    'url': f"https://twitter.com/{username}/status/{tweet.id}",
                    'full_text': tweet.text
                }

                tweets.append(tweet_data)

        except tweepy.TweepyException as e:
            if 'rate limit' in str(e).lower():
                raise RateLimitError('twitter')
            raise DataCollectionError('twitter', str(e))
        except Exception as e:
            raise DataCollectionError('twitter', f"Failed to get user tweets: {str(e)}")

        return tweets

    def get_trending_topics(self, location_id: int = 1) -> List[str]:
        """
        Get trending topics (requires elevated API access).

        Args:
            location_id: WOEID location ID (1 = Worldwide)

        Returns:
            List of trending topic names
        """
        # Note: This feature requires elevated API access
        # For basic tier, we return empty list
        return []
