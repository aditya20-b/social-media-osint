"""
Streamlit Web Dashboard for Social Media OSINT Analyzer.
Main application interface.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from collectors import RedditCollector, TwitterCollector, NewsCollector
from collectors.reddit_no_auth_collector import RedditNoAuthCollector
from analyzers.sentiment_analyzer import SentimentAnalyzer
from analyzers.enhanced_sentiment_analyzer import EnhancedSentimentAnalyzer
from visualizers import SentimentVisualizer
from utils.config import Config
from utils.report_generator import ReportGenerator
from utils.exceptions import (
    AuthenticationError,
    RateLimitError,
    DataCollectionError,
    NetworkError
)


# Page configuration
st.set_page_config(
    page_title="Social Media OSINT Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        color: #667eea;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 30px;
        border-radius: 5px;
        font-size: 1.1em;
    }
</style>
""", unsafe_allow_html=True)


def initialize_collectors():
    """Initialize data collectors based on available credentials."""
    collectors = {}
    errors = []

    # Reddit - Try authenticated first, fall back to no-auth
    try:
        if Config.validate_reddit_config():
            collectors['reddit'] = RedditCollector()
            st.sidebar.info("✅ Reddit: Using authenticated API")
        else:
            collectors['reddit'] = RedditNoAuthCollector()
            st.sidebar.success("✅ Reddit: Using public API (no auth needed!)")
    except Exception as e:
        # If authenticated fails, try no-auth
        try:
            collectors['reddit'] = RedditNoAuthCollector()
            st.sidebar.success("✅ Reddit: Using public API (no auth needed!)")
        except Exception as e2:
            errors.append(f"Reddit: {str(e2)}")

    # Twitter
    try:
        if Config.validate_twitter_config():
            collectors['twitter'] = TwitterCollector()
            st.sidebar.info("✅ Twitter: Authenticated API")
    except Exception as e:
        errors.append(f"Twitter: {str(e)}")

    # News (always available)
    try:
        collectors['news'] = NewsCollector()
        st.sidebar.info("✅ News: Web scraping")
    except Exception as e:
        errors.append(f"News: {str(e)}")

    return collectors, errors


def collect_data(collectors, keyword, platforms, limit):
    """Collect data from selected platforms."""
    all_posts = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    total_platforms = len(platforms)

    for idx, platform in enumerate(platforms):
        if platform not in collectors:
            st.warning(f"⚠️ {platform.capitalize()} collector not available (check credentials)")
            continue

        try:
            status_text.text(f"Collecting from {platform.capitalize()}...")

            if platform == 'reddit':
                posts = collectors['reddit'].search_posts(keyword, limit=limit)
            elif platform == 'twitter':
                posts = collectors['twitter'].search_tweets(keyword, limit=limit)
            elif platform == 'news':
                posts = collectors['news'].search_google_news(keyword, limit=limit)

            all_posts.extend(posts)
            st.success(f"✅ Collected {len(posts)} posts from {platform.capitalize()}")

        except RateLimitError as e:
            st.error(f"⚠️ Rate limit exceeded for {platform.capitalize()}. Try again later.")
        except AuthenticationError as e:
            st.error(f"❌ Authentication failed for {platform.capitalize()}: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error collecting from {platform.capitalize()}: {str(e)}")

        progress_bar.progress((idx + 1) / total_platforms)

    status_text.empty()
    progress_bar.empty()

    return all_posts


