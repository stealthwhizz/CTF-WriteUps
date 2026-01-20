#!/usr/bin/env python3

with open('binary_data.txt', 'r') as f:
    content = f.read()

# Split into binary values
lines = content.strip().split()
print(f"Total binary values: {len(lines)}")

# Convert each to decimal/ASCII
decoded_bytes = []
for i, line in enumerate(lines):
    if line:
        val = int(line, 2)
        decoded_bytes.append((i, val, chr(val) if 32 <= val < 127 else '.'))

# Show last 50 bytes
print("\nLast 50 bytes:")
for i, val, char in decoded_bytes[-50:]:
    print(f"{i}: {val:3d} (0x{val:02x}) '{char}'")

# Find where the padding starts (repeated values)
print("\n" + "="*60)
print("Looking for pattern changes...")

# Count occurrences of each value
from collections import Counter
value_counts = Counter(val for _, val, _ in decoded_bytes)
print(f"Unique byte values: {len(value_counts)}")
print(f"Most common: {value_counts.most_common(10)}")

# Find transition point where we get into padding
print("\n" + "="*60)
print("Looking for meaningful data end...")

# Convert everything to ASCII first half
for split_point in range(len(decoded_bytes) - 100, len(decoded_bytes)):
    chunk = decoded_bytes[:split_point]
    decoded_str = ''.join(c for _, _, c in chunk)
    
    # Check if it contains flag pattern
    if '{' in decoded_str and '}' in decoded_str:
        print(f"Found brackets at position {split_point}")
        start = decoded_str.rfind('{', 0, 100)  # Last { in last 100 chars
        if start != -1:
            end = decoded_str.find('}', start)
            if end != -1:
                print(f"Potential flag: {decoded_str[start:end+1]}")
