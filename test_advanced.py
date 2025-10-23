#!/usr/bin/env python3
"""
Advanced Testing: Real-world Sentiment Analysis Scenarios
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from analyzers.sentiment_analyzer import SentimentAnalyzer

print("=" * 70)
print("ADVANCED SENTIMENT ANALYSIS TESTING")
print("=" * 70)

analyzer = SentimentAnalyzer()

# Test various real-world scenarios
test_cases = [
    {
        "text": "I absolutely love this new feature! Best update ever!",
        "expected": "positive",
        "description": "Strong positive with exclamations"
    },
    {
        "text": "This is the worst product I've ever used. Complete waste of money.",
        "expected": "negative",
        "description": "Strong negative with superlatives"
    },
    {
        "text": "The product works as advertised. It does what it says.",
        "expected": "neutral",
        "description": "Factual statement"
    },
    {
        "text": "Great idea but terrible execution. Disappointed.",
        "expected": "negative",
        "description": "Mixed sentiment (overall negative)"
    },
    {
        "text": "Not bad. Could be better but it's okay for the price.",
        "expected": "neutral",
        "description": "Lukewarm sentiment"
    },
    {
        "text": "Amazing! Fantastic! Love it! Highly recommend!",
        "expected": "positive",
        "description": "Multiple positive words"
    },
    {
        "text": "Horrible, awful, terrible, worst experience ever!",
        "expected": "negative",
        "description": "Multiple negative words"
    },
    {
        "text": "The company released version 2.0 on Monday.",
        "expected": "neutral",
        "description": "Pure factual information"
    },
    {
        "text": "It's good but not great. Has some issues.",
        "expected": "neutral",
        "description": "Balanced mixed feelings"
    },
    {
        "text": "😊 Happy with this purchase! 👍",
        "expected": "positive",
        "description": "Text with emojis"
    }
]

print("\nTesting Sentiment Detection Accuracy")
print("-" * 70)

correct = 0
total = len(test_cases)

for i, test in enumerate(test_cases, 1):
    result = analyzer.analyze_text(test['text'])
    detected = result['sentiment']
    polarity = result['polarity']

    is_correct = detected == test['expected']
    if is_correct:
        correct += 1

    status = "✓" if is_correct else "✗"
    print(f"\n{status} Test {i}: {test['description']}")
    print(f"  Text: '{test['text'][:60]}...'")
    print(f"  Expected: {test['expected']}, Detected: {detected}")
    print(f"  Polarity: {polarity:.3f}, Subjectivity: {result['subjectivity']:.3f}")

accuracy = (correct / total) * 100
print("\n" + "=" * 70)
print(f"ACCURACY: {correct}/{total} ({accuracy:.1f}%)")
print("=" * 70)

# Test edge cases
print("\n\nEdge Cases Testing")
print("-" * 70)

edge_cases = [
    ("", "Empty string"),
    ("   ", "Whitespace only"),
    ("a", "Single character"),
    ("!!!", "Only punctuation"),
    ("The the the the", "Repeated words"),
    ("123456789", "Numbers only"),
    ("@#$%^&*()", "Special characters"),
]

print("\nTesting edge cases...")
for text, description in edge_cases:
    try:
        result = analyzer.analyze_text(text)
        print(f"✓ {description}: {result['sentiment']} (polarity: {result['polarity']:.3f})")
    except Exception as e:
        print(f"✗ {description}: Error - {e}")

# Test language variations
print("\n\nLanguage Variations")
print("-" * 70)

variations = [
    "Absolutely brilliant!!!",
    "AMAZING PRODUCT",
    "this is great",
    "ThIs Is WeIrD CaSiNg",
]

print("\nTesting text variations...")
for text in variations:
    result = analyzer.analyze_text(text)
    print(f"  '{text}' -> {result['sentiment']} (polarity: {result['polarity']:.3f})")

print("\n" + "=" * 70)
print("ADVANCED TESTING COMPLETE")
print("=" * 70)
