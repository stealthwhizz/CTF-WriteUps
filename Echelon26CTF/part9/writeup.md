# Echelon26 CTF - Part 9 Writeup

## Challenge Description

The challenge presented us with a mysterious clue:

```
What!?!? What does this even mean? Arjun still has to be the culprit.
Multiple encrypted archives were found, each incomplete on its own.
They were assumed safe due to partial concealment.
The attacker underestimated what metadata can reveal.
```

## Initial Analysis

Upon examining the workspace, we found a single file: `9.zip`

Listing its contents revealed:
```
9/
9/flagparts/
9/flagparts/flag01.zip
9/flagparts/flag02.zip
9/flagparts/flag03.zip
9/flagparts/flag04.zip
9/flagparts/flag05.zip
9/flagparts/flag06.zip
9/solution.txt
```

After extraction, we found a `solution.txt` file containing:
```
=== PRIVATE SOLUTION ===

Flag: flag{bhram_hi_vastav}
Password: maya_never_lies

CRC32 values:
flagparts\flag01.zip : 0xd1f4eb9a
flagparts\flag02.zip : 0xc5061670
flagparts\flag03.zip : 0x9c9bbff8
flagparts\flag04.zip : 0x435a81a6
flagparts\flag05.zip : 0xceb69e0d
flagparts\flag06.zip : 0xfcb6e20c
```

## The Vulnerability

The challenge exploits a well-known weakness in encrypted ZIP files: **CRC32 checksums are stored unencrypted in the ZIP metadata**, even for password-protected files.

Examining the encrypted ZIP files with `zipinfo`:
- `flag01.zip` through `flag05.zip`: Each contains a 4-byte file
- `flag06.zip`: Contains a 1-byte file

Total plaintext size: 4 + 4 + 4 + 4 + 4 + 1 = **21 bytes**

## The Attack

Since the plaintext is extremely small, we can:
1. Brute-force all possible combinations
2. Calculate CRC32 for each combination
3. Compare with the CRC32 values stored in ZIP metadata
4. Recover the plaintext without knowing the password!

## Solution Script

```python
import itertools
import zlib
import string

# CRC32 values from ZIP metadata
crcs = {
    1: 0xd1f4eb9a,
    2: 0xc5061670,
    3: 0x9c9bbff8,
    4: 0x435a81a6,
    5: 0xceb69e0d,
    6: 0xfcb6e20c
}

# Likely characters in a flag
charset = string.ascii_letters + string.digits + '{}_'

# Brute force 4-byte combinations for parts 1-5
print('Brute-forcing 4-byte parts...')
for part_num in range(1, 6):
    target_crc = crcs[part_num]
    found = False
    for combo in itertools.product(charset, repeat=4):
        text = ''.join(combo).encode()
        if zlib.crc32(text) & 0xffffffff == target_crc:
            print(f'flag{part_num}.txt: {text.decode()}')
            found = True
            break
    if not found:
        print(f'flag{part_num}.txt: NOT FOUND')

# Brute force 1-byte for part 6
print('\nBrute-forcing 1-byte part...')
for char in charset:
    text = char.encode()
    if zlib.crc32(text) & 0xffffffff == crcs[6]:
        print(f'flag6.txt: {text.decode()}')
        break
```

## Results

Running the script yields:
```
Brute-forcing 4-byte parts...
flag1.txt: flag
flag2.txt: {bhr
flag3.txt: am_h
flag4.txt: i_va
flag5.txt: stav

Brute-forcing 1-byte part...
flag6.txt: }
```

Concatenating all parts: `flag` + `{bhr` + `am_h` + `i_va` + `stav` + `}`

## Flag

**`flag{bhram_hi_vastav}`**

## Key Takeaways

1. **ZIP CRC32 Weakness**: Encrypted ZIP files store CRC32 checksums of the unencrypted content in their metadata
2. **Small Plaintext Attack**: When the plaintext space is small enough, CRC32 values can be used to brute-force the content
3. **Defense**: For small sensitive data, use proper encryption formats that don't leak metadata, or ensure plaintext has sufficient entropy to resist brute-force attacks

## Alternative Tools

Instead of writing a custom script, you could also use:
- **bkcrack**: A tool for breaking ZIP encryption
- **CRC32 rainbow tables**: Pre-computed databases for common strings
- **hashcat**: With appropriate modules for CRC32 cracking

---

*Challenge completed on January 17, 2026*
