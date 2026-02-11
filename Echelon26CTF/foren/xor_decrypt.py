#!/usr/bin/env python3

# The corrupted header was: aa d7 ba e0
# The correct header is:   ff d8 ff e0
# This gives us a potential key

corrupted = bytes.fromhex('aad7bae0')
correct = bytes.fromhex('ffd8ffe0')

# Calculate XOR key
xor_key = bytes([c ^ co for c, co in zip(correct, corrupted)])
print(f"XOR key from headers: {xor_key.hex()}")
print(f"XOR key bytes: {list(xor_key)}")

# Read binary data
with open('binary_data.txt', 'r') as f:
    binary = f.read()

binary = binary.replace(' ', '').replace('\n', '')

# Convert to bytes
bytes_data = []
for i in range(0, len(binary), 8):
    byte = binary[i:i+8]
    if len(byte) == 8:
        bytes_data.append(int(byte, 2))

print(f"\nTotal bytes: {len(bytes_data)}")

# Try XOR with repeating key
result = ''
for i, b in enumerate(bytes_data):
    xored = b ^ xor_key[i % len(xor_key)]
    result += chr(xored)

print("\nDecoded with XOR key from corrupted header:")
print(result[:500])

# Look for flag
import re
patterns = [r'[Ff]lag\{[^}]+\}', r'ECH\{[^}]+\}', r'ECHELON\{[^}]+\}']
for pattern in patterns:
    matches = re.findall(pattern, result)
    if matches:
        print(f"\n*** FOUND FLAG: {matches[0]} ***")

# Also try with just the first byte
print("\n" + "="*60)
print(f"Trying XOR with single byte: 0x{xor_key[0]:02x}")
result2 = ''
for b in bytes_data:
    xored = b ^ xor_key[0]
    if 32 <= xored <= 126:
        result2 += chr(xored)
    else:
        result2 += '.'

print(result2[:500])

for pattern in patterns:
    matches = re.findall(pattern, result2)
    if matches:
        print(f"\n*** FOUND FLAG: {matches[0]} ***")
