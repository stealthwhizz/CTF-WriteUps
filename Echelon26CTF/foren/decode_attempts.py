#!/usr/bin/env python3
import base64
import codecs

# Read and decode binary data
with open('binary_data.txt', 'r') as f:
    binary = f.read().replace(' ', '').replace('\n', '')

# Convert to ASCII
decoded = ''
for i in range(0, len(binary), 8):
    byte = binary[i:i+8]
    if len(byte) == 8:
        decoded += chr(int(byte, 2))

print("Original decoded text (first 200 chars):")
print(decoded[:200])
print()

# Try ROT13
print("="*60)
print("ROT13:")
try:
    rot13 = codecs.decode(decoded, 'rot_13')
    print(rot13[:200])
    if 'Flag{' in rot13 or 'flag{' in rot13 or 'ECH{' in rot13:
        print("\n*** FOUND FLAG IN ROT13! ***")
        import re
        for match in re.findall(r'[Ff]lag\{[^}]+\}|ECH\{[^}]+\}', rot13):
            print(f"FLAG: {match}")
except Exception as e:
    print(f"Error: {e}")

# Try reversing
print("\n" + "="*60)
print("Reversed:")
reversed_text = decoded[::-1]
print(reversed_text[:200])
if 'Flag{' in reversed_text or 'flag{' in reversed_text:
    print("\n*** FOUND FLAG IN REVERSED! ***")
    import re
    for match in re.findall(r'[Ff]lag\{[^}]+\}|ECH\{[^}]+\}', reversed_text):
        print(f"FLAG: {match}")

# Try Caesar shifts
print("\n" + "="*60)
print("Trying Caesar cipher shifts...")
for shift in range(1, 26):
    shifted = ''
    for char in decoded:
        if 'a' <= char <= 'z':
            shifted += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            shifted += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            shifted += char
    
    if 'Flag{' in shifted or 'flag{' in shifted or 'ECH{' in shifted:
        print(f"\n*** FOUND FLAG WITH SHIFT {shift}! ***")
        print(shifted[:300])
        import re
        for match in re.findall(r'[Ff]lag\{[^}]+\}|ECH\{[^}]+\}', shifted):
            print(f"FLAG: {match}")
        break

# Check if it's base64 or hex encoded
print("\n" + "="*60)
print("Checking for base64/hex patterns...")

# Look for flag-like patterns after various transforms
import re
# Maybe the numbers are significant?
numbers_only = ''.join(c for c in decoded if c.isdigit())
print(f"Numbers only (first 100): {numbers_only[:100]}")

# Maybe letters only?
letters_only = ''.join(c for c in decoded if c.isalpha())
print(f"Letters only (first 100): {letters_only[:100]}")

if 'Flag' in letters_only or 'flag' in letters_only or 'ECH' in letters_only:
    print("\n*** FOUND FLAG IN LETTERS ONLY! ***")
    for match in re.findall(r'[Ff]lag[A-Za-z]+|ECH[A-Za-z]+', letters_only):
        print(f"Potential flag: {match}")
