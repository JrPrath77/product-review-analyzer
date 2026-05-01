# Product Review Summarization & Insight Generator

## Overview

A Python-based NLP pipeline that analyzes raw product reviews and generates structured insights — sentiment, pros, cons, key phrases, and actionable suggestions. Available as both a CLI tool and an interactive Streamlit web app.

---

## Problem

Businesses receive hundreds of product reviews but lack a quick way to:
- Understand overall customer sentiment
- Identify recurring praise or complaints
- Extract actionable improvements from unstructured text

---

## Solution

An automated pipeline that takes raw review text (CSV or paste input) and outputs:
- Sentiment distribution (Positive / Negative / Neutral %)
- Extractive summary of key opinions
- Top pros and cons
- Aspect-based analysis (quality, price, performance, design, usability)
- Actionable business suggestions

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Language | Python 3.10+ |
| Sentiment | NLTK VADER |
| Keyword Extraction | N-grams + Counter |
| Data Handling | Pandas |
| Visualization | Plotly |
| Web UI | Streamlit |
| CLI | argparse |

---

## Architecture

```
Raw Reviews (CSV / Text / Paste)
        |
        v
  Preprocessing
  (clean, tokenize, filter quality)
        |
        v
  Sentiment Analysis
  (VADER — per review: Positive / Negative / Neutral)
        |
        v
  Insight Extraction
  ┌─────────────────────────────────┐
  │  Key Phrases  │  Pros  │  Cons  │
  │  Aspect Sentiments (5 aspects)  │
  │  Fake Review Detection          │
  └─────────────────────────────────┘
        |
        v
  Summary Generation
  (Extractive — top scored sentences)
        |
        v
  Actionable Suggestions
        |
        v
  Output: Report / Streamlit Dashboard / CSV Export
```

---

## Workflow Steps

1. **Input** — Upload CSV, paste text, or load sample data
2. **Preprocessing** — Remove noise, tokenize, filter low-quality reviews
3. **Sentiment Analysis** — VADER scores each review (compound score → label)
4. **Aspect Analysis** — Map reviews to 5 product aspects; compute sentiment per aspect
5. **Pros / Cons Extraction** — Pick top positive/negative sentences by VADER score
6. **Key Phrase Mining** — Unigram + bigram frequency ranking
7. **Summarization** — Score sentences by sentiment strength + length; pick top 3
8. **Fake Review Check** — Heuristics: excessive caps, repetition, suspicious keywords, length
9. **Suggestions** — Rule-based recommendations from aspect + overall sentiment data
10. **Output** — Display on dashboard or export as CSV

---

## Features

- Sentiment distribution with percentages
- Aspect-based sentiment (quality, price, performance, design, usability)
- Auto-extracted pros and cons (top 5 each)
- Extractive summarization
- Key phrase and bigram extraction
- Basic fake review detection
- Actionable business suggestions
- CSV export of results
- Quality filter for low-quality reviews
- Works with CSV, TXT, Excel file uploads

---

## Example Input

**File:** `sample_reviews.csv`

```
review
"This product exceeded my expectations! The quality is outstanding and the price is very reasonable."
"I'm really disappointed with this purchase. The material feels cheap and it broke after just one week."
"Good value for money. The design is sleek but the performance could be better."
```

**Expected Output:**

```
Sentiment Distribution:
  Positive : 70.0%
  Negative : 23.3%
  Neutral  : 6.7%

Summary:
  "The quality is outstanding and the price is very reasonable.
   Fast shipping, excellent quality, and customer service was amazing."

Pros:
  + The quality is outstanding and the price is very reasonable.
  + Good value for money.
  + Best purchase I've made this year!

Cons:
  - I'm really disappointed with this purchase.
  - Terrible experience.
  - Poor quality control.

Suggestions:
  * Highlight superior quality in marketing materials
  * Emphasize competitive pricing in promotions
```

---

## Run Steps

### Install Dependencies

```bash
pip install -r requirements.txt
```

### CLI Mode

```bash
# Run with built-in sample reviews
python3 product_review_analyzer.py

# Run with your own CSV/TXT file
python3 product_review_analyzer.py --file sample_reviews.csv

# Save report to file
python3 product_review_analyzer.py --file sample_reviews.csv --output report.txt
```

### Streamlit Web App

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

### Input Options in the App

- **Upload File** — CSV, TXT, or Excel with a `review` column
- **Paste Text** — One review per line
- **Sample Data** — Load built-in `sample_reviews.csv`

---

## Future Scope

- Integrate HuggingFace transformer models (e.g., `distilbert-base-uncased-finetuned-sst-2-english`) for higher accuracy sentiment
- Topic modeling with LDA for automatic category discovery
- Multi-language support
- Trend analysis over time (date-stamped reviews)
- Comparative analysis across multiple products
- REST API wrapper for integration with e-commerce platforms
- Rating prediction from review text
