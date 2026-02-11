#!/usr/bin/env python3

# Ciphertext from the PDF (including the lowercase chars which are important!)
ciphertext = "CKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCyC" + \
               "EKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEK EKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKF"

def vigenere_decrypt(ciphertext, key):
    """Decrypt Vigenere cipher"""
    plaintext = []
    key = key.upper()
    key_length = len(key)
    
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            key_char = key[i % key_length]
            if char.isupper():
                decrypted = chr((ord(char) - ord(key_char) + 26) % 26 + ord('A'))
            else:
                decrypted = chr((ord(char.upper()) - ord(key_char) + 26) % 26 + ord('a'))
            plaintext.append(decrypted)
        else:
            plaintext.append(char)
    
    return ''.join(plaintext)

# Try theme-related keys
theme_keys = [
    "ARCHIVE", "ASHES", "ASH", "FIRE", "BURN", "ARCHIVEOFASHES", 
    "TRINETRA", "CTF", "VIGENERE", "VIG", "SECURE",
    "HACKDATA", "NETRA", "TRI"
]

print("Trying theme-related keys:")
print("="*70)

for key in theme_keys:
    result = vigenere_decrypt(ciphertext, key)
    print(f"\nKey: {key} (length {len(key)})")
    print(f"First 100 chars: {result[:100]}")
    print(f"Last 50 chars: {result[-50:]}")
    
    if "TriNetra{" in result or "{" in result:
        print(f"\n*** POTENTIAL FLAG FOUND ***")
        print(f"Full result: {result}")
        print("="*70)

# Also let's check if maybe we need to look at it differently
# Maybe the key repeats at a different interval?
print("\n" + "="*70)
print("Checking for readable text hints...")
print("="*70)

for length in range(1, 20):
    # Try keys of different lengths with common letters
    for key in ["A"*length, "E"*length, "T"*length]:
        result = vigenere_decrypt(ciphertext, key)
        # Look for common English patterns
        if "THE" in result.upper() or "AND" in result.upper():
            print(f"\nKey '{key}' gives: {result[:150]}")

print("\n" + "="*70)
print("Let me also check what 'ASHES' gives us in detail:")
print("="*70)
result_ashes = vigenere_decrypt(ciphertext, "ASHES")
print(result_ashes)
