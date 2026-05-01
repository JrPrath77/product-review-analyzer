# 📊 Product Review Summarization & Insight Generator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io)
[![NLTK](https://img.shields.io/badge/NLTK-3.8%2B-green.svg)](https://nltk.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🤖 **AI-powered product review analysis tool** that extracts meaningful insights, sentiment patterns, and actionable suggestions from customer feedback using Natural Language Processing.

![Demo](https://img.shields.io/badge/Demo-Live-brightgreen)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

## ✨ Features

### 🎯 Core Functionality
- **📤 Multiple Input Methods**: Upload CSV/Excel files, paste text, or use sample data
- **😊 Sentiment Analysis**: Positive/Negative/Neutral sentiment with percentage breakdown
- **📝 Review Summarization**: Automatic 2-3 line summary of all reviews
- **🔍 Key Insights Extraction**: 
  - ✅ Positive points (bullet points)
  - ❌ Negative points (bullet points)
  - 🔑 Key phrases and topics
- **🎯 Aspect-based Analysis**: Sentiment breakdown by product features:
  - 🏗️ Quality
  - 💰 Price
  - ⚡ Performance
  - 🎨 Design
  - 👤 Usability
- **💡 Actionable Suggestions**: Business recommendations based on analysis
- **🔍 Fake Review Detection**: Basic heuristic analysis for review authenticity

### 🚀 Advanced Features
- **📊 Interactive Dashboard**: Clean, modern Streamlit interface
- **📈 Visualizations**: Charts for sentiment distribution and aspect analysis
- **🔧 Quality Filters**: Automatic filtering of low-quality reviews
- **💾 Export Functionality**: Download results as CSV
- **📊 Review Statistics**: Detailed metrics about review data

## � Table of Contents
- [Installation](#-installation)
- [Usage](#-usage)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Technical Details](#-technical-details)
- [Contributing](#-contributing)
- [License](#-license)

## �📁 Project Structure

```
product_review_analyzer/
├── app.py                 # Streamlit web application
├── analyzer.py            # Core NLP analysis logic
├── utils.py              # Helper functions and utilities
├── sample_reviews.csv    # Sample data for testing
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## � Quick Start

### 📋 Prerequisites
- **Python 3.8+** 
- **pip package manager**

### ⚡ Quick Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/product-review-analyzer.git
cd product-review-analyzer

# Create and activate virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

🎉 **The app will open at `http://localhost:8501`**

### 🐳 Docker Alternative
```bash
# Build and run with Docker
docker build -t review-analyzer .
docker run -p 8501:8501 review-analyzer
```

## 🎮 Usage Guide

### 📤 Input Methods

#### 1. **Upload Files**
- Supported formats: **CSV**, **TXT**, **Excel (.xlsx, .xls)**
- Auto-detects review columns
- Smart file parsing

#### 2. **Paste Text**
- Direct text input
- Multiple review separators (newline, semicolon)
- Automatic review splitting

#### 3. **Sample Data**
- Built-in 30 review dataset
- Perfect for testing features
- No setup required

### � Analysis Features

| Feature | Description | Output |
|---------|-------------|--------|
| **Sentiment Analysis** | VADER-based sentiment detection | Positive/Negative/Neutral % |
| **Summarization** | Extractive summary generation | 2-3 line overview |
| **Aspect Analysis** | Feature-wise sentiment breakdown | Quality, Price, Performance, Design, Usability |
| **Insight Extraction** | Key points identification | Positive/Negative bullet points |
| **Quality Detection** | Fake review heuristics | Authenticity indicators |

### 🎨 Dashboard Components

- **📊 Key Metrics**: Real-time sentiment distribution
- **📈 Interactive Charts**: Visual sentiment and aspect analysis
- **💡 Actionable Insights**: Business recommendations
- **📥 Export Options**: Download results as CSV

## �️ Technical Details

### 📚 Technology Stack
| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core language | 3.8+ |
| **Streamlit** | Web framework | 1.28+ |
| **NLTK** | NLP processing | 3.8+ |
| **Plotly** | Visualizations | 5.17+ |
| **Pandas** | Data handling | 2.1+ |
| **TextBlob** | Sentiment analysis | 0.17+ |

### 🧠 Analysis Methods

#### **Sentiment Analysis**
- **VADER** sentiment analyzer
- **Compound scores**: 
  - Positive (≥0.05)
  - Neutral (-0.05 to 0.05) 
  - Negative (≤-0.05)
- **Aspect-based** sentiment using keyword matching

#### **Summarization**
- **Extractive** approach
- **Sentence scoring** based on sentiment and length
- Returns **top 3** most relevant sentences

#### **Fake Review Detection**
- **Excessive capitalization** detection
- **Suspicious keyword** identification
- **Unnatural length** analysis
- **Repetitive text** detection

#### **Aspect-based Analysis**
- **Predefined feature keywords** for each aspect
- **Sentiment calculation** per aspect
- **Percentage distribution** for each feature

## 🎯 Customization

### 📝 Adding New Aspects
```python
# In analyzer.py
self.feature_keywords = {
    'quality': ['quality', 'build', 'material', ...],
    'price': ['price', 'cost', 'expensive', ...],
    # Add your new aspect here
    'new_aspect': ['keyword1', 'keyword2', ...]
}
```

### 🎨 Custom Styling
```python
# In app.py - modify local_css() function
def local_css():
    st.markdown("""
    .custom-style {
        /* Your CSS here */
    }
    """, unsafe_allow_html=True)
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **NLTK Download Errors** | `python -c "import nltk; nltk.download('all', force=True)"` |
| **Port Already in Use** | `streamlit run app.py --server.port 8502` |
| **File Upload Issues** | Check file format and review column names |
| **Memory Issues** | Use quality filters for large datasets |
| **Performance** | Analyze 100-500 reviews at a time |

## 📊 Sample Output

```
📈 Key Metrics:
- Total Reviews: 30
- Positive Sentiment: 46.7%
- Negative Sentiment: 26.7%
- Neutral Sentiment: 26.6%

📝 Summary:
"This product offers good value with mixed customer experiences. 
While many users praise the quality and design, others express concerns 
about durability and price."

✅ Key Positives:
1. Outstanding quality and reasonable price
2. Fast performance and beautiful design
3. Excellent customer service experience

❌ Key Negatives:
1. Product broke after minimal use
2. Poor quality control issues
3. Overpriced for the features offered

💡 Actionable Suggestions:
1. Focus on improving product quality and materials
2. Address customer concerns promptly to improve satisfaction
3. Highlight superior quality in marketing materials
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### 📋 Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/product-review-analyzer.git
cd product-review-analyzer

# Set up development environment
python -m venv dev-env
source dev-env/bin/activate  # Windows: dev-env\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Run tests
python -m pytest

# Start development server
streamlit run app.py
```

### � Contribution Guidelines
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### 📝 Code Style
- Follow **PEP 8** guidelines
- Add **docstrings** to new functions
- Include **type hints** where appropriate
- **Test** your changes thoroughly

## � License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🌟 Roadmap

### Upcoming Features
- [ ] **Machine Learning** fake review detection
- [ ] **Multi-language** support
- [ ] **Advanced summarization** using transformers
- [ ] **Real-time** analysis
- [ ] **API integration** with review platforms
- [ ] **Custom sentiment** models
- [ ] **Mobile app** version

### Version History
- **v1.0.0** - Initial release with core features
- **v1.1.0** - Added aspect-based analysis
- **v1.2.0** - Enhanced fake review detection
- **v2.0.0** - Planned ML integration

## 📞 Support & Community

- 🐛 **Bug Reports**: [Create an Issue](https://github.com/yourusername/product-review-analyzer/issues)
- 💡 **Feature Requests**: [Discussions](https://github.com/yourusername/product-review-analyzer/discussions)
- 📧 **Email**: support@productreviewanalyzer.com
- 💬 **Discord**: [Join our community](https://discord.gg/productreviewanalyzer)

## 🏆 Acknowledgments

- **NLTK Team** - Excellent NLP library
- **Streamlit** - Amazing web framework
- **Plotly** - Beautiful visualizations
- **OpenAI** - Inspiration for AI-powered tools

---

<div align="center">

**Made with ❤️ by [Your Name](https://github.com/yourusername)**

[⭐ Star this repo](https://github.com/yourusername/product-review-analyzer) • [🐛 Report issues](https://github.com/yourusername/product-review-analyzer/issues) • [📖 Documentation](https://github.com/yourusername/product-review-analyzer/wiki)

</div>
