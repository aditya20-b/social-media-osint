"""
Sentiment analysis using TextBlob.
Analyzes the sentiment of collected social media posts and articles.
"""

from textblob import TextBlob
from typing import List, Dict, Tuple
import pandas as pd
from collections import Counter


class SentimentAnalyzer:
    """Analyze sentiment of text using TextBlob."""

    # Sentiment thresholds
    POSITIVE_THRESHOLD = 0.1
    NEGATIVE_THRESHOLD = -0.1

    def __init__(self):
        """Initialize sentiment analyzer."""
        pass

    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text.

        Args:
            text: Input text to analyze

        Returns:
            Dictionary with sentiment scores and classification
        """
        if not text or not text.strip():
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'sentiment': 'neutral',
                'confidence': 0.0
            }

        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1

            # Classify sentiment
            if polarity > self.POSITIVE_THRESHOLD:
                sentiment = 'positive'
            elif polarity < self.NEGATIVE_THRESHOLD:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

            # Calculate confidence (how far from neutral)
            confidence = abs(polarity)

            return {
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3),
                'sentiment': sentiment,
                'confidence': round(confidence, 3)
            }

        except Exception as e:
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': str(e)
            }

    def analyze_posts(self, posts: List[Dict]) -> List[Dict]:
        """
        Analyze sentiment for a list of posts.

        Args:
            posts: List of post dictionaries with 'full_text' or 'text' field

        Returns:
            List of posts with added sentiment analysis
        """
        analyzed_posts = []

        for post in posts:
            # Get text content
            text = post.get('full_text') or post.get('text', '')

            # Analyze sentiment
            sentiment_data = self.analyze_text(text)

            # Add sentiment to post
            post_with_sentiment = post.copy()
            post_with_sentiment['sentiment_analysis'] = sentiment_data

            analyzed_posts.append(post_with_sentiment)

        return analyzed_posts

    def get_sentiment_distribution(self, posts: List[Dict]) -> Dict:
        """
        Get the distribution of sentiments in posts.

        Args:
            posts: List of analyzed posts

        Returns:
            Dictionary with sentiment counts and percentages
        """
        if not posts:
            return {
                'total': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'positive_pct': 0.0,
                'negative_pct': 0.0,
                'neutral_pct': 0.0
            }

        sentiments = [
            post.get('sentiment_analysis', {}).get('sentiment', 'neutral')
            for post in posts
        ]

        sentiment_counts = Counter(sentiments)
        total = len(posts)

        return {
            'total': total,
            'positive': sentiment_counts.get('positive', 0),
            'negative': sentiment_counts.get('negative', 0),
            'neutral': sentiment_counts.get('neutral', 0),
            'positive_pct': round((sentiment_counts.get('positive', 0) / total) * 100, 2),
            'negative_pct': round((sentiment_counts.get('negative', 0) / total) * 100, 2),
            'neutral_pct': round((sentiment_counts.get('neutral', 0) / total) * 100, 2)
        }

    def get_platform_sentiment(self, posts: List[Dict]) -> Dict[str, Dict]:
        """
        Get sentiment distribution by platform.

        Args:
            posts: List of analyzed posts

        Returns:
            Dictionary mapping platform to sentiment distribution
        """
        platform_posts = {}

        # Group posts by platform
        for post in posts:
            platform = post.get('platform', 'unknown')
            if platform not in platform_posts:
                platform_posts[platform] = []
            platform_posts[platform].append(post)

        # Calculate sentiment for each platform
        platform_sentiment = {}
        for platform, platform_post_list in platform_posts.items():
            platform_sentiment[platform] = self.get_sentiment_distribution(platform_post_list)

        return platform_sentiment

    def get_top_posts_by_sentiment(
        self,
        posts: List[Dict],
        sentiment: str = 'positive',
        limit: int = 5
    ) -> List[Dict]:
        """
        Get top posts with specific sentiment.

        Args:
            posts: List of analyzed posts
            sentiment: 'positive', 'negative', or 'neutral'
            limit: Number of posts to return

        Returns:
            List of top posts with specified sentiment
        """
        # Filter by sentiment
        filtered_posts = [
            post for post in posts
            if post.get('sentiment_analysis', {}).get('sentiment') == sentiment
        ]

        # Sort by confidence (absolute polarity)
        sorted_posts = sorted(
            filtered_posts,
            key=lambda p: p.get('sentiment_analysis', {}).get('confidence', 0),
            reverse=True
        )

        return sorted_posts[:limit]

    def get_average_sentiment(self, posts: List[Dict]) -> Dict:
        """
        Calculate average sentiment scores across all posts.

        Args:
            posts: List of analyzed posts

        Returns:
            Dictionary with average scores
        """
        if not posts:
            return {
                'avg_polarity': 0.0,
                'avg_subjectivity': 0.0,
                'overall_sentiment': 'neutral'
            }

        polarities = [
            post.get('sentiment_analysis', {}).get('polarity', 0)
            for post in posts
        ]

        subjectivities = [
            post.get('sentiment_analysis', {}).get('subjectivity', 0)
            for post in posts
        ]

        avg_polarity = sum(polarities) / len(polarities)
        avg_subjectivity = sum(subjectivities) / len(subjectivities)

        # Determine overall sentiment
        if avg_polarity > self.POSITIVE_THRESHOLD:
            overall_sentiment = 'positive'
        elif avg_polarity < self.NEGATIVE_THRESHOLD:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'

        return {
            'avg_polarity': round(avg_polarity, 3),
            'avg_subjectivity': round(avg_subjectivity, 3),
            'overall_sentiment': overall_sentiment
        }

    def get_sentiment_trends(self, posts: List[Dict]) -> pd.DataFrame:
        """
        Get sentiment trends over time.

        Args:
            posts: List of analyzed posts with timestamps

        Returns:
            DataFrame with time-based sentiment aggregation
        """
        if not posts:
            return pd.DataFrame()

        # Prepare data
        data = []
        for post in posts:
            timestamp = (
                post.get('created_at') or
                post.get('created_utc') or
                post.get('publish_date')
            )
            sentiment = post.get('sentiment_analysis', {}).get('sentiment', 'neutral')
            polarity = post.get('sentiment_analysis', {}).get('polarity', 0)

            if timestamp:
                data.append({
                    'timestamp': pd.to_datetime(timestamp),
                    'sentiment': sentiment,
                    'polarity': polarity
                })

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df = df.sort_values('timestamp')

        return df

    def generate_summary(self, posts: List[Dict]) -> str:
        """
        Generate a text summary of sentiment analysis.

        Args:
            posts: List of analyzed posts

        Returns:
            Human-readable summary string
        """
        if not posts:
            return "No posts to analyze."

        distribution = self.get_sentiment_distribution(posts)
        average = self.get_average_sentiment(posts)

        summary = f"""
Sentiment Analysis Summary
==========================
Total Posts Analyzed: {distribution['total']}

Sentiment Distribution:
- Positive: {distribution['positive']} ({distribution['positive_pct']}%)
- Negative: {distribution['negative']} ({distribution['negative_pct']}%)
- Neutral: {distribution['neutral']} ({distribution['neutral_pct']}%)

Average Sentiment:
- Polarity: {average['avg_polarity']} (range: -1 to 1)
- Subjectivity: {average['avg_subjectivity']} (range: 0 to 1)
- Overall: {average['overall_sentiment'].upper()}
"""

        return summary.strip()
