"""
main.py
Entry point for the AI-Powered Document Summarization System.
Integrates: file_handler, preprocessing, summarizer, analytics.
"""

from file_handler import load_document, export_summary_txt, export_summary_pdf
from preprocessing import preprocess_text
from summarizer import generate_summary
from analytics import print_analytics_report


def get_source_choice():
    print("\nSelect input source:")
    print("1. Text file (.txt)")
    print("2. PDF file (.pdf)")
    print("3. Direct input")
    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        path = input("Enter path to .txt file: ").strip()
        return "txt", path
    elif choice == "2":
        path = input("Enter path to .pdf file: ").strip()
        return "pdf", path
    elif choice == "3":
        return "input", None
    else:
        print("Invalid choice.")
        return None, None


def get_summary_ratio():
    while True:
        try:
            val = input("Enter summary length as % of original (e.g. 30): ").strip()
            ratio = float(val) / 100
            if 0 < ratio <= 1:
                return ratio
            print("Please enter a value between 1 and 100.")
        except ValueError:
            print("Invalid number. Try again.")


def get_method_choice():
    print("\nSelect summarization method:")
    print("1. Frequency-based")
    print("2. TF-IDF based")
    choice = input("Enter choice (1/2): ").strip()
    return "tfidf" if choice == "2" else "frequency"


def main():
    print("===== AI-Powered Document Summarization System =====")

    source_type, source_value = get_source_choice()
    if source_type is None:
        print("Exiting due to invalid input source.")
        return

    raw_text = load_document(source_type, source_value)
    if not raw_text or not raw_text.strip():
        print("Error: No text loaded. Exiting.")
        return

    result = preprocess_text(raw_text)
    if not result["sentences"]:
        print("Error: Could not process text. Exiting.")
        return

    ratio = get_summary_ratio()
    method = get_method_choice()

    summary, scores, top_indices = generate_summary(result, summary_ratio=ratio, method=method)

    print("\n========== ORIGINAL TEXT ==========")
    print(raw_text)

    print("\n========== SUMMARY ==========")
    print(summary)

    print_analytics_report(result["words"], result["sentences"], scores)

    export_choice = input("Export summary? (txt/pdf/none): ").strip().lower()
    if export_choice == "txt":
        export_summary_txt(summary, "outputs/summary.txt")
    elif export_choice == "pdf":
        export_summary_pdf(summary, "outputs/summary.pdf")
    else:
        print("No export selected.")

    print("\nDone.")


if __name__ == "__main__":
    main()