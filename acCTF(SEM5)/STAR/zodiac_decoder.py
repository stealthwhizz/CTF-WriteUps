#!/usr/bin/env python3
"""
Zodiac Cipher Decoder
Decodes messages using zodiac sign mappings
"""

# Zodiac signs in order
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Method 1: First letter of each zodiac sign
def decode_by_first_letter(zodiac_sequence):
    """Decode using first letter of zodiac sign names"""
    return ''.join([sign[0] for sign in zodiac_sequence])

# Method 2: Position in zodiac wheel (1-12) mapped to alphabet (A-L or continuing)
def decode_by_position(zodiac_sequence):
    """Decode using position of zodiac sign (1=A, 2=B, etc.)"""
    result = []
    for sign in zodiac_sequence:
        pos = ZODIAC_SIGNS.index(sign) + 1  # 1-indexed
        # Simple mapping: position to letter (1=A, 2=B, ..., 12=L)
        if pos <= 26:
            result.append(chr(64 + pos))  # 65 is 'A'
    return ''.join(result)

# Method 3: Zodiac symbols to their astrological letters
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

def decode_by_mapping(zodiac_sequence):
    """Decode using first letter mapping"""
    return ''.join([ZODIAC_TO_LETTER.get(sign, '?') for sign in zodiac_sequence])

# Example usage
if __name__ == "__main__":
    print("Zodiac Cipher Decoder")
    print("=" * 50)
    print("\nZodiac Signs (in order):")
    for i, sign in enumerate(ZODIAC_SIGNS, 1):
        print(f"{i:2d}. {sign:12s} → {ZODIAC_TO_LETTER[sign]}")
    
    print("\n" + "=" * 50)
    print("Enter your cipher as zodiac sign names (comma-separated)")
    print("Example: Aries,Leo,Gemini")
    print("Or type 'test' to see an example")
    print("=" * 50)
    
    user_input = input("\nEnter sequence: ").strip()
    
    if user_input.lower() == 'test':
        # Test with the hint signs
        test_sequence = ["Aries", "Leo", "Gemini"]
        print(f"\nTest sequence: {', '.join(test_sequence)}")
        print(f"Method 1 (First Letter): {decode_by_first_letter(test_sequence)}")
        print(f"Method 2 (Position): {decode_by_position(test_sequence)}")
        print(f"Method 3 (Mapping): {decode_by_mapping(test_sequence)}")
    elif user_input:
        # Parse user input
        zodiac_sequence = [s.strip().capitalize() for s in user_input.split(',')]
        
        # Validate input
        valid = all(sign in ZODIAC_SIGNS for sign in zodiac_sequence)
        if not valid:
            print("\nError: Invalid zodiac sign names. Please use:")
            print(", ".join(ZODIAC_SIGNS))
        else:
            print(f"\nDecoding: {', '.join(zodiac_sequence)}")
            print(f"Method 1 (First Letter): {decode_by_first_letter(zodiac_sequence)}")
            print(f"Method 2 (Position): {decode_by_position(zodiac_sequence)}")
            print(f"Method 3 (Mapping): {decode_by_mapping(zodiac_sequence)}")
