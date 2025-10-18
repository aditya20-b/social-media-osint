# 🔍 Social Media OSINT Analyzer

A comprehensive Python-based OSINT (Open Source Intelligence) tool for collecting and analyzing publicly available social media data from multiple platforms with advanced sentiment analysis and visualization capabilities.

## 📋 Overview

This tool extracts and analyzes publicly available information about specific keywords or hashtags from:
- **Reddit** (using PRAW)
- **Twitter/X** (using Tweepy)
- **News Sources** (using newspaper3k and BeautifulSoup)

It performs sentiment analysis, generates visualizations, and produces detailed reports with trends and insights.

## ✨ Features

- 📊 **Multi-Platform Data Collection**: Gather data from Reddit, Twitter, and news sources simultaneously
- 🤖 **Sentiment Analysis**: Analyze sentiment (positive, negative, neutral) using TextBlob
- 📈 **Interactive Visualizations**: Pie charts, timelines, histograms, and word clouds
- 🌐 **Web Dashboard**: User-friendly Streamlit interface
- 📄 **Report Generation**: JSON and HTML reports with comprehensive findings
- ⚡ **Async Collection**: Parallel data gathering for improved performance
- 🛡️ **Error Handling**: Robust exception handling for API limits and network errors
- 🎨 **Platform Comparison**: Compare sentiment across different social media platforms

## 🏗️ Project Structure

```
social-media-osint/
├── src/
│   ├── collectors/          # Data collection modules
│   │   ├── reddit_collector.py
│   │   ├── twitter_collector.py
│   │   └── news_collector.py
│   ├── analyzers/           # Sentiment analysis
│   │   └── sentiment_analyzer.py
│   ├── visualizers/         # Data visualization
│   │   └── charts.py
│   ├── utils/              # Utilities
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── report_generator.py
│   └── app.py              # Streamlit web application
├── output/
│   └── reports/            # Generated reports and visualizations
├── docs/                   # Documentation
├── tests/                  # Unit tests
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- API credentials for Reddit and Twitter (optional but recommended)

### Step 1: Clone the Repository

```bash
cd social-media-osint
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data (for TextBlob)

```bash
python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"
```

### Step 5: Configure API Credentials

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API credentials:

#### Reddit API Setup
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the details:
   - Name: Your app name
   - App type: Script
   - Redirect URI: http://localhost:8080
4. Copy the client ID and secret to `.env`

#### Twitter/X API Setup
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new project and app
3. Generate API keys and tokens
4. Copy credentials to `.env`

**Note**: News collection works without API credentials using web scraping.

## 📖 Usage

### Running the Web Dashboard

```bash
streamlit run src/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Using the Dashboard

1. **Enter a keyword or hashtag** in the sidebar (e.g., "climate change", "#AI")
2. **Select platforms** to collect data from
3. **Adjust the number of posts** per platform (10-100)
4. **Click "Start Analysis"** to begin collection and analysis
5. **View results** including:
   - Sentiment distribution charts
   - Platform comparisons
   - Timeline analysis
   - Top positive/negative posts
6. **Download reports** in JSON or HTML format

### Command-Line Usage

You can also use the collectors programmatically:

```python
from src.collectors import RedditCollector, TwitterCollector, NewsCollector
from src.analyzers import SentimentAnalyzer

# Collect data
reddit = RedditCollector()
posts = reddit.search_posts("climate change", limit=50)

# Analyze sentiment
analyzer = SentimentAnalyzer()
analyzed_posts = analyzer.analyze_posts(posts)

