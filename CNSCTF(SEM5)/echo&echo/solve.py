#!/usr/bin/env python3
import binascii

# Data from tshark output: frame, ip.id, icmp.seq, data, type
# Type 0 = Echo Reply, Type 8 = Echo Request
packets = [
    (1, 0x0101, 1, "1c15122c110b4440", 0),
    (7, 0x0001, 0, "f5f82214981c4ca16d2b4418da62d76d", 0),
    (10, 0x0001, 0, "f6a8890e9ea703f0d79b123aec2839d8", 0),
    (12, 0x0100, 0, "19121510051f5557", 0),
    (14, 0x0001, 0, "781c997ad449d9101e915de4b606", 8),
    (18, 0x0001, 0, "e64b265a7c", 8),
    (31, 0x0102, 2, "2f50414043514c", 0),
    (58, 0x0001, 0, "9c6ad827330a19df099ec7", 8),
]

# Filter echo replies (type 0) with 0x01XX IP IDs (signal)
replies = [p for p in packets if p[4] == 0 and (p[1] & 0xFF00) == 0x0100]
replies.sort(key=lambda x: x[1])

# Get the signal data
signal_data = ''.join([data_hex for _, _, _, data_hex, _ in replies])
signal_bytes = binascii.unhexlify(signal_data)

print("--- Signal (Echo Replies with 0x01XX) ---")
print(f"Hex: {signal_data}")
print(f"Length: {len(signal_bytes)} bytes")

# Get noise packets (echo requests with 0x0001)
requests = [p for p in packets if p[1] == 0x0001 and p[4] == 8]
requests.sort(key=lambda x: x[0])  # Sort by frame number

print("\n--- Noise (Echo Requests with 0x0001) ---")
for frame, _, _, data_hex, _ in requests:
    print(f"Frame {frame}: {data_hex} (length: {len(binascii.unhexlify(data_hex))})")

# Try XOR with each noise packet individually
print("\n--- XOR signal with each noise packet ---")
for frame, _, _, data_hex, _ in requests:
    key_bytes = binascii.unhexlify(data_hex)
    print(f"\nUsing noise from frame {frame} as XOR key:")
    # XOR with repeating key
    result = bytes([signal_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(signal_bytes))])
    print(f"Result: {result}")
    try:
        ascii_result = result.decode('ascii', errors='ignore')
        print(f"ASCII: {ascii_result}")
    except:
        pass

# Try concatenating all noise packets as the key
print("\n--- XOR with concatenated noise packets ---")
all_noise = ''.join([data_hex for _, _, _, data_hex, _ in requests])
noise_key = binascii.unhexlify(all_noise)
print(f"Combined noise key length: {len(noise_key)} bytes")
print(f"Signal length: {len(signal_bytes)} bytes")

if len(noise_key) >= len(signal_bytes):
    result = bytes([signal_bytes[i] ^ noise_key[i] for i in range(len(signal_bytes))])
    print(f"Result: {result}")
    try:
        ascii_result = result.decode('ascii')
        print(f"ASCII: {ascii_result}")
    except Exception as e:
        print(f"Decode error: {e}")
        print(f"ASCII (ignore errors): {result.decode('ascii', errors='ignore')}")
