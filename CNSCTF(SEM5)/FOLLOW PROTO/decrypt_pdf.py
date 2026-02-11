from PyPDF2 import PdfReader

# Path to the encrypted PDF
pdf_path = r"c:\Users\whizy\CTF\CNSCTF\FOLLOW PROTO\Flag.pdf"

# Password
password = "13779"

# Open the PDF
reader = PdfReader(pdf_path)

# Check if encrypted
if reader.is_encrypted:
    reader.decrypt(password)

# Extract text from all pages
text = ""
for page in reader.pages:
    text += page.extract_text()

print(text)