#!/usr/bin/env python3
"""
Extract complete edge LSB data and combine fragments
Focus on reconstructing from all four edges
"""

from PIL import Image
import os
import re

def extract_full_edge_lsb(image_path):
    """Extract complete LSB from all edges"""
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    
    print(f"Image: {image_path}")
    print(f"Size: {width}x{height}")
    print()
    
    edges = {}
    
    # Top edge (left to right)
    top = []
    for col in range(width):
        pixel = pixels[col, 0]
        lsb = pixel[0] & 1
        top.append(str(lsb))
    edges['top'] = ''.join(top)
    
    # Bottom edge (left to right)
    bottom = []
    for col in range(width):
        pixel = pixels[col, height-1]
        lsb = pixel[0] & 1
        bottom.append(str(lsb))
    edges['bottom'] = ''.join(bottom)
    
    # Left edge (top to bottom)
    left = []
    for row in range(height):
        pixel = pixels[0, row]
        lsb = pixel[0] & 1
        left.append(str(lsb))
    edges['left'] = ''.join(left)
    
    # Right edge (top to bottom)
    right = []
    for row in range(height):
        pixel = pixels[width-1, row]
        lsb = pixel[0] & 1
        right.append(str(lsb))
    edges['right'] = ''.join(right)
    
    return edges

def decode_bits_8bit(bits):
    """Decode 8-bit chunks to text"""
    decoded = ""
    for i in range(0, len(bits) - 7, 8):
        byte_val = int(bits[i:i+8], 2)
        if 32 <= byte_val <= 126:
            decoded += chr(byte_val)
        else:
            decoded += f"[{byte_val}]"
    return decoded

def decode_bits_7bit(bits):
    """Decode 7-bit chunks to text"""
    decoded = ""
    for i in range(0, len(bits) - 6, 7):
        byte_val = int(bits[i:i+7], 2)
        if 32 <= byte_val <= 126:
            decoded += chr(byte_val)
        else:
            decoded += f"[{byte_val}]"
    return decoded

def try_bit_reversal(bits):
    """Try reversing the bits"""
    return bits[::-1]

def extract_printable_fragments(text):
    """Extract contiguous printable fragments"""
    fragments = re.findall(r'[A-Za-z0-9_\-\{\}]{5,}', text)
    return fragments

def main():
    edges = extract_full_edge_lsb("bottom_section.png")
    
    for edge_name, bits in edges.items():
        print(f"\n{'='*70}")
        print(f"[{edge_name.upper()}] ({len(bits)} bits)")
        print('='*70)
        print(f"Bits: {bits[:100]}...")
        
        # Skip if all zeros (bottom edge)
        if len(set(bits)) == 1:
            print("(All same bit - skipping)")
            continue
        
        # Try 8-bit decoding
        print(f"\n[8-bit decoding]:")
        decoded_8 = decode_bits_8bit(bits)
        print(f"  {decoded_8[:150]}")
        fragments = extract_printable_fragments(decoded_8)
        if fragments:
            print(f"  Fragments: {fragments[:10]}")
        
        # Try 7-bit decoding  
        print(f"\n[7-bit decoding]:")
        decoded_7 = decode_bits_7bit(bits)
        print(f"  {decoded_7[:150]}")
        fragments = extract_printable_fragments(decoded_7)
        if fragments:
            print(f"  Fragments: {fragments[:10]}")
        
        # Try reversed
        print(f"\n[Reversed bits]:")
        rev_bits = try_bit_reversal(bits)
        decoded_rev = decode_bits_8bit(rev_bits)
        print(f"  {decoded_rev[:150]}")
        fragments = extract_printable_fragments(decoded_rev)
        if fragments:
            print(f"  Fragments: {fragments[:10]}")
    
    # Save bits for further analysis
    print(f"\n\n[*] Saving complete edge data for analysis...")
    with open("edge_lsb_data.txt", 'w') as f:
        for edge_name, bits in edges.items():
            f.write(f"# {edge_name}\n{bits}\n\n")
    print("[+] Saved to edge_lsb_data.txt")

if __name__ == "__main__":
    main()
