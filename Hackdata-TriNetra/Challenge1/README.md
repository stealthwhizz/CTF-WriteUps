# 🔓 Challenge 1 - The Ghidra Treat

> **CTF:** Hackdata TriNetra CTF  
> **Category:** Reverse Engineering  
> **Difficulty:** Medium  
> **Flag:** `TriNetra{Th3_7r34t_GhIdRa}`

---

## 📋 Table of Contents

- [Challenge Overview](#-challenge-overview)
- [Initial Reconnaissance](#-initial-reconnaissance)
- [Deep Dive Analysis](#-deep-dive-analysis)
- [The Breakthrough](#-the-breakthrough)
- [Exploitation](#-exploitation)
- [Flag](#-flag)
- [Key Takeaways](#-key-takeaways)

---

## 🎯 Challenge Overview

We're handed a binary file called `chellange_1` (yes, with that creative typo 😄). Running it prompts us for a password and spits out what looks like encrypted garbage.

```bash
$ ./chellange_1
Show me the PassWoRDDDD!!!!
test
Heres a sting for you UwU xD :
 \M�x����.��8
```

Time to dig in! 🕵️

---

## 🔍 Initial Reconnaissance

### File Type Analysis

```bash
$ file chellange_1
chellange_1: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), 
dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, 
BuildID[sha1]=bf06e995b4b3ae27dac5912ac92c87f398987b10, 
for GNU/Linux 3.2.0, not stripped
```

**Key Observations:**
- ✅ 64-bit ELF executable
- ✅ Dynamically linked
- ✅ **Not stripped** - symbols are intact (jackpot for reverse engineering!)

### String Extraction

Let's see what secrets the binary is hiding:

```bash
$ strings chellange_1
```

**Interesting Findings:**
```
EVP_DigestInit_ex
EVP_blake2b512
EVP_DecryptFinal_ex
EVP_DecryptInit_ex
EVP_DecryptUpdate
EVP_aes_256_cbc
...
ce2f380761f7894d6cd89f98a0a40b5b1a0242b0e49a720c41ab5976ebf63b26
Show me the PassWoRDDDD!!!!
Heres a sting for you UwU xD :
```

**What we learned:**
- 🔐 Uses OpenSSL cryptography functions
- 🔑 **BLAKE2b-512** for hashing
- 🔒 **AES-256-CBC** for encryption/decryption
- 📝 Contains a hardcoded hex string (probably the encrypted flag!)

---

## 🔬 Deep Dive Analysis

### Dynamic Analysis with ltrace

Let's trace the library calls to understand the program's behavior:

```bash
$ ltrace -s 100 ./chellange_1 <<< "test"
```

**Critical Output:**
```bash
strlen("ce2f380761f7894d6cd89f98a0a40b5b1a0242b0e49a720c41ab5976ebf63b26") = 64
puts("Show me the PassWoRDDDD!!!! ")
__isoc23_scanf(...)
strlen("test") = 4
EVP_MD_CTX_new(...)
EVP_blake2b512(...)
EVP_DigestInit_ex(...)
EVP_DigestUpdate(..., 0x7ffdba2a5cff, 1, ...)  # 🚨 Only 1 byte!
EVP_DigestFinal_ex(...)
...
EVP_aes_256_cbc(...)
EVP_DecryptInit_ex(...)
EVP_DecryptUpdate(...)
EVP_DecryptFinal_ex(...) = 0  # Failed!
```

---

## 💡 The Breakthrough

**CRITICAL DISCOVERY:** The `EVP_DigestUpdate` call processes only **1 byte** of input! 

This is the vulnerability we need. The program:

1. Takes your password input
2. Extracts a **single byte** from it
3. Hashes that byte with BLAKE2b-512
4. Derives AES-256 key (first 32 bytes) and IV (next 16 bytes) from the hash
5. Attempts to decrypt the hardcoded data

**The flaw?** Only **256 possible values** (0x00 to 0xFF) for a single byte. This is trivially brute-forceable!

---

## 🎪 Exploitation

Since there are only 256 possibilities, let's try them all!

### The Attack Script

```python
#!/usr/bin/env python3
from Crypto.Cipher import AES
from hashlib import blake2b
import string

# Encrypted data from the binary
encrypted_hex = "ce2f380761f7894d6cd89f98a0a40b5b1a0242b0e49a720c41ab5976ebf63b26"
encrypted_data = bytes.fromhex(encrypted_hex)

printable = set(string.printable)

# Brute force all possible single byte values
for byte_val in range(256):
    try:
        # Hash the single byte with BLAKE2b-512
        h = blake2b(bytes([byte_val]), digest_size=64)
        hash_result = h.digest()
        
        # Extract key (first 32 bytes) and IV (next 16 bytes) from hash
        key = hash_result[:32]
        iv = hash_result[32:48]
        
        # Try to decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data)
        
        # Check if decryption produced valid data
        try:
            decrypted_str = decrypted.decode('ascii', errors='ignore')
            
            # Check if most characters are printable
            printable_count = sum(1 for c in decrypted_str if c in printable and c != '\x00')
            
            if printable_count > len(decrypted_str) * 0.5:
                char_rep = chr(byte_val) if 32 <= byte_val < 127 else f'\\x{byte_val:02x}'
                print(f"\nByte: {byte_val} ('{char_rep}')")
                print(f"ASCII: {repr(decrypted_str)}")
                
                # Check for flag format
                if "TriNetra" in decrypted_str:
                    print(f"🎉 *** FLAG FOUND *** 🎉")
        except:
            pass
            
    except Exception as e:
        pass

print("\nDone!")
```

### Running the Exploit

```bash
$ python3 solve.py
...
Byte: 71 ('G')
ASCII: 'TriNetra{Th3_7r34t_GhIdRa}\x06\x06\x06\x06\x06\x06'
🎉 *** FLAG FOUND *** 🎉
...
Done!
```

**Victory!** The magic byte is **71** (the character **'G'**).

### Verification

```bash
$ echo "G" | ./chellange_1
Show me the PassWoRDDDD!!!!
Heres a sting for you UwU xD :
 TriNetra{Th3_7r34t_GhIdRa}
```

Perfect! ✅

---

## 🚩 Flag

```
TriNetra{Th3_7r34t_GhIdRa}
```

**Fun Fact:** The flag is a wordplay on **"Ghidra"** - the famous NSA reverse engineering tool! 😄

---

## 🎓 Key Takeaways

1. **🔑 Key Space Matters:** Even with military-grade cryptography (BLAKE2b-512 + AES-256-CBC), a tiny key space (256 possibilities) makes brute force trivial.

2. **🔧 Dynamic Analysis is King:** Using `ltrace` revealed the critical detail that static analysis might have missed - only 1 byte being hashed.

3. **📚 Library Calls Tell Stories:** Tracing system and library calls can expose algorithmic weaknesses.

4. **🎯 Strings are Your Friend:** Always run `strings` on binaries - you might find hardcoded secrets!

5. **⚙️ Not Stripped = Easier RE:** Symbols make reverse engineering significantly easier.

6. **🔒 Crypto Implementation Matters:** Strong algorithms don't help if improperly implemented!

---

**Author:** whizy  
**Date:** February 8, 2026  
**Tools Used:** `file`, `strings`, `ltrace`, Python, PyCryptodome

---

*Remember: In crypto, your weakest link is often not the algorithm, but how you use it!* 🔐
