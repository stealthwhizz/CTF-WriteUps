#!/usr/bin/env python3
"""
Extract and decode zodiac cipher from image
"""

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Installing required libraries...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'pillow', 'numpy'])
    from PIL import Image
    import numpy as np

# Zodiac symbols to letters
ZODIAC_MAP = {
    "♈": "A",  # Aries
    "♉": "T",  # Taurus
    "♊": "G",  # Gemini
    "♋": "C",  # Cancer
    "♌": "L",  # Leo
    "♍": "V",  # Virgo
    "♎": "L",  # Libra
    "♏": "S",  # Scorpio
    "♐": "S",  # Sagittarius
    "♑": "C",  # Capricorn
    "♒": "A",  # Aquarius
    "♓": "P",  # Pisces
}

def extract_text_from_image(image_path):
    """Try to extract text from image using OCR"""
    try:
        import pytesseract
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng')
        return text
    except:
        return None

def show_image_info(image_path):
    """Display image information"""
    img = Image.open(image_path)
    print(f"Image: {image_path}")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")
    print(f"Format: {img.format}")
    
    # Try to get text
    text = extract_text_from_image(image_path)
    if text:
        print(f"\nExtracted text:\n{text}")
        
        # Try to decode
        decoded = ""
        for char in text:
            if char in ZODIAC_MAP:
                decoded += ZODIAC_MAP[char]
        
        if decoded:
            print(f"\nDecoded: {decoded}")
            print(f"FLAG: ISFCR{{{decoded}}}")
            return decoded
    
    return None

def manual_decode():
    """Manual decoding interface"""
    print("\n" + "=" * 60)
    print("MANUAL DECODING")
    print("=" * 60)
    print("\nOpen ciphertext.png and identify the zodiac symbols.")
    print("\nZodiac Symbol Map:")
    print("♈ Aries → A")
    print("♉ Taurus → T")
    print("♊ Gemini → G")
    print("♋ Cancer → C")
    print("♌ Leo → L")
    print("♍ Virgo → V")
    print("♎ Libra → L")
    print("♏ Scorpio → S")
    print("♐ Sagittarius → S")
    print("♑ Capricorn → C")
    print("♒ Aquarius → A")
    print("♓ Pisces → P")
    
    print("\nEnter the sequence of symbols you see:")
    print("(You can use symbols like ♈♌♊ or names like Aries,Leo,Gemini)")
    
    user_input = input("\nInput: ").strip()
    
    if not user_input:
        return None
    
    # Decode
    decoded = ""
    
    # Check if using symbols
    if any(char in ZODIAC_MAP for char in user_input):
        for char in user_input:
            if char in ZODIAC_MAP:
                decoded += ZODIAC_MAP[char]
    else:
        # Assume names
        names = [n.strip().capitalize() for n in user_input.split(',')]
        name_map = {
            "Aries": "A", "Taurus": "T", "Gemini": "G", "Cancer": "C",
            "Leo": "L", "Virgo": "V", "Libra": "L", "Scorpio": "S",
            "Sagittarius": "S", "Capricorn": "C", "Aquarius": "A", "Pisces": "P"
        }
        for name in names:
            if name in name_map:
                decoded += name_map[name]
    
    if decoded:
        print(f"\nDecoded: {decoded}")
        print(f"\nFLAG: ISFCR{{{decoded}}}")
        return decoded
    
    return None

if __name__ == "__main__":
    print("=" * 60)
    print("ZODIAC CIPHER SOLVER - STAR CTF")
    print("=" * 60)
    
    result = show_image_info("ciphertext.png")
    
    if not result:
        manual_decode()
