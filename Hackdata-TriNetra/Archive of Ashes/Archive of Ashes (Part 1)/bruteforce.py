#!/usr/bin/env python3

# Ciphertext from the PDF
ciphertext = "CKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCyC" + \
               "EKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKF"

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

print("Brute forcing all 2-character keys...")
print("="*70)

results = []

for first in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    for second in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        key = first + second
        result = vigenere_decrypt(ciphertext, key)
        
        # Look for flag format or interesting patterns
        if "{" in result and "}" in result:
            results.append((key, result))
            print(f"\nKey: {key}")
            print(f"Result: {result}")
            print("-" * 70)
        elif result[:20].replace(result[0], '').replace(result[1], '') == '':
            # This means the first 20 chars are just two characters alternating
            # Could be interesting
            continue
        elif "trinetra" in result.lower() or "flag" in result.lower():
            results.append((key, result))
            print(f"\nKey: {key}")
            print(f"Result: {result}")
            print("-" * 70)

if results:
    print(f"\n\n{'='*70}")
    print(f"Found {len(results)} potential results")
    print(f"{'='*70}")
    for key, result in results:
        print(f"\nKey: {key}")
        print(f"Result: {result}")
else:
    print("\nNo obvious flag found. Let me show some interesting patterns...")
    
    # Show results that look interesting (not just repeating chars)
    for key in ["AB", "CK", "VI", "AS", "KE", "AR", "CH", "IV", "ES"]:
        result = vigenere_decrypt(ciphertext, key)
        unique_section = result[100:150]
        if len(set(unique_section)) > 2:  # More than 2 unique chars
            print(f"\nKey {key}: {result[:200]}")
