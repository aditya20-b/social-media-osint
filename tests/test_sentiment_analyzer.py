"""
Unit tests for the Sentiment Analyzer.
This is a sample test file demonstrating the testing structure.
"""

import pytest
from src.analyzers.sentiment_analyzer import SentimentAnalyzer


class TestSentimentAnalyzer:
    """Test cases for SentimentAnalyzer class."""

    @pytest.fixture
    def analyzer(self):
        """Create a SentimentAnalyzer instance for testing."""
        return SentimentAnalyzer()

    @pytest.fixture
    def sample_posts(self):
        """Sample posts for testing."""
        return [
            {
                'platform': 'reddit',
                'text': 'I love this amazing product!',
                'full_text': 'I love this amazing product!'
            },
            {
                'platform': 'twitter',
                'text': 'This is terrible and disappointing.',
                'full_text': 'This is terrible and disappointing.'
            },
            {
                'platform': 'news',
                'text': 'The company announced new features.',
                'full_text': 'The company announced new features.'
            }
        ]

    def test_analyze_positive_text(self, analyzer):
        """Test that positive text is correctly identified."""
        result = analyzer.analyze_text("I love this! It's wonderful and amazing!")

        assert result['sentiment'] == 'positive'
        assert result['polarity'] > 0
        assert 0 <= result['subjectivity'] <= 1

    def test_analyze_negative_text(self, analyzer):
        """Test that negative text is correctly identified."""
        result = analyzer.analyze_text("I hate this. It's terrible and awful.")

        assert result['sentiment'] == 'negative'
        assert result['polarity'] < 0
        assert 0 <= result['subjectivity'] <= 1

    def test_analyze_neutral_text(self, analyzer):
        """Test that neutral text is correctly identified."""
        result = analyzer.analyze_text("The meeting is scheduled for tomorrow.")

        assert result['sentiment'] == 'neutral'
        assert -0.1 <= result['polarity'] <= 0.1

    def test_analyze_empty_text(self, analyzer):
        """Test handling of empty text."""
        result = analyzer.analyze_text("")

        assert result['sentiment'] == 'neutral'
        assert result['polarity'] == 0.0
        assert result['subjectivity'] == 0.0

    def test_analyze_posts(self, analyzer, sample_posts):
        """Test analyzing multiple posts."""
        analyzed_posts = analyzer.analyze_posts(sample_posts)

        assert len(analyzed_posts) == 3
        assert all('sentiment_analysis' in post for post in analyzed_posts)
        assert analyzed_posts[0]['sentiment_analysis']['sentiment'] == 'positive'
        assert analyzed_posts[1]['sentiment_analysis']['sentiment'] == 'negative'

    def test_get_sentiment_distribution(self, analyzer, sample_posts):
        """Test sentiment distribution calculation."""
        analyzed_posts = analyzer.analyze_posts(sample_posts)
        distribution = analyzer.get_sentiment_distribution(analyzed_posts)

        assert distribution['total'] == 3
        assert distribution['positive'] == 1
        assert distribution['negative'] == 1
        assert distribution['neutral'] == 1
        assert distribution['positive_pct'] + distribution['negative_pct'] + distribution['neutral_pct'] == 100.0

    def test_get_platform_sentiment(self, analyzer, sample_posts):
        """Test platform-wise sentiment distribution."""
        analyzed_posts = analyzer.analyze_posts(sample_posts)
        platform_sentiment = analyzer.get_platform_sentiment(analyzed_posts)

        assert 'reddit' in platform_sentiment
        assert 'twitter' in platform_sentiment
        assert 'news' in platform_sentiment

    def test_get_top_posts_by_sentiment(self, analyzer, sample_posts):
        """Test retrieving top posts by sentiment."""
        analyzed_posts = analyzer.analyze_posts(sample_posts)
        top_positive = analyzer.get_top_posts_by_sentiment(analyzed_posts, 'positive', limit=1)

        assert len(top_positive) <= 1
        if top_positive:
            assert top_positive[0]['sentiment_analysis']['sentiment'] == 'positive'

    def test_get_average_sentiment(self, analyzer, sample_posts):
        """Test average sentiment calculation."""
        analyzed_posts = analyzer.analyze_posts(sample_posts)
        average = analyzer.get_average_sentiment(analyzed_posts)

        assert 'avg_polarity' in average
        assert 'avg_subjectivity' in average
        assert 'overall_sentiment' in average
        assert -1 <= average['avg_polarity'] <= 1
        assert 0 <= average['avg_subjectivity'] <= 1
        assert average['overall_sentiment'] in ['positive', 'negative', 'neutral']

    def test_generate_summary(self, analyzer, sample_posts):
        """Test summary generation."""
        analyzed_posts = analyzer.analyze_posts(sample_posts)
        summary = analyzer.generate_summary(analyzed_posts)

        assert isinstance(summary, str)
        assert 'Total Posts Analyzed: 3' in summary
        assert 'Sentiment Distribution' in summary


# Run tests with: pytest tests/test_sentiment_analyzer.py -v
