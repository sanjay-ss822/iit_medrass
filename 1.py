from PyPDF2 import PdfReader

# Specify the path to the PDF file using raw string notation
pdf_path = r"C:\Users\sanjay\Downloads\sanjay\iit-medrass\email-pdf-collector\uploads\92508471-Sbi-Statement.pdf"

# Read the PDF file
reader = PdfReader(pdf_path)
for page in reader.pages:
    print(page.extract_text())