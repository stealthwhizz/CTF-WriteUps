encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"

# The working pattern
shifts = [13, 4, 19, 22, 14]

print(f"Encrypted: {encrypted}")
print(f"Shift pattern: {shifts}")
print()

result = []
key_index = 0
for i, char in enumerate(encrypted):
    if char.isalpha():
        shift = shifts[key_index % len(shifts)]
        if char.isupper():
            decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        
        print(f"Pos {key_index}: '{char}' - {shift} = '{decrypted_char}'")
        result.append(decrypted_char)
        key_index += 1
    else:
        result.append(char)
        print(f"         '{char}' (unchanged)")

decrypted = ''.join(result)
print(f"\nFinal flag: {decrypted}")
print()

# Let me also check if maybe it's a double-encryption or needs further processing
print("Checking if this needs further decryption...")
# The format looks right: isfcr{...}
# The numbers look right: 4, 3, 1, 0, 07
# But the letters seem random

# Maybe this IS the correct flag and it's intentionally obfuscated?
# Or maybe the underscore-separated parts have meaning?

parts = decrypted[6:-1].split('_')  # Remove "isfcr{" and "}"
print(f"Parts separated by underscore: {parts}")
