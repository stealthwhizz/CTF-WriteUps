#!/usr/bin/env python3

with open('binary_data.txt', 'r') as f:
    content = f.read()

# Split into binary values
lines = content.strip().split()

# Convert each to decimal/ASCII
decoded_bytes = []
for line in lines:
    if line:
        decoded_bytes.append(int(line, 2))

print(f"Total bytes: {len(decoded_bytes)}")

# Find where padding starts - look for long runs of the same character
# Count consecutive identical bytes from the end
padding_start = len(decoded_bytes) - 1
while padding_start > 0 and decoded_bytes[padding_start] == decoded_bytes[padding_start - 1]:
    padding_start -= 1

print(f"Padding starts at index: {padding_start}")
print(f"Padding value: {decoded_bytes[padding_start]} ('{chr(decoded_bytes[padding_start])}')")
print(f"Padding length: {len(decoded_bytes) - padding_start} bytes")

# Get the actual meaningful data
actual_data = decoded_bytes[:padding_start]
print(f"\nActual data length: {len(actual_data)} bytes")

# Decode actual data
decoded_str = ''.join(chr(b) for b in actual_data)
print("\nDecoded actual data:")
print(decoded_str)

# Look for flags
import re
patterns = [r'[Ff]lag\{[^}]*\}', r'ECH\{[^}]*\}', r'\{[^}]+\}']
for pattern in patterns:
    matches = re.findall(pattern, decoded_str)
    if matches:
        print(f"\nFOUND with pattern '{pattern}':")
        for m in matches:
            print(f"  {m}")

# Also extract alphanumeric only
alphanum = ''.join(c for c in decoded_str if c.isalnum() or c in '{}_ ')
print("\nAlphanumeric only (first 200):")
print(alphanum[:200])

if 'Flag' in alphanum or 'flag' in alphanum:
    print("\nFOUND 'flag' in alphanumeric!")
    for match in re.findall(r'[Ff]lag[a-zA-Z0-9_}]*', alphanum):
        print(f"  {match}")
