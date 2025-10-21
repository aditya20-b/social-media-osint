"""
Reddit collector that works WITHOUT API authentication.
Uses Reddit's public JSON endpoints - no API keys needed!
"""

import requests
from datetime import datetime
from typing import List, Dict, Optional
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.exceptions import (
    DataCollectionError,
    NetworkError,
    RateLimitError
)


class RedditNoAuthCollector:
    """
    Collect Reddit data WITHOUT authentication using public JSON endpoints.

    This works because Reddit provides JSON versions of all public pages
    by simply adding .json to the URL. No API keys required!
    """

    def __init__(self):
        """Initialize the collector."""
        self.session = requests.Session()
        # Use a proper user agent to avoid 429 errors
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/120.0.0.0 Safari/537.36'
        })
        self.base_delay = 2  # Be respectful with rate limiting

    def search_posts(
        self,
        keyword: str,
        limit: int = 50,
        subreddit: str = 'all',
        sort: str = 'relevance',
        time_filter: str = 'week'
    ) -> List[Dict]:
        """
        Search Reddit posts using public JSON endpoints - NO AUTH NEEDED!

        Args:
            keyword: Search term
            limit: Maximum posts to retrieve
            subreddit: Subreddit to search (default: 'all')
            sort: Sort method ('relevance', 'hot', 'top', 'new')
            time_filter: Time period ('hour', 'day', 'week', 'month', 'year', 'all')

        Returns:
            List of post dictionaries
        """
        posts = []

        try:
            # Reddit's search endpoint (public, no auth needed!)
            url = f'https://www.reddit.com/r/{subreddit}/search.json'

            params = {
                'q': keyword,
                'limit': min(limit, 100),  # Reddit max per request
                'sort': sort,
                't': time_filter,
                'restrict_sr': 'true' if subreddit != 'all' else 'false'
            }

            print(f"Searching Reddit for: {keyword}")
            print(f"URL: {url}")

            response = self.session.get(url, params=params, timeout=15)

            # Handle rate limiting
            if response.status_code == 429:
                raise RateLimitError('reddit', retry_after=60)

            response.raise_for_status()

            data = response.json()

            if 'data' not in data or 'children' not in data['data']:
                return posts

            # Extract posts
            for child in data['data']['children'][:limit]:
                post_data = child['data']

                post = {
                    'platform': 'reddit',
                    'id': post_data.get('id', ''),
                    'title': post_data.get('title', ''),
                    'text': post_data.get('selftext', ''),
                    'author': post_data.get('author', '[deleted]'),
                    'score': post_data.get('score', 0),
                    'upvote_ratio': post_data.get('upvote_ratio', 0.5),
                    'num_comments': post_data.get('num_comments', 0),
                    'created_utc': datetime.fromtimestamp(
                        post_data.get('created_utc', 0)
                    ).isoformat(),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'subreddit': post_data.get('subreddit', ''),
                    'full_text': f"{post_data.get('title', '')}. {post_data.get('selftext', '')}"
                }

                posts.append(post)

            print(f"✓ Found {len(posts)} Reddit posts")

            # Be respectful - add delay
            time.sleep(self.base_delay)

        except RateLimitError:
            raise
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Failed to connect to Reddit: {str(e)}")
        except Exception as e:
            raise DataCollectionError('reddit', f"Failed to search posts: {str(e)}")

        return posts

    def get_subreddit_hot(
        self,
        subreddit: str,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get hot posts from a subreddit - NO AUTH NEEDED!

        Args:
            subreddit: Subreddit name
            limit: Number of posts

        Returns:
            List of hot posts
        """
        posts = []

        try:
            # Public hot posts endpoint
            url = f'https://www.reddit.com/r/{subreddit}/hot.json'

            params = {'limit': min(limit, 100)}

            print(f"Getting hot posts from r/{subreddit}")

            response = self.session.get(url, params=params, timeout=15)

            if response.status_code == 429:
                raise RateLimitError('reddit', retry_after=60)

            response.raise_for_status()

            data = response.json()

            if 'data' not in data or 'children' not in data['data']:
                return posts

            for child in data['data']['children'][:limit]:
                post_data = child['data']

                post = {
                    'platform': 'reddit',
                    'id': post_data.get('id', ''),
                    'title': post_data.get('title', ''),
                    'text': post_data.get('selftext', ''),
                    'author': post_data.get('author', '[deleted]'),
                    'score': post_data.get('score', 0),
                    'upvote_ratio': post_data.get('upvote_ratio', 0.5),
                    'num_comments': post_data.get('num_comments', 0),
                    'created_utc': datetime.fromtimestamp(
                        post_data.get('created_utc', 0)
                    ).isoformat(),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'subreddit': post_data.get('subreddit', ''),
                    'full_text': f"{post_data.get('title', '')}. {post_data.get('selftext', '')}"
                }

                posts.append(post)

            print(f"✓ Retrieved {len(posts)} hot posts")

            time.sleep(self.base_delay)

        except RateLimitError:
            raise
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Failed to connect to Reddit: {str(e)}")
        except Exception as e:
            raise DataCollectionError('reddit', f"Failed to get hot posts: {str(e)}")

        return posts

    def search_by_hashtag(self, hashtag: str, limit: int = 50) -> List[Dict]:
        """
        Search by hashtag (adds # if not present).

        Args:
            hashtag: Hashtag to search

        Returns:
            List of posts
        """
        if not hashtag.startswith('#'):
            hashtag = f'#{hashtag}'

        return self.search_posts(hashtag, limit=limit)

    def get_trending_from_multiple_subs(
        self,
        keyword: str,
        subreddits: List[str] = None,
        posts_per_sub: int = 10
    ) -> List[Dict]:
        """
        Search for keyword across multiple popular subreddits.

        Args:
            keyword: Search term
            subreddits: List of subreddit names
            posts_per_sub: Posts to get from each sub

        Returns:
            Combined list of posts
        """
        if subreddits is None:
            # Default popular subreddits
            subreddits = [
                'news', 'worldnews', 'technology', 'science',
                'AskReddit', 'todayilearned', 'explainlikeimfive'
            ]

        all_posts = []

        for sub in subreddits:
            try:
                posts = self.search_posts(
                    keyword=keyword,
                    limit=posts_per_sub,
                    subreddit=sub
                )
                all_posts.extend(posts)

                print(f"  ✓ r/{sub}: {len(posts)} posts")

                # Rate limiting
                time.sleep(self.base_delay)

            except Exception as e:
                print(f"  ✗ r/{sub}: {str(e)}")
                continue

        return all_posts
