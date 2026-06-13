# AI-Powered Document Summarization System

**Task ID:** AI-INT-1
**Domain:** Artificial Intelligence / NLP
**Internship:** Teyzix Core Internship (June Batch)

## Overview
This project is an extractive text summarization system built in Python.
It reads input from a text file, PDF file, or direct user input, preprocesses
the text using NLP techniques, scores sentences using Frequency-based or
TF-IDF based methods, and generates a concise summary while preserving key
information. It also provides analytics such as word frequency, top
keywords, and sentence importance ranking.

## Features
- **Multiple input sources:** .txt file, .pdf file, or direct user input
- **Text preprocessing:** lowercasing, stopword removal, tokenization,
  sentence segmentation (using NLTK)
- **Extractive summarization:**
  - Frequency-based sentence scoring
  - TF-IDF based sentence scoring
  - Adjustable summary length (as a percentage of original)
- **Analytics module:**
  - Word frequency analysis
  - Top keyword extraction
  - Sentence importance ranking
- **Output:**
  - Displays original text vs summarized text
  - Export summary as .txt or .pdf
- **Error handling** for missing files, empty input, and invalid choices

## Project Structure
```
AI-Powered Document Summarization System/
├── main.py            # Entry point - runs the full pipeline
├── file_handler.py     # Input loading & output export (txt/pdf)
├── preprocessing.py     # Text cleaning, tokenization, stopword removal
├── summarizer.py        # Frequency & TF-IDF based summarization logic
├── analytics.py         # Word frequency, keywords, sentence importance
├── samples/              # Sample input documents
├── outputs/              # Generated summaries (.txt / .pdf)
└── README.md
```

## Requirements
- Python 3.x
- NLTK
- PyPDF2
- fpdf

## Installation
```bash
pip install nltk PyPDF2 fpdf
```

One-time NLTK data download:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

## How to Run
```bash
python main.py
```

You will be prompted to:
1. Choose input source (txt file / pdf file / direct input)
2. Enter summary length as a percentage of the original (e.g. 30 for 30%)
3. Choose summarization method (Frequency-based / TF-IDF based)
4. Choose export format (txt / pdf / none)

## Example
**Input:** A paragraph about organizations and document management.

**Output:**
- Original text displayed
- Generated summary (shorter, key sentences only)
- Analytics report: top word frequencies, top keywords, and sentence
  importance ranking
- Optionally exported to `outputs/summary.txt` or `outputs/summary.pdf`

## Technical Approach
- **Preprocessing:** Text is cleaned, segmented into sentences (original
  case preserved for readability), and tokenized into lowercase,
  stopword-free words for scoring.
- **Frequency-based scoring:** Each sentence is scored by the sum of word
  frequencies of its meaningful words, normalized by sentence length.
- **TF-IDF based scoring:** Each sentence is scored using Term
  Frequency–Inverse Document Frequency, treating each sentence as a
  "document" within the text.
- **Ranking & selection:** Top-scoring sentences are selected based on the
  desired summary ratio and presented in their original order.

## Author
Developed as part of the Teyzix Core Internship (June Batch) - Task AI-INT-1.