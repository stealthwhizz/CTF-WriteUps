encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"
key = "13779"

print(f"Encrypted: {encrypted}")
print(f"Key: {key}")
print()

# The shifts we need are: 13, 4, 19, 22, 14
# Key digits are: 1, 3, 7, 7, 9

# What if we need to use DOUBLE the key? "1377913779..."
print("Method: Double/repeat key")
double_key = key + key
print(f"Double key: {double_key}")

result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = int(double_key[key_index % len(double_key)])
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)
decrypted = ''.join(result)
print(f"Decrypted: {decrypted}")
print()

# What about using key as: 1, 1+3=4, 1+3+7=11 (mod 26)...?
# Or 1, 3, 7, 7, 9, then repeat with next set...

# Let me try interpreting "13779" as "13 7 7 9"
print("Method: Parse as 13-7-7-9")
parsed_key = [13, 7, 7, 9]
result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = parsed_key[key_index % len(parsed_key)]
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)
decrypted = ''.join(result)
print(f"Decrypted: {decrypted}")
if decrypted.startswith('isfcr'):
    print("*** MATCH ***")
print()

# Try: 1-3-7-7-9 individual digits
print("Method: Individual digits 1-3-7-7-9")
parsed_key = [1, 3, 7, 7, 9]
result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = parsed_key[key_index % len(parsed_key)]
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)
decrypted = ''.join(result)
print(f"Decrypted: {decrypted}")
if decrypted.startswith('isfcr'):
    print("*** MATCH ***")
print()

# Let me try all possible parsings
print("Method: Try all possible key parsings")
possible_keys = [
    [1, 3, 7, 7, 9],
    [13, 7, 7, 9],
    [1, 37, 7, 9],
    [1, 3, 77, 9],
    [1, 3, 7, 79],
    [13, 77, 9],
    [13, 7, 79],
    [137, 7, 9],
    [1, 377, 9],
    [1, 3, 779],
    [13779],
]

for pk in possible_keys:
    result = []
    key_index = 0
    for char in encrypted:
        if char.isalpha():
            shift = pk[key_index % len(pk)] % 26
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    decrypted = ''.join(result)
    if decrypted.startswith('isfcr'):
        print(f"Key {pk}: {decrypted} *** MATCH ***")
