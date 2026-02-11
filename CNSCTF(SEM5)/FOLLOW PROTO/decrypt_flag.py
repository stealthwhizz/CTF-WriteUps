encrypted_flag = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"
key = "13779"

print(f"Encrypted: {encrypted_flag}")
print(f"Key: {key} (repeating)")
print()

# Vigenere-style decryption using numeric key directly
print("=== Vigenere with numeric key (each digit as shift) ===")
result = []
key_index = 0
for char in encrypted_flag:
    if char.isalpha():
        shift = int(key[key_index % len(key)])
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

# Try adding instead of subtracting
print("=== Vigenere with numeric key (ADD instead) ===")
result = []
key_index = 0
for char in encrypted_flag:
    if char.isalpha():
        shift = int(key[key_index % len(key)])
        if char.isupper():
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)
decrypted = ''.join(result)
print(f"Decrypted: {decrypted}")
print()

# Try using the full key "13779" as a word key (converting to letters)
print("=== Using key as alphabetic positions ===")
# 1=A, 3=C, 7=G, 7=G, 9=I
alpha_key = ""
for digit in key:
    num = int(digit)
    if num == 0:
        alpha_key += 'Z'  # or handle 0 differently
    else:
        alpha_key += chr(ord('A') + num - 1)
print(f"Alphabetic key: {alpha_key}")

result = []
key_index = 0
for char in encrypted_flag:
    if char.isalpha():
        shift = ord(alpha_key[key_index % len(alpha_key)]) - ord('A')
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)
decrypted = ''.join(result)
print(f"Decrypted: {decrypted}")

