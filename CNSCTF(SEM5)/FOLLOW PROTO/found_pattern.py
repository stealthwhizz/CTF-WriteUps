encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"
key_digits = [1, 3, 7, 7, 9]

print(f"Encrypted: {encrypted}")
print(f"Key: {key_digits}")
print()

# Pattern found: position^2 + key_digit (maybe with some adjustment)
# Let's try: (position + something)^2 + key_digit

# Or maybe: 12 + key_digit for certain positions?
# Notice: position 0 and 2 both have difference of 12

# Let me try: (position * position) + key + 12
print("Testing: i^2 + k + 12:")
for i in range(len(key_digits)):
    k = key_digits[i]
    calculated = ((i * i) + k + 12) % 26
    print(f"Position {i}: {i}^2 + {k} + 12 = {calculated}")

print()

# Use this formula to decrypt
shift_pattern = []
for i in range(50):  # Generate enough shifts
    k = key_digits[i % len(key_digits)]
    shift = ((i * i) + k + 12) % 26
    shift_pattern.append(shift)

print(f"Shift pattern (first 20): {shift_pattern[:20]}")
print()

result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = shift_pattern[key_index]
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
    print("*** MATCH! ***")
