#!/usr/bin/env python3

# The header was corrupted: aad7bae0 -> ffd8ffe0
# Let me find the XOR key more carefully

corrupted = bytes.fromhex('aad7bae0')
correct = bytes.fromhex('ffd8ffe0')

# Find which bits differ
print("Bit differences in header:")
for i, (c, co) in enumerate(zip(correct, corrupted)):
    xor = c ^ co
    print(f"Byte {i}: 0x{co:02x} ^ 0x{c:02x} = 0x{xor:02x}")
    # Show bit-by-bit
    bin_c = format(c, '08b')
    bin_co = format(co, '08b')
    print(f"  Correct: {bin_c}  Corrupted: {bin_co}")

# Read binary data
with open('binary_data.txt', 'r') as f:
    content = f.read().replace(' ', '').replace('\n', '')

# Convert to bytes list (take only real data, not padding)
byte_values = []
for i in range(0, min(len(content) - 50, 9512), 8):  # 1189 * 8 = 9512
    byte_str = content[i:i+8]
    if len(byte_str) == 8:
        byte_values.append(int(byte_str, 2))

print(f"\nTotal bytes in data: {len(byte_values)}")

# Try flipping each bit position systematically
print("\nTrying bit flips at each position...")

for bit_pos in range(8):
    decoded = ''
    for byte_val in byte_values:
        # Flip specific bit
        flipped = byte_val ^ (1 << bit_pos)
        char = chr(flipped) if 32 <= flipped < 127 else '.'
        decoded += char
    
    # Check for flag
    if 'Flag' in decoded or 'flag' in decoded or 'ECH{' in decoded:
        print(f"\n*** FOUND with bit flip at position {bit_pos}! ***")
        print(decoded[:500])
        import re
        for pattern in [r'[Ff]lag\{[^}]*\}', r'ECH\{[^}]*\}']:
            matches = re.findall(pattern, decoded)
            if matches:
                for m in matches:
                    print(f"FLAG: {m}")

# Try XOR with different single bytes
print("\n" + "="*60)
print("Trying XOR with single bytes...")

for xor_byte in [0x55, 0xAA, 0xFF, 0x01, 0x02, 0x04, 0x08]:
    decoded = ''
    for byte_val in byte_values:
        xored = byte_val ^ xor_byte
        char = chr(xored) if 32 <= xored < 127 else '.'
        decoded += char
    
    if 'Flag' in decoded or 'flag' in decoded or 'ECH{' in decoded:
        print(f"\n*** FOUND with XOR 0x{xor_byte:02x}! ***")
        print(decoded[:500])
        import re
        for pattern in [r'[Ff]lag\{[^}]*\}', r'ECH\{[^}]*\}']:
            matches = re.findall(pattern, decoded)
            if matches:
                for m in matches:
                    print(f"FLAG: {m}")
