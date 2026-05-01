#!/usr/bin/env python3
"""
Product Review Analyzer
A comprehensive tool for analyzing product reviews and generating structured insights.
"""

import re
import json
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from dataclasses import dataclass
import argparse

@dataclass
class ReviewAnalysis:
    overall_summary: str
    sentiment_analysis: Dict[str, float]
    key_positives: List[str]
    key_negatives: List[str]
    feature_insights: Dict[str, Dict[str, str]]
    actionable_insights: List[str]
    customer_intents: Dict[str, int]
    trend_patterns: List[str]

class ProductReviewAnalyzer:
    def __init__(self):
        # Sentiment keywords
        self.positive_words = {
            'excellent', 'amazing', 'great', 'good', 'love', 'perfect', 'awesome', 
            'fantastic', 'wonderful', 'best', 'nice', 'happy', 'satisfied', 'pleased',
            'impressed', 'recommend', 'quality', 'fast', 'easy', 'beautiful', 'solid'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'hate', 'disappoint', 'waste', 'poor', 'worst',
            'broken', 'defective', 'useless', 'cheap', 'slow', 'difficult', 'ugly',
            'frustrated', 'annoyed', 'unhappy', 'dissatisfied', 'problem', 'issue'
        }
        
        # Feature keywords
        self.feature_keywords = {
            'quality': ['quality', 'build', 'material', 'construction', 'craftsmanship'],
            'price': ['price', 'cost', 'value', 'money', 'expensive', 'cheap', 'affordable'],
            'performance': ['performance', 'speed', 'fast', 'slow', 'responsive', 'power'],
            'design': ['design', 'look', 'appearance', 'style', 'aesthetic', 'color'],
            'durability': ['durable', 'sturdy', 'last', 'longevity', 'fragile', 'break']
        }
        
        # Intent patterns
        self.intent_patterns = {
            'repeat_purchase': ['buy again', 'would buy', 'purchase again', 'coming back'],
            'recommendation': ['recommend', 'tell friends', 'suggest', 'advise'],
            'use_cases': ['use for', 'perfect for', 'great for', 'using it to']
        }

    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """Analyze sentiment of a single review."""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        if positive_count > negative_count:
            return 'Positive', positive_count / (positive_count + negative_count + 1)
        elif negative_count > positive_count:
            return 'Negative', negative_count / (positive_count + negative_count + 1)
        else:
            return 'Neutral', 0.5

    def extract_key_points(self, reviews: List[str], sentiment_filter: str = None) -> List[str]:
        """Extract frequently mentioned points from reviews."""
        all_text = ' '.join(reviews).lower()
        sentences = re.split(r'[.!?]+', all_text)
        
        # Filter by sentiment if specified
        if sentiment_filter:
            filtered_sentences = []
            for sentence in sentences:
                sent, _ = self.analyze_sentiment(sentence)
                if sent == sentiment_filter:
                    filtered_sentences.append(sentence)
            sentences = filtered_sentences
        
        # Extract common phrases and keywords
        common_phrases = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Filter out very short fragments
                common_phrases.append(sentence)
        
        # Count frequency and return top points
        phrase_counts = Counter(common_phrases)
        return [phrase for phrase, count in phrase_counts.most_common(10)]

    def analyze_features(self, reviews: List[str]) -> Dict[str, Dict[str, str]]:
        """Analyze sentiment for specific features."""
        feature_analysis = {}
        
        for feature, keywords in self.feature_keywords.items():
            feature_reviews = []
            
            for review in reviews:
                review_lower = review.lower()
                if any(keyword in review_lower for keyword in keywords):
                    feature_reviews.append(review)
            
            if feature_reviews:
                sentiments = [self.analyze_sentiment(review)[0] for review in feature_reviews]
                sentiment_counts = Counter(sentiments)
                dominant_sentiment = sentiment_counts.most_common(1)[0][0]
                
                feature_analysis[feature] = {
                    'sentiment': dominant_sentiment,
                    'mentions': len(feature_reviews),
                    'breakdown': dict(sentiment_counts)
                }
        
        return feature_analysis

    def detect_intents(self, reviews: List[str]) -> Dict[str, int]:
        """Detect customer intent patterns."""
        intent_counts = defaultdict(int)
        
        for review in reviews:
            review_lower = review.lower()
            for intent, patterns in self.intent_patterns.items():
                if any(pattern in review_lower for pattern in patterns):
                    intent_counts[intent] += 1
        
        return dict(intent_counts)

    def identify_trends(self, reviews: List[str]) -> List[str]:
        """Identify recurring trends and patterns."""
        trends = []
        
        # Common trend patterns to look for
        trend_patterns = {
            'shipping_issues': ['shipping', 'delivery', 'packaging', 'arrived'],
            'customer_service': ['support', 'service', 'help', 'response'],
            'expectation_mismatch': ['expected', 'thought', 'surprised', 'different'],
            'usage_difficulty': ['hard to', 'difficult', 'confusing', 'complicated'],
            'value_perception': ['worth', 'value', 'price', 'cost']
        }
        
        for trend, keywords in trend_patterns.items():
            count = sum(1 for review in reviews 
                       if any(keyword in review.lower() for keyword in keywords))
            if count > len(reviews) * 0.1:  # If mentioned in >10% of reviews
                trends.append(f"{trend.replace('_', ' ').title()}: {count} mentions")
        
        return trends

    def generate_summary(self, reviews: List[str], sentiment_data: Dict[str, float]) -> str:
        """Generate overall summary."""
        total_reviews = len(reviews)
        dominant_sentiment = max(sentiment_data, key=sentiment_data.get)
        
        summary = f"Analysis of {total_reviews} product reviews shows {dominant_sentiment.lower()} customer sentiment. "
        
        if dominant_sentiment == 'Positive':
            summary += "Customers generally praise the product's quality and performance. "
        elif dominant_sentiment == 'Negative':
            summary += "Customers express significant concerns about various aspects of the product. "
        else:
            summary += "Customer opinions are mixed with balanced positive and negative feedback. "
        
        summary += f"The overall satisfaction rate is {sentiment_data.get('Positive', 0):.1f}%."
        
        return summary

    def generate_actionable_insights(self, negatives: List[str], features: Dict[str, Dict[str, str]]) -> List[str]:
        """Generate actionable insights based on analysis."""
        insights = []
        
        # Insights from negative feedback
        if negatives:
            insights.append("Address the most common complaints to improve customer satisfaction")
            insights.append("Focus on quality control and product reliability")
        
        # Insights from feature analysis
        for feature, data in features.items():
            if data['sentiment'] == 'Negative':
                insights.append(f"Improve {feature} aspects of the product")
            elif data['sentiment'] == 'Positive':
                insights.append(f"Maintain and enhance {feature} strengths")
        
        # General insights
        insights.append("Monitor customer feedback regularly for emerging issues")
        insights.append("Consider implementing customer suggestions for product improvements")
        
        return insights[:5]  # Return top 5 insights

    def analyze_reviews(self, reviews: List[str]) -> ReviewAnalysis:
        """Perform comprehensive analysis of product reviews."""
        # Sentiment analysis
        sentiments = [self.analyze_sentiment(review)[0] for review in reviews]
        sentiment_counts = Counter(sentiments)
        total_reviews = len(reviews)
        sentiment_percentages = {
            sentiment: (count / total_reviews) * 100 
            for sentiment, count in sentiment_counts.items()
        }
        
        # Extract key points
        positives = self.extract_key_points(reviews, 'Positive')
        negatives = self.extract_key_points(reviews, 'Negative')
        
        # Feature analysis
        feature_insights = self.analyze_features(reviews)
        
        # Customer intents
        customer_intents = self.detect_intents(reviews)
        
        # Trend patterns
        trends = self.identify_trends(reviews)
        
        # Generate summary and insights
        overall_summary = self.generate_summary(reviews, sentiment_percentages)
        actionable_insights = self.generate_actionable_insights(negatives, feature_insights)
        
        return ReviewAnalysis(
            overall_summary=overall_summary,
            sentiment_analysis=sentiment_percentages,
            key_positives=positives[:5],
            key_negatives=negatives[:5],
            feature_insights=feature_insights,
            actionable_insights=actionable_insights,
            customer_intents=customer_intents,
            trend_patterns=trends
        )

    def format_report(self, analysis: ReviewAnalysis) -> str:
        """Format analysis results into a structured report."""
        report = []
        
        report.append("OVERALL SUMMARY:")
        report.append(f"- {analysis.overall_summary}\n")
        
        report.append("SENTIMENT ANALYSIS:")
        for sentiment, percentage in analysis.sentiment_analysis.items():
            report.append(f"- {sentiment}: {percentage:.1f}%")
        report.append("")
        
        report.append("KEY POSITIVES:")
        for positive in analysis.key_positives:
            report.append(f"- {positive}")
        report.append("")
        
        report.append("KEY NEGATIVES:")
        for negative in analysis.key_negatives:
            report.append(f"- {negative}")
        report.append("")
        
        report.append("FEATURE-WISE INSIGHTS:")
        for feature, data in analysis.feature_insights.items():
            report.append(f"- {feature.title()}: {data['sentiment']} ({data['mentions']} mentions)")
        report.append("")
        
        report.append("ACTIONABLE INSIGHTS:")
        for insight in analysis.actionable_insights:
            report.append(f"- {insight}")
        report.append("")
        
        report.append("CUSTOMER INTENT SIGNALS:")
        for intent, count in analysis.customer_intents.items():
            report.append(f"- {intent.replace('_', ' ').title()}: {count} mentions")
        report.append("")
        
        report.append("TREND PATTERNS:")
        for trend in analysis.trend_patterns:
            report.append(f"- {trend}")
        
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='Analyze product reviews')
    parser.add_argument('--file', help='File containing reviews (one per line)')
    parser.add_argument('--text', help='Single review text to analyze')
    parser.add_argument('--output', help='Output file for results')
    
    args = parser.parse_args()
    
    analyzer = ProductReviewAnalyzer()
    
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            reviews = [line.strip() for line in f if line.strip()]
    elif args.text:
        reviews = [args.text]
    else:
        # Example reviews for demonstration
        reviews = [
            "This product is amazing! Great quality and fast shipping.",
            "I love the design but it's a bit expensive for what you get.",
            "Terrible experience, the product broke after one week.",
            "Good value for money, works as expected.",
            "Would definitely buy again and recommend to friends.",
            "The customer service was helpful when I had issues.",
            "Packaging was damaged but the product itself is fine.",
            "Excellent build quality, worth every penny!",
            "Not satisfied with the performance, it's slower than advertised.",
            "Beautiful design and solid construction, very happy with purchase."
        ]
    
    analysis = analyzer.analyze_reviews(reviews)
    report = analyzer.format_report(analysis)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)

if __name__ == "__main__":
    main()
