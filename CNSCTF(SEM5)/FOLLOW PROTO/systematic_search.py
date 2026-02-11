encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"

# Port numbers
SSH = 22
DNS = 53
SMB = 445
FTP = 21
IMAP = 143
POP3 = 110
SMTP = 25
STUN = 3478
Echo = 7

# Calculated values
a = SSH + DNS  # 75
b = SMB - FTP  # 424
c = (IMAP + POP3) * SMTP  # 6325
d = STUN * Echo  # 24346
Key = 13779

print("Trying different combinations to get [13, 4, 19, 22, 14]:")
print()

# Pattern found: 13 (IMAP), ?, 19 (IMAP+POP3), 22 (SSH), ?
# For position 1 (shift 4): need value that % 26 = 4
# For position 4 (shift 14): need value that % 26 = 14

# Could it be: [IMAP, DNS, IMAP+POP3, SSH, ?]?
test1 = [IMAP, DNS, IMAP+POP3, SSH, FTP]
shifts1 = [v % 26 for v in test1]
print(f"[IMAP, DNS, IMAP+POP3, SSH, FTP] = {test1}")
print(f"Mod 26: {shifts1}")
if shifts1 == [13, 4, 19, 22, 14]:
    print("*** POTENTIAL MATCH! Testing...")
    
    result = []
    key_index = 0
    for char in encrypted:
        if char.isalpha():
            shift = shifts1[key_index % len(shifts1)]
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
        print("\n*** FLAG FOUND! ***\n")
print()

# Let me try other combinations
combinations = [
    ([IMAP, DNS, IMAP+POP3, SSH, 14], "[IMAP, DNS, IMAP+POP3, SSH, 14]"),
    ([IMAP, 30, IMAP+POP3, SSH, 40], "[IMAP, 30, IMAP+POP3, SSH, 40]"),
    ([143, 30, 253, 22, 40], "[143, 30, 253, 22, 40]"),
    ([IMAP, DNS, IMAP+POP3, SSH, Echo*2], "[IMAP, DNS, IMAP+POP3, SSH, Echo*2]"),
]

for combo, desc in combinations:
    shifts = [v % 26 for v in combo]
    if shifts == [13, 4, 19, 22, 14]:
        print(f"{desc} = {combo}")
        print(f"Mod 26: {shifts} *** MATCH! ***")
        
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
        print(f"Decrypted: {decrypted}\n")
        if decrypted.startswith('isfcr'):
            print("*** FLAG FOUND! ***\n")
            break

print("="*60)
print("Let me systematically try to find what gives [13, 4, 19, 22, 14]")
print("="*60)

# Try all reasonable port combinations
all_ports = [SSH, DNS, SMB, FTP, IMAP, POP3, SMTP, STUN, Echo]
all_calcs = [a, b, c, d, Key, IMAP+POP3, IMAP+SMTP, POP3+SMTP]

from itertools import product

# This would be too many combinations, so let's be smarter
# We know: pos 0 = IMAP (143), pos 2 = IMAP+POP3 (253), pos 3 = SSH (22)
# Need to find: pos 1 (shift 4) and pos 4 (shift 14)

print("\nFinding value for position 1 (need shift 4):")
for val in all_ports + all_calcs + list(range(4, 200, 26)):
    if val % 26 == 4:
        print(f"  {val} % 26 = 4")

print("\nFinding value for position 4 (need shift 14):")
for val in all_ports + all_calcs + list(range(14, 200, 26)):
    if val % 26 == 4:
        print(f"  {val} % 26 = 14")
