# The Ritual - CTF Challenge Writeup

## Challenge Overview
A web-based CTF challenge themed around Maya (illusion) and Indian mythology. The site appears to be related to a fictional "Operation Maya" data exfiltration. 6 flags total need to be discovered.

**Website:** https://maya5948.netlify.app/

---

## Flags Found (5/6)

### Flag 1: flag{prarambh}
**Location:** Main page HTML source  
**Method:** View page source - found in a hidden `<p>` tag with `color: transparent`
```html
<p style="color: transparent;">flag{prarambh}</p>
```
**Translation:** "Prarambh" means "beginning" in Hindi/Sanskrit

### Flag 2: flag{krodhit}
**Location:** robots.txt file  
**Method:** Checked robots.txt, found Base64-encoded message in comments
```
Disallow: T3BlcmF0aW9uIE1heWEgd2lsbCBiZSBjb25kdWN0ZWQgb24gdGhlIDMxc3QgSmFuIC0gMXN0IEZlYi4gSW5kaWEgd2lsbCBmZWVsIG91ciB3cmF0aC4gZmxhZ3trcm9kaGl0fQ==
```
**Decoded:** "Operation Maya will be conducted on the 31st Jan - 1st Feb. India will feel our wrath. flag{krodhit}"  
**Translation:** "Krodhit" means "angry/furious" in Hindi/Sanskrit

### Flag 3: flag{drishya_bhed}
**Location:** maya.jpg EXIF metadata  
**Method:** Downloaded maya.jpg, used `exiftool` and `strings` to find hidden message
```
Image Description: You have broken the first Maya, uncovering what lies beneath your very eyes. 
But I assure you, whoever you are, that you will not go further. 
You will stay at /shunya. flag{drishya_bhed}
```
**Translation:** "Drishya bhed" means "visual discrimination/appearance" in Sanskrit

### Flag 4: flag{mayajaal}
**Location:** GitHub profile bio - ArjunRampal5948  
**Method:** Following hint to check GitHub profile, found ROT-encrypted message in bio
```
Bio: "Vokfo lopybo iye qod iyebcovp rkbwon. Drsc sc k gkbxsxq. Kxn bowowlob, dro uoi sc dy eco dro psbcd drsxq sx dro Wkik. pvkq{wkiktkkv}"
```
**Decoded (ROT-10):** "Leave before you get yourself harmed. This is a warning. And remember, the key is to use the first thing in the Maya. flag{mayajaal}"  
**Translation:** "Mayajaal" means "web of illusion" in Hindi/Sanskrit

### Flag 5: flag{yudhishthira}
**Location:** GitHub repository - deleted .env file  
**Method:** Checked commit history, found "removed env" commit with encrypted flag
```
.env file content:
PORT=2001
SERVER=1234
DB=SQL
FLAG=nldyieiawzrr // Sensitive
```
**Decryption:** Used Vigenere cipher with key "prarambh" (the first flag - "the first thing in the Maya")
- Encrypted: nldyieiawzrr
- Key: prarambh
- Decrypted: yudhishthira

**Translation:** Yudhishthira is the eldest Pandava brother from the Mahabharata, known for his righteousness and adherence to dharma

---

## Technical Reconnaissance Summary

### Endpoints Discovered
- `/` - Main page
- `/shunya` - Secondary page (found via maya.jpg metadata hint)
- `/maya.jpg` - Main image
- `/maya2001.png` - Background image on /shunya page
- `/style.css` - Stylesheet
- `/robots.txt` - Contains flag #2

### GitHub Repository Analysis
**Profile:** ArjunRampal5948  
**Repository:** https://github.com/ArjunRampal5948/Maya  
**Author Email:** gattikabar@gmail.com

**Commits:**
1. `c85b17e` - "site" - Initial site creation with .env file
2. `429e9bb` - "removed env" - Removed .env containing encrypted flag #5
3. `3f0d81f` - "Delete maya2001.png" - Deleted original maya2001.png
4. `8d06b06` - "Add files via upload" - Re-added different maya2001.png (2.1KB vs original 8.5KB)

### Steganography Analysis
**maya.jpg (85KB JPEG):**
- Contains EXIF metadata with flag{drishya_bhed} and /shunya hint
- Has embedded steghide data (password protected - not yet cracked)

**maya2001.png (8.5KB PNG - Netlify version):**
- LSB steganography detected using `zsteg`
- Contains IRC-style conversation log:
```
[21:01] Seeker initiates channel from 27°05'40.6"N 76°17'28.7"E the earth hums like a yantra.
[21:02] Arjun Rampal responds this is where Shakti turned her face away.
[21:03] Seeker asks for the mark to carry forward through the curse.
[21:04] Rampal answers the banner bears only the place
```
- **Coordinates point to: Bhangarh Haunted Fort, Rajasthan, India**

**maya2001.png (2.1KB PNG - GitHub version):**
- Different file uploaded after deletion
- Smaller size, minimal steganography content

### Clues from Main Page
- "YADA YADA HI DHARMASYA" - Famous verse from Bhagavad Gita
- "The Scorpion waits in the dark"
- "Arjun tried to break the cycle. He left the keys in the void"
- "To find the truth, you must pierce the Maya"

---

## Flag 6 - Still Searching (1/6 remaining)

### Potential Locations to Explore:
1. **Steghide-protected data in maya.jpg** - Password still unknown, tried: maya, arjun, scorpion, dharma, shunya, krodhit, prarambh, drishya_bhed, void, keys, cycle, shakti, yantra, rampal, bhangarh, yudhishthira, mayajaal, gattikabar, ArjunRampal5948, 5948, 2001
2. **Browser Console/JavaScript** - No JavaScript files found in source, but might be dynamically loaded
3. **Hidden page elements** - CSS tricks, invisible text, or elements only visible with browser interaction
4. **HTTP headers** - Custom headers or cookies
5. **Bhangarh-related endpoints** - The coordinates clue strongly points to Bhangarh Fort
6. **Network requests** - Dynamic API calls when page loads in browser
7. **User interaction** - Clicking, hovering, or specific actions on the page

### Key Unsolved Clues:
- "The Scorpion waits in the dark" - Vrishchika (scorpion) not yet used
- "Arjun tried to break the cycle. He left the keys in the void" - "void" reference unclear
- "the banner bears only the place" - Bhangarh as the place, but banner not found
- Coordinates to Bhangarh Haunted Fort - Strong hint but no endpoint found

### Tools Used:
- `exiftool` - EXIF metadata extraction
- `strings` - String extraction from binaries
- `zsteg` - PNG steganography detection
- `steghide` - JPEG steganography (password protected)
- `stegseek` - Steghide password brute force
- `binwalk` - File signature analysis
- `curl` - HTTP requests and header analysis
- GitHub API - Repository analysis

---

## Summary

**5 out of 6 flags found:**
1. ✅ flag{prarambh} - HTML source
2. ✅ flag{krodhit} - robots.txt (Base64)
3. ✅ flag{drishya_bhed} - EXIF metadata
4. ✅ flag{mayajaal} - GitHub bio (ROT cipher)
5. ✅ flag{yudhishthira} - GitHub .env (Vigenere cipher)
6. ❌ **Still searching...**

The challenge demonstrates excellent use of:
- Web reconnaissance
- Steganography (EXIF, LSB)
- Cryptography (Base64, ROT, Vigenere)
- OSINT (GitHub profile hunting)
- Mythology and cultural references

**Next steps:** Browser-based investigation required for flag #6.
