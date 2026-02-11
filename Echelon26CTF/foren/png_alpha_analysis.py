#!/usr/bin/env python3
"""
Extract and analyze alpha channel (transparency)
Look for patterns and LSB data in alpha values
"""

from PIL import Image
import os
import sys

def analyze_alpha_channel(image_path):
    """Extract and analyze alpha channel"""
    try:
        img = Image.open(image_path)
        print(f"Image: {image_path}")
        print(f"Mode: {img.mode}")
        print(f"Size: {img.size}")
        
        if img.mode == 'RGBA':
            pixels = img.load()
            width, height = img.size
            
            print("\n[*] Alpha channel analysis:")
            
            # Extract alpha channel
            alpha_values = []
            for row in range(height):
                for col in range(width):
                    alpha = pixels[col, row][3]
                    alpha_values.append(alpha)
            
            print(f"Alpha values count: {len(alpha_values)}")
            print(f"Unique values: {len(set(alpha_values))}")
            print(f"Min: {min(alpha_values)}, Max: {max(alpha_values)}")
            
            # Extract LSB from alpha
            print("\n[*] Alpha LSB extraction:")
            alpha_bits = ''.join([str(val & 1) for val in alpha_values])
            print(f"LSB sequence: {alpha_bits[:100]}...")
            
            # Decode LSB
            print("\n[*] Decoding alpha LSB:")
            for chunk_size in [7, 8]:
                decoded = ""
                for i in range(0, len(alpha_bits) - chunk_size + 1, chunk_size):
                    try:
                        byte_val = int(alpha_bits[i:i+chunk_size], 2)
                        if 32 <= byte_val <= 126:
                            decoded += chr(byte_val)
                    except:
                        break
                if decoded:
                    print(f"  Chunk {chunk_size}: {decoded[:100]}...")
            
            # Extract alpha from edges
            print("\n[*] Alpha values from edges (first 8 pixels):")
            print("  Top-left:")
            for row in range(min(2, height)):
                for col in range(min(4, width)):
                    alpha = pixels[col, row][3]
                    print(f"    ({col},{row}): {alpha:08b} ({alpha})")
            
            # Check for null/zero alpha patterns
            zero_alpha_count = sum(1 for a in alpha_values if a == 0)
            max_alpha_count = sum(1 for a in alpha_values if a == 255)
            print(f"\n[*] Alpha patterns:")
            print(f"  Zero alpha (transparent): {zero_alpha_count}")
            print(f"  Max alpha (opaque): {max_alpha_count}")
            
            return alpha_values
            
        else:
            print(f"Image mode {img.mode} does not have alpha channel")
            # Try converting
            if img.mode == 'RGB':
                print("Converting RGB to RGBA...")
                rgba_img = img.convert('RGBA')
                return analyze_alpha_channel(image_path)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def extract_alpha_patterns(image_path):
    """Look for specific alpha patterns that might hide data"""
    try:
        img = Image.open(image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        pixels = img.load()
        width, height = img.size
        
        print("\n[*] Looking for suspicious alpha patterns:")
        
        # Pattern 1: Rows with mixed alpha values
        for row in range(height):
            alpha_row = [pixels[col, row][3] for col in range(width)]
            unique = len(set(alpha_row))
            if unique > 2 and unique < width:
                print(f"  Row {row}: {unique} unique alpha values (possible data)")
                print(f"    Values: {alpha_row[:20]}...")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "bottom_section.png"
    
    if os.path.exists(image_path):
        analyze_alpha_channel(image_path)
        extract_alpha_patterns(image_path)
    else:
        print(f"File not found: {image_path}")
