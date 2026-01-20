encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"
key = "13779"

print("Testing: Use KEY as literal string in different ways")
print(f"Encrypted: {encrypted}")
print(f"Key: {key}")
print()

# Method 1: XOR with key repeated as string (ASCII values)
print("Method 1: XOR with ASCII values of key string")
result = []
key_index = 0
for char in encrypted:
    key_char = key[key_index % len(key)]
    xor_result = chr(ord(char) ^ ord(key_char))
    result.append(xor_result)
    key_index += 1
decrypted = ''.join(result)
print(f"Decrypted: {decrypted}")
if 'isfcr' in decrypted:
    print("*** MATCH! ***")
print()

# Method 2: Subtract ASCII values
print("Method 2: Subtract ASCII values of key")
result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        key_char_val = ord(key[key_index % len(key)])
        new_val = (ord(char) - key_char_val) % 26
        if char.isupper():
            result.append(chr(new_val + ord('A')))
        else:
            result.append(chr(new_val + ord('a')))
        key_index += 1
    else:
        result.append(char)
decrypted = ''.join(result)
print(f"Decrypted: {decrypted}")
if 'isfcr' in decrypted:
    print("*** MATCH! ***")
print()

# Method 3: Use key as word "THIRTEEN SEVEN SEVEN NINE" -> "THIRTEEN..."
# Or just the initials or something
print("Method 3: Convert 13779 to words")
# Let me just try some creative interpretations
interpretations = [
    "THIRTEEN",
    "ONETHRSEVSEVNIN",  # ONE THREE SEVEN SEVEN NINE compressed
]

for interp in interpretations:
    result = []
    key_index = 0
    for char in encrypted:
        if char.isalpha():
            shift = ord(interp[key_index % len(interp)].upper()) - ord('A')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    decrypted = ''.join(result)
    print(f"Using '{interp}': {decrypted[:20]}...")
    if 'isfcr' in decrypted:
        print("*** MATCH! ***")
        print(f"Full: {decrypted}")

print()

# Method 4: What if "repeat the key" means use it twice? 1377913779?
print("Method 4: Key repeated once (1377913779)")
doubled_key = key + key
result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = int(doubled_key[key_index % len(doubled_key)])
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)
decrypted = ''.join(result)
print(f"Decrypted: {decrypted}")
if 'isfcr' in decrypted:
    print("*** MATCH! ***")
