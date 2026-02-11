#!/usr/bin/env python3
"""
Focus on hidden regions - look at border pixels in groups
Extract with various offsets and alignments
"""

from PIL import Image
import re

def test_region_extraction(image_path, description, x_start, y_start, x_end, y_end):
    """Extract from a specific region"""
    img = Image.open(image_path)
    pixels = img.load()
    
    bits = ""
    for y in range(y_start, min(y_end, img.size[1])):
        for x in range(x_start, min(x_end, img.size[0])):
            pixel = pixels[x, y]
            bits += str(pixel[0] & 1)
    
    # Decode
    decoded = ""
    for i in range(0, len(bits) - 7, 8):
        byte_val = int(bits[i:i+8], 2)
        if 32 <= byte_val <= 126:
            decoded += chr(byte_val)
        else:
            decoded += f"[{byte_val}]"
    
    print(f"\n[{description}]")
    print(f"Bits: {len(bits)}, Decoded length: {len(decoded)}")
    print(f"Sample: {decoded[:120]}")
    
    # Look for patterns
    readable = re.findall(r'[A-Za-z_]{8,}', decoded)
    if readable:
        print(f"Readable: {readable[:5]}")

def test_bit_shift(image_path, description, bit_offset):
    """Try starting from a bit offset"""
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    
    # Extract all bits from top row
    all_bits = ""
    for x in range(width):
        pixel = pixels[x, 0]
        for i in range(8):
            all_bits += str((pixel[0] >> i) & 1)
    
    # Decode from offset
    decoded = ""
    for i in range(bit_offset, len(all_bits) - 7, 8):
        byte_val = int(all_bits[i:i+8], 2)
        if 32 <= byte_val <= 126:
            decoded += chr(byte_val)
        else:
            decoded += f"[{byte_val}]"
    
    readable = re.findall(r'[A-Za-z_]{6,}', decoded)
    if readable and any(len(r) > 10 for r in readable):
        print(f"\n[Offset {bit_offset}] {readable[:3]}")

def main():
    img = Image.open("bottom_section.png")
    width, height = img.size
    
    print(f"Image: {width}x{height}")
    
    # Test border stripes
    test_region_extraction("bottom_section.png", "Top 1 pixel row", 0, 0, width, 1)
    test_region_extraction("bottom_section.png", "Top 2 pixel rows", 0, 0, width, 2)
    test_region_extraction("bottom_section.png", "Top 10 pixel rows", 0, 0, width, 10)
    test_region_extraction("bottom_section.png", "Top-left 10x10", 0, 0, 10, 10)
    test_region_extraction("bottom_section.png", "Top-right corner 10x10", width-10, 0, width, 10)
    test_region_extraction("bottom_section.png", "Left 10 pixels wide", 0, 0, 10, height)
    
    # Test bit offsets in top row
    print("\n[Testing bit offsets on top row]")
    for offset in [0, 1, 2, 3, 4, 5, 6, 7]:
        test_bit_shift("bottom_section.png", f"Offset {offset}", offset)

if __name__ == "__main__":
    main()
