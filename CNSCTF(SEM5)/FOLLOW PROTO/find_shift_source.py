encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"

#Required shifts: [13, 4, 19, 22, 14]
# Let me check all port-related values

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

# Check which values give us the required shifts
required_shifts = [13, 4, 19, 22, 14]
print("Finding source of required shifts:")
print(f"Required: {required_shifts}\n")

all_calc_values = {
    'a (SSH+DNS)': 75,
    'b (SMB-FTP)': 424,
    'c ((IMAP+POP3)*SMTP)': 6325,
    'd (STUN*Echo)': 24346,
    'Key': 13779,
    'SSH': 22,
    'DNS': 53,
    'SMB': 445,
    'FTP': 21,
    'IMAP': 143,
    'POP3': 110,
    'SMTP': 25,
    'STUN': 3478,
    'Echo': 7,
    '13': 13,  # First two digits of key
    '77': 77,  # Middle
    '79': 79,  # Last two
    '137': 137,
    '779': 779,
    'IMAP+POP3': 253,
}

for shift in required_shifts:
    print(f"Shift {shift}:")
    matches = []
    for name, val in all_calc_values.items():
        if val % 26 == shift:
            matches.append(f"  {name} = {val} (mod 26 = {shift})")
    if matches:
        for m in matches:
            print(m)
    else:
        print(f"  No direct match found")
    print()

# Hypothesis: Maybe it's [13, 30, 45, 22, 40]?
# 13, 30, 45, 22, 40 mod 26 = [13, 4, 19, 22, 14]
print("\n" + "="*50)
print("Hypothesis: shifts are [13, 30, 45, 22, 40]")
candidate_values = [13, 30, 45, 22, 40]
print(f"Values: {candidate_values}")
print(f"Mod 26: {[v % 26 for v in candidate_values]}")

# Let me check: what values from our calculation give these?
print("\nChecking matches:")
for val in candidate_values:
    for name, calc_val in all_calc_values.items():
        if calc_val == val:
            print(f"  {val} matches {name}")

# 13 = "13" from key
# 22 = SSH
# But 30, 45, 40 don't match anything obvious

# Let me try another approach: use the string "13779" parsed as "13", "7", "7", "9"
print("\n" + "="*50)
print("Try parsing key as: 13-7-7-9")
parsed = [13, 7, 7, 9]
print(f"Parsed: {parsed}")
print(f"Need to generate: {required_shifts}")

# What if I need to ADD something to these parsed values?
print("\nChecking if adding a constant works:")
for add_val in range(30):
    test = [(p + add_val) % 26 for p in parsed[:len(required_shifts)]]
    if test[:4] == required_shifts[:4]:  # Check first 4
        print(f"  Adding {add_val}: {test}")

# Or multiply?
print("\nChecking if multiplying works:")
for mult in range(1, 10):
    test = [(p * mult) % 26 for p in parsed[:len(required_shifts)]]
    if test[0] == required_shifts[0]:  # At least first matches
        print(f"  Multiplying by {mult}: {test}")
