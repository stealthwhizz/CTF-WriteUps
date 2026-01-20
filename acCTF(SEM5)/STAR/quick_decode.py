#!/usr/bin/env python3
"""
Quick Zodiac Decoder - Based on Hints
"""

# Based on the hints:
# Hint 1: "Aries begins the hunt, Gemini hides a twin meaning, and Leo guards the answer"
# Hint 2: "The constellations might spell them"

# Zodiac to letter mapping (first letter of each sign)
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

# Common Zodiac Killer cipher patterns
# The challenge mentions "symbols" - circles, triangles, crosses, squares
# These might map to zodiac signs

print("Zodiac Cipher Decoder")
print("=" * 50)
print("\nPlease describe or enter the symbols you see:")
print("Format: Enter zodiac symbols or their names")
print("\nZodiac Symbol Reference:")
for symbol, letter in ZODIAC_MAP.items():
    print(f"  {symbol} → {letter}")

print("\n" + "=" * 50)

# Try common patterns based on "ZODIAC" theme
test_patterns = [
    "♋♒♓♉♈♊♏",  # CAPTAS
    "♊♏♍♌♒♓",    # GSVLAP
]

print("\nTesting common patterns:")
for pattern in test_patterns:
    decoded = ''.join([ZODIAC_MAP.get(s, s) for s in pattern])
    print(f"{pattern} → {decoded} → ISFCR{{{decoded}}}")

# Manual input
print("\n" + "=" * 50)
symbols = input("\nEnter the symbols from the image (or press Enter to skip): ").strip()

if symbols:
    decoded = ''.join([ZODIAC_MAP.get(s, s) for s in symbols])
    print(f"\nDecoded: {decoded}")
    print(f"FLAG: ISFCR{{{decoded}}}")
