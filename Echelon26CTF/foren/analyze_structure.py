#!/usr/bin/env python3

with open('binary_data.txt', 'r') as f:
    content = f.read()

# Split into binary values
lines = content.strip().split()

# Take only the actual data (before padding)
actual_lines = lines[:1189]

# Convert each binary to hex
hex_values = []
for line in actual_lines:
    if line:
        val = int(line, 2)
        hex_values.append(f"{val:02x}")

hex_str = ''.join(hex_values)
print("Hex representation:")
print(hex_str[:200])
print()

# Maybe it's a cipher - let me check if the bytes follow a pattern
# First, let's look at the byte distribution
from collections import Counter
byte_list = [int(line, 2) for line in actual_lines if line]
counter = Counter(byte_list)

print("Byte frequency:")
sorted_bytes = sorted(counter.items(), key=lambda x: -x[1])
for byte_val, count in sorted_bytes[:20]:
    print(f"  {byte_val:3d} (0x{byte_val:02x} '{chr(byte_val) if 32 <= byte_val < 127 else '.'}')): {count:3d} occurrences")

print("\n" + "="*60)
# Maybe each byte needs to be shifted/rotated?
# Or maybe we need to look at pairs of bytes?

# Try looking at every other byte
print("Every other byte (0, 2, 4...):")
every_other = ''.join(chr(byte_list[i]) if 32 <= byte_list[i] < 127 else '.' for i in range(0, len(byte_list), 2))
print(every_other[:200])

if 'Flag' in every_other or 'flag' in every_other:
    print("FOUND FLAG!")

print("\nEvery other byte (1, 3, 5...):")
every_other2 = ''.join(chr(byte_list[i]) if 32 <= byte_list[i] < 127 else '.' for i in range(1, len(byte_list), 2))
print(every_other2[:200])

if 'Flag' in every_other2 or 'flag' in every_other2:
    print("FOUND FLAG!")

# Try looking at patterns based on byte value ranges
print("\n" + "="*60)
print("Looking for structure in the bytes...")

# Group by ranges
ranges = {
    '0-31': 0,
    '32-64': 0,
    '65-96': 0,
    '97-127': 0,
    '128-255': 0
}

for b in byte_list:
    if 0 <= b < 32:
        ranges['0-31'] += 1
    elif 32 <= b < 65:
        ranges['32-64'] += 1
    elif 65 <= b < 97:
        ranges['65-96'] += 1
    elif 97 <= b < 128:
        ranges['97-127'] += 1
    else:
        ranges['128-255'] += 1

print("Byte range distribution:")
for r, count in ranges.items():
    print(f"  {r}: {count}")
