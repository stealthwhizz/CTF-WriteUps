#!/usr/bin/env python3
"""
Analyze PNG chunk structure and extract data
Including chunks after IEND marker
"""

import struct
import os
import sys

def analyze_png_structure(file_path):
    """Analyze PNG file structure and extract chunks"""
    try:
        with open(file_path, 'rb') as f:
            # PNG signature
            signature = f.read(8)
            print(f"PNG Signature: {signature.hex()}")
            if signature != b'\x89PNG\r\n\x1a\n':
                print("ERROR: Not a valid PNG file")
                return
            
            chunks = []
            print("\n[*] PNG Chunks:")
            
            while True:
                # Read length
                length_bytes = f.read(4)
                if len(length_bytes) < 4:
                    break
                
                length = struct.unpack('>I', length_bytes)[0]
                
                # Read chunk type
                chunk_type = f.read(4)
                if len(chunk_type) < 4:
                    break
                
                # Read chunk data
                chunk_data = f.read(length)
                
                # Read CRC
                crc = f.read(4)
                
                chunk_info = {
                    'type': chunk_type.decode('latin1'),
                    'length': length,
                    'data': chunk_data,
                    'crc': crc.hex() if crc else None
                }
                chunks.append(chunk_info)
                
                print(f"  {chunk_info['type']:4s} - Length: {length:6d} - CRC: {chunk_info['crc']}")
                
                # Check for IEND
                if chunk_type == b'IEND':
                    print("\n[*] Data after IEND marker:")
                    remaining = f.read()
                    if remaining:
                        print(f"  Found {len(remaining)} bytes after IEND")
                        print(f"  Hex: {remaining.hex()[:200]}...")
                        try:
                            decoded = remaining.decode('utf-8', errors='ignore')
                            print(f"  Text: {decoded[:200]}")
                        except:
                            pass
                    else:
                        print("  No data after IEND")
                    break
            
            return chunks
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_text_chunks(file_path):
    """Extract text from tEXt, zTXt, iTXt chunks"""
    try:
        with open(file_path, 'rb') as f:
            f.read(8)  # Skip signature
            
            print("\n[*] Text Chunks (tEXt, zTXt, iTXt):")
            
            while True:
                length_bytes = f.read(4)
                if len(length_bytes) < 4:
                    break
                
                length = struct.unpack('>I', length_bytes)[0]
                chunk_type = f.read(4)
                chunk_data = f.read(length)
                crc = f.read(4)
                
                if chunk_type in [b'tEXt', b'zTXt', b'iTXt']:
                    print(f"\n  Chunk type: {chunk_type.decode('latin1')}")
                    print(f"  Data length: {length}")
                    print(f"  Raw data: {chunk_data.hex()[:100]}...")
                    try:
                        decoded = chunk_data.decode('utf-8', errors='ignore')
                        print(f"  Text: {decoded}")
                    except:
                        pass
                
                if chunk_type == b'IEND':
                    break
        
    except Exception as e:
        print(f"Error: {e}")

def extract_metadata(file_path):
    """Extract all metadata from PNG"""
    try:
        from PIL import Image
        from PIL.PngImagePlugin import PngInfo
        
        img = Image.open(file_path)
        
        print("\n[*] PIL Metadata:")
        if hasattr(img, 'info') and img.info:
            for key, value in img.info.items():
                print(f"  {key}: {value}")
        else:
            print("  No metadata found")
        
    except Exception as e:
        print(f"Error reading metadata: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "bottom_section.png"
    
    if os.path.exists(file_path):
        analyze_png_structure(file_path)
        extract_text_chunks(file_path)
        extract_metadata(file_path)
    else:
        print(f"File not found: {file_path}")
