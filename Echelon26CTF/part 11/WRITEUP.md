# Echelon26CTF - Part 11: Quiet Agreement - Writeup

## Challenge Description

The challenge hints at a second network capture with deceptive communication:
- Messages are intentionally misleading
- Real communication happens elsewhere
- Things are starting to make sense

From [question.txt](11/question.txt):
> The next capture contains traffic between 10.0.0.20 and 10.0.0.30 over port 443, but no readable payload data exists anywhere.
> Packets are exchanged continuously, using only TCP ACKs, yet decisions appear to be finalized.
> Closer inspection shows that the time gap between packets is consistent and intentional, clustering around two values: ~0.05 seconds and ~0.20 seconds.
> There are no other recurring patterns in size, flags, or content.
> If no one is speaking, then agreement must be happening through timing alone.

**Files provided:**
- `quiet_agreement.pcap` - Network capture file
- `question.txt` - Challenge description

## Initial Analysis

First, let's examine the PCAP file to understand the traffic:

```bash
tshark -r 11/quiet_agreement.pcap -T fields -e frame.time_relative -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.flags
```

**Observations:**
- All packets are between `10.0.0.20:40404` → `10.0.0.30:443`
- All packets have TCP flag `0x0010` (ACK only)
- No payload data in any packet
- 1,192 total packets
- Time deltas cluster around **0.05 seconds** and **0.20 seconds**

## The Technique: Timing Covert Channel

The challenge uses a **timing covert channel** - a method of encoding information in the timing between events rather than in the content of the events themselves.

This is a legitimate steganography technique where:
- **No visible data is transmitted** (empty TCP ACKs)
- **Information is encoded in timing patterns**
- Detection is difficult without knowing what to look for

### Encoding Scheme

Based on the hint about two time values:
- **Short delay (~0.05s) = Binary 0**
- **Long delay (~0.20s) = Binary 1**

## Solution Process

### Step 1: Extract Packet Timestamps

```bash
tshark -r 11/quiet_agreement.pcap -T fields -e frame.time_relative > times.txt
```

### Step 2: Calculate Time Deltas

Create a Python script to analyze the timing:

```python
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
```

**Results:**
- Total packets: 1,192
- Total deltas: 1,191

### Step 3: Decode Binary from Timing

The timing pattern shows consistent values:
- ~0.05s (short) → **0**
- ~0.20s (long) → **1**

```python
# Decode: Short delay (~0.05s) = 0, Long delay (~0.20s) = 1
binary_str = ""
for delta in deltas:
    if delta < 0.1:  # Short delay
        binary_str += "0"
    else:  # Long delay
        binary_str += "1"
```

This produces a 1,191-bit binary string.

### Step 4: Convert Binary to ASCII

Group the binary string into 8-bit bytes and convert to ASCII:

```python
# Convert binary to ASCII (8 bits per character)
message = ""
for i in range(0, len(binary_str), 8):
    byte = binary_str[i:i+8]
    if len(byte) == 8:
        char = chr(int(byte, 2))
        message += char

print(f"\nDecoded message:")
print(message)
```

### Step 5: Extract the Flag

**Decoded message:**
```
On further inspection from the CBI and checking their DB, you realize that the only matching person Arjun Rampal died back in 2011. flag{arjun_dies}
```

## Flag

**`flag{arjun_dies}`**

## Key Takeaways

1. **Covert Channels** - Information can be hidden in metadata (timing, packet size, sequence) rather than content
2. **Binary Encoding** - Two distinct timing values create a binary alphabet
3. **Network Analysis** - Sometimes the answer isn't in the payload but in the packet characteristics
4. **Steganography** - The art of hiding information in plain sight (or in this case, in empty packets)

## Tools Used

- **tshark** - Command-line network protocol analyzer
- **Python 3** - For timing analysis and binary decoding

## Difficulty Assessment

**Difficulty:** Hard

**Skills Required:**
- Network traffic analysis
- Understanding of covert channels
- Binary/ASCII conversion
- Pattern recognition in timing data
- Scripting/automation

## References

- [Timing Covert Channels](https://en.wikipedia.org/wiki/Covert_channel#Timing_channels)
- [Network Steganography](https://en.wikipedia.org/wiki/Network_steganography)
