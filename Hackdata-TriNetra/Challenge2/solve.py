# Extract TARGET values from the hex dump
# The encoding logic from the bytecode:
# - i % 3 == 0: ord(c) ^ 33
# - i % 3 == 1: ord(c) + 4
# - i % 3 == 2: ord(c) * 2

TARGET = [
    0x75, 0x76, 0x67, 0x6F, 0x69, 0x72, 0x53, 0x65,
    0x79, 0x71, 0x7D, 0x52, 0x49, 0x34, 0x6C, 0x7E,
    0x57, 0x66, 0x15, 0x68, 0x2E, 0x56, 0x63, 0x4A,
    0x11, 0x6B, 0x2F, 0x42, 0x81
]

# Reverse the encoding
flag = []
for i, val in enumerate(TARGET):
    if i % 3 == 0:
        # Encoded as: ord(c) ^ 33
        # Decode: val ^ 33
        flag.append(chr(val ^ 33))
    elif i % 3 == 1:
        # Encoded as: ord(c) + 4
        # Decode: val - 4
        flag.append(chr(val - 4))
    else:  # i % 3 == 2
        # Encoded as: ord(c) * 2
        # Decode: val // 2
        flag.append(chr(val // 2))

result = ''.join(flag)
print(f"Flag: {result}")