def main():
    """Main application function."""

    # Header
    st.markdown('<h1 class="main-header">🔍 Social Media OSINT Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### Analyze sentiment from Reddit, Twitter/X, and News sources")

    # Sidebar
    st.sidebar.header("⚙️ Configuration")

    # Initialize collectors
    with st.spinner("Initializing collectors..."):
        collectors, init_errors = initialize_collectors()

    if init_errors:
        with st.sidebar.expander("⚠️ Initialization Warnings", expanded=False):
            for error in init_errors:
                st.warning(error)

    # Show available platforms
    available_platforms = list(collectors.keys())
    st.sidebar.success(f"✅ Available platforms: {', '.join([p.capitalize() for p in available_platforms])}")

    # Search configuration
    st.sidebar.subheader("🔎 Search Settings")
    keyword = st.sidebar.text_input("Keyword or Hashtag", value="climate change", help="Enter a keyword or hashtag to search")

    platforms = st.sidebar.multiselect(
        "Select Platforms",
        options=available_platforms,
        default=available_platforms,
        help="Choose which platforms to collect data from"
    )

    limit_per_platform = st.sidebar.slider(
        "Posts per Platform",
        min_value=10,
        max_value=100,
        value=50,
        step=10,
        help="Number of posts to collect from each platform"
    )

    # Analysis button
    analyze_button = st.sidebar.button("🚀 Start Analysis", use_container_width=True)

    # Main content area
    if not analyze_button:
        # Show welcome screen
        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("**📊 Multi-Platform**\n\nCollect data from Reddit, Twitter, and news sources simultaneously")

        with col2:
            st.info("**🤖 Sentiment Analysis**\n\nAnalyze sentiment using TextBlob with polarity and subjectivity scores")

        with col3:
            st.info("**📈 Visualizations**\n\nInteractive charts, graphs, and word clouds for insights")

        st.markdown("---")
        st.markdown("### 🎯 How to use:")
        st.markdown("""
        1. **Configure API credentials** in the `.env` file (see `.env.example`)
        2. **Enter a keyword** or hashtag in the sidebar
        3. **Select platforms** to collect data from
        4. **Click 'Start Analysis'** to begin
        5. **View results** and download reports
        """)

        st.markdown("---")
        st.markdown("### 📚 Required Libraries:")
        st.code("""
        • praw - Reddit API access
        • tweepy - Twitter/X API access
        • newspaper3k - News article extraction
        • beautifulsoup4 - Web scraping
        • textblob - Sentiment analysis
        • matplotlib & plotly - Visualizations
        • streamlit - Web dashboard
        """)

    else:
        # Run analysis
        if not keyword:
            st.error("❌ Please enter a keyword or hashtag")
            return

        if not platforms:
            st.error("❌ Please select at least one platform")
            return

        st.markdown("---")
        st.header(f"📊 Analysis Results: '{keyword}'")

        # Step 1: Collect data
        with st.spinner("🔍 Collecting data..."):
            posts = collect_data(collectors, keyword, platforms, limit_per_platform)

        if not posts:
            st.error("❌ No data collected. Please check your credentials and try again.")
            return

        st.info(f"✅ Collected {len(posts)} total posts")

        # Step 2: Analyze sentiment with ENHANCED analyzer
        with st.spinner("🤖 Analyzing sentiment with advanced AI..."):
            analyzer = EnhancedSentimentAnalyzer()  # Using enhanced analyzer!
            analyzed_posts = analyzer.analyze_posts(posts)
            distribution = analyzer.get_sentiment_distribution(analyzed_posts)

            # Calculate platform and average sentiment manually since enhanced analyzer
            # doesn't have all the same methods
            platform_posts = {}
            for post in analyzed_posts:
                platform = post.get('platform', 'unknown')
                if platform not in platform_posts:
                    platform_posts[platform] = []
                platform_posts[platform].append(post)

            platform_sentiment = {}
            for platform, platform_post_list in platform_posts.items():
                platform_sentiment[platform] = analyzer.get_sentiment_distribution(platform_post_list)

            # Calculate average
            polarities = [p.get('sentiment_analysis', {}).get('vader_compound', 0) for p in analyzed_posts]
            subjectivities = [p.get('sentiment_analysis', {}).get('textblob_subjectivity', 0) for p in analyzed_posts]

            avg_polarity = sum(polarities) / len(polarities) if polarities else 0
            avg_subjectivity = sum(subjectivities) / len(subjectivities) if subjectivities else 0

            if avg_polarity > 0.05:
                overall = 'positive'
            elif avg_polarity < -0.05:
                overall = 'negative'
            else:
                overall = 'neutral'

            average_sentiment = {
                'avg_polarity': round(avg_polarity, 3),
                'avg_subjectivity': round(avg_subjectivity, 3),
                'overall_sentiment': overall
            }

            # Get top posts
            top_positive = sorted(
                [p for p in analyzed_posts if p.get('sentiment_analysis', {}).get('sentiment') == 'positive'],
                key=lambda p: p.get('sentiment_analysis', {}).get('vader_compound', 0),
                reverse=True
            )[:5]

            top_negative = sorted(
                [p for p in analyzed_posts if p.get('sentiment_analysis', {}).get('sentiment') == 'negative'],
                key=lambda p: p.get('sentiment_analysis', {}).get('vader_compound', 0)
            )[:5]

        st.success("✅ Enhanced sentiment analysis complete with detailed explanations!")

        # Display metrics
        st.markdown("### 📈 Sentiment Overview")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Posts", distribution['total'])

        with col2:
            st.metric("Positive", f"{distribution['positive']} ({distribution['positive_pct']}%)")

        with col3:
            st.metric("Negative", f"{distribution['negative']} ({distribution['negative_pct']}%)")

        with col4:
            st.metric("Neutral", f"{distribution['neutral']} ({distribution['neutral_pct']}%)")

        # Average sentiment
        st.markdown("### 📊 Average Sentiment Scores")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Overall Sentiment", average_sentiment['overall_sentiment'].upper())

        with col2:
            polarity_delta = f"{average_sentiment['avg_polarity']:+.3f}"
            st.metric("Avg Polarity", f"{average_sentiment['avg_polarity']:.3f}", delta=polarity_delta)

        with col3:
            st.metric("Avg Subjectivity", f"{average_sentiment['avg_subjectivity']:.3f}")

        # Visualizations
        st.markdown("---")
        st.header("📊 Visualizations")

        visualizer = SentimentVisualizer(output_dir=Config.OUTPUT_DIRECTORY)

        # Pie chart
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Sentiment Distribution")
            fig_pie = visualizer.create_sentiment_pie_chart(distribution)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.subheader("Polarity Distribution")
            fig_hist = visualizer.create_polarity_histogram(analyzed_posts)
            st.plotly_chart(fig_hist, use_container_width=True)

        # Platform comparison
        if len(platforms) > 1:
            st.subheader("Platform Comparison")
            fig_platform = visualizer.create_platform_comparison_chart(platform_sentiment)
            st.plotly_chart(fig_platform, use_container_width=True)

        # Timeline
        st.subheader("Sentiment Timeline")
        fig_timeline = visualizer.create_sentiment_timeline(analyzed_posts)
        st.plotly_chart(fig_timeline, use_container_width=True)

        # Top posts
        st.markdown("---")
        st.header("📝 Top Posts")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✨ Most Positive")
            for post in top_positive:
                analysis = post.get('sentiment_analysis', {})
                vader_score = analysis.get('vader_compound', 0)
                with st.expander(f"{post.get('platform', 'unknown').capitalize()} - Score: {vader_score:+.3f}"):
                    st.write("**Post:**")
                    st.write(post.get('title') or post.get('text', '')[:300])

                    st.markdown("---")
                    st.write("**🔍 WHY IS THIS POSITIVE?**")
                    st.info(analysis.get('explanation', 'No explanation available'))

                    if analysis.get('positive_words'):
                        st.write("**✅ Positive Words Found:**")
                        for word, strength in analysis.get('positive_words', [])[:5]:
                            st.write(f"• '{word}' ({strength})")

                    if analysis.get('reasoning'):
                        st.write("**💡 Reasoning:**")
                        for reason in analysis.get('reasoning', []):
                            st.write(f"• {reason}")

                    st.markdown(f"[View Full Post]({post.get('url', '#')})")

        with col2:
            st.subheader("⚠️ Most Negative")
            for post in top_negative:
                analysis = post.get('sentiment_analysis', {})
                vader_score = analysis.get('vader_compound', 0)
                with st.expander(f"{post.get('platform', 'unknown').capitalize()} - Score: {vader_score:+.3f}"):
                    st.write("**Post:**")
                    st.write(post.get('title') or post.get('text', '')[:300])

                    st.markdown("---")
                    st.write("**🔍 WHY IS THIS NEGATIVE?**")
                    st.warning(analysis.get('explanation', 'No explanation available'))

                    if analysis.get('negative_words'):
                        st.write("**❌ Negative Words Found:**")
                        for word, strength in analysis.get('negative_words', [])[:5]:
                            st.write(f"• '{word}' ({strength})")

                    if analysis.get('reasoning'):
                        st.write("**💡 Reasoning:**")
                        for reason in analysis.get('reasoning', []):
                            st.write(f"• {reason}")

                    st.markdown(f"[View Full Post]({post.get('url', '#')})")

        # Platform breakdown
        st.markdown("---")
        st.header("🌐 Platform Breakdown")

        platform_df = pd.DataFrame(platform_sentiment).T
        platform_df = platform_df[['total', 'positive', 'negative', 'neutral', 'positive_pct', 'negative_pct', 'neutral_pct']]
        platform_df.columns = ['Total', 'Positive', 'Negative', 'Neutral', 'Positive %', 'Negative %', 'Neutral %']
        st.dataframe(platform_df, use_container_width=True)

        # Generate reports
        st.markdown("---")
        st.header("📄 Download Reports")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📥 Generate JSON Report", use_container_width=True):
                with st.spinner("Generating JSON report..."):
                    report_gen = ReportGenerator(output_dir=Config.OUTPUT_DIRECTORY)
                    json_path = report_gen.generate_json_report(
                        keyword, analyzed_posts, distribution,
                        platform_sentiment, average_sentiment,
                        top_positive, top_negative
                    )
                    st.success(f"✅ JSON report saved: {json_path}")

        with col2:
            if st.button("📥 Generate HTML Report", use_container_width=True):
                with st.spinner("Generating HTML report..."):
                    report_gen = ReportGenerator(output_dir=Config.OUTPUT_DIRECTORY)
                    html_path = report_gen.generate_html_report(
                        keyword, analyzed_posts, distribution,
                        platform_sentiment, average_sentiment,
                        top_positive, top_negative
                    )
                    st.success(f"✅ HTML report saved: {html_path}")

        # Text summary
        with st.expander("📋 View Text Summary"):
            report_gen = ReportGenerator()
            summary = report_gen.generate_text_summary(
                keyword, distribution, average_sentiment, platform_sentiment
            )
            st.code(summary)


if __name__ == "__main__":
    main()
