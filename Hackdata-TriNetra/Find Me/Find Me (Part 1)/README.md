# 🗺️ Find Me (Part 1) - Arctic Mystery

> **CTF:** Hackdata-TriNetra CTF  
> **Category:** OSINT / Geolocation  
> **Difficulty:** Hard  
> **Status:** 🔍 Investigation In Progress

---

## 📋 Table of Contents

- [Challenge Overview](#-challenge-overview)
- [The Hunt](#-the-hunt)
- [Evidence Collected](#-evidence-collected)
- [Code Breaking](#-code-breaking)
- [Geographic Analysis](#-geographic-analysis)
- [Current Theories](#-current-theories)
- [Investigation Notes](#-investigation-notes)

---

## 🎯 Challenge Overview

A mysterious artifact leads us to a GitHub repository. The challenge asks us to find:
- **A city that "shouldn't exist on the map"** - a glitch location
- **~12km from an anchor point**
- **Physical boundaries** marking "unseen lines"
- **When the boundary was set** (year)

This is a multi-layered OSINT puzzle combining:
- 🔍 GitHub archaeology
- 🗺️ Geolocation analysis
- 🧮 Data decoding
- 🌍 Geographic knowledge

---

## 🔍 The Hunt

### Step 1: The GitHub Trail

**Keywords Found:** `GHOST` + `FRAME` + `BYTE`

**Repository Discovered:** `ghostframebyte/event-assets` ✅

### Step 2: Repository Contents

```
event-assets/
├── 06-11-2019.png      # Terminal photograph
├── network.config      # Network configuration
├── deploy.log          # Deployment log with ASCII art
└── README.md          # Mentions "sensitive values removed"
```

The README hints that sensitive data was **removed** from the config files. Time to dig into Git history! 🕵️

---

## 📦 Evidence Collected

### Git History Analysis

```bash
git log --all --oneline
git diff 88bcfa8 HEAD -- network.config
```

### Original network.config (Commit 88bcfa8)

```ini
# network bootstrap
iface=eth0
mtu=1500
txqueuelen=1000
rx_checksum=on
tx_checksum=on

# primary hardware address
hwaddr=52:49:50:45:9A:3C

# legacy / fallback
backup_hwaddr=AC:DE:48:00:11:22
gateway=10.0.0.1
dns=1.1.1.1

# temporary external endpoint
endpoint=81.128.0.1
```

### Current network.config

**Deleted Line:**
```
endpoint=81.128.0.1
```

**Added Line:**
```
81.2.82.11
```

### deploy.log Contents

```
      ~
     ~~~
    ~~~~~
   [X] [X] [X]
================
```

**Interpretation:** Three boundary markers (`[X]`) with water (`~`) above them, possibly representing:
- Border posts
- Maritime boundary
- Coastal markers

---

## 🔓 Code Breaking

### MAC Address Decode

```
hwaddr=52:49:50:45:9A:3C
```

**Hex to ASCII:**
- `52` = **R**
- `49` = **I**  
- `50` = **P**
- `45` = **E**
- `9A:3C` = (non-ASCII)

**Result:** **RIPE** 🎯

**What is RIPE?**
- **RIPE NCC** = Regional Internet Registry for **Europe, Middle East, and Central Asia**
- This narrows our search to the RIPE region!

---

## 🌍 Geographic Analysis

### IP Addresses as Coordinates

The deleted and added IP addresses might encode GPS coordinates!

| IP Address | Possible Lat/Lon |
|-----------|------------------|
| `81.128.0.1` | 81.128°N, 0.1°E |
| `81.2.82.11` | 81.2°N, 82.11°E |

### Geographic Context

**81°N Latitude** = **HIGH ARCTIC** ❄️

| Longitude | Location |
|-----------|----------|
| 0.1°E | Near **Svalbard, Norway** |
| 82.11°E | Near **Franz Josef Land, Russia** |

### Distance Calculation

The challenge mentions **~12km from anchor point**. Using the coordinates:
- Point 1: 81.128°N, 0.1°E
- Point 2: 81.2°N, 82.11°E

These points are **thousands of kilometers apart**, so we likely need to interpret the coordinates differently, or find points 12km apart within one of these regions.

---

## 🧩 Current Theories

### Theory 1: Svalbard Treaty Zone

**Svalbard** (Norwegian: Spitsbergen) has unique status:
- Norwegian sovereignty but **international treaty** (1920)
- Special economic zone
- Demilitarized area
- Could be considered a "glitch" in normal territorial sovereignty

**Main Settlement:** Longyearbyen (78.2°N) - but this doesn't match our 81°N coordinate 🤔

### Theory 2: Franz Josef Land

**Russian Arctic archipelago:**
- Disputed access rights historically
- Research station territories
- Could have boundary markers

### Theory 3: Archipelagic Anomalies

Looking for:
- Islands that appear/disappear from maps
- Disputed territorial waters
- Research stations in neutral zones
- Enclaves or special zones

### Theory 4: The Date Connection

**06-11-2019** could mean:
- June 11, 2019 (US format)
- November 6, 2019 (EU format)

**Research needed:**
- Arctic boundary agreements in 2019
- Treaty modifications
- New territorial claims

---

## 📝 Investigation Notes

### Challenge Clues Decoded

| Clue | Interpretation |
|------|----------------|
| "Place that shouldn't exist on the map" | Disputed territory / special status zone |
| "~12km from anchor point" | Distance between two specific locations |
| "Physical boundaries drawn" | Border markers / territorial division |
| "Track unseen lines" | Maritime boundaries / EEZ borders |
| "Find the CITY" | Specific settlement/research station |

### Keywords for Further Research

- [ ] Arctic disputed territories 2019
- [ ] Svalbard treaty modifications
- [ ] Franz Josef Land access rights
- [ ] Norway-Russia Arctic border demarcation
- [ ] 81°N latitude settlements
- [ ] Arctic research stations
- [ ] Maritime boundary markers

### Coordinate Interpretations to Try

1. **Direct GPS:**
   - 81.128°N, 0.1°E
   - 81.2°N, 82.11°E

2. **Reversed:**
   - 0.1°N, 81.128°E
   - 82.11°N, 81.2°E

3. **Split differently:**
   - 81.12° N, 80.01° E
   - 81.2° N, 82.11° E

4. **Decimal encoding:**
   - First two octets = latitude
   - Last two octets = longitude

---

## 🛠️ Tools & Techniques Used

| Tool/Method | Purpose |
|------------|---------|
| Git history analysis | Recover deleted data |
| Hex-to-ASCII conversion | Decode MAC address |
| Geographic databases | Location research |
| Treaty archives | Historical boundary information |
| Satellite imagery | Visual confirmation |

---

## 🎯 Next Steps

1. **Research Arctic settlements** at exactly 81°N latitude
2. **Check maritime boundary databases** for installations
3. **Look up 2019 Arctic treaties** and boundary agreements
4. **Examine satellite imagery** of suspected coordinates
5. **Search for "glitch cities"** in Arctic mapping databases
6. **Investigate research station** locations and names

---

## 🤔 Open Questions

- ❓ What is the exact coordinate interpretation method?
- ❓ Is there a research station or settlement at 81°N?
- ❓ What boundary was established around the given date?
- ❓ What makes this city a "glitch" on the map?
- ❓ How do the three boundary markers in deploy.log fit?

---

## 📚 Reference Links

- [Svalbard Treaty (Wikipedia)](https://en.wikipedia.org/wiki/Svalbard_Treaty)
- [Franz Josef Land](https://en.wikipedia.org/wiki/Franz_Josef_Land)
- [RIPE NCC Service Region](https://www.ripe.net/)
- [Arctic Research Stations Database](https://www.arctic.gov/)

---

**Difficulty Rating:** ⭐⭐⭐⭐⭐  
**Brain-Teaser Factor:** ⭐⭐⭐⭐⭐  
**Requires:** Deep OSINT skills, geographic knowledge, creative thinking

---

*This is an ongoing investigation. If you've solved this or have insights, contributions are welcome!* 🔍

---

**Status:** Investigation in progress  
**Last Updated:** February 8, 2026  
**Investigator:** whizy
