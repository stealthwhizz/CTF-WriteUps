#!/usr/bin/env python3
from PIL import Image
import numpy as np

# Open the PNG
img = Image.open('bottom_section.png')
arr = np.array(img)

print(f"Image shape: {arr.shape}")

# Try extracting LSB from each color channel separately
for channel_idx, channel_name in enumerate(['Red', 'Green', 'Blue']):
    print(f"\n{'='*60}")
    print(f"Channel: {channel_name} (index {channel_idx})")
    
    channel_data = arr[:, :, channel_idx]
    flat = channel_data.flatten()
    
    # Extract LSB
    lsb_bits = ''.join(str(byte_val & 1) for byte_val in flat)
    
    # Decode as ASCII
    decoded = ''
    for i in range(0, len(lsb_bits) - 8, 8):
        byte_bits = lsb_bits[i:i+8]
        char_code = int(byte_bits, 2)
        if 32 <= char_code < 127:
            decoded += chr(char_code)
        else:
            decoded += '.'
    
    print(f"Decoded (first 300 chars): {decoded[:300]}")
    
    if 'Flag' in decoded or 'flag' in decoded or 'ECH{' in decoded:
        print(f"*** FOUND FLAG IN {channel_name}! ***")
        import re
        for pattern in [r'[Ff]lag\{[^}]*\}', r'ECH\{[^}]*\}']:
            matches = re.findall(pattern, decoded)
            for m in matches:
                print(f"FLAG: {m}")

# Also try combining all LSBs from all channels
print(f"\n{'='*60}")
print("Combining all channels (interleaved):")

lsb_all = []
for pixel_row in arr:
    for pixel in pixel_row:
        for channel_val in pixel:
            lsb_all.append(str(channel_val & 1))

lsb_string = ''.join(lsb_all)
decoded_all = ''
for i in range(0, len(lsb_string) - 8, 8):
    byte_bits = lsb_string[i:i+8]
    char_code = int(byte_bits, 2)
    if 32 <= char_code < 127:
        decoded_all += chr(char_code)
    else:
        decoded_all += '.'

print(f"Decoded (first 300 chars): {decoded_all[:300]}")

if 'Flag' in decoded_all or 'flag' in decoded_all:
    print("*** FOUND FLAG! ***")
    import re
    for pattern in [r'[Ff]lag\{[^}]*\}', r'ECH\{[^}]*\}']:
        matches = re.findall(pattern, decoded_all)
        for m in matches:
            print(f"FLAG: {m}")
