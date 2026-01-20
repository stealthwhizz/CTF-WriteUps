from PIL import Image
import pytesseract

# Open the image
img = Image.open('Mentor_Chellenge_fixed.jpg')

# Use OCR to extract text
text = pytesseract.image_to_string(img)

# Print the extracted text
print("Extracted text:")
print(text)

# Find binary patterns
import re
binary_pattern = r'[01]{8,}'
binaries = re.findall(binary_pattern, text)

if binaries:
    print("\n\nFound binary strings:")
    # Combine all binary
    all_binary = ''.join(binaries)
    print(f"Total binary length: {len(all_binary)} bits")
    
    # Try to decode
    try:
        # Convert to bytes
        n = 8
        bytes_list = [all_binary[i:i+n] for i in range(0, len(all_binary), n)]
        decoded = ''.join([chr(int(b, 2)) for b in bytes_list if len(b) == 8])
        print("\nDecoded text:")
        print(decoded)
    except Exception as e:
        print(f"Error decoding: {e}")
