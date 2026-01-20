#!/usr/bin/env python3

with open('binary_data.txt', 'r') as f:
    binary = f.read().replace(' ', '').replace('\n', '')

decoded = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8) if len(binary[i:i+8]) == 8)

# Extract alphanumeric and common flag characters
result = ''.join(c for c in decoded if c.isalnum() or c in '{}_')
print(result)
