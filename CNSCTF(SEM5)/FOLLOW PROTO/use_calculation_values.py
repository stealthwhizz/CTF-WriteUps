encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"

# I know these are the exact shifts needed for the first 5 characters
# Let me just apply them and see what the full message says
required_first_5 = [13, 4, 19, 22, 14]

print(f"Encrypted: {encrypted}")
print(f"Known shifts for first 5: {required_first_5}")
print()

# Apply these shifts repeating
result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = required_first_5[key_index % len(required_first_5)]
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

# This gives us: isfcr{t4iemyb_x3tsq_c1t_emw_enlamsfneed_u0_07}
# The beginning "isfcr{" looks right!
# Let me see if I can figure out what the full message should be

# The pattern seems to work! So the question is: how do we derive 
# [13, 4, 19, 22, 14] from key "13779"?

# Let me check: could it be that we need to look at the CALCULATION itself?
# The values from the calculation were:
# a = 75
# b = 424
# c = 6325
# d = 24346
# Key = 13779

print("Values from calculation:")
print("a = 75")
print("b = 424") 
print("c = 6325")
print("d = 24346")
print("Key = 13779")
print()

# Maybe use these values?
values = [75, 424, 6325, 24346, 13779]
shifts_from_values = [v % 26 for v in values]
print(f"Values mod 26: {shifts_from_values}")

result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = shifts_from_values[key_index % len(shifts_from_values)]
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)

decrypted = ''.join(result)
print(f"\nUsing [a, b, c, d, key] mod 26 = {shifts_from_values}:")
print(decrypted)

if decrypted.startswith('isfcr'):
    print("\n*** MATCH FOUND! ***")
    print(f"\nThe flag is: {decrypted}")
