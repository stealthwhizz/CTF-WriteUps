# 🕵️ Catch Me - Digital Footprint Hunt

> **CTF:** Hackdata-TriNetra CTF  
> **Category:** OSINT (Open-Source Intelligence)  
> **Difficulty:** Easy  
> **Answer:** `TriNetra{ghostframebyte}`

---

## 📋 Table of Contents

- [Challenge Story](#-challenge-story)
- [The Investigation](#-the-investigation)
- [Digital Footprint Analysis](#-digital-footprint-analysis)
- [The Answer](#-the-answer)
- [OSINT Techniques](#-osint-techniques)
- [Key Takeaways](#-key-takeaways)

---

## 📖 Challenge Story

The ACM Student Chapter at Shiv Nadar University recently conducted a fun and engaging campus event. Photos from the event were meant to remain **internal until the official release**.

However, **one image was leaked online**. 🚨

Initial investigation suggests that one of the **ACM Leads** was responsible. To avoid being identified, the person attempted to cover their tracks by removing obvious traces and spreading the image across different platforms.

### 🎯 The Mission

Use **OSINT (Open-Source Intelligence)** techniques to retrace the digital footprint, uncover hidden clues, and ultimately identify who leaked the image.

**Question 1:** What is the online username associated with the leaked image?

**Hint:** The photo itself is an important piece of evidence. Look closely at everything the image contains.

---

## 🔍 The Investigation

### Step 1: Examine the Evidence

The challenge provides us with key files:
- `question1.txt` - Challenge description
- `ghostframebyte.txt` - Appears to be investigation results

Wait a minute... 🤔 The filename itself is `ghostframebyte.txt`!

### Step 2: Analyze the Image

Following the hint, we need to examine the leaked image closely. This could involve:
- **EXIF metadata** - Camera info, GPS, timestamps
- **Visual elements** - Usernames, watermarks, identifiable features
- **Reverse image search** - Find where else the image appears
- **Steganography** - Hidden data within the image

### Step 3: Username Discovery

Opening `ghostframebyte.txt` reveals a comprehensive list of online profiles:

```
https://github.com/ghostframebyte
https://tryhackme.com/p/ghostframebyte
https://letterboxd.com/ghostframebyte
https://spotify.com/user/ghostframebyte
... (26 total platforms)
```

**Total Websites Username Detected On: 26** 🎯

---

## 🌐 Digital Footprint Analysis

### The Username: **ghostframebyte**

This creative username appears to be a combination of:
- **GHOST** - Stealth, hidden presence
- **FRAME** - Photography/video terminology
- **BYTE** - Computing/digital data

Perfect for someone trying to cover their tracks while leaking digital images! 😄

### Platform Presence

| Category | Platforms |
|----------|-----------|
| **Development** | GitHub, GitLab GNOME |
| **Security/CTF** | TryHackMe, HackenProof |
| **Social** | Mastodon, Hubski, Lemmy |
| **Media** | Spotify, Letterboxd, Archive.org |
| **Professional** | GeeksForGeeks, Envato Forums |
| **Misc** | TypeRacer, NationStates, Slashdot |

### OSINT Tools Used

To discover this username across 26 platforms, investigators likely used:

| Tool | Purpose |
|------|---------|
| **Sherlock** | Username enumeration across social media |
| **WhatsMyName** | Web account discovery |
| **Namechk** | Username availability checker |
| **Social-Analyzer** | Profile aggregation |
| **Maigret** | Collect information about username |

---

## 🚩 The Answer

**Username:** `ghostframebyte`

This is the online identity of the person who leaked the image. Their digital footprint spans **26 different platforms**, making them relatively easy to track once the username is discovered!

---

## 🎓 OSINT Techniques

### 1. 🖼️ Image Analysis

When investigating leaked images, always check:

```bash
# Extract EXIF metadata
exiftool leaked_image.jpg

# Check for steganography
strings leaked_image.jpg
binwalk leaked_image.jpg
steghide extract -sf leaked_image.jpg

# Reverse image search
# - Google Images
# - TinEye
# - Yandex Images
```

### 2. 🔍 Username Enumeration

Once you have a potential username:

```bash
# Sherlock - Check username across platforms
sherlock ghostframebyte

# WhatsMyName
whatsmyname -u ghostframebyte

# Maigret
maigret ghostframebyte
```

### 3. 📊 Pattern Recognition

Digital footprints often reveal patterns:
- Username consistency across platforms
- Similar profile pictures/avatars
- Posting times (timezone analysis)
- Interest correlations
- Linguistic patterns

### 4. 🌐 Platform-Specific Searches

```bash
# GitHub
https://github.com/[username]

# TryHackMe
https://tryhackme.com/p/[username]

# Archive.org
https://archive.org/details/@[username]
```

---

## 🛠️ OSINT Toolkit

### Essential Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| **Sherlock** | Hunt down social media accounts | Username enumeration |
| **theHarvester** | Email, subdomain, name gathering | Initial reconnaissance |
| **Maltego** | Data mining and link analysis | Visual investigation |
| **SpiderFoot** | Automated OSINT collection | Comprehensive scanning |
| **Recon-ng** | Web reconnaissance framework | Modular OSINT |
| **OSINT Framework** | Collection of OSINT tools | Resource directory |

### Installation (Sherlock Example)

```bash
# Clone the repository
git clone https://github.com/sherlock-project/sherlock.git

# Install dependencies
cd sherlock
pip install -r requirements.txt

# Run Sherlock
python3 sherlock ghostframebyte
```

---

## 🎯 Key Takeaways

### 1. 🌐 **Digital Footprints Are Persistent**
Once you establish an online identity, it spreads across platforms. In this case, **26 platforms** all linked to one username!

### 2. 🔗 **Username Consistency = Easy Tracking**
Using the same username everywhere makes OSINT trivial. For anonymity, use **unique usernames per platform**.

### 3. 🖼️ **Images Contain Metadata**
Photos can reveal:
- GPS coordinates
- Camera model
- Timestamp
- Software used
- Author information

### 4. 🛡️ **Operational Security (OpSec) Matters**
To truly "cover your tracks," you need:
- Different usernames per platform
- Metadata stripping
- VPN/Tor usage
- Burner accounts
- Careful platform selection

### 5. 🔍 **OSINT is Powerful and Legal**
All this information is **publicly available**. OSINT demonstrates the importance of:
- Privacy settings
- Information sharing awareness
- Digital hygiene

---

## 📚 Further Learning

### OSINT Resources

- **[OSINT Framework](https://osintframework.com/)** - Comprehensive tool directory
- **[Bellingcat's Guide](https://www.bellingcat.com/resources/how-tos/)** - Professional OSINT techniques
- **[Trace Labs](https://www.tracelabs.org/)** - OSINT CTF practice
- **[SANS OSINT Summit](https://www.sans.org/)** - Training and resources

### Practice Platforms

- **TryHackMe** - OSINT rooms
- **Hack The Box** - OSINT challenges
- **CTFtime** - OSINT-focused CTFs

---

## 🔐 Privacy Lessons

### How to Minimize Your Digital Footprint

1. **Use unique usernames** for different contexts
2. **Strip metadata** from images before sharing
3. **Review privacy settings** on all platforms
4. **Google yourself** regularly to see what's public
5. **Use aliases** for non-professional accounts
6. **Be mindful** of what you post and where

---

**Difficulty Rating:** ⭐⭐☆☆☆  
**Real-World Relevance:** ⭐⭐⭐⭐⭐  
**Teaching Value:** ⭐⭐⭐⭐⭐

---

*Remember: Everything you post online contributes to your digital footprint. Think before you share!* 🔍

---

**Category:** OSINT  
**Skills Learned:** Username enumeration, digital footprint analysis, OSINT tools  
**Real-World Application:** Cyber threat intelligence, fraud investigation, journalism

---
---
