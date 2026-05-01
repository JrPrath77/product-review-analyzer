"""
Utility functions for Product Review Analyzer
Helper functions for data processing, file operations, and visualization
"""

import pandas as pd
import io
import re
from typing import List, Dict, Union
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def validate_file_upload(uploaded_file) -> Union[pd.DataFrame, None]:
    """
    Validate and process uploaded file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        DataFrame with reviews or None if invalid
    """
    if uploaded_file is None:
        return None
    
    try:
        # Read file based on extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        elif file_extension == 'txt':
            # For text files, create DataFrame with each line as a review
            content = uploaded_file.read().decode('utf-8')
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            df = pd.DataFrame({'review': lines})
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Standardize column names
        df.columns = df.columns.str.lower()
        
        # Find the review column
        review_column = None
        for col in df.columns:
            if 'review' in col or 'text' in col or 'comment' in col or 'feedback' in col:
                review_column = col
                break
        
        if review_column is None:
            # If no obvious review column, use the first text column
            for col in df.columns:
                if df[col].dtype == 'object':
                    review_column = col
                    break
        
        if review_column is None:
            raise ValueError("No review column found in the uploaded file")
        
        # Rename to standard 'review' column
        df = df.rename(columns={review_column: 'review'})
        
        # Clean the review column
        df['review'] = df['review'].astype(str).str.strip()
        df = df[df['review'] != '']
        df = df[df['review'] != 'nan']
        
        return df[['review']]
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

def process_text_input(text_input: str) -> pd.DataFrame:
    """
    Process text input and convert to DataFrame
    
    Args:
        text_input: Raw text input
        
    Returns:
        DataFrame with reviews
    """
    if not text_input or not text_input.strip():
        return pd.DataFrame(columns=['review'])
    
    # Split by lines and create individual reviews
    lines = [line.strip() for line in text_input.split('\n') if line.strip()]
    
    # If there's only one line, treat it as a single review
    if len(lines) == 1:
        # Try to split by common delimiters
        delimiters = [';', '.', '\n\n']
        for delimiter in delimiters:
            if delimiter in lines[0] and len(lines[0].split(delimiter)) > 2:
                reviews = [r.strip() for r in lines[0].split(delimiter) if r.strip()]
                break
        else:
            reviews = lines
    else:
        reviews = lines
    
    return pd.DataFrame({'review': reviews})

def create_sentiment_chart(sentiment_dist: Dict[str, float]) -> go.Figure:
    """
    Create a pie chart for sentiment distribution
    
    Args:
        sentiment_dist: Dictionary with sentiment percentages
        
    Returns:
        Plotly figure
    """
    colors = {
        'Positive': '#2E8B57',
        'Negative': '#DC143C', 
        'Neutral': '#708090'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(sentiment_dist.keys()),
        values=list(sentiment_dist.values()),
        hole=0.3,
        marker_colors=[colors.get(sentiment, '#95A5A6') for sentiment in sentiment_dist.keys()],
        textinfo='label+percent',
        textfont_size=12
    )])
    
    fig.update_layout(
        title="Sentiment Distribution",
        font=dict(size=14),
        showlegend=True,
        height=400
    )
    
    return fig