# Get results
distribution = analyzer.get_sentiment_distribution(analyzed_posts)
print(distribution)
```

## 📚 Library Documentation

### Core Libraries

| Library | Purpose | Usage in Project |
|---------|---------|-----------------|
| **praw** | Reddit API wrapper | Authenticates with Reddit API, searches posts, retrieves comments, handles rate limiting |
| **tweepy** | Twitter/X API wrapper | Connects to Twitter API v2, searches tweets, manages OAuth authentication |
| **newspaper3k** | News article extraction | Parses news articles, extracts text, images, and metadata from news websites |
| **beautifulsoup4** | HTML/XML parsing | Scrapes Google News RSS feeds, parses HTML when newspaper3k fails |
| **textblob** | Sentiment analysis | Analyzes text polarity (-1 to 1) and subjectivity (0 to 1), classifies sentiment |
| **matplotlib** | Static visualizations | Creates word clouds and static charts |
| **plotly** | Interactive visualizations | Generates interactive pie charts, bar charts, timelines, and histograms |
| **streamlit** | Web framework | Provides the web dashboard interface with real-time updates |
| **pandas** | Data manipulation | Organizes data, creates DataFrames, aggregates sentiment trends |

See [docs/libraries_explanation.md](docs/libraries_explanation.md) for detailed explanations.

## 📊 Features Breakdown

### 1. Data Collection

- **Reddit**: Search by keyword, subreddit, time filter
- **Twitter**: Search recent tweets, hashtags, user timelines
- **News**: Google News search, article extraction from URLs

### 2. Sentiment Analysis

- **Polarity Score**: -1 (negative) to +1 (positive)
- **Subjectivity Score**: 0 (objective) to 1 (subjective)
- **Classification**: Positive, Negative, Neutral
- **Confidence**: Strength of sentiment

### 3. Visualizations

- **Pie Charts**: Overall sentiment distribution
- **Bar Charts**: Platform comparison
- **Timeline**: Sentiment trends over time
- **Histograms**: Polarity score distribution
- **Word Clouds**: Common terms by sentiment

### 4. Reports

- **JSON**: Machine-readable data with all posts and analysis
- **HTML**: Beautiful web-based report with visualizations
- **Text**: Console-friendly summary

## 🛡️ Exception Handling

The tool handles various error scenarios:

- **Rate Limits**: Automatic backoff and retry
- **API Errors**: Graceful degradation, continues with other platforms
- **Network Issues**: Timeout handling, connection retry
- **Missing Data**: Default values, skip problematic items
- **Authentication Errors**: Clear error messages, credential validation

## 📈 Sample Output

```
╔══════════════════════════════════════════════════════════════╗
║         SOCIAL MEDIA OSINT ANALYSIS SUMMARY                  ║
╚══════════════════════════════════════════════════════════════╝

Keyword: "artificial intelligence"
Generated: 2024-01-15 14:30:22

───────────────────────────────────────────────────────────────
OVERALL SENTIMENT DISTRIBUTION
───────────────────────────────────────────────────────────────
Total Posts: 150
✅ Positive: 78 (52.0%)
❌ Negative: 32 (21.33%)
⚪ Neutral:  40 (26.67%)

───────────────────────────────────────────────────────────────
AVERAGE SENTIMENT SCORES
───────────────────────────────────────────────────────────────
Overall Sentiment: POSITIVE
Average Polarity: 0.145 (range: -1 to 1)
Average Subjectivity: 0.523 (range: 0 to 1)
```

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/
```

## 🔒 Privacy & Ethics

This tool:
- ✅ Collects only **publicly available** information
- ✅ Respects **robots.txt** and API rate limits
- ✅ Does not bypass authentication or paywalls
- ✅ Follows platform terms of service
- ❌ Should not be used for harassment or stalking
- ❌ Should not be used to scrape private/protected data

## 📝 Requirements

See `requirements.txt` for complete list. Key dependencies:

```
praw>=7.7.1
tweepy>=4.14.0
newspaper3k>=0.2.8
beautifulsoup4>=4.12.2
textblob>=0.17.1
matplotlib>=3.8.2
plotly>=5.18.0
streamlit>=1.29.0
pandas>=2.1.4
```

## 🐛 Troubleshooting

### "Authentication failed" errors
- Check your API credentials in `.env`
- Ensure credentials are not expired
- Verify you have the correct permissions

### "Rate limit exceeded"
- Wait for the specified retry period
- Reduce the number of posts per platform
- Use fewer platforms simultaneously

### News collection fails
- Some websites block scrapers
- Try different news sources
- Check your internet connection

### Import errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Download NLTK data: `python -c "import nltk; nltk.download('all')"`

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Ensure compliance with platform terms of service and local laws when using this tool.

## 👨‍💻 Author

Created for CIA-2 OSINT Analysis Project

## 🙏 Acknowledgments

- PRAW developers for Reddit API wrapper
- Tweepy developers for Twitter API wrapper
- newspaper3k developers for article extraction
- Streamlit team for the amazing web framework
- TextBlob for sentiment analysis

## 📞 Support

For issues and questions:
- Check the documentation in `/docs`
- Review example usage in the code
- Create an issue in the repository

---

**⚠️ Disclaimer**: This tool is for educational and research purposes only. Users are responsible for ensuring compliance with applicable laws and platform terms of service.
