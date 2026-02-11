#!/usr/bin/env python3

# Read and decode binary data
with open('binary_data.txt', 'r') as f:
    binary = f.read().replace(' ', '').replace('\n', '')

# Convert to ASCII
decoded = ''
for i in range(0, len(binary), 8):
    byte = binary[i:i+8]
    if len(byte) == 8:
        decoded += chr(int(byte, 2))

# Extract uppercase letters
uppercase = ''.join(c for c in decoded if c.isupper())
print("Uppercase letters:")
print(uppercase)
print(f"Length: {len(uppercase)}")
print()

# Try to find readable text by spacing it out
print("Trying to find spacing patterns...")
# Words might be concatenated
# Let's look for common patterns like "FLAG", "CTF", etc.

if 'FLAG' in uppercase:
    print("Found 'FLAG' in uppercase!")
    idx = uppercase.find('FLAG')
    print(f"Position: {idx}")
    print(f"Context: {uppercase[max(0,idx-10):idx+20]}")

# Try different spacing
print("\nTrying to manually parse uppercase:")
# NIOGHTYCSTSNAFELQMMPTOHMTLDUNOSHSHNPMTPPPTHMTPTMSTPTPGTTHHT
# Let me look for word breaks
# NI O GHTY CSTSNMMPTOHMTLDUNOSHSHNPMTPPPTHMTPTMSTPTPGTTHHT
# Could be: NIGHTY? CSTS? 
# Or: N I O GHT Y CST S N A F E L...

# Let me also check lowercase
lowercase = ''.join(c for c in decoded if c.islower())
print("\nLowercase letters:")
print(lowercase[:200])

# Mixed alphanumeric
print("\nAll letters (preserving case):")
all_letters = ''.join(c for c in decoded if c.isalpha())
print(all_letters[:200])

# Check if alternating case contains message
print("\nAlternating upper/lower preservation:")
print(all_letters)

# Let me look for "Flag" with any case
import re
all_text = ''.join(c for c in decoded if c.isalnum() or c in '{}_')
if re.search(r'[Ff]lag', all_text):
    print("\nFound 'flag' pattern!")
    matches = re.findall(r'.{0,20}[Ff]lag.{0,30}', all_text)
    for m in matches:
        print(f"  {m}")

# Try looking at specific positions where I saw "CSTSA" earlier
print("\n" + "="*60)
print("Detailed character analysis around interesting patterns:")
for i, c in enumerate(decoded):
    if c == 'C' and i+5 < len(decoded):
        print(f"Found 'C' at position {i}: {decoded[i:i+10]}")
