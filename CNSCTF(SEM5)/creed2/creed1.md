# Assassin's Creed — Welcome to the Creed (CNSCTF) Writeup

## Overview
- Portal: `0.cloud.chals.io`
- Given password: `creed123`
- Goal: Login securely and obtain the INITiation message / flag

## Hints and Interpretation
- "now numbering 24263 members" → points to port `24263`.
- "Login ... SECURELY" → use SSH (secure shell), not HTTP/HTTPS.
- MOTD line "Being an assassin means to be HIDDEN" → likely hidden dotfile in home directory (e.g., `.flag.txt`).

## Recon
Identify the running service and correct port.

```bash
# Check the hinted port
nc -vz 0.cloud.chals.io 24263

# Peek at banner (reveals SSH)
timeout 5 nc 0.cloud.chals.io 24263 | head -n 5

# (Optional) TLS probe showed no cert, confirming not HTTPS on 24263
openssl s_client -connect 0.cloud.chals.io:24263 -servername 0.cloud.chals.io </dev/null | head
```

Findings:
- `nc` showed TCP success on `24263`.
- Banner returned `SSH-2.0-OpenSSH_10.0p2` → service is SSH on `24263`.

## Exploitation (Login)
Try the likely username suggested by “INITiation”: `init`.

```bash
ssh -p 24263 init@0.cloud.chals.io
# password prompt → enter: creed123
```

On login, a themed MOTD confirms access.

## Flag Retrieval
List files (including hidden) and read the hidden flag file.

```bash
ls -la
cat .flag.txt
```

Flag:
```
isfcr{B3in6_4n_a55as5in_d3m4nd5_5il3nc3}
```

## One-Liner (Optional)
You can fetch the hidden file directly once you know it:

```bash
scp -P 24263 init@0.cloud.chals.io:.flag.txt ./creed_flag.txt
# password: creed123
```

## Notes & Lessons
- Numerical clue in prompt can be a port (24263).
- "SECURELY" nudges to SSH; HTTP/HTTPS were dead-ends.
- Banner/MOTD hint about being "HIDDEN" mapped to a dotfile `.flag.txt`.
- Always list with `-a` to catch hidden files.

## Artifacts
- Local copy saved at: `flag.txt`
- Full path: `c:\Users\whizy\CTF\CNSCTF\CREED\flag.txt`

## Commands Summary
```bash
# Recon
nc -vz 0.cloud.chals.io 24263
timeout 5 nc 0.cloud.chals.io 24263 | head -n 5

# Login
ssh -p 24263 init@0.cloud.chals.io   # pw: creed123

# Find and read flag
ls -la
cat .flag.txt

# Optional: copy flag locally
scp -P 24263 init@0.cloud.chals.io:.flag.txt ./creed_flag.txt
```
