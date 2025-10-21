"""
News collector using newspaper3k and BeautifulSoup.
Scrapes news articles from various sources.
"""

import requests
from newspaper import Article, Source
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin, urlparse
import sys
from pathlib import Path

# Add src to path for absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import Config
from utils.exceptions import (
    DataCollectionError,
    NetworkError
)


class NewsCollector:
    """Collect news articles using newspaper3k and BeautifulSoup."""

    # Popular news sources for general searching
    NEWS_SOURCES = [
        'https://www.bbc.com/news',
        'https://www.cnn.com',
        'https://www.reuters.com',
        'https://www.theguardian.com',
        'https://www.npr.org',
    ]

    def __init__(self):
        """Initialize news collector."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = Config.REQUEST_TIMEOUT

    def search_articles(
        self,
        keyword: str,
        limit: int = None,
        sources: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search for news articles containing the keyword.

        Args:
            keyword: Search term or topic
            limit: Maximum number of articles to retrieve
            sources: List of news source URLs (default: use predefined sources)

        Returns:
            List of article dictionaries
        """
        if limit is None:
            limit = Config.MAX_POSTS_PER_PLATFORM

        if sources is None:
            sources = self.NEWS_SOURCES

        articles = []
        articles_per_source = max(limit // len(sources), 5)

        for source_url in sources:
            try:
                source_articles = self._search_source(
                    source_url,
                    keyword,
                    articles_per_source
                )
                articles.extend(source_articles)

                if len(articles) >= limit:
                    break

                time.sleep(1)  # Be respectful to the servers

            except Exception as e:
                # Continue with other sources if one fails
                print(f"Warning: Failed to fetch from {source_url}: {str(e)}")
                continue

        return articles[:limit]

    def _search_source(
        self,
        source_url: str,
        keyword: str,
        limit: int
    ) -> List[Dict]:
        """
        Search for articles in a specific news source.

        Args:
            source_url: Base URL of the news source
            keyword: Search keyword
            limit: Maximum articles from this source

        Returns:
            List of articles from this source
        """
        articles = []

        try:
            # Build newspaper Source object
            source = Source(source_url)
            source.download()
            source.parse()

            # Filter articles by keyword in URL or title
            relevant_articles = [
                article for article in source.articles
                if keyword.lower() in article.url.lower()
            ][:limit]

            # If not enough articles found, try all articles
            if len(relevant_articles) < limit // 2:
                relevant_articles = source.articles[:limit * 2]

            for article_obj in relevant_articles[:limit]:
                try:
                    article_data = self._extract_article(article_obj, keyword)
                    if article_data and self._is_relevant(article_data['full_text'], keyword):
                        articles.append(article_data)
                except Exception:
                    continue

                if len(articles) >= limit:
                    break

        except Exception as e:
            raise DataCollectionError('news', f"Failed to search {source_url}: {str(e)}")

        return articles

    def _extract_article(self, article_obj: Article, keyword: str = None) -> Optional[Dict]:
        """
        Extract data from a newspaper Article object.

        Args:
            article_obj: Newspaper Article object
            keyword: Optional keyword for relevance checking

        Returns:
            Dictionary with article data
        """
        try:
            # Download and parse article
            article_obj.download()
            article_obj.parse()

            # Skip if no content
            if not article_obj.text:
                return None

            # Extract publish date
            publish_date = article_obj.publish_date
            if publish_date:
                publish_date = publish_date.isoformat()
            else:
                publish_date = datetime.now().isoformat()

            # Get domain name for source
            domain = urlparse(article_obj.url).netloc

            article_data = {
                'platform': 'news',
                'source': domain,
                'title': article_obj.title or 'No title',
                'text': article_obj.text,
                'authors': article_obj.authors,
                'publish_date': publish_date,
                'url': article_obj.url,
                'top_image': article_obj.top_image,
                'keywords': article_obj.keywords,
                'summary': article_obj.summary if hasattr(article_obj, 'summary') else '',
                'full_text': f"{article_obj.title}. {article_obj.text}"
            }

            return article_data

        except Exception as e:
            return None

    def get_article_from_url(self, url: str) -> Optional[Dict]:
        """
        Extract article data from a specific URL.

        Args:
            url: URL of the news article

        Returns:
            Dictionary with article data
        """
        try:
            article = Article(url)
            return self._extract_article(article)
        except Exception as e:
            raise DataCollectionError('news', f"Failed to extract article from {url}: {str(e)}")

    def search_google_news(self, keyword: str, limit: int = 20) -> List[Dict]:
        """
        Search Google News for articles (using web scraping).

        Args:
            keyword: Search keyword
            limit: Maximum number of articles

        Returns:
            List of article URLs and metadata
        """
        articles = []

        try:
            # Google News RSS feed
            search_url = f"https://news.google.com/rss/search?q={keyword}&hl=en-US&gl=US&ceid=US:en"

            response = self.session.get(search_url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item', limit=limit)

            for item in items:
                try:
                    title = item.find('title').text if item.find('title') else 'No title'
                    link = item.find('link').text if item.find('link') else ''
                    pub_date = item.find('pubDate').text if item.find('pubDate') else ''
                    source = item.find('source').text if item.find('source') else 'Unknown'
                    description = item.find('description').text if item.find('description') else ''

                    article_data = {
                        'platform': 'news',
                        'source': source,
                        'title': title,
                        'text': description,
                        'publish_date': pub_date,
                        'url': link,
                        'full_text': f"{title}. {description}"
                    }

                    articles.append(article_data)

                except Exception:
                    continue

        except requests.RequestException as e:
            raise NetworkError(f"Failed to connect to Google News: {str(e)}")
        except Exception as e:
            raise DataCollectionError('news', f"Failed to parse Google News: {str(e)}")

        return articles

    def _is_relevant(self, text: str, keyword: str) -> bool:
        """
        Check if article text is relevant to the keyword.

        Args:
            text: Article text
            keyword: Search keyword

        Returns:
            True if relevant, False otherwise
        """
        if not text:
            return False

        # Simple relevance check: keyword appears in text
        return keyword.lower() in text.lower()

    def get_articles_from_urls(self, urls: List[str]) -> List[Dict]:
        """
        Extract articles from a list of URLs.

        Args:
            urls: List of article URLs

        Returns:
            List of article dictionaries
        """
        articles = []

        for url in urls:
            try:
                article_data = self.get_article_from_url(url)
                if article_data:
                    articles.append(article_data)
                time.sleep(0.5)  # Rate limiting
            except Exception:
                continue

        return articles
