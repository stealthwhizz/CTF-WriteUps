#!/usr/bin/env python3
from PIL import Image
import re

# Open the PNG
img = Image.open('bottom_section.png')

# Just try red channel LSB
pixels = img.getdata()
lsb_bits = ''.join(str((pixel[0] if isinstance(pixel, tuple) else pixel) & 1) for pixel in pixels)

# Decode as ASCII - take first 2000 bits (250 bytes)
decoded = ''
for i in range(0, min(2000, len(lsb_bits)), 8):
    byte_bits = lsb_bits[i:i+8]
    if len(byte_bits) == 8:
        char_code = int(byte_bits, 2)
        if 32 <= char_code < 127:
            decoded += chr(char_code)

print("LSB Red channel decoded:")
print(decoded)

if 'Flag' in decoded or 'flag' in decoded or 'ECH{' in decoded:
    print("\n*** FOUND FLAG! ***")
    for pattern in [r'[Ff]lag\{[^}]*\}', r'ECH\{[^}]*\}']:
        matches = re.findall(pattern, decoded)
        for m in matches:
            print(f"FLAG: {m}")
