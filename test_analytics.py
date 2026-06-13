from preprocessing import preprocess_text
from summarizer import generate_summary
from analytics import print_analytics_report

text = """Organizations deal with large volumes of documents such as reports, emails, and articles. Manual summarization is time-consuming and inconsistent. TEYZIX CORE requires an AI-based solution that extracts key insights automatically. AI can process documents faster than humans. Automation improves efficiency in organizations."""

result = preprocess_text(text)
summary, scores, idx = generate_summary(result, summary_ratio=0.5, method="tfidf")
print("SUMMARY:", summary)

print_analytics_report(result["words"], result["sentences"], scores)