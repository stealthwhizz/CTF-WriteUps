#!/usr/bin/env python3
# Search for flag patterns in the decoded binary

with open('binary_data.txt', 'r') as f:
    binary = f.read()

# Remove spaces and newlines
binary = binary.replace(' ', '').replace('\n', '')

# Convert binary to ASCII
result = ''
for i in range(0, len(binary), 8):
    byte = binary[i:i+8]
    if len(byte) == 8:
        result += chr(int(byte, 2))

print("Full decoded text:")
print(result)
print("\n" + "="*60)

# Look for patterns that might be flags
import re

# Search for common flag patterns
patterns = [
    r'[Ff]lag\{[^}]+\}',
    r'ECH\{[^}]+\}',
    r'ECHELON\{[^}]+\}',
    r'\{[A-Za-z0-9_]+\}',
]

for pattern in patterns:
    matches = re.findall(pattern, result)
    if matches:
        print(f"\nFound with pattern '{pattern}':")
        for match in matches:
            print(f"  {match}")

# Also look for split flag parts
print("\n" + "="*60)
print("Looking for curly braces (potential flag delimiters):")
if '{' in result:
    print(f"Found {{ at positions: {[i for i, c in enumerate(result) if c == '{']}")
if '}' in result:
    print(f"Found }} at positions: {[i for i, c in enumerate(result) if c == '}']}")

# Print all characters around braces
for i, c in enumerate(result):
    if c in '{}':
        start = max(0, i-20)
        end = min(len(result), i+20)
        print(f"\nContext around {c} at position {i}:")
        print(f"  ...{result[start:end]}...")
