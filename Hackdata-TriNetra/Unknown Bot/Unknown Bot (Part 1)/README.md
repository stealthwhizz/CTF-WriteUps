# 🤖 Unknown Bot (Part 1) - Silent Service

> **CTF:** Hackdata-TriNetra CTF  
> **Category:** OSINT / Forensics  
> **Difficulty:** Easy  
> **Flag:** `TriNetra{silent_service_bot}`

---

## 📋 Table of Contents

- [Challenge Story](#-challenge-story)
- [The Hunt Begins](#-the-hunt-begins)
- [EXIF Deep Dive](#-exif-deep-dive)
- [Flag Discovery](#-flag-discovery)
- [Analysis](#-analysis)
- [Key Takeaways](#-key-takeaways)

---

## 📖 Challenge Story

An internal screenshot began circulating after a minor operational outage was discussed in a private forum. The screenshot shows a short alert message, repeated across different days with **identical wording and structure**.

The alert appears to originate from a **background system** that was never meant to draw attention unless something went wrong. According to those familiar with the incident, this system normally runs **quietly** and only surfaces during failures.

Shortly after the screenshot appeared, fragments of operational notes began leaking to public paste sites. These notes reference archived alert identifiers, maintenance approvals, and post-incident audits, but **do not identify the system responsible**.

### 🎯 The Question

**Identify the automated system responsible for generating the alert using evidence inherent to the artifact itself.**

The key phrase: *"evidence inherent to the artifact itself"* 🔍

---

## 🔍 The Hunt Begins

### What We're Given

The challenge provides a zip file containing:
- `question1.txt` - Challenge description
- `image.jpeg` - The "leaked screenshot"

### First Look

The hint says to use "evidence **inherent to the artifact**" - this suggests we need to look **beyond** what's visible in the image itself. Time to check the metadata! 🕵️

---

## 🔬 EXIF Deep Dive

### Quick File Type Check

```bash
file image.jpeg
```

**Output:**
```
image.jpeg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, 
segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=7, 
description=internal alert snapshot, xresolution=122, yresolution=130, 
resolutionunit=1, software=SupportOps Monitor], baseline, precision 8, 
1159x568, components 3
```

Already interesting! Even `file` command reveals:
- **Description:** "internal alert snapshot"
- **Software:** "SupportOps Monitor"

### Complete Metadata Extraction

```bash
exiftool image.jpeg
```

**The Treasure Trove:**

| EXIF Field | Value |
|-----------|--------|
| **Image Description** | internal alert snapshot |
| **Software** | SupportOps Monitor |
| **User Comment** | **TriNetra{silent_service_bot}** 🎉 |
| **X Resolution** | 1 |
| **Y Resolution** | 1 |

---

## 🚩 Flag Discovery

**Found it!** The flag was hiding in the **User Comment** field:

```
User Comment: TriNetra{silent_service_bot}
```

This field is often overlooked but can store custom metadata - perfect for hiding secrets! 🎯

---

## 🧩 Analysis

### Breaking Down the Flag

The automated system is identified as **`silent_service_bot`** - let's decode what this tells us:

| Component | Meaning | Challenge Clue |
|-----------|---------|----------------|
| **silent** | Operates quietly | "system normally runs **quietly**" |
| **service** | Background system service | "**background system**" |
| **bot** | Automated system | "automated system" (not human) |

### The Perfect Fit

The flag name **perfectly aligns** with the challenge narrative:
- ✅ Runs in the background
- ✅ Only surfaces during failures
- ✅ Automated (not human-generated)
- ✅ Silent operation under normal conditions

### Why User Comment?

The **User Comment** EXIF field is:
- Part of the EXIF 2.2 standard
- Designed for custom user annotations
- Often ignored by casual analysis
- Not displayed in image viewers
- Perfect for embedding metadata flags! 🎭

---

## 🎓 Key Takeaways

### 1. 🔍 **Metadata is a Goldmine**
Images, documents, and media files contain **hidden information** not visible to the naked eye. Always check:
- EXIF data (images)
- Document properties (PDFs, Office files)  
- ID3 tags (audio)
- File attributes

### 2. 📖 **Read Challenge Hints Carefully**
The phrase **"evidence inherent to the artifact"** was a direct hint to look at file metadata, not the visual content.

### 3. 🛠️ **Know Your Tools**

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `exiftool` | Extract all metadata | First stop for any file analysis |
| `file` | Quick file type & basic info | Initial reconnaissance |
| `strings` | Extract readable text | Looking for hidden strings |
| `hexdump/xxd` | Binary inspection | Deep dive analysis |

### 4. 💭 **Context Validates Findings**
The flag components (silent + service + bot) perfectly matched the challenge story, confirming we found the right answer.

### 5. 🎯 **EXIF Fields to Always Check**
- **User Comment** - Custom annotations
- **Image Description** - Often contains notes
- **Software** - What created the file
- **GPS Data** - Location information  
- **Camera Settings** - Camera fingerprinting
- **Creation/Modification Dates** - Temporal analysis

---

## 🛠️ Tools Arsenal

```bash
# Quick metadata view
exiftool image.jpeg

# Extract specific field
exiftool -UserComment image.jpeg

# All EXIF data in table format
exiftool -s -G image.jpeg

# Remove all metadata (for privacy)
exiftool -all= image.jpeg
```

---

## 🎯 Quick Solution Path

```bash
# 1. Extract the challenge
unzip unknown_bot_p1.zip

# 2. Check the metadata
exiftool image.jpeg | grep -i "user comment"
# Output: User Comment: TriNetra{silent_service_bot}

# 3. Submit flag!
```

---

**Difficulty Rating:** ⭐☆☆☆☆  
**Real-World Relevance:** ⭐⭐⭐⭐⭐  
**Learning Value:** ⭐⭐⭐⭐⭐

---

*Remember: In OSINT and forensics, the most valuable information often hides in metadata, not content!* 🔐
