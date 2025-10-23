# Social Media OSINT Analyzer

A tool to scrape and analyze public social media posts from Reddit, Twitter, and news sources. Built for CIA-2 assignment.

## What it does

Searches for keywords/hashtags across multiple platforms, runs sentiment analysis on the posts, and generates visualizations and reports. Useful for tracking public opinion on topics or monitoring trends.

**Platforms:**
- Reddit (PRAW API)
- Twitter/X (Tweepy API)
- News sites (web scraping)

**Features:**
- Sentiment analysis with polarity scores
- Interactive charts and word clouds
- Web dashboard (Streamlit)
- JSON/HTML report export
- Multi-platform comparison

## Setup

**Requirements:**
- Python 3.8+
- API keys for Reddit/Twitter (optional but recommended)

**Installation:**

```bash
# Clone and navigate
cd social-media-osint

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"
```

**API Setup (optional):**

1. Copy `.env.example` to `.env`
2. Add your API credentials:

For Reddit: https://www.reddit.com/prefs/apps
- Create app as "script" type
- Copy client ID and secret

For Twitter: https://developer.twitter.com/en/portal/dashboard
- Create project/app
- Copy API keys

News scraping works without any credentials.

## Usage

**Web Dashboard:**

```bash
streamlit run src/app.py
```

Opens at `http://localhost:8501`

1. Enter keyword/hashtag
2. Select platforms
3. Set number of posts (10-100)
4. Click "Start Analysis"
5. View charts and download reports

**Programmatic Usage:**

```python
from src.collectors import RedditCollector
from src.analyzers import SentimentAnalyzer

reddit = RedditCollector()
posts = reddit.search_posts("climate change", limit=50)

analyzer = SentimentAnalyzer()
analyzed_posts = analyzer.analyze_posts(posts)
print(analyzer.get_sentiment_distribution(analyzed_posts))
```

## Tech Stack

- **praw** - Reddit API
- **tweepy** - Twitter API
- **newspaper3k** - News article scraping
- **beautifulsoup4** - HTML parsing
- **textblob** - Sentiment analysis (polarity -1 to 1)
- **plotly** - Interactive charts
- **streamlit** - Web dashboard
- **pandas** - Data processing

## How it works

**Data Collection:**
- Reddit: searches posts by keyword/subreddit
- Twitter: searches tweets and hashtags
- News: scrapes articles from Google News

**Sentiment Analysis:**
- Polarity score: -1 (negative) to +1 (positive)
- Classifies as positive/negative/neutral
- Calculates subjectivity (0-1 scale)

**Visualizations:**
- Sentiment distribution pie charts
- Platform comparison bar charts
- Timeline trends
- Word clouds

## Common Issues

**API errors:** Check credentials in `.env`, make sure they're not expired

**Rate limits:** Reduce number of posts or wait before retrying

**News scraping fails:** Some sites block scrapers, try different sources

**Import errors:** Make sure venv is activated, reinstall requirements

## Testing

```bash
pytest tests/
```

## Notes

- Only scrapes publicly available data
- Respects API rate limits and robots.txt
- For educational use only
- Don't use this to harass people or scrape private data

## License

Educational project - make sure you comply with platform ToS and local laws.

---

Built for CIA-2 assignment.
