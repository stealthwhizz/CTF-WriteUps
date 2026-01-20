#!/usr/bin/env python3
import subprocess
import sys

# Extract packet times from pcap
cmd = ["tshark", "-r", "11/quiet_agreement.pcap", "-T", "fields", "-e", "frame.time_relative"]
result = subprocess.run(cmd, capture_output=True, text=True)
times = [float(t) for t in result.stdout.strip().split('\n')]

# Calculate time deltas between consecutive packets
deltas = []
for i in range(1, len(times)):
    delta = times[i] - times[i-1]
    deltas.append(delta)

print(f"Total packets: {len(times)}")
print(f"Total deltas: {len(deltas)}")
print(f"\nFirst 20 deltas:")
for i, d in enumerate(deltas[:20]):
    print(f"{i}: {d:.6f}s")

# Decode: Short delay (~0.05s) = 0, Long delay (~0.20s) = 1
binary_str = ""
for delta in deltas:
    if delta < 0.1:  # Short delay
        binary_str += "0"
    else:  # Long delay
        binary_str += "1"

print(f"\nBinary string ({len(binary_str)} bits):")
print(binary_str)

# Convert binary to ASCII (8 bits per character)
message = ""
for i in range(0, len(binary_str), 8):
    byte = binary_str[i:i+8]
    if len(byte) == 8:
        char = chr(int(byte, 2))
        message += char

print(f"\nDecoded message:")
print(message)
