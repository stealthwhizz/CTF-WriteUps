# Reconstructed secret.py functions from bytecode analysis

def enc(s):
    """Encode a string based on position"""
    out = []
    for i, c in enumerate(s):
        if i % 3 == 0:
            out.append(ord(c) ^ 33)
        elif i % 3 == 1:
            out.append(ord(c) + 4)
        else:
            out.append(ord(c) * 2)
    return out

# TARGET from bytecode
TARGET = [
    0x75, 0x76, 0x67, 0x6F, 0x69, 0x72, 0x53, 0x65,
    0x79, 0x71, 0x7D, 0x52, 0x49, 0x34, 0x6C, 0x7E,
    0x57, 0x66, 0x15, 0x68, 0x2E, 0x56, 0x63, 0x4A,
    0x11, 0x6B, 0x2F, 0x42, 0x81
]

def verify(x):
    """Verify if encoded x matches TARGET"""
    return enc(x) == TARGET

# Test and find the flag
flag = []
for i, val in enumerate(TARGET):
    if i % 3 == 0:
        flag.append(chr(val ^ 33))
    elif i % 3 == 1:
        flag.append(chr(val - 4))
    else:
        flag.append(chr(val // 2))

result = ''.join(flag)
print(f"Decoded: {result}")
print(f"Verification: {verify(result)}")
print(f"Encoded back: {enc(result)}")
print(f"Target:       {TARGET}")
