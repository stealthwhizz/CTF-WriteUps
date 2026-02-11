#!/usr/bin/env python3
"""
Automatic Zodiac Cipher Decoder with OCR
"""

from PIL import Image
import sys

def try_ocr():
    """Try multiple OCR approaches"""
    try:
        import pytesseract
        
        img = Image.open("ciphertext.png")
        
        # Try default OCR
        text1 = pytesseract.image_to_string(img)
        print("OCR Attempt 1 (default):")
        print(repr(text1))
        print()
        
        # Try with different config
        text2 = pytesseract.image_to_string(img, config='--psm 6')
        print("OCR Attempt 2 (psm 6):")
        print(repr(text2))
        print()
        
        # Try to detect symbols
        text3 = pytesseract.image_to_string(img, config='--psm 13')
        print("OCR Attempt 3 (psm 13):")
        print(repr(text3))
        
        return text1 or text2 or text3
        
    except ImportError:
        print("pytesseract not available")
        return None
    except Exception as e:
        print(f"OCR failed: {e}")
        return None

def decode_zodiac_text(text):
    """Decode text containing zodiac symbols or names"""
    zodiac_map = {
        "♈": "A", "Aries": "A",
        "♉": "T", "Taurus": "T",
        "♊": "G", "Gemini": "G",
        "♋": "C", "Cancer": "C",
        "♌": "L", "Leo": "L",
        "♍": "V", "Virgo": "V",
        "♎": "L", "Libra": "L",
        "♏": "S", "Scorpio": "S",
        "♐": "S", "Sagittarius": "S",
        "♑": "C", "Capricorn": "C",
        "♒": "A", "Aquarius": "A",
        "♓": "P", "Pisces": "P"
    }
    
    decoded = ""
    for char in text:
        if char in zodiac_map:
            decoded += zodiac_map[char]
    
    # Also try word matching
    for sign, letter in zodiac_map.items():
        if isinstance(sign, str) and len(sign) > 1:  # Sign names
            if sign.lower() in text.lower():
                decoded += letter
    
    return decoded

# Try to read with OCR
print("=" * 60)
print("Attempting automatic decode...")
print("=" * 60)

text = try_ocr()

if text:
    decoded = decode_zodiac_text(text)
    if decoded:
        print(f"\n{'=' * 60}")
        print(f"DECODED: {decoded}")
        print(f"FLAG: ISFCR{{{decoded}}}")
        print(f"{'=' * 60}")
    else:
        print("\nNo zodiac symbols found in OCR output")
else:
    print("\nOCR not available or failed")

print("\n" + "=" * 60)
print("If automatic decode failed, please visually inspect")
print("ciphertext.png and enter the zodiac symbols/signs you see")
print("=" * 60)
