#!/usr/bin/env python3
"""
Extract using different bit patterns from edges
Try skipping bits, using upper bits, etc.
"""

from PIL import Image
import re

def get_edge_pixels_bits(image_path, edge='top', bits_per_pixel=8):
    """Extract all bits from an edge"""
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    
    all_bits = []
    
    if edge == 'top':
        for col in range(width):
            pixel = pixels[col, 0]
            # Extract all 8 bits of R channel
            for i in range(8):
                bit = (pixel[0] >> i) & 1
                all_bits.append(str(bit))
    
    elif edge == 'left':
        for row in range(height):
            pixel = pixels[0, row]
            for i in range(8):
                bit = (pixel[0] >> i) & 1
                all_bits.append(str(bit))
    
    elif edge == 'right':
        for row in range(height):
            pixel = pixels[width-1, row]
            for i in range(8):
                bit = (pixel[0] >> i) & 1
                all_bits.append(str(bit))
    
    elif edge == 'combined_corners':
        # Extract from corners
        corners = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
        for x, y in corners:
            pixel = pixels[x, y]
            for ch in range(3):  # R, G, B
                for i in range(8):
                    bit = (pixel[ch] >> i) & 1
                    all_bits.append(str(bit))
    
    return ''.join(all_bits)

def try_every_rotation(bits):
    """Try starting from every possible bit offset"""
    results = []
    
    for start in range(min(100, len(bits))):
        # Try 8-bit chunks from this offset
        decoded = ""
        for i in range(start, len(bits) - 7, 8):
            try:
                byte_val = int(bits[i:i+8], 2)
                if 32 <= byte_val <= 126:
                    decoded += chr(byte_val)
                else:
                    break
            except:
                break
        
        if len(decoded) > 15 and re.search(r'Flag|flag|[A-Z]{5,}', decoded):
            results.append((start, decoded))
    
    return results

def main():
    print("[*] Extracting full bit depth from edges")
    print()
    
    for edge in ['top', 'left', 'right']:
        print(f"\n[{edge.upper()} EDGE]")
        bits = get_edge_pixels_bits("bottom_section.png", edge)
        print(f"Total bits: {len(bits)}")
        print(f"First 100 bits: {bits[:100]}")
        
        # Try rotations
        results = try_every_rotation(bits)
        if results:
            print(f"Found {len(results)} readable sequences:")
            for offset, decoded in results[:5]:
                print(f"  Offset {offset}: {decoded[:80]}")
        
        # Try reversing
        rev_bits = bits[::-1]
        results_rev = try_every_rotation(rev_bits)
        if results_rev:
            print(f"Found {len(results_rev)} readable sequences (reversed):")
            for offset, decoded in results_rev[:5]:
                print(f"  Offset {offset}: {decoded[:80]}")

if __name__ == "__main__":
    main()
