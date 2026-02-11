encrypted = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"
key_str = "13779"

print(f"Encrypted: {encrypted}")
print(f"Key string: {key_str}")
print()

# The target should start with "isfcr"
# Let's work backwards: what key would transform "vwyyf" to "isfcr"?

source = "vwyyf"
target = "isfcr"

print("Required shifts to get from encrypted to target:")
required_shifts = []
for i in range(len(source)):
    shift = (ord(source[i]) - ord(target[i])) % 26
    required_shifts.append(shift)
    print(f"  {source[i]} -> {target[i]}: shift {shift}")
print(f"Required pattern: {required_shifts}")
print()

# Required: [13, 4, 19, 22, 14]
# Key: "13779" -> digits [1, 3, 7, 7, 9]
# Hmm... 13, 4... wait, what if it's: 1*10+3=13, 3+1=4, 7*2+5=19...?
# Or: could there be an offset/seed value?

# What if the key calculation needs to involve the protocol calculation itself?
# Let me try using the key digits with different operations

print("Testing mathematical combinations:")
key_digits = [int(d) for d in key_str]
print(f"Key digits: {key_digits}")

# Try: first digit as-is, then add previous...
running_shifts = []
prev = 0
for d in key_digits:
    current = (prev + d) % 26
    running_shifts.append(current)
    prev = current
print(f"Running sum (mod 26): {running_shifts}")

# Try decryption with running sum
result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = running_shifts[key_index % len(running_shifts)]
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
print()

# What if I multiply each position?
print("Testing: position * key_digit:")
pos_mult = []
for i, d in enumerate(key_digits):
    val = ((i+1) * d) % 26
    pos_mult.append(val)
print(f"Position multiplied: {pos_mult}")

result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = pos_mult[key_index % len(pos_mult)]
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
print()

# Try using full calculated key as number: 13779
# Maybe modulo or division operations?
print("Using full key value 13779:")
full_key = 13779

# Generate shift sequence from key
shift_sequence = []
temp = full_key
while len(shift_sequence) < 50:  # Generate enough shifts
    digit = temp % 10
    shift_sequence.append(digit)
    temp = temp // 10
    if temp == 0:
        temp = full_key  # Reset

shift_sequence.reverse()  # Original order
print(f"Shift sequence from key: {shift_sequence[:20]}")

result = []
key_index = 0
for char in encrypted:
    if char.isalpha():
        shift = shift_sequence[key_index % len(shift_sequence)]
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
