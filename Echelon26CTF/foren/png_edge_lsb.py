#!/usr/bin/env python3
"""
Extract LSB data from PNG edges (first/last rows and columns)
This targets the "Focus on the edges" hint
"""

from PIL import Image
import os
import sys

def extract_edge_lsb(image_path, edge_width=1):
    """Extract LSB from image edges"""
    try:
        img = Image.open(image_path)
        pixels = img.load()
        width, height = img.size
        
        print(f"Image: {image_path}")
        print(f"Size: {width}x{height}")
        print(f"Mode: {img.mode}")
        print()
        
        # Extract from edges
        edge_bits = []
        
        # Top edge
        print("[*] Top edge LSB:")
        for row in range(edge_width):
            for col in range(width):
                pixel = pixels[col, row]
                if isinstance(pixel, tuple):
                    lsb = pixel[0] & 1
                else:
                    lsb = pixel & 1
                edge_bits.append(str(lsb))
        top_bits = ''.join(edge_bits)
        print(f"    Bits: {top_bits[:100]}...")
        print()
        
        # Bottom edge
        edge_bits = []
        print("[*] Bottom edge LSB:")
        for row in range(height - edge_width, height):
            for col in range(width):
                pixel = pixels[col, row]
                if isinstance(pixel, tuple):
                    lsb = pixel[0] & 1
                else:
                    lsb = pixel & 1
                edge_bits.append(str(lsb))
        bottom_bits = ''.join(edge_bits)
        print(f"    Bits: {bottom_bits[:100]}...")
        print()
        
        # Left edge
        edge_bits = []
        print("[*] Left edge LSB:")
        for row in range(height):
            for col in range(edge_width):
                pixel = pixels[col, row]
                if isinstance(pixel, tuple):
                    lsb = pixel[0] & 1
                else:
                    lsb = pixel & 1
                edge_bits.append(str(lsb))
        left_bits = ''.join(edge_bits)
        print(f"    Bits: {left_bits[:100]}...")
        print()
        
        # Right edge
        edge_bits = []
        print("[*] Right edge LSB:")
        for row in range(height):
            for col in range(width - edge_width, width):
                pixel = pixels[col, row]
                if isinstance(pixel, tuple):
                    lsb = pixel[0] & 1
                else:
                    lsb = pixel & 1
                edge_bits.append(str(lsb))
        right_bits = ''.join(edge_bits)
        print(f"    Bits: {right_bits[:100]}...")
        print()
        
        # Decode all edges
        for name, bits in [("top", top_bits), ("bottom", bottom_bits), ("left", left_bits), ("right", right_bits)]:
            print(f"[*] Attempting to decode {name} edge:")
            for chunk_size in [7, 8]:
                print(f"    Chunk size: {chunk_size}")
                decoded = ""
                for i in range(0, len(bits) - chunk_size + 1, chunk_size):
                    try:
                        byte_val = int(bits[i:i+chunk_size], 2)
                        if 32 <= byte_val <= 126:
                            decoded += chr(byte_val)
                        else:
                            decoded += f"[{byte_val}]"
                    except:
                        break
                if decoded:
                    print(f"      {decoded[:150]}")
            print()
        
        return {
            "top": top_bits,
            "bottom": bottom_bits,
            "left": left_bits,
            "right": right_bits
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_all_channels_edges(image_path):
    """Extract LSB from all color channels at edges"""
    try:
        img = Image.open(image_path)
        if img.mode not in ['RGB', 'RGBA']:
            img = img.convert('RGB')
        
        pixels = img.load()
        width, height = img.size
        
        print(f"\n[*] Extracting LSB from all channels (top-left corner):")
        for row in range(min(2, height)):
            for col in range(min(4, width)):
                pixel = pixels[col, row]
                print(f"  ({col},{row}): R={pixel[0]:08b} G={pixel[1]:08b} B={pixel[2]:08b}")
        
    except Exception as e:
        print(f"Error analyzing channels: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "bottom_section.png"
    
    if os.path.exists(image_path):
        extract_edge_lsb(image_path)
        extract_all_channels_edges(image_path)
    else:
        print(f"File not found: {image_path}")
