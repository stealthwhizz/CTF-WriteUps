#!/usr/bin/env python3

# Read and decode binary data
with open('binary_data.txt', 'r') as f:
    binary = f.read().replace(' ', '').replace('\n', '')

# Convert to ASCII
decoded = ''
for i in range(0, len(binary), 8):
    byte = binary[i:i+8]
    if len(byte) == 8:
        decoded += chr(int(byte, 2))

# Try extracting uppercase letters only (might be a flag)
uppercase = ''.join(c for c in decoded if c.isupper())
print("Uppercase letters only:")
print(uppercase)
print()

# Try extracting based on specific ASCII ranges
print("Alphanumeric + underscore only:")
alphanum = ''.join(c for c in decoded if c.isalnum() or c == '_')
print(alphanum[:300])
print()

# Look for patterns in the data that might indicate flag format
import re

# Check if there's a pattern like ECH or Flag embedded
print("Searching for common CTF flag patterns...")
print()

# Maybe it's every Nth character?
for n in [2, 3, 4, 5]:
    every_nth = ''.join(decoded[i] for i in range(0, len(decoded), n) if decoded[i].isprintable())
    if 'Flag' in every_nth or 'flag' in every_nth or 'ECH' in every_nth:
        print(f"*** FOUND in every {n}th character! ***")
        print(every_nth[:200])
        for match in re.findall(r'[Ff]lag\{[^}]+\}|ECH\{[^}]+\}', every_nth):
            print(f"FLAG: {match}")

# Check the actual bytes for ASCII patterns
print("\nLooking at character codes for patterns...")
byte_values = [int(binary[i:i+8], 2) for i in range(0, len(binary), 8) if len(binary[i:i+8]) == 8]

# Check for flags in specific positions or patterns
print(f"First 50 byte values: {byte_values[:50]}")
print()

# Maybe flag is in specific bit positions?
# Let's try looking at odd/even positions
odd_chars = ''.join(decoded[i] for i in range(1, len(decoded), 2))
even_chars = ''.join(decoded[i] for i in range(0, len(decoded), 2))

print("Odd position characters (every other, starting at 1):")
print(odd_chars[:200])
if 'Flag' in odd_chars or 'ECH' in odd_chars:
    print("*** FOUND FLAG IN ODD POSITIONS! ***")
    for match in re.findall(r'[Ff]lag\{[^}]+\}|ECH\{[^}]+\}', odd_chars):
        print(f"FLAG: {match}")

print("\nEven position characters (every other, starting at 0):")
print(even_chars[:200])
if 'Flag' in even_chars or 'ECH' in even_chars:
    print("*** FOUND FLAG IN EVEN POSITIONS! ***")
    for match in re.findall(r'[Ff]lag\{[^}]+\}|ECH\{[^}]+\}', even_chars):
        print(f"FLAG: {match}")
