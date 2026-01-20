encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"

# Find the shift needed to turn 'v' into 'i'
# v = 21, i = 8
# shift = (21 - 8) = 13
shift_needed = (ord('v') - ord('i'))
print(f"Shift from 'v' to 'i': {shift_needed}")
print()

# Try ROT-13
print("ROT-13:")
result = []
for char in encrypted:
    if char.isalpha():
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - 13) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - 13) % 26 + ord('a')))
    else:
        result.append(char)
print(''.join(result))
print()

# Try all ROT possibilities looking for "isfcr"
print("All ROT possibilities:")
for rot in range(26):
    result = []
    for char in encrypted:
        if char.isalpha():
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - rot) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - rot) % 26 + ord('a')))
        else:
            result.append(char)
    decrypted = ''.join(result)
    if decrypted.startswith('isfcr'):
        print(f"ROT-{rot}: {decrypted} *** MATCH ***")
    else:
        print(f"ROT-{rot}: {decrypted}")
