#!/usr/bin/env python3
"""
Validate that Streamlit app can start without errors
"""

import subprocess
import sys
import time
import signal

print("="*70)
print("STREAMLIT APP VALIDATION")
print("="*70)

print("\n1. Testing Python imports...")
# Test imports
try:
    sys.path.insert(0, 'src')
    from collectors import RedditCollector, TwitterCollector, NewsCollector
    from analyzers import SentimentAnalyzer
    from visualizers import SentimentVisualizer
    from utils.config import Config
    print("   ✓ All imports successful")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

print("\n2. Checking Streamlit installation...")
try:
    import streamlit
    print(f"   ✓ Streamlit {streamlit.__version__} installed")
except ImportError:
    print("   ✗ Streamlit not installed")
    sys.exit(1)

print("\n3. Testing app startup (will run for 5 seconds)...")
print("   Starting Streamlit server...")

# Start Streamlit in background
proc = subprocess.Popen(
    ['streamlit', 'run', 'src/app.py', '--server.headless=true', '--server.port=8502'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait a bit for startup
time.sleep(5)

# Check if process is still running
if proc.poll() is None:
    print("   ✓ Streamlit server started successfully")
    print("   ✓ No import errors detected")

    # Kill the process
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()

    print("\n" + "="*70)
    print("✅ VALIDATION SUCCESSFUL")
    print("="*70)
    print("\nThe app is ready to run!")
    print("\nTo start the dashboard:")
    print("  ./run.sh")
    print("  or")
    print("  streamlit run src/app.py")
else:
    # Process died, check error
    stdout, stderr = proc.communicate()
    print("   ✗ Streamlit failed to start")
    print("\nError output:")
    print(stderr)
    sys.exit(1)
