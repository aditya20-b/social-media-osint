#!/usr/bin/env python3
"""
Test Visualization Generation
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from analyzers.sentiment_analyzer import SentimentAnalyzer
from visualizers.charts import SentimentVisualizer

print("=" * 70)
print("VISUALIZATION TESTING")
print("=" * 70)

# Create sample dataset
sample_posts = []

# Add posts over time with varying sentiments
base_time = datetime.now() - timedelta(days=7)

posts_data = [
    ("Reddit post: Amazing new feature released!", "reddit", 0),
    ("Twitter: This is terrible and broken", "twitter", 1),
    ("News: Company announces quarterly results", "news", 2),
    ("Reddit: Love the improvements, great work!", "reddit", 3),
    ("Twitter: Disappointed with the update", "twitter", 4),
    ("News: Industry trends show positive growth", "news", 5),
    ("Reddit: This is the best app ever!", "reddit", 6),
    ("Twitter: Worst experience, would not recommend", "twitter", 1),
    ("News: Market analysis reveals new opportunities", "news", 2),
    ("Reddit: Pretty good overall", "reddit", 3),
]

for text, platform, days_offset in posts_data:
    timestamp = base_time + timedelta(days=days_offset)
    sample_posts.append({
        'platform': platform,
        'text': text,
        'full_text': text,
        'created_at': timestamp.isoformat(),
        'url': f'https://example.com/{platform}/post'
    })

print(f"\nCreated {len(sample_posts)} sample posts")

# Analyze sentiment
print("\nAnalyzing sentiment...")
analyzer = SentimentAnalyzer()
analyzed_posts = analyzer.analyze_posts(sample_posts)

distribution = analyzer.get_sentiment_distribution(analyzed_posts)
platform_sentiment = analyzer.get_platform_sentiment(analyzed_posts)
average_sentiment = analyzer.get_average_sentiment(analyzed_posts)

print(f"✓ Sentiment analysis complete")
print(f"  - Positive: {distribution['positive']}")
print(f"  - Negative: {distribution['negative']}")
print(f"  - Neutral: {distribution['neutral']}")

# Create visualizations
print("\nGenerating visualizations...")
visualizer = SentimentVisualizer(output_dir='./output/reports')

try:
    # 1. Sentiment Pie Chart
    fig = visualizer.create_sentiment_pie_chart(
        distribution,
        title="Test Sentiment Distribution",
        save_path="test_pie_chart.html"
    )
    print("✓ Pie chart saved to: output/reports/test_pie_chart.html")
except Exception as e:
    print(f"✗ Pie chart failed: {e}")

try:
    # 2. Platform Comparison
    fig = visualizer.create_platform_comparison_chart(
        platform_sentiment,
        title="Test Platform Comparison",
        save_path="test_platform_comparison.html"
    )
    print("✓ Platform comparison saved to: output/reports/test_platform_comparison.html")
except Exception as e:
    print(f"✗ Platform comparison failed: {e}")

try:
    # 3. Sentiment Timeline
    fig = visualizer.create_sentiment_timeline(
        analyzed_posts,
        title="Test Sentiment Timeline",
        save_path="test_timeline.html"
    )
    print("✓ Timeline saved to: output/reports/test_timeline.html")
except Exception as e:
    print(f"✗ Timeline failed: {e}")

try:
    # 4. Polarity Histogram
    fig = visualizer.create_polarity_histogram(
        analyzed_posts,
        title="Test Polarity Distribution",
        save_path="test_histogram.html"
    )
    print("✓ Histogram saved to: output/reports/test_histogram.html")
except Exception as e:
    print(f"✗ Histogram failed: {e}")

try:
    # 5. Word Cloud
    visualizer.create_word_cloud(
        analyzed_posts,
        save_path="test_wordcloud_all.png"
    )
    print("✓ Overall word cloud saved to: output/reports/test_wordcloud_all.png")
except Exception as e:
    print(f"✗ Word cloud failed: {e}")

try:
    # 6. Positive Word Cloud
    visualizer.create_word_cloud(
        analyzed_posts,
        sentiment='positive',
        save_path="test_wordcloud_positive.png"
    )
    print("✓ Positive word cloud saved to: output/reports/test_wordcloud_positive.png")
except Exception as e:
    print(f"✗ Positive word cloud failed: {e}")

try:
    # 7. Negative Word Cloud
    visualizer.create_word_cloud(
        analyzed_posts,
        sentiment='negative',
        save_path="test_wordcloud_negative.png"
    )
    print("✓ Negative word cloud saved to: output/reports/test_wordcloud_negative.png")
except Exception as e:
    print(f"✗ Negative word cloud failed: {e}")

print("\n" + "=" * 70)
print("VISUALIZATION GENERATION COMPLETE")
print("=" * 70)
print("\nGenerated files in output/reports/:")
print("  - test_pie_chart.html")
print("  - test_platform_comparison.html")
print("  - test_timeline.html")
print("  - test_histogram.html")
print("  - test_wordcloud_all.png")
print("  - test_wordcloud_positive.png")
print("  - test_wordcloud_negative.png")
