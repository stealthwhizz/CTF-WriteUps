#!/usr/bin/env python3

data = open('12/12/ghost_identity.pcap', 'rb').read()
marker = b'OeiL'

# Find all OeiL occurrences
positions = []
i = 0
while True:
    pos = data.find(marker, i)
    if pos == -1:
        break
    positions.append(pos)
    i = pos + 1

print(f"Found {len(positions)} OeiL markers")

# Extract 10 bytes after each OeiL
for idx, pos in enumerate(positions):
    if pos + len(marker) + 10 < len(data):
        after_bytes = data[pos+len(marker):pos+len(marker)+10]
        print(f'{idx}: offset={pos} after={after_bytes.hex()} ascii={repr(after_bytes)}')

# Try extracting a specific byte from each
print("\nExtracting 5th byte after OeiL:")
extracted = []
for pos in positions:
    if pos + len(marker) + 5 < len(data):
        byte = data[pos+len(marker)+4]
        extracted.append(byte)

print("Bytes:", [hex(b) for b in extracted])
print("As ASCII:", ''.join(chr(b) if 32 <= b < 127 else f'[{b}]' for b in extracted))
