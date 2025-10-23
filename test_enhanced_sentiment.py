#!/usr/bin/env python3
"""
Test Enhanced Sentiment Analyzer with Explanations
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from analyzers.enhanced_sentiment_analyzer import EnhancedSentimentAnalyzer

print("=" * 80)
print("ENHANCED SENTIMENT ANALYSIS TEST")
print("=" * 80)

analyzer = EnhancedSentimentAnalyzer()

# Test cases with varying complexity
test_cases = [
    {
        "text": "I absolutely love this product! It's amazing and works perfectly!",
        "label": "Strong Positive"
    },
    {
        "text": "This is the worst thing I've ever bought. Complete waste of money. Terrible quality.",
        "label": "Strong Negative"
    },
    {
        "text": "Not bad, but not great either. It's okay for the price.",
        "label": "Mixed/Neutral (with negations)"
    },
    {
        "text": "The app crashes constantly and the customer service is horrible. Very disappointing experience.",
        "label": "Negative with Intensifier"
    },
    {
        "text": "It's not terrible, but I wouldn't say it's good either.",
        "label": "Negated Terms"
    },
    {
        "text": "Great idea, but the execution is terrible. I really wanted to like it.",
        "label": "Mixed Sentiment"
    },
    {
        "text": "The company announced quarterly results yesterday.",
        "label": "Neutral/Factual"
    },
    {
        "text": "Absolutely fantastic! The best purchase I've made in years! Highly recommend!",
        "label": "Very Strong Positive"
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"TEST {i}: {test['label']}")
    print(f"{'='*80}")
    print(f"\nText: \"{test['text']}\"")
    print(f"\n{'-'*80}")

    result = analyzer.analyze_text(test['text'])

    # Main scores
    print(f"\n📊 SCORES:")
    print(f"  VADER Compound: {result['vader_compound']:.3f} "
          f"(Positive: {result['vader_positive']:.3f}, "
          f"Negative: {result['vader_negative']:.3f}, "
          f"Neutral: {result['vader_neutral']:.3f})")
    print(f"  TextBlob Polarity: {result['textblob_polarity']:.3f}")
    print(f"  TextBlob Subjectivity: {result['textblob_subjectivity']:.3f}")

    # Classification
    print(f"\n🎯 CLASSIFICATION:")
    print(f"  Sentiment: {result['sentiment'].upper()}")
    print(f"  Confidence: {result['confidence'].upper()}")

    # Word breakdown
    if result['positive_words']:
        print(f"\n✅ POSITIVE INDICATORS:")
        for word, strength in result['positive_words']:
            print(f"  • '{word}' ({strength})")

    if result['negative_words']:
        print(f"\n❌ NEGATIVE INDICATORS:")
        for word, strength in result['negative_words']:
            print(f"  • '{word}' ({strength})")

    if result['negations']:
        print(f"\n🔄 NEGATIONS FOUND:")
        print(f"  {', '.join(result['negations'])}")

    if result['intensifiers']:
        print(f"\n💪 INTENSIFIERS FOUND:")
        print(f"  {', '.join(result['intensifiers'])}")

    # Explanation
    print(f"\n📝 EXPLANATION:")
    print(f"  {result['explanation']}")

    # Reasoning
    print(f"\n💡 REASONING:")
    for reason in result['reasoning']:
        print(f"  • {reason}")

    # Sentence breakdown
    if result['sentence_breakdown']:
        print(f"\n📄 SENTENCE BREAKDOWN:")
        for j, sent in enumerate(result['sentence_breakdown'], 1):
            emoji = "✅" if sent['sentiment'] == 'positive' else "❌" if sent['sentiment'] == 'negative' else "⚪"
            print(f"  {j}. [{emoji} {sent['sentiment'].upper()}] ({sent['score']:+.3f})")
            print(f"     \"{sent['text']}\"")

print(f"\n{'='*80}")
print("TEST COMPLETE - Enhanced Sentiment Analysis with Explanations")
print(f"{'='*80}")
print("\n✅ Key Improvements:")
print("  • Uses VADER (better for social media)")
print("  • Shows WHY text is positive/negative")
print("  • Word-level sentiment breakdown")
print("  • Detects negations and intensifiers")
print("  • Sentence-by-sentence analysis")
print("  • Detailed explanations and reasoning")
