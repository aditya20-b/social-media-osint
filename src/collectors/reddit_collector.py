"""
Reddit data collector using praw (Python Reddit API Wrapper).
Collects posts and comments based on keywords/hashtags.
"""

import praw
from datetime import datetime
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


class RedditCollector:
    """Collect data from Reddit using the PRAW library."""

    def __init__(self):
        """Initialize Reddit API client."""
        if not Config.validate_reddit_config():
            raise AuthenticationError(
                'reddit',
                'Missing Reddit API credentials. Check your .env file.'
            )

        try:
            self.reddit = praw.Reddit(
                client_id=Config.REDDIT_CLIENT_ID,
                client_secret=Config.REDDIT_CLIENT_SECRET,
                user_agent=Config.REDDIT_USER_AGENT
            )
            # Test authentication
            self.reddit.user.me()
        except praw.exceptions.ResponseException as e:
            raise AuthenticationError('reddit', str(e))
        except Exception as e:
            raise NetworkError(f"Failed to connect to Reddit: {str(e)}")

    def search_posts(
        self,
        keyword: str,
        limit: int = None,
        subreddit: str = 'all',
        time_filter: str = 'week'
    ) -> List[Dict]:
        """
        Search for Reddit posts containing the keyword.

        Args:
            keyword: Search term or hashtag
            limit: Maximum number of posts to retrieve
            subreddit: Subreddit to search (default: 'all')
            time_filter: Time period ('hour', 'day', 'week', 'month', 'year', 'all')

        Returns:
            List of post dictionaries with relevant data
        """
        if limit is None:
            limit = Config.MAX_POSTS_PER_PLATFORM

        posts = []
        try:
            subreddit_obj = self.reddit.subreddit(subreddit)

            for submission in subreddit_obj.search(
                keyword,
                limit=limit,
                time_filter=time_filter
            ):
                post_data = {
                    'platform': 'reddit',
                    'id': submission.id,
                    'title': submission.title,
                    'text': submission.selftext,
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'score': submission.score,
                    'upvote_ratio': submission.upvote_ratio,
                    'num_comments': submission.num_comments,
                    'created_utc': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'url': f"https://reddit.com{submission.permalink}",
                    'subreddit': str(submission.subreddit),
                    'is_self': submission.is_self,
                    'awards': submission.total_awards_received
                }

                # Combine title and text for analysis
                post_data['full_text'] = f"{post_data['title']}. {post_data['text']}"

                posts.append(post_data)

                # Respect rate limits
                time.sleep(0.1)

        except praw.exceptions.RedditAPIException as e:
            if 'RATELIMIT' in str(e):
                raise RateLimitError('reddit')
            raise DataCollectionError('reddit', str(e))
        except Exception as e:
            raise DataCollectionError('reddit', f"Failed to search posts: {str(e)}")

        return posts

    def get_trending_posts(
        self,
        subreddit: str = 'all',
        limit: int = 50,
        time_filter: str = 'day'
    ) -> List[Dict]:
        """
        Get trending/hot posts from a subreddit.

        Args:
            subreddit: Subreddit name
            limit: Number of posts to retrieve
            time_filter: Time period for top posts

        Returns:
            List of trending post dictionaries
        """
        posts = []
        try:
            subreddit_obj = self.reddit.subreddit(subreddit)

            for submission in subreddit_obj.hot(limit=limit):
                post_data = {
                    'platform': 'reddit',
                    'id': submission.id,
                    'title': submission.title,
                    'text': submission.selftext,
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'score': submission.score,
                    'upvote_ratio': submission.upvote_ratio,
                    'num_comments': submission.num_comments,
                    'created_utc': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'url': f"https://reddit.com{submission.permalink}",
                    'subreddit': str(submission.subreddit),
                    'full_text': f"{submission.title}. {submission.selftext}"
                }

                posts.append(post_data)
                time.sleep(0.1)

        except Exception as e:
            raise DataCollectionError('reddit', f"Failed to get trending posts: {str(e)}")

        return posts

    def get_post_comments(self, post_id: str, limit: int = 10) -> List[Dict]:
        """
        Get comments from a specific post.

        Args:
            post_id: Reddit post ID
            limit: Maximum number of comments

        Returns:
            List of comment dictionaries
        """
        comments = []
        try:
            submission = self.reddit.submission(id=post_id)
            submission.comments.replace_more(limit=0)  # Remove "More Comments" objects

            for comment in submission.comments.list()[:limit]:
                comment_data = {
                    'id': comment.id,
                    'text': comment.body,
                    'author': str(comment.author) if comment.author else '[deleted]',
                    'score': comment.score,
                    'created_utc': datetime.fromtimestamp(comment.created_utc).isoformat(),
                    'is_submitter': comment.is_submitter
                }
                comments.append(comment_data)

        except Exception as e:
            raise DataCollectionError('reddit', f"Failed to get comments: {str(e)}")

        return comments

    def search_by_hashtag(self, hashtag: str, limit: int = None) -> List[Dict]:
        """
        Search posts by hashtag (Reddit uses # in titles/text).

        Args:
            hashtag: Hashtag to search (with or without #)

        Returns:
            List of posts containing the hashtag
        """
        if not hashtag.startswith('#'):
            hashtag = f'#{hashtag}'

        return self.search_posts(hashtag, limit=limit)
