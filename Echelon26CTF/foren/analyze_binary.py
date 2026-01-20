#!/usr/bin/env python3
# Analyze the binary data for patterns

with open('binary_data.txt', 'r') as f:
    binary = f.read()

# Remove spaces and newlines
binary = binary.replace(' ', '').replace('\n', '')

print(f"Total bits: {len(binary)}")
print(f"Total bytes: {len(binary)//8}")

# Try different bit manipulations
def decode_with_transform(binary, transform_fn, name):
    result = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            transformed = transform_fn(byte)
            char_val = int(transformed, 2)
            if 32 <= char_val <= 126:  # Printable ASCII
                result += chr(char_val)
            else:
                result += '.'
    
    # Check for flag pattern
    if 'Flag{' in result or 'flag{' in result or 'ECH{' in result:
        print(f"\n{'='*60}")
        print(f"FOUND with {name}!")
        print(f"{'='*60}")
        print(result[:500])
        
        # Extract flag
        for pattern in ['Flag{', 'flag{', 'ECH{']:
            if pattern in result:
                start = result.find(pattern)
                end = result.find('}', start)
                if end != -1:
                    print(f"\n*** FLAG FOUND: {result[start:end+1]} ***")
        return True
    return False

# Original
print("\n1. Original (no transformation):")
if not decode_with_transform(binary, lambda x: x, "Original"):
    print("No flag found")

# Flip LSB (least significant bit)
print("\n2. Flipping LSB of each byte:")
decode_with_transform(binary, lambda x: x[:-1] + ('0' if x[-1]=='1' else '1'), "LSB Flip")

# Flip MSB (most significant bit)  
print("\n3. Flipping MSB of each byte:")
decode_with_transform(binary, lambda x: ('0' if x[0]=='1' else '1') + x[1:], "MSB Flip")

# Invert all bits
print("\n4. Inverting all bits:")
decode_with_transform(binary, lambda x: ''.join('0' if b=='1' else '1' for b in x), "Invert All")

# Try XOR with common values
for xor_val in [0x01, 0x55, 0xAA, 0xFF]:
    print(f"\n5. XOR with 0x{xor_val:02X}:")
    decode_with_transform(binary, 
        lambda x, xor=xor_val: format(int(x, 2) ^ xor, '08b'), 
        f"XOR 0x{xor_val:02X}")
