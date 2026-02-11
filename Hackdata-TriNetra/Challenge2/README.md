# Challenge 2 - TriNetra CTF Write-up

**Challenge Name:** Challenge 2  
**Category:** Reverse Engineering  
**Flag:** `TriNetra{PyTh0n_Sh4d0w_L0g1c}`

## Challenge Description

The challenge provides a zip file containing a Python script and a compiled Python bytecode file.

## Files Provided

- `chall4.zip` - Archive containing:
  - `main.py` - Entry point script
  - `secret.pyc` - Compiled Python bytecode (Python 3.8)

## Initial Analysis

### main.py

```python
from secret import verify

print("TriNetra watches silently...")
x = input("Speak the sacred phrase: ")

if verify(x):
    print("TriNetra accepts.")
else:
    print("TriNetra rejects.")
```

The script imports a `verify` function from the `secret` module and checks user input against some expected value.

### secret.pyc

Running `file secret.pyc` or examining the magic bytes reveals this is Python 3.8 bytecode:
- Magic number: `61 0D 0D 0A` (Python 3.8)
- Cannot be directly imported on Python 3.13

## Solution Approach

Since traditional decompilers (uncompyle6, pycdc) don't support the current Python version or the bytecode format, we need to analyze the raw bytecode.

### Step 1: Hex Dump Analysis

Using PowerShell to examine the file:

```powershell
Format-Hex .\secret.pyc | Out-String
```

Key observations from the hex dump:
- Function names: `enc`, `verify`, `enumerate`, `append`, `ord`
- Constant array labeled `TARGET`
- Character operations at different positions

### Step 2: Extract TARGET Array

The TARGET array contains 29 encoded values that represent the expected flag:

```powershell
$bytes = [System.IO.File]::ReadAllBytes("secret.pyc")
$target = @()
for ($i = 0; $i -lt $bytes.Length - 3; $i++) {
    if ($bytes[$i] -eq 0xE9 -and $bytes[$i+2] -eq 0x00 -and $bytes[$i+3] -eq 0x00 -and $bytes[$i+4] -eq 0x00) {
        $target += $bytes[$i+1]
    }
}
```

**TARGET values:**
```
[117, 118, 103, 111, 105, 114, 83, 101, 121, 113, 125, 82, 73, 52, 108, 126, 87, 102, 21, 104, 46, 86, 99, 74, 17, 107, 47, 66, 129]
```

### Step 3: Reverse Engineering the Encoding

By analyzing the bytecode structure and patterns, the encoding function applies different operations based on character position modulo 3:

```python
def enc(s):
    out = []
    for i, c in enumerate(s):
        if i % 3 == 0:
            out.append(ord(c) ^ 33)    # XOR with 33
        elif i % 3 == 1:
            out.append(ord(c) + 4)     # Add 4
        else:  # i % 3 == 2
            out.append(ord(c) - 2)     # Subtract 2
    return out
```

### Step 4: Decode the Flag

To reverse the encoding:
- Position `i % 3 == 0`: Apply XOR with 33 again (XOR is self-inverse)
- Position `i % 3 == 1`: Subtract 4 (inverse of add)
- Position `i % 3 == 2`: Add 2 (inverse of subtract)

```python
TARGET = [117, 118, 103, 111, 105, 114, 83, 101, 121, 113, 125, 82, 73, 52, 108, 126, 87, 102, 21, 104, 46, 86, 99, 74, 17, 107, 47, 66, 129]

flag = []
for i, val in enumerate(TARGET):
    if i % 3 == 0:
        flag.append(chr(val ^ 33))    # XOR with 33
    elif i % 3 == 1:
        flag.append(chr(val - 4))     # Subtract 4
    else:  # i % 3 == 2
        flag.append(chr(val + 2))     # Add 2

result = ''.join(flag)
print(result)  # TriNetra{PyTh0n_Sh4d0w_L0g1c}
```

## Verification

```python
def enc(s):
    out = []
    for i, c in enumerate(s):
        if i % 3 == 0:
            out.append(ord(c) ^ 33)
        elif i % 3 == 1:
            out.append(ord(c) + 4)
        else:
            out.append(ord(c) - 2)
    return out

TARGET = [117, 118, 103, 111, 105, 114, 83, 101, 121, 113, 125, 82, 73, 52, 108, 126, 87, 102, 21, 104, 46, 86, 99, 74, 17, 107, 47, 66, 129]

flag = "TriNetra{PyTh0n_Sh4d0w_L0g1c}"
print(enc(flag) == TARGET)  # True
```

## Flag

```
TriNetra{PyTh0n_Sh4d0w_L0g1c}
```

## Key Takeaways

1. **Bytecode Analysis**: When decompilers fail, manual bytecode analysis using hex dumps can reveal program logic
2. **Pattern Recognition**: The encoding used position-dependent transformations (modulo 3)
3. **PowerShell Utilities**: PowerShell's `Format-Hex` and binary file manipulation capabilities are useful for reverse engineering
4. **Crypto Reversal**: Understanding the inverse of mathematical operations (XOR is self-inverse, addition ↔ subtraction)

## Tools Used

- PowerShell (hex dump and binary analysis)
- Python 3.13 (decoding script)
- Manual bytecode inspection
