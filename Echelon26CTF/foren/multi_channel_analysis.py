#!/usr/bin/env python3
"""
Extract LSB from all color channels separately
Try different combinations to find readable flag
"""

from PIL import Image
import re

def extract_channel_edge_lsb(image_path, channel_idx=0):
    """Extract LSB from specific color channel at edges"""
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    
    channels = ['R', 'G', 'B', 'A']
    channel_name = channels[channel_idx] if channel_idx < len(channels) else f"C{channel_idx}"
    
    print(f"\n[Channel {channel_name}]")
    
    edges = {}
    
    # Top edge
    top = []
    for col in range(width):
        pixel = pixels[col, 0]
        if isinstance(pixel, tuple) and channel_idx < len(pixel):
            lsb = pixel[channel_idx] & 1
        else:
            lsb = pixel & 1
        top.append(str(lsb))
    edges['top'] = ''.join(top)
    
    # Bottom edge
    bottom = []
    for col in range(width):
        pixel = pixels[col, height-1]
        if isinstance(pixel, tuple) and channel_idx < len(pixel):
            lsb = pixel[channel_idx] & 1
        else:
            lsb = pixel & 1
        bottom.append(str(lsb))
    edges['bottom'] = ''.join(bottom)
    
    # Left edge
    left = []
    for row in range(height):
        pixel = pixels[0, row]
        if isinstance(pixel, tuple) and channel_idx < len(pixel):
            lsb = pixel[channel_idx] & 1
        else:
            lsb = pixel & 1
        left.append(str(lsb))
    edges['left'] = ''.join(left)
    
    # Right edge
    right = []
    for row in range(height):
        pixel = pixels[width-1, row]
        if isinstance(pixel, tuple) and channel_idx < len(pixel):
            lsb = pixel[channel_idx] & 1
        else:
            lsb = pixel & 1
        right.append(str(lsb))
    edges['right'] = ''.join(right)
    
    return edges

def decode_and_find_flag(bits, description=""):
    """Try to decode and find flag-like patterns"""
    # 8-bit decode
    decoded = ""
    for i in range(0, len(bits) - 7, 8):
        byte_val = int(bits[i:i+8], 2)
        if 32 <= byte_val <= 126:
            decoded += chr(byte_val)
        else:
            decoded += f"[{byte_val}]"
    
    # Look for Flag pattern
    flags = re.findall(r'Flag\{[^[\]]*\}', decoded)
    if flags:
        print(f"  {description} FOUND: {flags[0]}")
        return flags[0]
    
    # Look for any braced content
    braced = re.findall(r'\{[A-Za-z0-9_\-\.]+\}', decoded)
    if braced and len(braced[0]) > 5:
        print(f"  {description} candidate: {braced[0]}")
        return braced[0]
    
    # Look for readable fragments
    fragments = re.findall(r'[A-Za-z0-9_\-\.]{8,}', decoded)
    if fragments and len(fragments[0]) > 8:
        return fragments[0]
    
    return None

def main():
    img = Image.open("bottom_section.png")
    print(f"Image mode: {img.mode}")
    
    all_results = {}
    
    # Try all channels
    num_channels = len(img.mode)
    for ch in range(num_channels):
        edges = extract_channel_edge_lsb("bottom_section.png", ch)
        
        for edge_name, bits in edges.items():
            if len(set(bits)) > 1:  # Skip if all same
                result = decode_and_find_flag(bits, f"{img.mode[ch]}{edge_name.upper()}")
                if result and len(result) > 10:
                    key = f"{img.mode[ch]}_{edge_name}"
                    all_results[key] = result
    
    # Try combining adjacent bits from different channels
    print("\n[Combined Channel Analysis]")
    edges_r = extract_channel_edge_lsb("bottom_section.png", 0)
    if num_channels > 1:
        edges_g = extract_channel_edge_lsb("bottom_section.png", 1)
        edges_b = extract_channel_edge_lsb("bottom_section.png", 2)
        
        # Try R+G+B interleaved
        for edge_name in ['top', 'left', 'right']:
            r_bits = edges_r[edge_name]
            g_bits = edges_g[edge_name]
            b_bits = edges_b[edge_name]
            
            # Try different combinations
            combined = ""
            for i in range(min(len(r_bits), len(g_bits), len(b_bits))):
                combined += r_bits[i] + g_bits[i] + b_bits[i]
            
            if len(set(combined)) > 1:
                result = decode_and_find_flag(combined, f"RGB_{edge_name}_interleave")
                if result and len(result) > 10:
                    all_results[f"RGB_{edge_name}"] = result
    
    print("\n" + "="*70)
    print("[All Candidates Found]")
    for key, value in all_results.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
