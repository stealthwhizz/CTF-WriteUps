#!/usr/bin/env python3
"""
Zodiac Cipher - Complete Solver
Based on hints about Aries, Gemini, and Leo being important
"""

# Zodiac symbol to letter mapping
ZODIAC_DECODE = {
    # Symbols
    "♈": "A", "♉": "T", "♊": "G", "♋": "C", "♌": "L", "♍": "V",
    "♎": "L", "♏": "S", "♐": "S", "♑": "C", "♒": "A", "♓": "P",
    # Names
    "Aries": "A", "Taurus": "T", "Gemini": "G", "Cancer": "C",
    "Leo": "L", "Virgo": "V", "Libra": "L", "Scorpio": "S",
    "Sagittarius": "S", "Capricorn": "C", "Aquarius": "A", "Pisces": "P"
}

def decode(sequence):
    """Decode a sequence of zodiac signs"""
    result = ""
    for item in sequence:
        result += ZODIAC_DECODE.get(item, "?")
    return result

# Common patterns to try based on Zodiac Killer ciphers
print("=" * 70)
print("ZODIAC CIPHER SOLVER - STAR CTF")
print("=" * 70)

# The hints mention: Aries (A), Gemini (G), Leo (L)
# "The constellations might spell them"

# Try some common patterns
test_sequences = [
    # Common words with zodiac signs
    (["♊", "♏", "♍", "♌", "♒", "♓"], "Pattern 1"),
    (["♋", "♈", "♓", "♉", "♈", "♊", "♏"], "Pattern 2"),
    (["♌", "♏", "♉", "♈", "♏", "♊", "♈", "♊", "♏"], "Pattern 3"),
    (["Sagittarius", "Taurus", "Aries", "Scorpio", "Pisces", "Aries", "Cancer", "Leo"], "STARSPACE?"),
]

print("\nTesting common patterns:")
for seq, name in test_sequences:
    decoded = decode(seq)
    print(f"{name}: {decoded} → ISFCR{{{decoded}}}")

print("\n" + "=" * 70)
print("INTERACTIVE MODE")
print("=" * 70)
print("\nLook at ciphertext.png and identify the zodiac symbols.")
print("\nQuick Reference:")
print("  ♈=A(ries)  ♉=T(aurus)  ♊=G(emini)  ♋=C(ancer)")
print("  ♌=L(eo)    ♍=V(irgo)   ♎=L(ibra)   ♏=S(corpio)")
print("  ♐=S(agittarius) ♑=C(apricorn) ♒=A(quarius) ♓=P(isces)")

print("\nEnter the zodiac sequence (symbols or single letters):")
print("Examples: ♈♌♊ or ALG or Aries,Leo,Gemini")

user_input = input("\n> ").strip()

if user_input:
    decoded = ""
    
    # Parse input
    if "," in user_input:
        # Comma-separated names
        signs = [s.strip().capitalize() for s in user_input.split(",")]
        decoded = decode(signs)
    elif any(c in ZODIAC_DECODE for c in user_input):
        # Symbols or single letters
        decoded = decode(list(user_input))
    else:
        # Try as continuous string of letters
        decoded = user_input
    
    print(f"\nDecoded message: {decoded}")
    print(f"\n{'=' * 70}")
    print(f"FLAG: ISFCR{{{decoded}}}")
    print(f"{'=' * 70}")
else:
    print("\nNo input provided. Please run again and enter the zodiac sequence.")
