"""
Visualization module for sentiment analysis results.
Creates charts and graphs using matplotlib and plotly.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
from pathlib import Path


class SentimentVisualizer:
    """Create visualizations for sentiment analysis data."""

    # Color scheme for sentiments
    COLORS = {
        'positive': '#4CAF50',  # Green
        'negative': '#F44336',  # Red
        'neutral': '#9E9E9E'    # Grey
    }

    def __init__(self, output_dir: str = './output/reports'):
        """
        Initialize visualizer.

        Args:
            output_dir: Directory to save charts
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid')

    def create_sentiment_pie_chart(
        self,
        distribution: Dict,
        title: str = 'Sentiment Distribution',
        save_path: Optional[str] = None
    ) -> go.Figure:
        """
        Create a pie chart showing sentiment distribution.

        Args:
            distribution: Sentiment distribution dictionary
            title: Chart title
            save_path: Path to save the chart

        Returns:
            Plotly Figure object
        """
        labels = ['Positive', 'Negative', 'Neutral']
        values = [
            distribution.get('positive', 0),
            distribution.get('negative', 0),
            distribution.get('neutral', 0)
        ]
        colors = [self.COLORS['positive'], self.COLORS['negative'], self.COLORS['neutral']]

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])

        fig.update_layout(
            title=title,
            showlegend=True,
            height=500,
            font=dict(size=14)
        )

        if save_path:
            fig.write_html(str(self.output_dir / save_path))

        return fig

    def create_platform_comparison_chart(
        self,
        platform_sentiment: Dict[str, Dict],
        title: str = 'Sentiment by Platform',
        save_path: Optional[str] = None
    ) -> go.Figure:
        """
        Create a grouped bar chart comparing sentiment across platforms.

        Args:
            platform_sentiment: Dictionary mapping platform to sentiment distribution
            title: Chart title
            save_path: Path to save the chart

        Returns:
            Plotly Figure object
        """
        platforms = list(platform_sentiment.keys())
        positive = [platform_sentiment[p].get('positive', 0) for p in platforms]
        negative = [platform_sentiment[p].get('negative', 0) for p in platforms]
        neutral = [platform_sentiment[p].get('neutral', 0) for p in platforms]

        fig = go.Figure(data=[
            go.Bar(name='Positive', x=platforms, y=positive, marker_color=self.COLORS['positive']),
            go.Bar(name='Negative', x=platforms, y=negative, marker_color=self.COLORS['negative']),
            go.Bar(name='Neutral', x=platforms, y=neutral, marker_color=self.COLORS['neutral'])
        ])

        fig.update_layout(
            title=title,
            xaxis_title='Platform',
            yaxis_title='Number of Posts',
            barmode='group',
            height=500,
            font=dict(size=14)
        )

        if save_path:
            fig.write_html(str(self.output_dir / save_path))

        return fig

    def create_sentiment_timeline(
        self,
        posts: List[Dict],
        title: str = 'Sentiment Over Time',
        save_path: Optional[str] = None
    ) -> go.Figure:
        """
        Create a timeline chart showing sentiment trends.

        Args:
            posts: List of analyzed posts with timestamps
            title: Chart title
            save_path: Path to save the chart

        Returns:
            Plotly Figure object
        """
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
            # Return empty figure
            fig = go.Figure()
            fig.add_annotation(
                text="No timeline data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig

        df = pd.DataFrame(data)
        df = df.sort_values('timestamp')

        # Aggregate by hour or day
        if len(df) > 100:
            df['time_bucket'] = df['timestamp'].dt.floor('D')
        else:
            df['time_bucket'] = df['timestamp'].dt.floor('H')

        # Count sentiment by time bucket
        sentiment_by_time = df.groupby(['time_bucket', 'sentiment']).size().unstack(fill_value=0)

        fig = go.Figure()

        for sentiment in ['positive', 'negative', 'neutral']:
            if sentiment in sentiment_by_time.columns:
                fig.add_trace(go.Scatter(
                    x=sentiment_by_time.index,
                    y=sentiment_by_time[sentiment],
                    mode='lines+markers',
                    name=sentiment.capitalize(),
                    line=dict(color=self.COLORS[sentiment], width=2),
                    marker=dict(size=6)
                ))

        fig.update_layout(
            title=title,
            xaxis_title='Time',
            yaxis_title='Number of Posts',
            height=500,
            hovermode='x unified',
            font=dict(size=14)
        )

        if save_path:
            fig.write_html(str(self.output_dir / save_path))

        return fig

    def create_word_cloud(
        self,
        posts: List[Dict],
        sentiment: Optional[str] = None,
        save_path: Optional[str] = None
    ) -> None:
        """
        Create a word cloud from post text.

        Args:
            posts: List of posts
            sentiment: Filter by sentiment ('positive', 'negative', 'neutral', or None for all)
            save_path: Path to save the image
        """
        # Filter by sentiment if specified
        if sentiment:
            posts = [
                p for p in posts
                if p.get('sentiment_analysis', {}).get('sentiment') == sentiment
            ]

        # Collect all text
        text = ' '.join([
            p.get('full_text', '') or p.get('text', '')
            for p in posts
        ])

        if not text.strip():
            print("No text available for word cloud")
            return

        # Generate word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate(text)

        # Create figure
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        if sentiment:
            plt.title(f'Word Cloud - {sentiment.capitalize()} Sentiment', fontsize=20, pad=20)
        else:
            plt.title('Word Cloud - All Posts', fontsize=20, pad=20)

        if save_path:
            plt.savefig(str(self.output_dir / save_path), bbox_inches='tight', dpi=150)
        else:
            plt.tight_layout()

        plt.close()

    def create_polarity_histogram(
        self,
        posts: List[Dict],
        title: str = 'Polarity Distribution',
        save_path: Optional[str] = None
    ) -> go.Figure:
        """
        Create a histogram showing polarity score distribution.

        Args:
            posts: List of analyzed posts
            title: Chart title
            save_path: Path to save the chart

        Returns:
            Plotly Figure object
        """
        polarities = [
            post.get('sentiment_analysis', {}).get('polarity', 0)
            for post in posts
        ]

        fig = go.Figure(data=[go.Histogram(
            x=polarities,
            nbinsx=50,
            marker_color='#2196F3',
            opacity=0.75
        )])

        fig.update_layout(
            title=title,
            xaxis_title='Polarity Score (-1 to 1)',
            yaxis_title='Number of Posts',
            height=500,
            font=dict(size=14),
            showlegend=False
        )

        # Add vertical lines for thresholds
        fig.add_vline(x=-0.1, line_dash="dash", line_color="red", annotation_text="Negative")
        fig.add_vline(x=0.1, line_dash="dash", line_color="green", annotation_text="Positive")

        if save_path:
            fig.write_html(str(self.output_dir / save_path))

        return fig

    def create_top_posts_table(
        self,
        posts: List[Dict],
        sentiment: str = 'positive',
        limit: int = 5
    ) -> pd.DataFrame:
        """
        Create a table of top posts by sentiment.

        Args:
            posts: List of analyzed posts
            sentiment: Sentiment type
            limit: Number of posts

        Returns:
            DataFrame with top posts
        """
        # Filter by sentiment
        filtered = [
            p for p in posts
            if p.get('sentiment_analysis', {}).get('sentiment') == sentiment
        ]

        # Sort by confidence
        sorted_posts = sorted(
            filtered,
            key=lambda p: p.get('sentiment_analysis', {}).get('confidence', 0),
            reverse=True
        )[:limit]

        # Create table data
        table_data = []
        for post in sorted_posts:
            table_data.append({
                'Platform': post.get('platform', 'unknown').capitalize(),
                'Text': (post.get('title') or post.get('text', ''))[:100] + '...',
                'Polarity': post.get('sentiment_analysis', {}).get('polarity', 0),
                'Confidence': post.get('sentiment_analysis', {}).get('confidence', 0),
                'URL': post.get('url', 'N/A')
            })

        return pd.DataFrame(table_data)

    def create_dashboard(
        self,
        posts: List[Dict],
        distribution: Dict,
        platform_sentiment: Dict[str, Dict],
        keyword: str
    ) -> None:
        """
        Create a comprehensive dashboard with multiple visualizations.

        Args:
            posts: List of analyzed posts
            distribution: Overall sentiment distribution
            platform_sentiment: Sentiment by platform
            keyword: Search keyword
        """
        print(f"\n📊 Generating visualizations for '{keyword}'...")

        # 1. Sentiment Pie Chart
        self.create_sentiment_pie_chart(
            distribution,
            title=f'Sentiment Distribution: {keyword}',
            save_path='sentiment_pie_chart.html'
        )
        print("✓ Sentiment pie chart created")

        # 2. Platform Comparison
        if len(platform_sentiment) > 1:
            self.create_platform_comparison_chart(
                platform_sentiment,
                title=f'Platform Comparison: {keyword}',
                save_path='platform_comparison.html'
            )
            print("✓ Platform comparison chart created")

        # 3. Timeline
        self.create_sentiment_timeline(
            posts,
            title=f'Sentiment Timeline: {keyword}',
            save_path='sentiment_timeline.html'
        )
        print("✓ Sentiment timeline created")

        # 4. Polarity Histogram
        self.create_polarity_histogram(
            posts,
            title=f'Polarity Distribution: {keyword}',
            save_path='polarity_histogram.html'
        )
        print("✓ Polarity histogram created")

        # 5. Word Clouds
        self.create_word_cloud(posts, save_path='wordcloud_all.png')
        print("✓ Overall word cloud created")

        self.create_word_cloud(posts, sentiment='positive', save_path='wordcloud_positive.png')
        print("✓ Positive word cloud created")

        self.create_word_cloud(posts, sentiment='negative', save_path='wordcloud_negative.png')
        print("✓ Negative word cloud created")

        print(f"\n✅ All visualizations saved to: {self.output_dir}")
