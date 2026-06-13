"""
app.py
Streamlit UI for the AI-Powered Document Summarization System.
"""

import streamlit as st
from preprocessing import preprocess_text
from summarizer import generate_summary
from analytics import get_word_frequencies, get_top_keywords, get_sentence_importance
from file_handler import read_pdf_file

st.set_page_config(page_title="AI Document Summarizer", layout="wide")

st.title("📄 AI-Powered Document Summarization System")
st.write("Upload a document or paste text to generate an extractive summary with analytics.")

# ---------- Input Section ----------
st.subheader("1. Input")

input_method = st.radio("Choose input method:", ["Paste Text", "Upload .txt", "Upload .pdf"])

raw_text = ""

if input_method == "Paste Text":
    raw_text = st.text_area("Paste your text here:", height=200)

elif input_method == "Upload .txt":
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded_file is not None:
        raw_text = uploaded_file.read().decode("utf-8", errors="ignore")

elif input_method == "Upload .pdf":
    uploaded_file = st.file_uploader("Upload a .pdf file", type=["pdf"])
    if uploaded_file is not None:
        temp_path = "temp_uploaded.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        raw_text = read_pdf_file(temp_path)

# ---------- Settings ----------
st.subheader("2. Settings")

col1, col2 = st.columns(2)
with col1:
    ratio = st.slider("Summary length (% of original)", 10, 90, 30, step=5) / 100
with col2:
    method = st.selectbox("Summarization method", ["TF-IDF", "Frequency-based"])
    method_key = "tfidf" if method == "TF-IDF" else "frequency"

# ---------- Process ----------
if st.button("Generate Summary"):
    if not raw_text or not raw_text.strip():
        st.error("Please provide some text (paste, .txt, or .pdf) before generating a summary.")
    else:
        result = preprocess_text(raw_text)

        if not result["sentences"]:
            st.error("Could not process the provided text. Please check the input.")
        else:
            summary, scores, top_indices = generate_summary(
                result, summary_ratio=ratio, method=method_key
            )

            st.subheader("3. Results")

            tab1, tab2, tab3 = st.tabs(["Summary", "Original vs Summary", "Analytics"])

            with tab1:
                st.markdown("### Generated Summary")
                st.write(summary)

                st.download_button(
                    "Download Summary (.txt)",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )

            with tab2:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("### Original Text")
                    st.write(raw_text)
                with col_b:
                    st.markdown("### Summarized Text")
                    st.write(summary)

            with tab3:
                st.markdown("### Word Frequency (Top 10)")
                freq_data = get_word_frequencies(result["words"], top_n=10)
                if freq_data:
                    st.bar_chart({word: count for word, count in freq_data})

                st.markdown("### Top Keywords")
                keywords = get_top_keywords(result["words"], top_n=10)
                st.write(", ".join(keywords) if keywords else "No keywords found.")

                st.markdown("### Sentence Importance Ranking")
                importance = get_sentence_importance(result["sentences"], scores)
                for idx, sentence, score in importance[:10]:
                    st.write(f"**[{idx}]** (score: {score:.4f}) {sentence}")