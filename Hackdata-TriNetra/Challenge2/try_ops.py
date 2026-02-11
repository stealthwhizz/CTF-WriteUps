TARGET = [117, 118, 103, 111, 105, 114, 83, 101, 121, 113, 125, 82, 73, 52, 108, 126, 87, 102, 21, 104, 46, 86, 99, 74, 17, 107, 47, 66, 129]

# Try different operations for position i % 3 == 2
operations = [
    ('xor', 'add', 'mul'),  # Original: XOR 33, +4, *2
    ('xor', 'add', 'add2'), # Try: XOR 33, +4, +2
    ('xor', 'add', 'sub'),  # Try: XOR 33, +4, -something
]

for ops in operations:
    flag = []
    for i, val in enumerate(TARGET):
        mod = i % 3
        if mod == 0:  # XOR 33
            flag.append(chr(val ^ 33))
        elif mod == 1:  # +4
            flag.append(chr(val - 4))
        else:  # mod == 2
            if ops[2] == 'mul':
                flag.append(chr(val // 2))
            elif ops[2] == 'add2':
                flag.append(chr(val - 2))
            elif ops[2] == 'sub':
                flag.append(chr(val + 2))
    
    result = ''.join(flag)
    print(f"{ops}: {result}")
    if 'TriNetra{' in result:
        print("  *** FOUND! ***")
