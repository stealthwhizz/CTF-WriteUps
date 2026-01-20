# Echelon26 CTF - Part 8: Hidden Message in Dataset

## Challenge Description

> A structured dataset was pulled from an internal dump.
> Everything appears legitimate, purposeful, and clean.
> But investigators suspect the meaning lies beneath interpretation.

**Flag**: `flag{satya_chhupa_hai}`

## Initial Analysis

The challenge provides a zip file containing:
- `dataset.csv` - A seemingly legitimate ML dataset with 515 rows
- `solution.txt` - A hint file (found after extraction)

### Dataset Structure

The CSV file appears to be a standard machine learning dataset with the following columns:
- `feature_1` - Integer values (3-12 range)
- `feature_2` - Integer values (0-9 range)
- `normalized` - Normalized float values
- `class_label` - Classification labels (0-3)
- `confidence` - Confidence scores (0.5-1.0)

Sample data:
```csv
feature_1,feature_2,normalized,class_label,confidence
7,3,0.574803,1,0.8027
11,0,0.866142,2,0.7613
3,2,0.251969,0,0.6793
```

At first glance, this looks like a legitimate dataset for classification tasks. The normalized values, class labels, and confidence scores all appear statistically reasonable.

## The Hidden Message

The key insight from the solution file reveals:

> **Decoding logic:**
> ```
> ascii = feature_1 * 10 + feature_2
> chr(ascii) for each row
> ```

The first two columns (`feature_1` and `feature_2`) encode ASCII character values! The remaining columns are just noise/decoy data to make it look legitimate.

## Solution Method

### Decoding Script

```python
import csv

with open('dataset.csv', 'r') as f:
    reader = csv.DictReader(f)
    message = ""
    for row in reader:
        feature_1 = int(row['feature_1'])
        feature_2 = int(row['feature_2'])
        ascii_val = feature_1 * 10 + feature_2
        message += chr(ascii_val)
    print(message)
```

### How It Works

Each row encodes one character:
- Row 1: `7 × 10 + 3 = 73` → `chr(73)` = `'I'`
- Row 2: `11 × 10 + 0 = 110` → `chr(110)` = `'n'`
- Row 3: `3 × 10 + 2 = 32` → `chr(32)` = `' '` (space)

## Decoded Message

Running the decoder reveals a cryptographic riddle:

```
In Maya's veil, numbers braid like mantras, two primes whispering Ra and Sa. 
Arjuna draws his bow at reflections, for illusion splits truth as keys split 
locks. A public face gleams in the hall of mirrors, signed and verified by the 
crowd. Yet the private hand is elsewhere, unseen, multiplying silence behind 
the screen. Know this riddle: the name you read authenticates, but does not 
encrypt the deed. Thus it is revealed, Arjun Rampal is a shadow on the wall, 
not the hacker at the core. flag{satya_chhupa_hai}
```

### Message Analysis

The decoded text is a poetic riddle about RSA cryptography:
- **"Maya's veil"** - Illusion (steganography/hiding in plain sight)
- **"Two primes whispering Ra and Sa"** - RSA uses two prime numbers (p and q)
- **"Public face... signed and verified"** - Public key cryptography
- **"Private hand... unseen, multiplying"** - Private key operations
- **"The name you read authenticates, but does not encrypt"** - RSA signatures vs encryption
- **"Arjun Rampal"** - A red herring (Bollywood actor's name sounds like "RSA")

## Flag

**`flag{satya_chhupa_hai}`**

In Hindi, "satya chhupa hai" (सत्य छुपा है) means **"the truth is hidden"** - a perfect metaphor for this steganography challenge!

## Key Takeaways

1. **Steganography in Plain Sight**: The dataset looked completely normal, hiding the message in what appeared to be legitimate ML features
2. **ASCII Encoding**: Simple but effective - using decimal digits to encode ASCII values (tens and ones place)
3. **Decoy Data**: The normalized, class_label, and confidence columns were completely meaningless - just statistical noise to maintain the illusion
4. **Challenge Theme**: The entire challenge is about hidden truth - from the encoding method to the flag's meaning

## Tools Used

- Python 3 with csv module
- Basic ASCII character conversion

---

**Difficulty**: Medium  
**Category**: Steganography / Forensics  
**Skills**: Data analysis, pattern recognition, ASCII encoding
