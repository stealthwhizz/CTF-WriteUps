key_digits = [1, 3, 7, 7, 9]
required_shifts = [13, 4, 19, 22, 14]

print("Analyzing relationship between key and required shifts:")
print(f"Key digits:      {key_digits}")
print(f"Required shifts: {required_shifts}")
print()

# Let's check various mathematical relationships
for i in range(len(key_digits)):
    k = key_digits[i]
    r = required_shifts[i]
    print(f"Position {i}: key={k}, required={r}")
    print(f"  r - k = {r - k}")
    print(f"  r + k = {r + k}")
    print(f"  r * k = {r * k}")
    print(f"  r / k = {r / k if k != 0 else 'N/A'}")
    print(f"  r % k = {r % k if k != 0 else 'N/A'}")
    print()

# Looking for a pattern...
# Position 0: k=1, r=13 -> difference=12, r-k=12
# Position 1: k=3, r=4 -> difference=1, r-k=1
# Position 2: k=7, r=19 -> difference=12, r-k=12
# Position 3: k=7, r=22 -> difference=15, r-k=15
# Position 4: k=9, r=14 -> difference=5, r-k=14

print("Differences: ", [required_shifts[i] - key_digits[i] for i in range(len(key_digits))])

# Hmm, [12, 1, 12, 15, 5]
# Could this be based on position? Let's see:
# pos 0: +12
# pos 1: +1
# pos 2: +12
# pos 3: +15
# pos 4: +5

# Wait! Let me check if it's fibonacci or another sequence
# Or maybe it's: position^2 + key_digit?
for i in range(len(key_digits)):
    k = key_digits[i]
    r = required_shifts[i]
    calculated = (i * i + k) % 26
    print(f"i^2 + k: {i}^2 + {k} = {calculated} (required: {r})")

print()

# Try: (position * 12) + key_digit
for i in range(len(key_digits)):
    k = key_digits[i]
    r = required_shifts[i]
    calculated = ((i * 12) + k) % 26
    print(f"(i * 12) + k: ({i} * 12) + {k} = {calculated} (required: {r})")

print()

# Maybe we need to use the cumulative sum of ports or another derived value?
# Let's try using position index more creatively

# Or maybe reverse: use the required shifts directly!
print("What if the required shifts ARE correct and we need to apply them?")
encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"

# Let me just try applying [13, 4, 19, 22, 14] repeatedly
result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = required_shifts[key_index % len(required_shifts)]
        if char.isupper():
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        key_index += 1
    else:
        result.append(char)
decrypted = ''.join(result)
print(f"Using [13, 4, 19, 22, 14]: {decrypted}")

# Maybe the pattern continues differently?
# Let me try building the full pattern programmatically
print("\nTrying to derive the full shift pattern...")
