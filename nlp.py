from PyPDF2 import PdfReader

# Specify the path to the PDF file
pdf_path = r"C:\Users\sanjay\Downloads\sanjay\iit-medrass\email-pdf-collector\uploads\92508471-Sbi-Statement.pdf"

# Read the PDF file
reader = PdfReader(pdf_path)

# Extract text and save to a file
with open("extracted_text.txt", "w", encoding="utf-8") as output_file:
    for page in reader.pages:
        text = page.extract_text()
        if text:  # Check if text is not None
            output_file.write(text + "\n")  # Write each page's text to the file