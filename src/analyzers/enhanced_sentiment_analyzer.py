"""
Enhanced Sentiment Analysis with detailed explanations.
Uses VADER (better for social media) and provides reasoning for sentiment scores.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from typing import List, Dict, Tuple
import re
from collections import Counter


class EnhancedSentimentAnalyzer:
    """
    Advanced sentiment analyzer that provides:
    - VADER scores (better for social media text)
    - Detailed explanations of WHY text is positive/negative
    - Word-level sentiment breakdown
    - Aspect-based analysis
    """

    def __init__(self):
        """Initialize the enhanced sentiment analyzer."""
        self.vader = SentimentIntensityAnalyzer()

        # Enhanced emotion lexicons
        self.strong_positive = {
            'love', 'amazing', 'excellent', 'fantastic', 'wonderful', 'brilliant',
            'awesome', 'great', 'perfect', 'outstanding', 'superb', 'incredible',
            'magnificent', 'spectacular', 'phenomenal', 'exceptional', 'fabulous'
        }

        self.strong_negative = {
            'hate', 'terrible', 'awful', 'horrible', 'worst', 'disgusting',
            'pathetic', 'useless', 'garbage', 'trash', 'disappointing',
            'disaster', 'nightmare', 'dreadful', 'appalling', 'atrocious'
        }

        self.positive_words = {
            'good', 'nice', 'fine', 'ok', 'decent', 'solid', 'happy', 'pleased',
            'satisfied', 'enjoyable', 'fun', 'interesting', 'cool', 'helpful',
            'useful', 'effective', 'efficient', 'reliable', 'quality'
        }

        self.negative_words = {
            'bad', 'poor', 'weak', 'disappointing', 'frustrating', 'annoying',
            'sad', 'unhappy', 'difficult', 'hard', 'confusing', 'complicated',
            'slow', 'expensive', 'broken', 'buggy', 'error', 'issue', 'problem'
        }

        # Negations that flip sentiment
        self.negations = {
            'not', 'no', 'never', 'nothing', 'neither', 'nobody', 'nowhere',
            'none', "don't", "doesn't", "didn't", "won't", "wouldn't", "shouldn't",
            "can't", "cannot", "couldn't"
        }

        # Intensifiers that amplify sentiment
        self.intensifiers = {
            'very', 'extremely', 'incredibly', 'absolutely', 'completely',
            'totally', 'really', 'quite', 'fairly', 'pretty', 'highly',
            'exceptionally', 'remarkably', 'extraordinarily'
        }

    def analyze_text(self, text: str) -> Dict:
        """
        Perform comprehensive sentiment analysis with detailed explanations.

        Args:
            text: Input text to analyze

        Returns:
            Dictionary with scores, classification, and detailed explanations
        """
        if not text or not text.strip():
            return self._empty_result()

        # Get VADER scores
        vader_scores = self.vader.polarity_scores(text)

        # Get TextBlob for comparison
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity

        # Analyze text components
        words = self._tokenize(text.lower())
        sentences = self._split_sentences(text)

        # Find sentiment-driving words
        positive_indicators = self._find_sentiment_words(words, 'positive')
        negative_indicators = self._find_sentiment_words(words, 'negative')

        # Detect modifiers
        negations_found = self._find_negations(words)
        intensifiers_found = self._find_intensifiers(words)

        # Sentence-level analysis
        sentence_sentiments = self._analyze_sentences(sentences)

        # Determine overall sentiment using VADER (better for social media)
        compound = vader_scores['compound']

        if compound >= 0.05:
            sentiment = 'positive'
            confidence = 'high' if compound >= 0.5 else 'moderate' if compound >= 0.25 else 'low'
        elif compound <= -0.05:
            sentiment = 'negative'
            confidence = 'high' if compound <= -0.5 else 'moderate' if compound <= -0.25 else 'low'
        else:
            sentiment = 'neutral'
            confidence = 'moderate'

        # Generate detailed explanation
        explanation = self._generate_explanation(
            sentiment=sentiment,
            compound=compound,
            positive_indicators=positive_indicators,
            negative_indicators=negative_indicators,
            negations_found=negations_found,
            intensifiers_found=intensifiers_found,
            sentence_sentiments=sentence_sentiments
        )

        return {
            # VADER scores (primary)
            'vader_compound': round(compound, 3),
            'vader_positive': round(vader_scores['pos'], 3),
            'vader_negative': round(vader_scores['neg'], 3),
            'vader_neutral': round(vader_scores['neu'], 3),

            # TextBlob scores (secondary)
            'textblob_polarity': round(textblob_polarity, 3),
            'textblob_subjectivity': round(textblob_subjectivity, 3),

            # Overall classification
            'sentiment': sentiment,
            'confidence': confidence,

            # Detailed breakdown
            'positive_words': positive_indicators,
            'negative_words': negative_indicators,
            'negations': negations_found,
            'intensifiers': intensifiers_found,
            'sentence_breakdown': sentence_sentiments,

            # Explanation
            'explanation': explanation,
            'reasoning': self._generate_reasoning(
                sentiment, positive_indicators, negative_indicators,
                negations_found, intensifiers_found
            )
        }

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return re.findall(r'\b\w+\b', text.lower())

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _find_sentiment_words(self, words: List[str], sentiment_type: str) -> List[Tuple[str, str]]:
        """Find words that indicate sentiment and their strength."""
        indicators = []

        if sentiment_type == 'positive':
            for word in words:
                if word in self.strong_positive:
                    indicators.append((word, 'strong'))
                elif word in self.positive_words:
                    indicators.append((word, 'moderate'))
        else:  # negative
            for word in words:
                if word in self.strong_negative:
                    indicators.append((word, 'strong'))
                elif word in self.negative_words:
                    indicators.append((word, 'moderate'))

        return indicators

    def _find_negations(self, words: List[str]) -> List[str]:
        """Find negation words."""
        return [w for w in words if w in self.negations]

    def _find_intensifiers(self, words: List[str]) -> List[str]:
        """Find intensifier words."""
        return [w for w in words if w in self.intensifiers]

    def _analyze_sentences(self, sentences: List[str]) -> List[Dict]:
        """Analyze sentiment of individual sentences."""
        results = []
        for sentence in sentences[:5]:  # Limit to first 5 sentences
            if not sentence:
                continue

            vader_scores = self.vader.polarity_scores(sentence)
            compound = vader_scores['compound']

            if compound >= 0.05:
                sent_sentiment = 'positive'
            elif compound <= -0.05:
                sent_sentiment = 'negative'
            else:
                sent_sentiment = 'neutral'

            results.append({
                'text': sentence[:100] + '...' if len(sentence) > 100 else sentence,
                'sentiment': sent_sentiment,
                'score': round(compound, 3)
            })

        return results

    def _generate_explanation(
        self,
        sentiment: str,
        compound: float,
        positive_indicators: List[Tuple[str, str]],
        negative_indicators: List[Tuple[str, str]],
        negations_found: List[str],
        intensifiers_found: List[str],
        sentence_sentiments: List[Dict]
    ) -> str:
        """Generate human-readable explanation of sentiment."""

        explanation_parts = []

        # Overall sentiment
        if sentiment == 'positive':
            explanation_parts.append(f"This text is **POSITIVE** (score: {compound:.3f}).")
        elif sentiment == 'negative':
            explanation_parts.append(f"This text is **NEGATIVE** (score: {compound:.3f}).")
        else:
            explanation_parts.append(f"This text is **NEUTRAL** (score: {compound:.3f}).")

        # Why positive?
        if positive_indicators:
            strong_pos = [w for w, s in positive_indicators if s == 'strong']
            moderate_pos = [w for w, s in positive_indicators if s == 'moderate']

            if strong_pos:
                explanation_parts.append(
                    f"Strong positive words found: {', '.join(set(strong_pos))}."
                )
            if moderate_pos:
                explanation_parts.append(
                    f"Positive words: {', '.join(set(moderate_pos))}."
                )

        # Why negative?
        if negative_indicators:
            strong_neg = [w for w, s in negative_indicators if s == 'strong']
            moderate_neg = [w for w, s in negative_indicators if s == 'moderate']

            if strong_neg:
                explanation_parts.append(
                    f"Strong negative words found: {', '.join(set(strong_neg))}."
                )
            if moderate_neg:
                explanation_parts.append(
                    f"Negative words: {', '.join(set(moderate_neg))}."
                )

        # Modifiers
        if negations_found:
            explanation_parts.append(
                f"Negations detected ({', '.join(set(negations_found))}) which may flip sentiment."
            )

        if intensifiers_found:
            explanation_parts.append(
                f"Intensifiers found ({', '.join(set(intensifiers_found))}) which amplify sentiment."
            )

        # Sentence breakdown
        if len(sentence_sentiments) > 1:
            pos_sentences = sum(1 for s in sentence_sentiments if s['sentiment'] == 'positive')
            neg_sentences = sum(1 for s in sentence_sentiments if s['sentiment'] == 'negative')

            if pos_sentences > neg_sentences:
                explanation_parts.append(
                    f"Most sentences ({pos_sentences}/{len(sentence_sentiments)}) are positive."
                )
            elif neg_sentences > pos_sentences:
                explanation_parts.append(
                    f"Most sentences ({neg_sentences}/{len(sentence_sentiments)}) are negative."
                )

        return " ".join(explanation_parts)

    def _generate_reasoning(
        self,
        sentiment: str,
        positive_indicators: List[Tuple[str, str]],
        negative_indicators: List[Tuple[str, str]],
        negations: List[str],
        intensifiers: List[str]
    ) -> List[str]:
        """Generate bullet-point reasoning for the sentiment."""

        reasons = []

        if sentiment == 'positive':
            if positive_indicators:
                reasons.append(f"Contains {len(positive_indicators)} positive indicators")
            if intensifiers:
                reasons.append(f"Uses {len(intensifiers)} intensifiers to strengthen tone")
            if not negative_indicators:
                reasons.append("No significant negative language detected")

        elif sentiment == 'negative':
            if negative_indicators:
                reasons.append(f"Contains {len(negative_indicators)} negative indicators")
            if intensifiers:
                reasons.append(f"Uses {len(intensifiers)} intensifiers to strengthen criticism")
            if not positive_indicators:
                reasons.append("No significant positive language detected")

        else:  # neutral
            reasons.append("Balanced or factual language")
            if not positive_indicators and not negative_indicators:
                reasons.append("Lacks strong emotional indicators")

        if negations:
            reasons.append(f"Contains {len(negations)} negations that may affect meaning")

        return reasons

    def _empty_result(self) -> Dict:
        """Return empty/neutral result for empty text."""
        return {
            'vader_compound': 0.0,
            'vader_positive': 0.0,
            'vader_negative': 0.0,
            'vader_neutral': 1.0,
            'textblob_polarity': 0.0,
            'textblob_subjectivity': 0.0,
            'sentiment': 'neutral',
            'confidence': 'low',
            'positive_words': [],
            'negative_words': [],
            'negations': [],
            'intensifiers': [],
            'sentence_breakdown': [],
            'explanation': 'Empty or invalid text.',
            'reasoning': ['No content to analyze']
        }

    def analyze_posts(self, posts: List[Dict]) -> List[Dict]:
        """Analyze sentiment for multiple posts."""
        analyzed_posts = []

        for post in posts:
            text = post.get('full_text') or post.get('text', '')
            analysis = self.analyze_text(text)

            post_copy = post.copy()
            post_copy['sentiment_analysis'] = analysis
            analyzed_posts.append(post_copy)

        return analyzed_posts

    def get_sentiment_distribution(self, posts: List[Dict]) -> Dict:
        """Get distribution of sentiments across posts."""
        if not posts:
            return {
                'total': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'positive_pct': 0.0,
                'negative_pct': 0.0,
                'neutral_pct': 0.0
            }

        sentiments = [
            post.get('sentiment_analysis', {}).get('sentiment', 'neutral')
            for post in posts
        ]

        sentiment_counts = Counter(sentiments)
        total = len(posts)

        return {
            'total': total,
            'positive': sentiment_counts.get('positive', 0),
            'negative': sentiment_counts.get('negative', 0),
            'neutral': sentiment_counts.get('neutral', 0),
            'positive_pct': round((sentiment_counts.get('positive', 0) / total) * 100, 2),
            'negative_pct': round((sentiment_counts.get('negative', 0) / total) * 100, 2),
            'neutral_pct': round((sentiment_counts.get('neutral', 0) / total) * 100, 2)
        }
