encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"
key = "13779"

print("Testing different decryption methods:")
print(f"Encrypted: {encrypted}")
print(f"Key: {key}")
print()

# Method: Use key as direct character mapping/substitution
# Let's see what we get if each letter maps based on key position
# v->i means shift of 13
# Let me check: what shift turns "vwyyf" into "isfcr"?

target = "isfcr"
source = "vwyyf"

print("Character shift analysis:")
for i in range(min(len(source), len(target))):
    shift = (ord(source[i]) - ord(target[i])) % 26
    print(f"{source[i]} -> {target[i]}: shift = {shift}")
print()

# Try using those shifts: 13, 14, 14, 14, 3
# This matches the pattern: 1+3+7+7+9 mod something?

# Let's try: maybe the key needs to be summed cumulatively?
print("Method: Cumulative key sum")
key_sum = 0
shifts = []
for d in key:
    key_sum += int(d)
    shifts.append(key_sum % 26)
print(f"Cumulative shifts: {shifts}")

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
print(f"Decrypted: {decrypted}")
print()

# Let me also check if pattern is: 13, 14, 14, 14, 3
# which could be key digits multiplied or added differently
print("Method: Pattern 13,14,14,14,3,13,14...")
# Let's see: 13 = 1*10+3? Or 1+3+9 (from 1,3,7,7,9)?
# Actually: v->i = 13, w->s = 4, y->f = 19, y->c = 22, f->r = 10

# Let me try a pattern where we use key differently
print("Method: Key digit pairs and patterns")
# What if 13779 means: shift by 13, then 7, then 79, then...?
patterns = ["13779", "137", "1377", "13", "7", "79", "377", "9"]
for pattern in patterns:
    result = []
    key_index = 0
    for char in encrypted:
        if char.isalpha():
            if len(pattern) > key_index:
                try:
                    shift = int(pattern[key_index:key_index+2] if key_index+1 < len(pattern) else pattern[key_index])
                except:
                    shift = int(pattern[key_index])
            else:
                shift = int(pattern[key_index % len(pattern)])
            
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    decrypted = ''.join(result)
    if decrypted.startswith('isfcr'):
        print(f"Pattern '{pattern}': {decrypted} *** MATCH ***")
