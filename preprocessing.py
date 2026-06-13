"""
preprocess.py
Handles text preprocessing: lowercasing, tokenization,
sentence segmentation, and stopword removal.
"""

import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))


def clean_text(text):
    """Basic cleanup: remove extra spaces/newlines."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def to_lowercase(text):
    """Convert text to lowercase."""
    return text.lower()


def segment_sentences(text):
    """Split text into sentences (uses original-case text for readability)."""
    try:
        return sent_tokenize(text)
    except Exception as e:
        print(f"Error in sentence segmentation: {e}")
        return []


def tokenize_words(text):
    """Split text into word tokens."""
    try:
        return word_tokenize(text)
    except Exception as e:
        print(f"Error in word tokenization: {e}")
        return []


def remove_stopwords(tokens):
    """Remove stopwords and non-alphabetic tokens from a list of tokens."""
    return [w for w in tokens if w.isalpha() and w.lower() not in STOPWORDS]


def preprocess_text(text):
    """
    Full preprocessing pipeline.
    Returns a dict with:
      - cleaned_text
      - sentences (original case, for summary output)
      - words (lowercase, stopwords removed, for scoring)
    """
    if not text or not text.strip():
        print("Error: Empty text provided for preprocessing.")
        return {"cleaned_text": "", "sentences": [], "words": []}

    cleaned = clean_text(text)
    sentences = segment_sentences(cleaned)

    lowered = to_lowercase(cleaned)
    tokens = tokenize_words(lowered)
    words = remove_stopwords(tokens)

    return {
        "cleaned_text": cleaned,
        "sentences": sentences,
        "words": words
    }

if __name__ == "__main__":
    sample = "Pakistan is a beautiful country. It has mountains, rivers, and deserts. Many tourists visit Pakistan every year."
    result = preprocess_text(sample)
    print("Sentences:", result["sentences"])
    print("Words:", result["words"])