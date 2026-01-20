#!/usr/bin/env python3
"""
Detailed pixel analysis to find the correct decoding pattern
Look at corners and border pixels systematically
"""

from PIL import Image

def analyze_pixels_detailed():
    """Examine pixel values at critical locations"""
    img = Image.open("bottom_section.png")
    pixels = img.load()
    width, height = img.size
    
    print(f"Image size: {width}x{height}")
    print(f"Mode: {img.mode}")
    print()
    
    # Examine corners
    corners = [
        ("TL", 0, 0),
        ("TR", width-1, 0),
        ("BL", 0, height-1),
        ("BR", width-1, height-1),
    ]
    
    print("[Corner Pixels]")
    for name, x, y in corners:
        pixel = pixels[x, y]
        print(f"{name} ({x},{y}): {pixel}")
        if isinstance(pixel, tuple):
            print(f"  R={pixel[0]:08b} ({pixel[0]:3d})")
            print(f"  G={pixel[1]:08b} ({pixel[1]:3d})")
            print(f"  B={pixel[2]:08b} ({pixel[2]:3d})")
            lsb_r = pixel[0] & 1
            lsb_g = pixel[1] & 1
            lsb_b = pixel[2] & 1
            print(f"  LSB: R={lsb_r} G={lsb_g} B={lsb_b}")
    
    # Look at first few rows and columns
    print("\n[First 8 pixels of first row]")
    for x in range(min(8, width)):
        pixel = pixels[x, 0]
        if isinstance(pixel, tuple):
            print(f"({x},0): RGB={pixel} -> LSBs: R={pixel[0]&1} G={pixel[1]&1} B={pixel[2]&1}")
    
    # Look for patterns in border regions (8 pixels in)
    print("\n[Border region (8 pixels in from top-left)]")
    for y in range(min(8, height)):
        for x in range(min(8, width)):
            pixel = pixels[x, y]
            if isinstance(pixel, tuple):
                r_lsb = pixel[0] & 1
                g_lsb = pixel[1] & 1
                b_lsb = pixel[2] & 1
                combined = f"{r_lsb}{g_lsb}{b_lsb}"
                print(f"({x:2},{y:2}): RGB={combined} value={int(combined,2):3d} char={chr(int(combined,2)) if 32<=int(combined,2)<=126 else '?'}")
    
    # Extract 3-bit values from border
    print("\n[Attempting 3-bit decode of top edge]")
    bits_3 = ""
    for x in range(width):
        pixel = pixels[x, 0]
        if isinstance(pixel, tuple):
            bits_3 += str(pixel[0] & 1) + str(pixel[1] & 1) + str(pixel[2] & 1)
    
    decoded = ""
    for i in range(0, len(bits_3) - 7, 8):
        byte_val = int(bits_3[i:i+8], 2)
        if 32 <= byte_val <= 126:
            decoded += chr(byte_val)
        else:
            decoded += f"[{byte_val}]"
    
    print(f"Result: {decoded[:200]}")

if __name__ == "__main__":
    analyze_pixels_detailed()
