# Let me try different orderings of the encoding rules

TARGET = [
    0x75, 0x76, 0x67, 0x6F, 0x69, 0x72, 0x53, 0x65,
    0x79, 0x71, 0x7D, 0x52, 0x49, 0x34, 0x6C, 0x7E,
    0x57, 0x66, 0x15, 0x68, 0x2E, 0x56, 0x63, 0x4A,
    0x11, 0x6B, 0x2F, 0x42, 0x81
]

# Try different combinations
def try_decode(rules):
    """Try decoding with different rules for each position mod 3"""
    flag = []
    for i, val in enumerate(TARGET):
        mod = i % 3
        if rules[mod] == 'xor':
            flag.append(chr(val ^ 33))
        elif rules[mod] == 'add':
            flag.append(chr(val - 4))
        elif rules[mod] == 'mul':
            flag.append(chr(val // 2))
    return ''.join(flag)

# Try all 6 permutations
from itertools import permutations
for perm in permutations(['xor', 'add', 'mul']):
    result = try_decode(perm)
    print(f"{perm}: {result}")
    if result.startswith('TriNetra{'):
        print(f"  *** FOUND! ***")
