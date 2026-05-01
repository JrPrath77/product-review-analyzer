"""
Product Review Analyzer - Core NLP Logic
Handles sentiment analysis, summarization, and insight generation
"""

import re
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from collections import Counter
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data (only once)
for _pkg in ['punkt', 'punkt_tab', 'vader_lexicon', 'stopwords']:
    try:
        nltk.download(_pkg, quiet=True)
    except Exception:
        pass

class ReviewAnalyzer:
    """Main class for analyzing product reviews"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
        # Feature keywords for aspect-based analysis
        self.feature_keywords = {
            'quality': ['quality', 'build', 'material', 'durable', 'sturdy', 'well-made', 'cheap', 'flimsy'],
            'price': ['price', 'cost', 'expensive', 'cheap', 'affordable', 'value', 'worth', 'budget'],
            'performance': ['performance', 'speed', 'fast', 'slow', 'efficient', 'powerful', 'responsive'],
            'design': ['design', 'look', 'appearance', 'style', 'aesthetic', 'color', 'size', 'shape'],
            'usability': ['easy', 'difficult', 'simple', 'complex', 'user-friendly', 'intuitive', 'confusing']
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not isinstance(text, str):
            text = str(text)
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text.lower()
    
    def get_sentiment(self, text: str) -> Tuple[str, float]:
        """Analyze sentiment using VADER"""
        # VADER uses punctuation, caps, and exclamation marks — do NOT clean before scoring
        scores = self.sentiment_analyzer.polarity_scores(text if isinstance(text, str) else str(text))
        
        compound_score = scores['compound']
        
        if compound_score >= 0.05:
            sentiment = 'Positive'
        elif compound_score <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return sentiment, compound_score
    
    def extract_key_phrases(self, texts: List[str], top_n: int = 10) -> List[str]:
        """Extract key phrases using n-grams"""
        all_words = []
        
        for text in texts:
            cleaned = self.clean_text(text)
            words = word_tokenize(cleaned)
            words = [word for word in words if word not in self.stop_words and len(word) > 2]
            all_words.extend(words)
        
        # Get bigrams and unigrams
        bigrams = list(ngrams(all_words, 2))
        bigram_strings = [' '.join(bigram) for bigram in bigrams]
        
        # Count frequencies
        word_freq = Counter(all_words)
        bigram_freq = Counter(bigram_strings)
        
        # Get top phrases
        top_words = [f"{word} ({count})" for word, count in word_freq.most_common(top_n//2)]
        top_bigrams = [f"{bigram} ({count})" for bigram, count in bigram_freq.most_common(top_n//2)]
        
        return top_words + top_bigrams
    
    def aspect_based_sentiment(self, texts: List[str]) -> Dict[str, Dict[str, float]]:
        """Perform aspect-based sentiment analysis"""
        aspect_sentiments = {aspect: {'Positive': 0, 'Negative': 0, 'Neutral': 0} 
                            for aspect in self.feature_keywords.keys()}
        
        for text in texts:
            sentiment, _ = self.get_sentiment(text)
            cleaned = self.clean_text(text)
            
            for aspect, keywords in self.feature_keywords.items():
                if any(keyword in cleaned for keyword in keywords):
                    aspect_sentiments[aspect][sentiment] += 1
        
        # Convert to percentages
        for aspect in aspect_sentiments:
            total = sum(aspect_sentiments[aspect].values())
            if total > 0:
                for sentiment in aspect_sentiments[aspect]:
                    aspect_sentiments[aspect][sentiment] = round(
                        (aspect_sentiments[aspect][sentiment] / total) * 100, 1
                    )
        
        return aspect_sentiments
    
    def generate_summary(self, texts: List[str]) -> str:
        """Generate a simple extractive summary"""
        if not texts:
            return "No reviews available for analysis."
        
        # Get sentence scores based on sentiment and length
        sentences = []
        for text in texts:
            sentences.extend(sent_tokenize(text))
        
        if len(sentences) <= 3:
            return ' '.join(sentences)
        
        # Score sentences
        sentence_scores = []
        for sentence in sentences:
            _, score = self.get_sentiment(sentence)
            length_score = min(len(sentence.split()) / 10, 1)  # Prefer medium-length sentences
            combined_score = abs(score) * 0.7 + length_score * 0.3
            sentence_scores.append((sentence, combined_score))
        
        # Get top 3 sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in sentence_scores[:3]]
        
        return ' '.join(top_sentences)
    
    def extract_positives_negatives(self, texts: List[str]) -> Tuple[List[str], List[str]]:
        """Extract key positive and negative points"""
        positive_points = []
        negative_points = []
        
        for text in texts:
            sentiment, score = self.get_sentiment(text)
            
            if sentiment == 'Positive' and score > 0.3:
                # Extract positive phrases
                cleaned = self.clean_text(text)
                sentences = sent_tokenize(text)
                for sentence in sentences:
                    _, sent_score = self.get_sentiment(sentence)
                    if sent_score > 0.3:
                        positive_points.append(sentence.strip())
                        break
            
            elif sentiment == 'Negative' and score < -0.3:
                # Extract negative phrases
                cleaned = self.clean_text(text)
                sentences = sent_tokenize(text)
                for sentence in sentences:
                    _, sent_score = self.get_sentiment(sentence)
                    if sent_score < -0.3:
                        negative_points.append(sentence.strip())
                        break
        
        return positive_points[:5], negative_points[:5]  # Return top 5 each
    
    def detect_fake_reviews(self, texts: List[str]) -> Dict[str, int]:
        """Basic fake review detection using heuristics"""
        fake_indicators = {
            'excessive_capitalization': 0,
            'repetitive_text': 0,
            'suspicious_keywords': 0,
            'unnatural_length': 0
        }
        
        suspicious_keywords = ['best ever', 'perfect', 'amazing', 'incredible', 'life changing', 
                              'worst ever', 'terrible', 'horrible', 'disaster']
        
        for text in texts:
            # Check for excessive capitalization
            if len(text) > 0 and sum(1 for c in text if c.isupper()) / len(text) > 0.3:
                fake_indicators['excessive_capitalization'] += 1

            # Check for repetitive text (duplicate words > 40% of content)
            words = text.lower().split()
            if len(words) > 3 and len(set(words)) / len(words) < 0.6:
                fake_indicators['repetitive_text'] += 1

            # Check for suspicious keywords
            cleaned = self.clean_text(text)
            if any(keyword in cleaned for keyword in suspicious_keywords):
                fake_indicators['suspicious_keywords'] += 1

            # Check for unnatural length (too short or too long)
            if len(text.split()) < 3 or len(text.split()) > 100:
                fake_indicators['unnatural_length'] += 1
        
        return fake_indicators
    
    def generate_actionable_suggestions(self, texts: List[str], aspect_sentiments: Dict) -> List[str]:
        """Generate actionable suggestions based on analysis"""
        suggestions = []
        
        # Analyze aspect sentiments
        for aspect, sentiments in aspect_sentiments.items():
            if sentiments['Negative'] > 40:
                if aspect == 'quality':
                    suggestions.append("Focus on improving product quality and materials")
                elif aspect == 'price':
                    suggestions.append("Consider pricing strategy or value proposition improvements")
                elif aspect == 'performance':
                    suggestions.append("Enhance product performance and speed")
                elif aspect == 'design':
                    suggestions.append("Revise product design and aesthetics")
                elif aspect == 'usability':
                    suggestions.append("Improve user experience and ease of use")
            
            elif sentiments['Positive'] > 70:
                if aspect == 'quality':
                    suggestions.append("Highlight superior quality in marketing materials")
                elif aspect == 'price':
                    suggestions.append("Emphasize competitive pricing in promotions")
                elif aspect == 'performance':
                    suggestions.append("Showcase performance capabilities in advertising")
        
        # General suggestions based on overall sentiment
        overall_sentiments = [self.get_sentiment(text)[0] for text in texts]
        positive_ratio = overall_sentiments.count('Positive') / len(overall_sentiments)
        
        if positive_ratio > 0.8:
            suggestions.append("Leverage high customer satisfaction in testimonials")
        elif positive_ratio < 0.4:
            suggestions.append("Address customer concerns promptly to improve satisfaction")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def analyze_reviews(self, reviews_df: pd.DataFrame) -> Dict:
        """Main analysis function"""
        if 'review' not in reviews_df.columns:
            raise ValueError("DataFrame must have a 'review' column")
        
        texts = reviews_df['review'].dropna().tolist()
        
        if not texts:
            return {"error": "No valid reviews found"}
        
        # Perform all analyses (cache repeated computations)
        pos_neg = self.extract_positives_negatives(texts)
        aspect_sentiments = self.aspect_based_sentiment(texts)
        results = {
            'summary': self.generate_summary(texts),
            'sentiment_distribution': self.get_overall_sentiment_distribution(texts),
            'key_phrases': self.extract_key_phrases(texts),
            'positives': pos_neg[0],
            'negatives': pos_neg[1],
            'aspect_sentiments': aspect_sentiments,
            'fake_review_indicators': self.detect_fake_reviews(texts),
            'actionable_suggestions': self.generate_actionable_suggestions(texts, aspect_sentiments),
            'total_reviews': len(texts)
        }
        
        return results
    
    def get_overall_sentiment_distribution(self, texts: List[str]) -> Dict[str, float]:
        """Get overall sentiment distribution with percentages"""
        sentiments = [self.get_sentiment(text)[0] for text in texts]
        total = len(sentiments)
        
        distribution = {
            'Positive': round((sentiments.count('Positive') / total) * 100, 1),
            'Negative': round((sentiments.count('Negative') / total) * 100, 1),
            'Neutral': round((sentiments.count('Neutral') / total) * 100, 1)
        }
        
        return distribution
