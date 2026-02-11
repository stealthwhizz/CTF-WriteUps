#!/usr/bin/env python3
"""
Zodiac Cipher Solver - STAR CTF Challenge
"""

from PIL import Image
import pytesseract
import re

# Zodiac signs mapping to letters (first letter)
ZODIAC_TO_LETTER = {
    "Aries": "A",
    "Taurus": "T", 
    "Gemini": "G",
    "Cancer": "C",
    "Leo": "L",
    "Virgo": "V",
    "Libra": "L",
    "Scorpio": "S",
    "Sagittarius": "S",
    "Capricorn": "C",
    "Aquarius": "A",
    "Pisces": "P"
}

# Zodiac symbols (Unicode)
ZODIAC_SYMBOLS = {
    "♈": "Aries",
    "♉": "Taurus",
    "♊": "Gemini",
    "♋": "Cancer",
    "♌": "Leo",
    "♍": "Virgo",
    "♎": "Libra",
    "♏": "Scorpio",
    "♐": "Sagittarius",
    "♑": "Capricorn",
    "♒": "Aquarius",
    "♓": "Pisces"
}

def analyze_image(image_path):
    """Analyze the cipher image"""
    try:
        img = Image.open(image_path)
        print(f"Image loaded: {img.size[0]}x{img.size[1]} pixels")
        print(f"Mode: {img.mode}")
        
        # Try to extract text/symbols
        text = pytesseract.image_to_string(img)
        print("\nExtracted text:")
        print(text)
        
        return text
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return None

def decode_zodiac_symbols(text):
    """Decode zodiac symbols to letters"""
    result = []
    for char in text:
        if char in ZODIAC_SYMBOLS:
            sign = ZODIAC_SYMBOLS[char]
            letter = ZODIAC_TO_LETTER[sign]
            result.append(letter)
            print(f"{char} → {sign} → {letter}")
    
    decoded = ''.join(result)
    return decoded

def main():
    print("=" * 60)
    print("ZODIAC CIPHER SOLVER")
    print("=" * 60)
    
    image_path = "ciphertext.png"
    
    # Try to analyze the image
    print("\n[1] Analyzing image...")
    text = analyze_image(image_path)
    
    if text:
        print("\n[2] Decoding zodiac symbols...")
        decoded = decode_zodiac_symbols(text)
        
        if decoded:
            flag = f"ISFCR{{{decoded}}}"
            print("\n" + "=" * 60)
            print(f"FLAG: {flag}")
            print("=" * 60)
        else:
            print("\nNo zodiac symbols found in automatic extraction.")
            print("Please manually identify the symbols from the image.")
    
    # Manual input option
    print("\n" + "=" * 60)
    print("MANUAL DECODING MODE")
    print("=" * 60)
    print("Enter the zodiac symbols you see (use Unicode symbols):")
    print("♈=Aries, ♉=Taurus, ♊=Gemini, ♋=Cancer, ♌=Leo, ♍=Virgo")
    print("♎=Libra, ♏=Scorpio, ♐=Sagittarius, ♑=Capricorn, ♒=Aquarius, ♓=Pisces")
    print("\nOr enter zodiac sign names (comma-separated):")
    
    user_input = input("\nInput: ").strip()
    
    if user_input:
        # Check if Unicode symbols
        if any(char in ZODIAC_SYMBOLS for char in user_input):
            decoded = decode_zodiac_symbols(user_input)
        else:
            # Parse as names
            signs = [s.strip().capitalize() for s in user_input.split(',')]
            decoded = ''.join([ZODIAC_TO_LETTER.get(sign, '?') for sign in signs])
        
        flag = f"ISFCR{{{decoded}}}"
        print("\n" + "=" * 60)
        print(f"DECODED: {decoded}")
        print(f"FLAG: {flag}")
        print("=" * 60)

if __name__ == "__main__":
    main()
