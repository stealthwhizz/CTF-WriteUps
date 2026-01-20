#!/usr/bin/env python3
"""
Combine all PNG forensic techniques and previous binary data
Find the real flag by combining fragments
"""

import os
import sys
import subprocess
import re

def read_previous_data():
    """Read previously extracted binary data"""
    data = {}
    
    # Read binary data
    if os.path.exists("binary_data.txt"):
        with open("binary_data.txt", 'r') as f:
            content = f.read()
            data['binary'] = content
            print("[*] Binary data loaded")
    
    # Read steganopayload
    if os.path.exists("steganopayload2064102.txt"):
        with open("steganopayload2064102.txt", 'r') as f:
            content = f.read()
            data['stego'] = content
            print("[*] Steganopayload loaded")
    
    return data

def run_all_png_analysis():
    """Run all PNG analysis scripts"""
    print("\n" + "="*60)
    print("[*] Running comprehensive PNG forensics")
    print("="*60)
    
    results = {}
    
    # Run edge LSB extraction
    print("\n[PHASE 1] PNG Edge LSB Extraction")
    print("-"*60)
    try:
        result = subprocess.run(['python3', 'png_edge_lsb.py', 'bottom_section.png'], 
                               capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print("[!] Errors:", result.stderr)
        results['edge_lsb'] = result.stdout
    except Exception as e:
        print(f"Error: {e}")
    
    # Run chunk analysis
    print("\n[PHASE 2] PNG Chunk Structure Analysis")
    print("-"*60)
    try:
        result = subprocess.run(['python3', 'png_chunk_analysis.py', 'bottom_section.png'],
                               capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print("[!] Errors:", result.stderr)
        results['chunks'] = result.stdout
    except Exception as e:
        print(f"Error: {e}")
    
    # Run alpha analysis
    print("\n[PHASE 3] PNG Alpha Channel Analysis")
    print("-"*60)
    try:
        result = subprocess.run(['python3', 'png_alpha_analysis.py', 'bottom_section.png'],
                               capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print("[!] Errors:", result.stderr)
        results['alpha'] = result.stdout
    except Exception as e:
        print(f"Error: {e}")
    
    return results

def extract_text_from_results(results):
    """Extract readable text from analysis results"""
    print("\n" + "="*60)
    print("[*] Extracting candidates from results")
    print("="*60)
    
    candidates = []
    
    for phase, output in results.items():
        print(f"\n[{phase}]")
        # Look for Flag{...} patterns
        flags = re.findall(r'Flag\{[^}]+\}', output, re.IGNORECASE)
        if flags:
            print(f"  Found flags: {flags}")
            candidates.extend(flags)
        
        # Look for common text patterns
        words = re.findall(r'[A-Za-z_]{5,}', output)
        if words:
            unique_words = set(words)
            interesting = [w for w in unique_words if len(w) > 3 and w.lower() not in 
                          ['chunk', 'length', 'data', 'error', 'bytes', 'alpha', 'extraction']]
            if interesting:
                print(f"  Text fragments: {list(interesting)[:10]}")
                candidates.extend(interesting)
    
    return candidates

def try_combining_fragments():
    """Try combining fragments from different sources"""
    print("\n" + "="*60)
    print("[*] Attempting to combine fragments")
    print("="*60)
    
    prev_data = read_previous_data()
    
    if 'binary' in prev_data:
        print(f"\n[Binary data preview] {prev_data['binary'][:200]}")
    
    if 'stego' in prev_data:
        print(f"\n[Steganopayload preview] {prev_data['stego'][:200]}")
    
    # Look for pattern combinations
    if 'binary' in prev_data and 'stego' in prev_data:
        # Try concatenating
        combined = prev_data['binary'] + prev_data['stego']
        # Extract flag-like patterns
        flags = re.findall(r'[Ff]lag\{[^}]{0,100}\}', combined)
        if flags:
            print(f"\n[Combined] Potential flags:")
            for flag in flags:
                print(f"  {flag}")

def main():
    print("[*] CTF Forensics - Complete PNG Analysis Suite")
    print("[*] Target: bottom_section.png")
    print()
    
    # First read previous data
    print("[PHASE 0] Reading previous extraction data")
    print("-"*60)
    prev_data = read_previous_data()
    
    # Run all PNG analyses
    results = run_all_png_analysis()
    
    # Extract and combine
    extract_text_from_results(results)
    try_combining_fragments()
    
    print("\n" + "="*60)
    print("[*] Analysis complete")
    print("[*] Check output above for extracted fragments")
    print("="*60)

if __name__ == "__main__":
    main()
