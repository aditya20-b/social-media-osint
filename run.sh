#!/bin/bash

# Social Media OSINT Analyzer - Startup Script
# This script sets up the environment and runs the Streamlit application

set -e  # Exit on error

echo "================================================"
echo "   Social Media OSINT Analyzer - Setup"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python is installed
echo -e "${BLUE}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
    echo ""
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Check if dependencies are installed
echo -e "${BLUE}Checking dependencies...${NC}"
if ! python -c "import streamlit" 2>/dev/null; then
    echo -e "${YELLOW}Dependencies not found. Installing...${NC}"
    pip install -r requirements.txt
    echo ""
    echo -e "${GREEN}✓ Dependencies installed${NC}"
    echo ""
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
    echo ""
fi

# Download NLTK data if not exists
echo -e "${BLUE}Checking NLTK data...${NC}"
python3 -c "import nltk; nltk.download('brown', quiet=True); nltk.download('punkt', quiet=True)" 2>/dev/null
echo -e "${GREEN}✓ NLTK data ready${NC}"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Warning: .env file not found${NC}"
    echo "   Copy .env.example to .env and add your API credentials"
    echo ""
    echo "   For Reddit API: https://www.reddit.com/prefs/apps"
    echo "   For Twitter API: https://developer.twitter.com/en/portal/dashboard"
    echo ""
    echo -e "${BLUE}Do you want to create .env from template? (y/n)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created. Please edit it with your credentials.${NC}"
        echo ""
        echo -e "${YELLOW}Press Enter to continue after editing .env...${NC}"
        read -r
    fi
else
    echo -e "${GREEN}✓ .env file found${NC}"
    echo ""
fi

# Create output directory if it doesn't exist
mkdir -p output/reports
echo -e "${GREEN}✓ Output directory ready${NC}"
echo ""

# Display available platforms
echo "================================================"
echo "   Checking Platform Availability"
echo "================================================"
echo ""

python3 << 'PYEOF'
import os
from dotenv import load_dotenv
load_dotenv()

platforms = []

# Check Reddit
if os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET'):
    platforms.append('✓ Reddit')
else:
    platforms.append('✗ Reddit (credentials missing)')

# Check Twitter
if os.getenv('TWITTER_BEARER_TOKEN') or os.getenv('TWITTER_API_KEY'):
    platforms.append('✓ Twitter/X')
else:
    platforms.append('✗ Twitter/X (credentials missing)')

# News is always available
platforms.append('✓ News Sources')

for platform in platforms:
    print(platform)
PYEOF

echo ""
echo "================================================"
echo "   Starting Streamlit Application"
echo "================================================"
echo ""
echo -e "${GREEN}Application will open in your browser automatically${NC}"
echo -e "${BLUE}Press Ctrl+C to stop the server${NC}"
echo ""

# Run Streamlit
streamlit run src/app.py