def create_aspect_chart(aspect_sentiments: Dict[str, Dict[str, float]]) -> go.Figure:
    """
    Create a grouped bar chart for aspect-based sentiment
    
    Args:
        aspect_sentiments: Dictionary with aspect-wise sentiment percentages
        
    Returns:
        Plotly figure
    """
    aspects = list(aspect_sentiments.keys())
    sentiments = ['Positive', 'Negative', 'Neutral']
    
    fig = go.Figure()
    
    colors = {
        'Positive': '#2E8B57',
        'Negative': '#DC143C',
        'Neutral': '#708090'
    }
    
    for sentiment in sentiments:
        values = [aspect_sentiments[aspect].get(sentiment, 0) for aspect in aspects]
        fig.add_trace(go.Bar(
            name=sentiment,
            x=aspects,
            y=values,
            marker_color=colors[sentiment]
        ))
    
    fig.update_layout(
        title="Aspect-based Sentiment Analysis",
        xaxis_title="Product Aspects",
        yaxis_title="Percentage (%)",
        barmode='group',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_fake_review_chart(fake_indicators: Dict[str, int]) -> go.Figure:
    """
    Create a bar chart for fake review indicators
    
    Args:
        fake_indicators: Dictionary with fake review indicator counts
        
    Returns:
        Plotly figure
    """
    indicators = list(fake_indicators.keys())
    counts = list(fake_indicators.values())
    
    # Convert indicator names to readable format
    readable_names = {
        'excessive_capitalization': 'Excessive Caps',
        'repetitive_text': 'Repetitive Text',
        'suspicious_keywords': 'Suspicious Keywords',
        'unnatural_length': 'Unnatural Length'
    }
    
    x_labels = [readable_names.get(indicator, indicator.replace('_', ' ').title()) 
                for indicator in indicators]
    
    fig = go.Figure(data=[go.Bar(
        x=x_labels,
        y=counts,
        marker_color='#FF6B6B'
    )])
    
    fig.update_layout(
        title="Potential Fake Review Indicators",
        xaxis_title="Indicator Type",
        yaxis_title="Count",
        height=400
    )
    
    return fig

def format_insights_text(text: str, max_length: int = 100) -> str:
    """
    Format text for display with truncation if needed
    
    Args:
        text: Input text
        max_length: Maximum length before truncation
        
    Returns:
        Formatted text
    """
    if not text:
        return "No data available"
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."

def create_download_data(analysis_results: Dict) -> pd.DataFrame:
    """
    Create a downloadable DataFrame with analysis results
    
    Args:
        analysis_results: Dictionary containing all analysis results
        
    Returns:
        DataFrame with formatted results
    """
    data = []
    
    # Add summary information
    data.append(['Metric', 'Value'])
    data.append(['Total Reviews', analysis_results.get('total_reviews', 0)])
    data.append(['Summary', analysis_results.get('summary', 'N/A')])
    
    # Add sentiment distribution
    sentiment_dist = analysis_results.get('sentiment_distribution', {})
    for sentiment, percentage in sentiment_dist.items():
        data.append([f'Sentiment - {sentiment}', f'{percentage}%'])
    
    # Add key points
    positives = analysis_results.get('positives', [])
    for i, positive in enumerate(positives[:3], 1):
        data.append([f'Positive Point {i}', positive])
    
    negatives = analysis_results.get('negatives', [])
    for i, negative in enumerate(negatives[:3], 1):
        data.append([f'Negative Point {i}', negative])
    
    # Add suggestions
    suggestions = analysis_results.get('actionable_suggestions', [])
    for i, suggestion in enumerate(suggestions[:3], 1):
        data.append([f'Suggestion {i}', suggestion])
    
    return pd.DataFrame(data, columns=['Aspect', 'Details'])

def validate_review_quality(text: str) -> Dict[str, bool]:
    """
    Validate review quality with various checks
    
    Args:
        text: Review text
        
    Returns:
        Dictionary with quality indicators
    """
    quality_checks = {
        'has_minimum_length': len(text.split()) >= 3,
        'not_all_caps': text != text.upper(),
        'has_meaningful_content': len(set(text.lower().split())) > 2,
        'not_repetitive': len(text.split()) > len(set(text.lower().split())) * 0.7
    }
    
    return quality_checks

def filter_quality_reviews(df: pd.DataFrame, min_quality_score: float = 0.5) -> pd.DataFrame:
    """
    Filter reviews based on quality metrics
    
    Args:
        df: DataFrame with reviews
        min_quality_score: Minimum quality score (0-1)
        
    Returns:
        Filtered DataFrame
    """
    if 'review' not in df.columns:
        return df
    
    quality_scores = []
    for review in df['review']:
        checks = validate_review_quality(str(review))
        score = sum(checks.values()) / len(checks)
        quality_scores.append(score)
    
    df['quality_score'] = quality_scores
    filtered_df = df[df['quality_score'] >= min_quality_score].copy()
    
    return filtered_df.drop('quality_score', axis=1)

def get_review_statistics(df: pd.DataFrame) -> Dict[str, Union[int, float]]:
    """
    Get basic statistics about reviews
    
    Args:
        df: DataFrame with reviews
        
    Returns:
        Dictionary with statistics
    """
    if 'review' not in df.columns or df.empty:
        return {'total_reviews': 0}
    
    reviews = df['review'].astype(str)
    
    stats = {
        'total_reviews': len(reviews),
        'avg_review_length': reviews.str.len().mean(),
        'min_review_length': reviews.str.len().min(),
        'max_review_length': reviews.str.len().max(),
        'total_words': reviews.str.split().str.len().sum(),
        'avg_words_per_review': reviews.str.split().str.len().mean()
    }
    
    # Round float values
    for key, value in stats.items():
        if isinstance(value, float):
            stats[key] = round(value, 1)
    
    return stats
