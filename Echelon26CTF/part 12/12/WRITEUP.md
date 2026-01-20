# CTF Challenge Writeup: Ghost Identity

## Challenge Overview
**Challenge Name:** Ghost Identity  
**Category:** Network Forensics / PCAP Analysis  
**Difficulty:** Hard  
**Flag:** `flag{maya_unreveal}`

## Initial Clues

The challenge description provided several key hints:
1. HQ is based in Singapore
2. DNS records show "unusual persistence"
3. "No messages were logged. No data was transferred."
4. "Yet an identity remains."

The question file revealed:
- Username: `arjun.rampal`
- Session ID: `a9f3c2e1` (repeated across multiple protocols)
- DNS queries for `arjun-rampal.internal` return TXT records with structured data
- Certificate validity ended on 2014-01-01
- Authentication activity occurs well after the certificate expiry
- Key insight: "If the credentials are valid but the identity expired years earlier, then the name was never the actor"

## Investigation Process

### Step 1: Initial PCAP Analysis

First, I extracted the archive and examined the packet capture structure:

```bash
unzip -o 12.zip
```

Contents:
- `ghost_identity.pcap` - Network traffic capture
- `question.txt` - Challenge description
- `solution.txt` - Solution reference

### Step 2: Protocol Hierarchy

Checked what protocols were present:

```bash
tshark -r "12/ghost_identity.pcap" -q -z io,phs
```

Results:
- 32 total frames
- 30 DNS packets (UDP)
- 2 TCP packets

This immediately highlighted that DNS traffic was the primary focus.

### Step 3: DNS Query Analysis

Examined DNS queries to understand the pattern:

```bash
tshark -r "12/ghost_identity.pcap" -Y "dns" -T fields -e dns.qry.name -e dns.qry.type
```

Findings:
- All 30 DNS queries were for `arjun-rampal.internal`
- Query type: 16 (TXT records)
- Queries sent from `10.0.0.50` to `8.8.8.8` (Google DNS)

### Step 4: DNS TXT Records Extraction

The key breakthrough came from examining the DNS TXT record responses:

```bash
tshark -r "12/ghost_identity.pcap" -Y "dns.txt" -T fields -e dns.txt
```

Each TXT record contained:
```
a9f3c2e1:There re
a9f3c2e1:ally was
a9f3c2e1: no Arju
a9f3c2e1:n Rampal
a9f3c2e1:. He was
a9f3c2e1: used as
a9f3c2e1: a scape
a9f3c2e1:goat. Yo
a9f3c2e1:u are sl
a9f3c2e1:owly bre
a9f3c2e1:aking th
a9f3c2e1:e Maya.
a9f3c2e1:flag{may
a9f3c2e1:a_unreve
a9f3c2e1:al}
```

**Clue Analysis:**
- Each fragment prefixed with session ID `a9f3c2e1`
- Message split across 15 DNS TXT records
- This demonstrates "unusual persistence" - data hidden in DNS infrastructure

### Step 5: Message Reconstruction

Concatenated all TXT record fragments:

```bash
tshark -r "12/ghost_identity.pcap" -Y "dns.txt" -T fields -e dns.txt | sed 's/a9f3c2e1://g' | tr -d '\n'
```

**Complete message:**
```
There really was no Arjun Rampal. He was used as a scapegoat. You are slowly breaking the Maya. flag{maya_unreveal}
```

### Step 6: TCP Traffic Analysis

Examined the 2 TCP packets to understand the authentication context:

```bash
tshark -r "12/ghost_identity.pcap" -Y "tcp" -T fields -e tcp.payload | xxd -r -p
```

**Frame 31 (Request):**
```http
POST /auth HTTP/1.1
Host: arjun-rampal.internal
X-Session: a9f3c2e1
User: arjun.rampal
```

**Frame 32 (Response):**
```
Certificate Validity:
Not Before: 2010-01-01
Not After:  2014-01-01
```

**Key Finding:**
- Certificate expired on 2014-01-01
- PCAP traffic timestamps show activity in January 2026
- **12 years after expiration!**

## Solution Breakdown

### The "Ghost Identity" Concept

1. **Arjun Rampal never existed as a real operator** - The name was a fabricated identity
2. **Certificate expired in 2014** - Yet authentication continued in 2026
3. **Session ID persistence** - `a9f3c2e1` ties all the evidence together
4. **DNS as a covert channel** - Message hidden in TXT records, not logged as traditional data transfer

### Understanding the Clues

| Clue | Meaning | Evidence |
|------|---------|----------|
| "DNS records show unusual persistence" | Data embedded in DNS TXT records | 15 TXT records containing message fragments |
| "No messages were logged" | Not traditional communication | Data in DNS infrastructure, not HTTP/application logs |
| "No data was transferred" | Covert channel usage | DNS queries appear legitimate but carry hidden payload |
| "Yet an identity remains" | Ghost identity persists | arjun.rampal continues to authenticate despite expiry |
| "Singapore HQ" | Red herring / context | Misdirection or broader operation context |

### The "Maya" Reference

**Maya** (माया) in Sanskrit/Hindu philosophy means **illusion** or **deception**.

The flag `maya_unreveal` signifies:
- Unveiling/breaking through the illusion
- Discovering that Arjun Rampal was never real
- The ghost identity was manufactured misdirection

## Technical Techniques Used

1. **PCAP Analysis** - Using tshark/wireshark for packet inspection
2. **DNS Forensics** - Examining TXT records for hidden data
3. **Data Reconstruction** - Reassembling fragmented message from multiple DNS responses
4. **Certificate Analysis** - Comparing validity periods with activity timestamps
5. **Session Tracking** - Following session ID `a9f3c2e1` across protocols

## Key Commands

```bash
# Extract all DNS TXT records
tshark -r ghost_identity.pcap -Y "dns.txt" -T fields -e dns.txt

# Reconstruct complete message
tshark -r ghost_identity.pcap -Y "dns.txt" -T fields -e dns.txt | sed 's/a9f3c2e1://g' | tr -d '\n'

# Examine TCP payloads
tshark -r ghost_identity.pcap -Y "tcp" -T fields -e tcp.payload | xxd -r -p

# Check protocol distribution
tshark -r ghost_identity.pcap -q -z io,phs
```

## Conclusion

The challenge cleverly used:
- **DNS TXT records as a steganographic channel** to hide the flag
- **Expired certificate timestamps** to prove the identity was fabricated
- **Session ID correlation** across DNS and HTTP to tie evidence together
- **Philosophical naming** (Maya = illusion) to hint at the ghost identity concept

**Flag:** `flag{maya_unreveal}`

## Lessons Learned

1. DNS TXT records can be used for covert data exfiltration
2. Certificate validity checking is crucial for identity verification
3. Session/transaction IDs can link disparate network events
4. "Unusual persistence" in DNS context means repeated queries or data embedded in responses
5. Always correlate timestamps across different data sources to detect anomalies
