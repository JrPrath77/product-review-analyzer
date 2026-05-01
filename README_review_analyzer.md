# Product Review Analyzer

A comprehensive Python tool for analyzing product reviews and generating structured insights with sentiment analysis, feature-wise breakdowns, and actionable recommendations.

## Features

- **Sentiment Analysis**: Automatic classification of reviews as Positive, Negative, or Neutral
- **Feature-wise Insights**: Analysis of specific product aspects (Quality, Price, Performance, Design, Durability)
- **Key Points Extraction**: Identifies most frequently mentioned positives and negatives
- **Customer Intent Detection**: Recognizes patterns like repeat purchase likelihood and recommendations
- **Trend Identification**: Detects recurring issues and emerging patterns
- **Actionable Insights**: Generates specific recommendations for improvement

## Installation

No external dependencies required - uses Python standard library only.

```bash
python product_review_analyzer.py
```

## Usage

### Command Line Options

```bash
# Analyze reviews from a file (one review per line)
python product_review_analyzer.py --file reviews.txt

# Analyze a single review
python product_review_analyzer.py --text "This product is amazing!"

# Save results to a file
python product_review_analyzer.py --file reviews.txt --output report.txt

# Run with example data
python product_review_analyzer.py
```

### Input Format

Reviews should be provided as:
- Text file with one review per line
- Direct text input via command line
- List of strings when using programmatically

### Output Format

The tool generates a structured report with:

📌 **Overall Summary**: Concise 3-5 sentence summary of customer sentiment

😊 **Sentiment Analysis**: Percentage breakdown (e.g., 70% Positive, 20% Negative, 10% Neutral)

⭐ **Key Positives**: Most frequently mentioned strengths grouped by similarity

⚠️ **Key Negatives**: Common complaints and critical issues

🔍 **Feature-wise Insights**: Sentiment analysis for Quality, Price, Performance, Design, Durability

💡 **Actionable Insights**: Specific improvement suggestions based on negative feedback

🧠 **Customer Intent Signals**: Patterns like repeat purchase likelihood and recommendations

📊 **Trend Patterns**: Recurring trends and emerging issues

## Example Output

```
📌 Overall Summary:
- Analysis of 10 product reviews shows positive customer sentiment. Customers generally praise the product's quality and performance. The overall satisfaction rate is 60.0%.

😊 Sentiment Analysis:
- Positive: 60.0%
- Negative: 30.0%
- Neutral: 10.0%

⭐ Key Positives:
- this product is amazing
- great quality and fast shipping
- excellent build quality
- beautiful design and solid construction
- good value for money

⚠️ Key Negatives:
- terrible experience
- not satisfied with the performance
- it's slower than advertised
- the product broke after one week
- packaging was damaged

🔍 Feature-wise Insights:
- Quality: Positive (3 mentions)
- Price: Positive (2 mentions)
- Performance: Negative (2 mentions)
- Design: Positive (2 mentions)

💡 Actionable Insights:
- Address the most common complaints to improve customer satisfaction
- Focus on quality control and product reliability
- Improve performance aspects of the product
- Maintain and enhance price strengths
- Monitor customer feedback regularly for emerging issues

🧠 Customer Intent Signals:
- Repeat Purchase: 1 mentions
- Recommendation: 1 mentions

📊 Trend Patterns:
- Shipping Issues: 2 mentions
- Expectation Mismatch: 2 mentions
```

## Programmatic Usage

```python
from product_review_analyzer import ProductReviewAnalyzer

# Initialize analyzer
analyzer = ProductReviewAnalyzer()

# Analyze reviews
reviews = [
    "Great product, excellent quality!",
    "Not worth the price, disappointing.",
    "Would buy again, highly recommend."
]

analysis = analyzer.analyze_reviews(reviews)
report = analyzer.format_report(analysis)
print(report)
```

## Customization

The analyzer can be customized by modifying:

- **Sentiment keywords**: Add to `positive_words` and `negative_words` sets
- **Feature keywords**: Modify `feature_keywords` dictionary
- **Intent patterns**: Update `intent_patterns` dictionary
- **Trend patterns**: Adjust `trend_patterns` in `identify_trends()` method

## Limitations

- Uses keyword-based sentiment analysis (not ML-based)
- Works best with English language reviews
- Accuracy depends on keyword coverage
- May miss nuanced sentiments or sarcasm

## Contributing

Feel free to extend the tool with:
- Machine learning sentiment analysis
- Multi-language support
- Additional feature categories
- Visualization capabilities
- Integration with review APIs
