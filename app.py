"""
Product Review Summarization & Insight Generator
Streamlit Web Application
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
import base64
from analyzer import ReviewAnalyzer
from utils import (
    validate_file_upload, process_text_input, create_sentiment_chart,
    create_aspect_chart, create_fake_review_chart, format_insights_text,
    create_download_data, filter_quality_reviews, get_review_statistics
)

# Configure Streamlit page
st.set_page_config(
    page_title="Product Review Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
def local_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .positive-text {
        color: #2E8B57;
        font-weight: bold;
    }
    .negative-text {
        color: #DC143C;
        font-weight: bold;
    }
    .neutral-text {
        color: #708090;
        font-weight: bold;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    local_css()
    
    # Initialize session state
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = ReviewAnalyzer()
    
    # Header
    st.markdown('<h1 class="main-header">📊 Product Review Summarization & Insight Generator</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Analyze product reviews to extract meaningful insights, sentiment patterns, and actionable suggestions.
    Upload a file or paste reviews to get started.
    """)
    
    # Sidebar for input methods
    st.sidebar.header("📥 Input Options")
    
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Upload File", "Paste Text", "Use Sample Data"]
    )
    
    reviews_df = None
    
    if input_method == "Upload File":
        st.sidebar.subheader("📁 Upload Reviews")
        uploaded_file = st.sidebar.file_uploader(
            "Choose a file",
            type=['csv', 'txt', 'xlsx', 'xls'],
            help="Supported formats: CSV, TXT, Excel"
        )
        
        if uploaded_file:
            reviews_df = validate_file_upload(uploaded_file)
            if reviews_df is not None:
                st.sidebar.success(f"✅ Loaded {len(reviews_df)} reviews")
                st.sidebar.dataframe(reviews_df.head())
            else:
                st.sidebar.error("❌ Failed to load file. Please check the format.")
    
    elif input_method == "Paste Text":
        st.sidebar.subheader("✏️ Paste Reviews")
        text_input = st.sidebar.text_area(
            "Enter product reviews (one per line or separated by semicolons):",
            height=200,
            placeholder="Product is amazing! Works great.\nGood value for money.\nCould be better in terms of quality..."
        )
        
        if st.sidebar.button("Process Text"):
            reviews_df = process_text_input(text_input)
            if not reviews_df.empty:
                st.sidebar.success(f"✅ Processed {len(reviews_df)} reviews")
            else:
                st.sidebar.error("❌ No valid reviews found in text.")
    
    else:  # Use Sample Data
        st.sidebar.subheader("📋 Sample Data")
        if st.sidebar.button("Load Sample Reviews"):
            try:
                reviews_df = pd.read_csv('sample_reviews.csv')
                st.sidebar.success(f"✅ Loaded {len(reviews_df)} sample reviews")
            except FileNotFoundError:
                st.sidebar.error("❌ Sample file not found. Please upload your own data.")
    
    # Quality filter options
    if reviews_df is not None and not reviews_df.empty:
        st.sidebar.subheader("🔍 Quality Filters")
        apply_quality_filter = st.sidebar.checkbox(
            "Apply quality filters",
            value=False,
            help="Remove low-quality reviews automatically"
        )
        
        if apply_quality_filter:
            min_quality = st.sidebar.slider(
                "Minimum quality score",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.1
            )
            original_count = len(reviews_df)
            reviews_df = filter_quality_reviews(reviews_df, min_quality)
            filtered_count = len(reviews_df)
            st.sidebar.info(f"Filtered: {original_count} → {filtered_count} reviews")
    
    # Main analysis section
    if reviews_df is not None and not reviews_df.empty:
        st.header("🔬 Analysis Results")
        
        # Analyze button
        if st.button("🚀 Analyze Reviews", type="primary"):
            with st.spinner("Analyzing reviews... This may take a moment."):
                try:
                    st.session_state.analysis_results = st.session_state.analyzer.analyze_reviews(reviews_df)
                    st.success("✅ Analysis completed successfully!")
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    st.session_state.analysis_results = None
        
        # Display results
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Key metrics row
            st.subheader("📈 Key Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Reviews",
                    results.get('total_reviews', 0),
                    delta=None
                )
            
            with col2:
                pos_pct = results.get('sentiment_distribution', {}).get('Positive', 0)
                st.metric(
                    "Positive Sentiment",
                    f"{pos_pct}%",
                    delta=None,
                    delta_color="normal"
                )
            
            with col3:
                neg_pct = results.get('sentiment_distribution', {}).get('Negative', 0)
                st.metric(
                    "Negative Sentiment", 
                    f"{neg_pct}%",
                    delta=None,
                    delta_color="normal"
                )
            
            with col4:
                neu_pct = results.get('sentiment_distribution', {}).get('Neutral', 0)
                st.metric(
                    "Neutral Sentiment",
                    f"{neu_pct}%",
                    delta=None,
                    delta_color="normal"
                )
            
            # Summary section
            st.subheader("📝 Summary")
            summary = results.get('summary', 'No summary available')
            st.markdown(f'<div class="insight-box">{summary}</div>', unsafe_allow_html=True)
            
            # Charts row
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("😊 Sentiment Distribution")
                sentiment_chart = create_sentiment_chart(results.get('sentiment_distribution', {}))
                st.plotly_chart(sentiment_chart, use_container_width=True)
            
            with col2:
                st.subheader("🎯 Aspect-based Analysis")
                aspect_chart = create_aspect_chart(results.get('aspect_sentiments', {}))
                st.plotly_chart(aspect_chart, use_container_width=True)
            
            # Key insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✅ Key Positives")
                positives = results.get('positives', [])
                if positives:
                    for i, positive in enumerate(positives[:5], 1):
                        st.markdown(f"{i}. {positive}")
                else:
                    st.info("No significant positive points identified")
            
            with col2:
                st.subheader("❌ Key Negatives")
                negatives = results.get('negatives', [])
                if negatives:
                    for i, negative in enumerate(negatives[:5], 1):
                        st.markdown(f"{i}. {negative}")
                else:
                    st.info("No significant negative points identified")
            
            # Key phrases
            st.subheader("🔑 Key Phrases & Topics")
            key_phrases = results.get('key_phrases', [])
            if key_phrases:
                cols = st.columns(3)
                for i, phrase in enumerate(key_phrases[:12]):
                    with cols[i % 3]:
                        st.markdown(f"• {phrase}")
            else:
                st.info("No key phrases identified")
            
            # Actionable suggestions
            st.subheader("💡 Actionable Suggestions")
            suggestions = results.get('actionable_suggestions', [])
            if suggestions:
                for i, suggestion in enumerate(suggestions, 1):
                    st.markdown(f'<div class="insight-box">{i}. {suggestion}</div>', 
                               unsafe_allow_html=True)
            else:
                st.info("No specific suggestions available")
            
            # Fake review detection
            st.subheader("🔍 Review Quality Analysis")
            fake_indicators = results.get('fake_review_indicators', {})
            if any(fake_indicators.values()):
                st.warning("⚠️ Some potential fake review indicators detected:")
                fake_chart = create_fake_review_chart(fake_indicators)
                st.plotly_chart(fake_chart, use_container_width=True)
            else:
                st.success("✅ No significant fake review indicators detected")
            
            # Download results
            st.subheader("📥 Export Results")
            col1, col2 = st.columns(2)
            
            with col1:
                # CSV download
                download_df = create_download_data(results)
                csv = download_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Results (CSV)",
                    data=csv,
                    file_name="review_analysis_results.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Review statistics
                stats = get_review_statistics(reviews_df)
                st.markdown("**Review Statistics:**")
                for key, value in stats.items():
                    if key != 'total_reviews':  # Already shown in metrics
                        st.markdown(f"• {key.replace('_', ' ').title()}: {value}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<center><small>Product Review Analyzer | Built with Streamlit & NLP</small></center>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
