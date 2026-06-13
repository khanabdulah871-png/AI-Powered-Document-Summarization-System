"""
summarizer.py
Extractive summarization using frequency-based and TF-IDF based scoring.
"""

import math
from collections import Counter
from nltk.tokenize import word_tokenize
from preprocessing import remove_stopwords, to_lowercase


def word_frequencies(words):
    """Return frequency count of words."""
    return Counter(words)


def score_sentences_frequency(sentences, word_freq):
    """
    Score each sentence based on sum of frequencies
    of its (cleaned, non-stopword) words.
    """
    scores = {}
    for i, sentence in enumerate(sentences):
        tokens = word_tokenize(to_lowercase(sentence))
        words = remove_stopwords(tokens)

        if not words:
            scores[i] = 0
            continue

        score = sum(word_freq.get(w, 0) for w in words)
        # Normalize by sentence length to avoid bias toward long sentences
        scores[i] = score / len(words)

    return scores


def score_sentences_tfidf(sentences, all_words_per_sentence):
    """
    Score each sentence using TF-IDF.
    all_words_per_sentence: list of word-lists, one per sentence.
    """
    n_sentences = len(all_words_per_sentence)
    if n_sentences == 0:
        return {}

    # Document frequency: how many sentences contain each word
    df = Counter()
    for words in all_words_per_sentence:
        for w in set(words):
            df[w] += 1

    scores = {}
    for i, words in enumerate(all_words_per_sentence):
        if not words:
            scores[i] = 0
            continue

        tf = Counter(words)
        total_words = len(words)
        sentence_score = 0

        for w, count in tf.items():
            tf_val = count / total_words
            idf_val = math.log((n_sentences + 1) / (df[w] + 1)) + 1
            sentence_score += tf_val * idf_val

        scores[i] = sentence_score / total_words

    return scores


def rank_sentences(scores, top_n):
    """
    Return indices of top_n highest scoring sentences,
    sorted in original order (to preserve readability).
    """
    if top_n <= 0:
        return []

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_indices = [idx for idx, _ in ranked[:top_n]]
    return sorted(top_indices)


def generate_summary(preprocessed, summary_ratio=0.3, method="frequency"):
    """
    Generate extractive summary.

    preprocessed: dict from preprocess_text() -> {cleaned_text, sentences, words}
    summary_ratio: fraction of sentences to keep (0 < ratio <= 1)
    method: "frequency" or "tfidf"

    Returns: (summary_text, sentence_scores, top_indices)
    """
    sentences = preprocessed.get("sentences", [])

    if not sentences:
        print("Error: No sentences available to summarize.")
        return "", {}, []

    total_sentences = len(sentences)
    top_n = max(1, math.ceil(total_sentences * summary_ratio))

    if method == "frequency":
        word_freq = word_frequencies(preprocessed.get("words", []))
        scores = score_sentences_frequency(sentences, word_freq)

    elif method == "tfidf":
        all_words_per_sentence = []
        for sentence in sentences:
            tokens = word_tokenize(to_lowercase(sentence))
            words = remove_stopwords(tokens)
            all_words_per_sentence.append(words)
        scores = score_sentences_tfidf(sentences, all_words_per_sentence)

    else:
        print(f"Error: Unknown method '{method}'. Use 'frequency' or 'tfidf'.")
        return "", {}, []

    top_indices = rank_sentences(scores, top_n)
    summary = " ".join(sentences[i] for i in top_indices)

    return summary, scores, top_indices
