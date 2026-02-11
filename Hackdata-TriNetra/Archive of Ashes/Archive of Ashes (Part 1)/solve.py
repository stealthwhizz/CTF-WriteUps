#!/usr/bin/env python3

# Ciphertext from the PDF
ciphertext_lines = [
    "CKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCKCyC",
    "EKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKEKF"
]

ciphertext = ''.join(ciphertext_lines)

print(f"Ciphertext length: {len(ciphertext)}")
print(f"First 100 chars: {ciphertext[:100]}")

# Analyze patterns - this looks like a repeating key cipher
# The repeating "CK" and "EK" patterns suggest the key is repeating

def vigenere_decrypt(ciphertext, key):
    """Decrypt Vigenere cipher"""
    plaintext = []
    key = key.upper()
    key_length = len(key)
    
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            # Get the key character for this position
            key_char = key[i % key_length]
            
            # Decrypt the character
            if char.isupper():
                decrypted = chr((ord(char) - ord(key_char) + 26) % 26 + ord('A'))
            else:
                decrypted = chr((ord(char.upper()) - ord(key_char) + 26) % 26 + ord('a'))
            
            plaintext.append(decrypted)
        else:
            plaintext.append(char)
    
    return ''.join(plaintext)

def find_key_length(ciphertext):
    """Find likely key length using Kasiski examination"""
    # Look for repeating sequences
    sequences = {}
    for length in range(3, 6):  # Look for 3-5 character sequences
        for i in range(len(ciphertext) - length):
            seq = ciphertext[i:i+length]
            if seq.isalpha():
                if seq in sequences:
                    sequences[seq].append(i)
                else:
                    sequences[seq] = [i]
    
    # Find sequences that repeat
    print("\nRepeating sequences:")
    for seq, positions in sequences.items():
        if len(positions) > 1:
            distances = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
            print(f"  {seq}: positions {positions[:5]}, distances {distances[:5]}")

# The repeating pattern "CK" and "EK" suggests the plaintext might be "AA" or similar
# Let's try to deduce the key from the pattern

# If plaintext is "A" (0) and ciphertext is "C" (2), then key char is "C" (2)
# If plaintext is "A" (0) and ciphertext is "K" (10), then key char is "K" (10)

# The pattern CK repeating suggests the key is 2 characters: "CK"
# Let's test

print("\n" + "="*50)
print("Testing key: CK")
print("="*50)
result = vigenere_decrypt(ciphertext, "CK")
print(result)

# Also try other possibilities
for key in ["AB", "AA", "KEY", "VIG", "CIPHER"]:
    print(f"\n{'='*50}")
    print(f"Testing key: {key}")
    print("="*50)
    result = vigenere_decrypt(ciphertext, key)
    print(result[:200])
    if "TriNetra" in result or "trinetra" in result.lower():
        print(f"\n*** FOUND FLAG with key: {key} ***")
        print(result)
        break
