"""
analytics.py
Provides word frequency analysis, keyword extraction,
and sentence importance scoring display.
"""

from collections import Counter


def get_word_frequencies(words, top_n=10):
    """Return the top_n most common words with their counts."""
    if not words:
        print("Error: No words provided for frequency analysis.")
        return []

    freq = Counter(words)
    return freq.most_common(top_n)


def get_top_keywords(words, top_n=10):
    """
    Extract top_n keywords based on frequency.
    (Words are already lowercase and stopword-free from preprocessing.)
    """
    if not words:
        print("Error: No words provided for keyword extraction.")
        return []

    freq = Counter(words)
    return [word for word, _ in freq.most_common(top_n)]


def get_sentence_importance(sentences, scores):
    """
    Combine sentences with their importance scores.
    Returns a list of tuples: (sentence_index, sentence, score)
    sorted by score descending.
    """
    if not sentences or not scores:
        print("Error: No sentences or scores provided.")
        return []

    combined = [(i, sentences[i], scores.get(i, 0)) for i in range(len(sentences))]
    combined.sort(key=lambda x: x[2], reverse=True)
    return combined


def print_analytics_report(words, sentences, scores, top_n=10):
    """Print a formatted analytics report."""
    print("\n===== ANALYTICS REPORT =====")

    print(f"\nTop {top_n} Word Frequencies:")
    for word, count in get_word_frequencies(words, top_n):
        print(f"  {word}: {count}")

    print(f"\nTop {top_n} Keywords:")
    for kw in get_top_keywords(words, top_n):
        print(f"  - {kw}")

    print("\nSentence Importance Ranking (Top 5):")
    importance = get_sentence_importance(sentences, scores)
    for idx, sentence, score in importance[:5]:
        print(f"  [{idx}] (score: {score:.4f}) {sentence}")

    print("=============================\n")