"""
file_handler.py
Handles input (txt, pdf, direct text) and output (export to txt/pdf).
"""

import os
from fpdf import FPDF

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None


def read_text_file(file_path):
    """Read text from a .txt file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading text file: {e}")
        return ""


def read_pdf_file(file_path):
    """Read text from a .pdf file (optional feature)."""
    if PyPDF2 is None:
        print("Error: PyPDF2 not installed. Run 'pip install PyPDF2'.")
        return ""

    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""


def get_direct_input():
    """Take text input directly from the user."""
    print("Enter/Paste your text. Type 'END' on a new line when finished:")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def load_document(source_type, source_value=None):
    """
    Unified loader.
    source_type: 'txt', 'pdf', or 'input'
    source_value: file path (for txt/pdf)
    """
    source_type = source_type.lower().strip()

    if source_type == "txt":
        if not source_value:
            print("Error: No file path provided for txt input.")
            return ""
        return read_text_file(source_value)

    elif source_type == "pdf":
        if not source_value:
            print("Error: No file path provided for pdf input.")
            return ""
        return read_pdf_file(source_value)

    elif source_type == "input":
        return get_direct_input()

    else:
        print(f"Error: Unsupported source type '{source_type}'. Use 'txt', 'pdf', or 'input'.")
        return ""


def export_summary_txt(summary, output_path):
    """Export summary as a .txt file."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved to {output_path}")
    except Exception as e:
        print(f"Error saving txt file: {e}")


def export_summary_pdf(summary, output_path):
    """Export summary as a .pdf file."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Split text into lines that fit the page width
        for line in summary.split("\n"):
            pdf.multi_cell(0, 10, line)

        pdf.output(output_path)
        print(f"Summary saved to {output_path}")
    except Exception as e:
        print(f"Error saving pdf file: {e}")

if __name__ == "__main__":
    text = get_direct_input()
    print("\n--- You entered ---")
    print(text)
    export_summary_txt(text, "outputs/test.txt")