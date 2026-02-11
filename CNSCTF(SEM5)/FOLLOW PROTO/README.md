# Following Protocol

## Challenge Description

This is a CTF (Capture The Flag) challenge titled "Following Protocol". The goal is to solve a series of equations involving network protocol port numbers to obtain a key, then use that key to unlock an encrypted PDF file containing the flag.

## Files

- `Calculation.txt`: Contains the equations and instructions.
- `Flag.pdf`: An encrypted PDF file that requires a password to access the flag.

## Steps to Solve

### 1. Read the Equations

The content of `Calculation.txt` is:

```
Following Protocol
a = SSH + DNS
b = SMB - FTP
c = (IMAP + POP3) * SMTP
d = STUN * Echo

Compute: Key = (a * b) + (c - d)
```

### 2. Identify Port Numbers

Use standard network protocol port numbers:

- SSH: 22
- DNS: 53
- SMB: 445
- FTP: 21
- IMAP: 143
- POP3: 110
- SMTP: 25
- STUN: 3478
- Echo: 7

### 3. Solve the Equations

- a = 22 + 53 = 75
- b = 445 - 21 = 424
- c = (143 + 110) * 25 = 253 * 25 = 6325
- d = 3478 * 7 = 24346
- Key = (75 * 424) + (6325 - 24346) = 31800 + (-18021) = 13779

### 4. Unlock the PDF

Use the key "13779" as the password to decrypt `Flag.pdf`.

### 5. Extract the Flag

The decrypted PDF contains the flag: `isfcr{13779}`

## Notes

- The PDF also includes additional text: "The network hides its secrets, repeat the key to uncover them." This appears to be a hint, but the flag is directly the calculated key in the specified format.
- Ensure you have a PDF reader that supports password-protected files.

## Tools Used

- Basic arithmetic for calculations.
- PDF decryption tool (e.g., Python with PyPDF2 library or a PDF reader).

## Solution Script

If using Python to decrypt the PDF:

```python
from PyPDF2 import PdfReader

pdf_path = "Flag.pdf"
password = "13779"

reader = PdfReader(pdf_path)
if reader.is_encrypted:
    reader.decrypt(password)

text = ""
for page in reader.pages:
    text += page.extract_text()

print(text)
```

This will output the flag and any additional content.