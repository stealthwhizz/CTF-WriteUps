encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"

# The pattern that works for the first 5 characters
# [143 (IMAP), 30, 253 (IMAP+POP3), 22 (SSH), 40]
# Which gives shifts: [13, 4, 19, 22, 14]

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

# Try to figure out what 30 and 40 are
print("What are 30 and 40?")
print(f"30 = ? (could be: DNS-23={DNS-23}, FTP+9={FTP+9}, Echo*4+2={Echo*4+2}, SMTP+5={SMTP+5})")
print(f"40 = ? (could be: FTP*2-2={FTP*2-2}, DNS-13={DNS-13}, SSH+18={SSH+18}, DNS-DNS={DNS-DNS+40})")
print()

# Let me check if 30 = DNS - 23 or something simpler
# 30 could be: DNS (53) - 23 = 30
# Or: 30 could be from another calculation

# 40 could be: SSH (22) + 18 = 40
# Or Echo (7) * 5 + 5 = 40
# Or: 40 standalone

# For now, just use the shifts we know work
shifts = [13, 4, 19, 22, 14]

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
print(f"Decrypted with [13, 4, 19, 22, 14] repeating:")
print(decrypted)
print()

# The decrypted text is: isfcr{t4iemyb_x3tsq_c1t_emw_enlamsf_u0_07}
# This starts correctly with "isfcr{" but the rest seems odd
# Let me check if maybe I need a LONGER pattern, not just repeating these 5

# What if the full pattern is derived from all protocols in order?
# Let's try: [IMAP, DNS-23, IMAP+POP3, SSH, SSH+18, ...]

# Or maybe the pattern continues based on the equation order:
# a uses SSH+DNS
# b uses SMB-FTP
# c uses (IMAP+POP3)*SMTP -> we used IMAP+POP3 which is 253
# d uses STUN*Echo

# Let me try building a longer sequence
print("Trying longer patterns based on the calculation structure:")
print()

# Pattern attempt 1: Use all individual ports in equation order
pattern1 = [IMAP, DNS, IMAP+POP3, SSH, SMTP, STUN, Echo]
shifts1 = [v % 26 for v in pattern1]
print(f"Pattern 1 (ports in calc order): {pattern1}")
print(f"Shifts: {shifts1}")

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

decrypted1 = ''.join(result)
print(f"Decrypted: {decrypted1}")
if decrypted1.startswith('isfcr{') and '}' in decrypted1:
    # Check if it looks more readable
    print("Checking readability...")
print()

# Since the first 5 work, maybe I just need to continue the pattern differently
# Let me try: the numbers 30 and 40 might be: DNS-23=30, and (something)=40

# Actually, let me check: could it be DNS (53) - 23 = 30?
print(f"DNS - 23 = {DNS - 23} (this is 30!)")
print(f"Need to find what gives 40...")
print(f"  FTP*2 - 2 = {FTP*2-2}")
print(f"  SSH + 18 = {SSH+18}")
print(f"  SMTP + 15 = {SMTP+15}")
print()

# Let me try: [IMAP, DNS-23, IMAP+POP3, SSH, SMTP+15, ...]
pattern2 = [IMAP, DNS-23, IMAP+POP3, SSH, SMTP+15]
shifts2 = [v % 26 for v in pattern2]
print(f"Pattern 2: {pattern2}")
print(f"Shifts: {shifts2}")

if shifts2 == [13, 4, 19, 22, 14]:
    print("This matches! Let me extend it...")
    
    # What comes next? Continue the pattern...
    # Maybe: POP3, SMB, FTP, STUN, Echo?
    extended = [IMAP, DNS-23, IMAP+POP3, SSH, SMTP+15, POP3, SMB, FTP, STUN, Echo]
    shifts_ext = [v % 26 for v in extended]
    print(f"Extended pattern: {extended}")
    print(f"Shifts: {shifts_ext}")
    
    result = []
    key_index = 0
    for char in encrypted:
        if char.isalpha():
            shift = shifts_ext[key_index % len(shifts_ext)]
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    
    decrypted_ext = ''.join(result)
    print(f"\nFinal decrypted: {decrypted_ext}")
