# 🚀 Quick Start Guide

Get the Social Media OSINT Analyzer running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Internet connection
- (Optional) API credentials for Reddit and Twitter

## Installation Steps

### 1. Navigate to Project Directory

```bash
cd social-media-osint
```

### 2. Run the Setup Script

```bash
./run.sh
```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Download required NLTK data
- Set up the output directory
- Start the Streamlit application

### 3. Configure API Credentials (Optional but Recommended)

If `run.sh` doesn't find a `.env` file, it will ask if you want to create one.

**For Reddit API:**
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" → Select "script"
3. Copy Client ID and Secret
4. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_secret
   ```

**For Twitter API:**
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a project and app
3. Generate Bearer Token
4. Add to `.env`:
   ```
   TWITTER_BEARER_TOKEN=your_bearer_token
   ```

**Note:** News collection works without any API credentials!

### 4. Use the Application

Once the server starts:
1. Your browser will open automatically to `http://localhost:8501`
2. Enter a keyword (e.g., "climate change", "#AI")
3. Select platforms (Reddit, Twitter, News)
4. Click "Start Analysis"
5. View results and download reports

## Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your favorite editor

# Run the application
streamlit run src/app.py
```

## Testing Without API Credentials

You can test the application immediately using only news sources:

1. Run `./run.sh`
2. When the app opens, deselect Reddit and Twitter
3. Leave only "News" selected
4. Enter a keyword and click "Start Analysis"

## Troubleshooting

### "Command not found: ./run.sh"
```bash
chmod +x run.sh
./run.sh
```

### "Python 3 not found"
Install Python from https://www.python.org/downloads/

### "Module not found" errors
```bash
pip install -r requirements.txt --force-reinstall
```

### "Rate limit exceeded"
- Wait a few minutes
- Reduce the number of posts per platform
- Use fewer platforms

### "Authentication failed"
- Check your API credentials in `.env`
- Ensure no extra spaces in the `.env` file
- Verify credentials are not expired

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [docs/libraries_explanation.md](docs/libraries_explanation.md) for library details
- Explore the generated reports in `output/reports/`

## Quick Commands

```bash
# Start the application
./run.sh

# Activate virtual environment manually
source venv/bin/activate

# Run tests
pytest tests/

# Deactivate virtual environment
deactivate
```

## Sample Searches

Try these keywords for interesting results:
- "artificial intelligence"
- "climate change"
- "#technology"
- "cryptocurrency"
- "space exploration"
- "renewable energy"

## Output Locations

- Reports: `output/reports/`
- Visualizations: `output/reports/*.html`, `*.png`
- JSON data: `output/reports/*.json`

## Getting Help

- Check documentation in `/docs`
- Review error messages in the Streamlit interface
- Ensure `.env` file is properly configured
- Verify internet connectivity

---

**Ready to analyze social media? Run `./run.sh` and get started!** 🚀
