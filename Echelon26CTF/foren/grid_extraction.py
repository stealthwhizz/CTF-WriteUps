#!/usr/bin/env python3
"""
Systematically extract LSB from specific regions
Try:
1. Corner pixels only
2. Diagonal pixels
3. Grid pattern
"""

from PIL import Image
import re

def extract_from_grid(image_path, start_x=0, start_y=0, step_x=1, step_y=1, lsb_only=True):
    """Extract bits from a grid pattern of pixels"""
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    
    bits = ""
    count = 0
    
    x, y = start_x, start_y
    while y < height:
        while x < width:
            pixel = pixels[x, y]
            if lsb_only:
                # Just LSB from R channel
                bits += str(pixel[0] & 1)
            else:
                # All 8 bits from R channel
                for i in range(8):
                    bits += str((pixel[0] >> i) & 1)
            x += step_x
            count += 1
        x = start_x
        y += step_y
    
    return bits, count

def decode_ascii(bits):
    """Decode 8-bit chunks"""
    text = ""
    for i in range(0, len(bits) - 7, 8):
        byte_val = int(bits[i:i+8], 2)
        if 32 <= byte_val <= 126:
            text += chr(byte_val)
        else:
            text += f"[{byte_val}]"
    return text

def main():
    print("[*] Systematic grid extraction from PNG edges and corners")
    print()
    
    img = Image.open("bottom_section.png")
    width, height = img.size
    print(f"Image size: {width}x{height}")
    print()
    
    # Try extracting from 1st row only (top edge as one line)
    print("[TOP ROW - Full 8-bit]")
    bits, _ = extract_from_grid("bottom_section.png", 0, 0, 1, 1000, lsb_only=False)
    decoded = decode_ascii(bits)
    print(f"Length: {len(bits)} bits")
    print(f"Sample: {decoded[:150]}")
    flags = re.findall(r'[A-Za-z_][^[\]]{10,}', decoded)
    if flags:
        print(f"Candidates: {flags[:3]}")
    print()
    
    # Try extracting from 1st column only (left edge as one line)
    print("[LEFT COLUMN - Full 8-bit]")
    bits, _ = extract_from_grid("bottom_section.png", 0, 0, 1000, 1, lsb_only=False)
    decoded = decode_ascii(bits)
    print(f"Length: {len(bits)} bits")
    print(f"Sample: {decoded[:150]}")
    flags = re.findall(r'[A-Za-z_][^[\]]{10,}', decoded)
    if flags:
        print(f"Candidates: {flags[:3]}")
    print()
    
    # Try alternating bit extraction from top-left to bottom-right diagonal
    print("[DIAGONAL extraction - LSB only]")
    img_pixels = img.load()
    diag_bits = ""
    for i in range(min(width, height)):
        pixel = img_pixels[i, i]
        diag_bits += str(pixel[0] & 1)
    decoded = decode_ascii(diag_bits)
    print(f"Length: {len(diag_bits)} bits")
    print(f"Decoded: {decoded[:150]}")
    print()
    
    # Try specific corner region (first 4x4 pixels)
    print("[CORNER REGION extraction - Full bits]")
    corner_bits = ""
    for y in range(min(4, height)):
        for x in range(min(4, width)):
            pixel = img_pixels[x, y]
            for i in range(8):
                corner_bits += str((pixel[0] >> i) & 1)
    decoded = decode_ascii(corner_bits)
    print(f"Length: {len(corner_bits)} bits")
    print(f"Decoded: {decoded}")

if __name__ == "__main__":
    main()
