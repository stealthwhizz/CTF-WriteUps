# Following Protocol — CTF Writeup

**Challenge:** Following Protocol  
**Goal:** Unlock the PDF and recover the flag.  
**Ciphertext extracted from the unlocked PDF:**
```
vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}
```

---

## 🧮 Step 1 — Compute the Key

Using standard network protocol ports:

- SSH = 22  
- DNS = 53 → **a = 75**

- SMB = 445  
- FTP = 21 → **b = 424**

- IMAP = 143  
- POP3 = 110  
- SMTP = 25 → **c = 6325**

- STUN = 3478  
- Echo = 7 → **d = 24346**

Final numeric key:
```
(a × b) + (c – d)
= (75 × 424) + (6325 – 24346)
= 31800 – 18021
= 13779
```

**Computed key = `13779`**

---

## 🔑 Step 2 — Interpreting “The network hides its secrets, repeat the key”

The phrase strongly hints at a *repeated-key* cipher.  
Trying likely Vigenère keys derived from the clue:

- `13779` (digit shifts) → fails  
- `"13779"` (XOR) → fails  
- **`network`** → ✔ produces valid plaintext

The hidden hint was the word **network**.

---

## 🔓 Step 3 — Decrypting the Ciphertext

Ciphertext:
```
vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}
```

Using Vigenère key: `network`  
Decrypted result:
```
isfcr{p4ckets_n3ver_l1e_but_headers_d0_07}
```

---

## 🏁 Final Flag

```
isfcr{p4ckets_n3ver_l1e_but_headers_d0_07}
```

---

## 🐍 Reproducible Python Snippet

```python
def vigenere_decrypt(cipher, key):
    res = []
    ki = 0
    for ch in cipher:
        if 'a' <= ch <= 'z':
            k = ord(key[ki % len(key)].lower()) - ord('a')
            res.append(chr((ord(ch) - ord('a') - k) % 26 + ord('a')))
            ki += 1
        elif 'A' <= ch <= 'Z':
            k = ord(key[ki % len(key)].lower()) - ord('a')
            res.append(chr((ord(ch) - ord('A') - k) % 26 + ord('A')))
            ki += 1
        else:
            res.append(ch)
    return ''.join(res)

cipher = "vwyyf{g4mximo_b3moe_p1x_xik_rrewafj_n0_07}"
key = "network"

print(vigenere_decrypt(cipher, key))
```

---

## ✔ Notes

- The flag shape `isfcr{...}` confirms successful decryption.  
- The challenge blends port-number arithmetic with a classic Vigenère cipher twist.  
- The hint text intentionally hides the keyword in plain sight.

---
