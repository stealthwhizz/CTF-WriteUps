def enc(s):
    """Actual encoding function"""
    out = []
    for i, c in enumerate(s):
        if i % 3 == 0:
            out.append(ord(c) ^ 33)
        elif i % 3 == 1:
            out.append(ord(c) + 4)
        else:  # i % 3 == 2
            out.append(ord(c) - 2)
    return out

TARGET = [117, 118, 103, 111, 105, 114, 83, 101, 121, 113, 125, 82, 73, 52, 108, 126, 87, 102, 21, 104, 46, 86, 99, 74, 17, 107, 47, 66, 129]

flag = "TriNetra{PyTh0n_Sh4d0w_L0g1c}"
encoded = enc(flag)

print(f"Flag: {flag}")
print(f"Encoded: {encoded}")
print(f"Target:  {TARGET}")
print(f"Match: {encoded == TARGET}")
