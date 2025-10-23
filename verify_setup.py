#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all dependencies and configurations are correct.
"""

import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    """Print a formatted header."""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  {GREEN}✓{RESET} Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  {RED}✗{RESET} Python {version.major}.{version.minor}.{version.micro} (need 3.8+)")
        return False


def check_dependencies():
    """Check if all required packages are installed."""
    print("\nChecking dependencies...")

    required_packages = [
        'praw',
        'tweepy',
        'newspaper',
        'bs4',
        'textblob',
        'matplotlib',
        'plotly',
        'streamlit',
        'pandas',
        'dotenv',
        'jinja2',
        'requests',
        'nltk',
        'wordcloud'
    ]

    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"  {GREEN}✓{RESET} {package}")
        except ImportError:
            print(f"  {RED}✗{RESET} {package} (not installed)")
            all_installed = False

    return all_installed


def check_nltk_data():
    """Check if required NLTK data is downloaded."""
    print("\nChecking NLTK data...")

    try:
        import nltk

        required_data = ['brown', 'punkt']
        all_present = True

        for data_name in required_data:
            try:
                nltk.data.find(f'corpora/{data_name}')
                print(f"  {GREEN}✓{RESET} {data_name}")
            except LookupError:
                print(f"  {YELLOW}!{RESET} {data_name} (downloading...)")
                nltk.download(data_name, quiet=True)
                print(f"  {GREEN}✓{RESET} {data_name} (installed)")

        return True
    except Exception as e:
        print(f"  {RED}✗{RESET} Error checking NLTK data: {e}")
        return False


def check_env_file():
    """Check if .env file exists and has required variables."""
    print("\nChecking environment configuration...")

    env_path = Path('.env')

    if not env_path.exists():
        print(f"  {YELLOW}!{RESET} .env file not found")
        print(f"     Copy .env.example to .env and add your credentials")
        return False

    print(f"  {GREEN}✓{RESET} .env file exists")

    # Check for required variables
    from dotenv import load_dotenv
    load_dotenv()

    platforms = []

    # Reddit
    if os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET'):
        print(f"  {GREEN}✓{RESET} Reddit credentials configured")
        platforms.append('reddit')
    else:
        print(f"  {YELLOW}!{RESET} Reddit credentials missing (optional)")

    # Twitter
    if os.getenv('TWITTER_BEARER_TOKEN') or os.getenv('TWITTER_API_KEY'):
        print(f"  {GREEN}✓{RESET} Twitter credentials configured")
        platforms.append('twitter')
    else:
        print(f"  {YELLOW}!{RESET} Twitter credentials missing (optional)")

    # News (always available)
    print(f"  {GREEN}✓{RESET} News sources available (no credentials needed)")
    platforms.append('news')

    return len(platforms) > 0


def check_directory_structure():
    """Check if required directories exist."""
    print("\nChecking directory structure...")

    required_dirs = [
        'src',
        'src/collectors',
        'src/analyzers',
        'src/visualizers',
        'src/utils',
        'docs',
        'tests',
        'output/reports'
    ]

    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  {GREEN}✓{RESET} {dir_path}")
        else:
            print(f"  {RED}✗{RESET} {dir_path} (missing)")
            all_exist = False

    return all_exist


def check_source_files():
    """Check if all source files are present."""
    print("\nChecking source files...")

    required_files = [
        'src/app.py',
        'src/collectors/reddit_collector.py',
        'src/collectors/twitter_collector.py',
        'src/collectors/news_collector.py',
        'src/analyzers/sentiment_analyzer.py',
        'src/visualizers/charts.py',
        'src/utils/config.py',
        'src/utils/exceptions.py',
        'src/utils/report_generator.py',
        'requirements.txt',
        'README.md'
    ]

    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  {GREEN}✓{RESET} {file_path}")
        else:
            print(f"  {RED}✗{RESET} {file_path} (missing)")
            all_exist = False

    return all_exist


def test_imports():
    """Test if all modules can be imported."""
    print("\nTesting module imports...")

    sys.path.insert(0, str(Path('src').absolute()))

    modules = [
        ('src.utils.config', 'Config'),
        ('src.utils.exceptions', 'OSINTError'),
        ('src.analyzers.sentiment_analyzer', 'SentimentAnalyzer'),
        ('src.visualizers.charts', 'SentimentVisualizer'),
    ]

    all_imported = True
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  {GREEN}✓{RESET} {module_name}")
        except Exception as e:
            print(f"  {RED}✗{RESET} {module_name}: {str(e)}")
            all_imported = False

    return all_imported


def main():
    """Run all verification checks."""
    print_header("Social Media OSINT Analyzer - Setup Verification")

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("NLTK Data", check_nltk_data),
        ("Environment Configuration", check_env_file),
        ("Directory Structure", check_directory_structure),
        ("Source Files", check_source_files),
        ("Module Imports", test_imports),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"{RED}Error in {name}: {e}{RESET}")
            results.append((name, False))

    # Summary
    print_header("Verification Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{name:<30} {status}")

    print(f"\n{BLUE}Score: {passed}/{total}{RESET}")

    if passed == total:
        print(f"\n{GREEN}✓ All checks passed! You're ready to run the application.{RESET}")
        print(f"\n{BLUE}Run the application with:{RESET}")
        print(f"  {GREEN}./run.sh{RESET}")
        print(f"  or")
        print(f"  {GREEN}streamlit run src/app.py{RESET}")
        return 0
    else:
        print(f"\n{YELLOW}! Some checks failed. Please address the issues above.{RESET}")
        print(f"\n{BLUE}Common fixes:{RESET}")
        print(f"  • Install dependencies: {GREEN}pip install -r requirements.txt{RESET}")
        print(f"  • Create .env file: {GREEN}cp .env.example .env{RESET}")
        print(f"  • Download NLTK data: {GREEN}python -c 'import nltk; nltk.download(\"all\")''{RESET}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
