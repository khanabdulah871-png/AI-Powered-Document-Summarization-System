from preprocessing import preprocess_text
from summarizer import generate_summary

text = """Organizations deal with large volumes of documents such as reports, emails, and articles. Manual summarization is time-consuming and inconsistent. TEYZIX CORE requires an AI-based solution that extracts key insights automatically."""

result = preprocess_text(text)
summary, scores, idx = generate_summary(result, summary_ratio=0.5, method="tfidf")

print("ORIGINAL:")
print(text)
print("\nSUMMARY:")
print(summary)