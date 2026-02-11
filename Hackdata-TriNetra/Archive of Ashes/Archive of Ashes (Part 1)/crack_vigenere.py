#!/usr/bin/env python3
import collections

# Ciphertext from the PDF
ciphertext_lines = [
    "CKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCyC",
    "EKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKF"
]

ciphertext = ''.join(ciphertext_lines)

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

# The pattern analysis
print("Analyzing the ciphertext pattern:")
print(f"First 120 chars: {ciphertext[:120]}")
print(f"Pattern: {'CK' * 60}")
print()

# Count character frequencies
print("Character frequency:")
counter = collections.Counter(ciphertext)
for char, count in sorted(counter.items()):
    print(f"  {char}: {count}")
print()

# The pattern is almost entirely CK and EK repeating
# This suggests the key is 2 characters long and the plaintext is also repetitive

# Let's try different 2-character keys
print("Trying 2-character keys:")
for first in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    for second in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        key = first + second
        result = vigenere_decrypt(ciphertext, key)
        
        # Look for flag format
        if "TriNetra{" in result or "trinetra{" in result.lower():
            print(f"\n*** FOUND FLAG with key: {key} ***")
            print(result)
            break
        # Look for common words
        elif "flag" in result.lower() or "the " in result.lower():
            print(f"Possible key {key}: {result[:100]}")
    else:
        continue
    break

# Alternative: Try known plaintext attack
# If we assume the plaintext starts with something like "TriNetra" or "flag"
print("\n" + "="*60)
print("Trying known plaintext attack...")
print("="*60)

# Assuming plaintext might start with "TriNetra"
potential_plaintexts = ["TriNetra", "TRINETRA", "FLAG", "flag", "the", "THE"]

for pt in potential_plaintexts:
    # Calculate key from first few characters
    pt = pt.upper()
    if len(ciphertext) >= len(pt):
        key_chars = []
        for i in range(min(len(pt), len(ciphertext))):
            if ciphertext[i].isalpha() and pt[i].isalpha():
                # Key = Cipher - Plain (mod 26)
                key_char = chr((ord(ciphertext[i]) - ord(pt[i]) + 26) % 26 + ord('A'))
                key_chars.append(key_char)
        
        if key_chars:
            # Try to find repeating pattern in key
            potential_key = ''.join(key_chars[:2])
            print(f"\nIf plaintext starts with '{pt}', key might be: {potential_key}")
            result = vigenere_decrypt(ciphertext, potential_key)
            print(f"Decrypted: {result[:150]}")

# Since the ciphertext has a very strong CK and EK pattern, 
# let's try to figure out what single character repeated would give us this
print("\n" + "="*60)
print("Analysis: What repeated plaintext gives us CK and EK?")
print("="*60)

# If plaintext is same character repeated and KEY is 2 chars
# P + K[0] = C, P + K[1] = K (for CKCK part)
# P + K[0] = E, P + K[1] = K (for EKEK part)

# From CKCK: P + K[0] = C, P + K[1] = K
# From EKEK: P' + K[0] = E, P' + K[1] = K

# Since K[1] appears in both: P + K[1] = K and P' + K[1] = K
# This means P = P', so same plaintext character!

# From first: P + K[0] = C (2), P + K[1] = K (10)
# So K[1] - K[0] = 8

# From EKEK: P + K[0] = E (4)
# So P = E - K[0] and P = C - K[0]
# This is impossible unless... wait, they must be different plaintext chars

# Let me recalculate assuming DIFFERENT positions map to different plaintext
print("\nLet's try systematic brute force with common keys:")

common_keys = ["KEY", "VIG", "CODE", "PASS", "HIDE", "SECRET", "CRYPTO", "ENIGMA", 
               "CIPHER", "ASHES", "FIRE", "BURN", "ASH", "ARCHIVE"]

for key in common_keys:
    result = vigenere_decrypt(ciphertext, key)
    if "TriNetra" in result or any(word in result.lower() for word in ["flag", "ctf", "trinetra"]):
        print(f"\n*** Potential match with key '{key}': ***")
        print(result[:300])
