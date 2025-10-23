#!/usr/bin/env python3
"""
Test that the Streamlit app can be imported without errors
"""

import sys
from pathlib import Path

# This simulates how Streamlit will import the app
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("Testing app imports...")

try:
    # Test all the imports that app.py uses
    from collectors import RedditCollector, TwitterCollector, NewsCollector
    print("✓ Collectors imported")

    from analyzers import SentimentAnalyzer
    print("✓ Sentiment analyzer imported")

    from visualizers import SentimentVisualizer
    print("✓ Visualizer imported")

    from utils.config import Config
    print("✓ Config imported")

    from utils.report_generator import ReportGenerator
    print("✓ Report generator imported")

    from utils.exceptions import (
        AuthenticationError,
        RateLimitError,
        DataCollectionError,
        NetworkError
    )
    print("✓ Exceptions imported")

    print("\n" + "="*60)
    print("✅ ALL IMPORTS SUCCESSFUL")
    print("="*60)
    print("\nThe Streamlit app should now start without import errors.")
    print("\nTo run the app:")
    print("  cd /Users/aditya/Documents/Github/OSINT-CIA2/social-media-osint")
    print("  source venv/bin/activate")
    print("  streamlit run src/app.py")

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
