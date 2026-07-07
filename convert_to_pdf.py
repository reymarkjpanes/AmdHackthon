"""Convert all text documents in 'test files' folder to PDF."""
import os
from fpdf import FPDF

SOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test files")
OUTPUT_DIR = os.path.join(SOURCE_DIR, "pdf")

os.makedirs(OUTPUT_DIR, exist_ok=True)

txt_files = sorted(f for f in os.listdir(SOURCE_DIR) if f.endswith(".txt"))

for txt_file in txt_files:
    txt_path = os.path.join(SOURCE_DIR, txt_file)
    pdf_name = os.path.splitext(txt_file)[0] + ".pdf"
    pdf_path = os.path.join(OUTPUT_DIR, pdf_name)

    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)

    # Title from filename
    title = os.path.splitext(txt_file)[0].replace("_", " ")
    pdf.set_font("Helvetica", "B", size=14)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", size=10)

    for line in content.split("\n"):
        if line.strip() == "":
            pdf.ln(4)
        else:
            # Replace problematic characters and encode to latin-1
            safe_line = line.encode("latin-1", errors="replace").decode("latin-1")
            try:
                pdf.multi_cell(0, 5, safe_line)
            except Exception:
                # If still fails, truncate or skip
                try:
                    pdf.cell(0, 5, safe_line[:100], ln=True)
                except Exception:
                    pass

    pdf.output(pdf_path)
    print(f"  Created: {pdf_name}")

print(f"\nAll {len(txt_files)} files converted to PDF.")
print(f"Output folder: {OUTPUT_DIR}")
