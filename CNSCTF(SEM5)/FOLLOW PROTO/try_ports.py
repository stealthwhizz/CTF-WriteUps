encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"

# Protocol port numbers from the challenge
ports = {
    'SSH': 22,
    'DNS': 53,
    'SMB': 445,
    'FTP': 21,
    'IMAP': 143,
    'POP3': 110,
    'SMTP': 25,
    'STUN': 3478,
    'Echo': 7
}

print("Port numbers:")
for name, port in ports.items():
    print(f"  {name}: {port} (mod 26 = {port % 26})")

print()

# Try using port numbers in order they appear
port_sequence = [22, 53, 445, 21, 143, 110, 25, 3478, 7]
shifts_from_ports = [p % 26 for p in port_sequence]
print(f"Port sequence mod 26: {shifts_from_ports}")

result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = shifts_from_ports[key_index % len(shifts_from_ports)]
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)

decrypted = ''.join(result)
print(f"\nUsing all ports in order:")
print(decrypted)
if decrypted.startswith('isfcr'):
    print("*** MATCH! ***")

print("\n" + "="*50)

# What if I need: a, b, then the individual components?
# a = SSH + DNS = 75
# b = SMB - FTP = 424
# Then SSH, DNS, SMB, FTP individually?

combined_sequence = [75, 424, 22, 53, 445]  # a, b, then individual ports
shifts = [v % 26 for v in combined_sequence]
print(f"\nTrying [a, b, SSH, DNS, SMB] = {combined_sequence}")
print(f"Shifts (mod 26): {shifts}")

result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = shifts[key_index % len(shifts)]
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)

decrypted = ''.join(result)
print(f"\nDecrypted:")
print(decrypted)
if decrypted.startswith('isfcr'):
    print("*** MATCH! ***")

print("\n" + "="*50)

# Let me try: [Key, a, b, c, d]
sequence = [13779, 75, 424, 6325, 24346]
shifts = [v % 26 for v in sequence]
print(f"\nTrying [Key, a, b, c, d] = {sequence}")
print(f"Shifts (mod 26): {shifts}")

result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = shifts[key_index % len(shifts)]
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)

decrypted = ''.join(result)
print(f"\nDecrypted:")
print(decrypted)
if decrypted.startswith('isfcr'):
    print("*** MATCH! ***")

print("\n" + "="*50)

# Required shifts are: [13, 4, 19, 22, 14]
# Let me check what gives us these...
# 13 = ?
# 22 mod 26 = 22 (SSH!)
# Let me try: [key%26, something, something, SSH, something]

# Actually, let's work backwards from required shifts
required = [13, 4, 19, 22, 14]
print(f"\nRequired shifts: {required}")
print("Checking which values mod 26 give these:")
print(f"  13: could be 13, 39, 65, 91, 117, 143...")
print(f"  4: could be 4, 30, 56, 82, 108, 134...")  
print(f"  19: could be 19, 45, 71, 97, 123, 149...")
print(f"  22: could be 22 (SSH!), 48, 74, 100...")
print(f"  14: could be 14, 40, 66, 92, 118...")

# 13 could be 13 (part of key!)
# 22 could be 22 (SSH!)
# Let me check: 13779 % 26 = ?
print(f"\n13779 % 26 = {13779 % 26}")  # Should be 25

# Hmm, what about the first two digits: "13" from "13779"?
print(f"First two digits of key: 13")
print(f"13 % 26 = {13}")  # This matches!
