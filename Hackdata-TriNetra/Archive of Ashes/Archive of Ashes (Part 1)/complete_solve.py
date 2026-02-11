#!/usr/bin/env python3

# Complete ciphertext extracted from the PDF - it's in 3 parts:
# 1. CKCK...CyC
# 2. DRDRDRDRD
# 3. EKEK...ekf

cipher_part1 = "CKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCyC"
cipher_part2 = "DRDRDRDRD"
cipher_part3 = "EKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKF"

ciphertext = cipher_part1 + cipher_part2 + cipher_part3

print(f"Total ciphertext length: {len(ciphertext)}")
print(f"Part 1 length: {len(cipher_part1)}")
print(f"Part 2 length: {len(cipher_part2)}")
print(f"Part 3 length: {len(cipher_part3)}")
print()

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

# Try the complete alphabet as keys
print("="*70)
print("Testing all 2-character keys and looking for flags...")
print("="*70)

found_flags = []

for first in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    for second in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        key = first + second
        result = vigenere_decrypt(ciphertext, key)
        
        # Look for flag patterns or readable text
        if "{" in result:
            print(f"\nKey {key}: Found '{{' in result")
            print(result)
            found_flags.append((key, result))
        elif "TriNetra" in result or "trinetra" in result.lower():
            print(f"\nKey {key}: Found 'TriNetra'")
            print(result)
            found_flags.append((key, result))

if found_flags:
    print(f"\n\n{'='*70}")
    print(f"FOUND {len(found_flags)} POTENTIAL FLAGS")
    print(f"{'='*70}")
    for key, flag in found_flags:
        print(f"\nKey: {key}")
        print(f"Flag: {flag}")
else:
    print("\nNo flags found with 2-char keys. Let me try some longer keys...")
    
    # Try longer keys
    for key in ["ARCHIVE", "ASHES", "ASH", "FIRE", "CK", "ARCHIVEOFASHES", "VIG"]:
        result = vigenere_decrypt(ciphertext, key)
        print(f"\nKey '{key}':")
        print(f"  First 100: {result[:100]}")
        print(f"  Last 100: {result[-100:]}")
        
        if "{" in result or "flag" in result.lower():
            print(f"  *** Contains special chars or 'flag' ***")
            print(f"  Full: {result}")
