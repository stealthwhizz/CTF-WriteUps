# The Insider's Network — Writeup

Challenge hint
> When domains speak in ancient tongues of sixty-four,
> And ping's echoes carry secrets through the network's core,
> Combine their whispers to unlock the door.

Interpretation
- "ancient tongues of sixty-four": Base64 — look at DNS TXT records.
- "ping's echoes": ICMP Echo payloads — look at ICMP data.
- "Combine their whispers": Concatenate the parts to get the flag.

Tools used
- `tshark` to extract DNS/ICMP fields
- `base64` to decode DNS TXT
- `xxd`, `tr`, and `sed`/`grep` for quick ICMP payload handling

PCAP: `suspicious_traffic_server_4.pcap`

---

Step 1 — DNS TXT (Base64)
List TXT payloads and decode when concatenated:
```bash
cd "/mnt/c/Users/whizy/CTF/CNSCTF/The Insider's Network"
# Show TXT chunks
tshark -r suspicious_traffic_server_4.pcap -Y "dns.txt" -T fields -e dns.txt
# aXNmY3J7
# U1QzRzRO
# MF80VEg=

# Concatenate and decode
tshark -r suspicious_traffic_server_4.pcap -Y "dns.txt" -T fields -e dns.txt \
  | tr -d '\r\n' | base64 -d; echo
# isfcr{ST3G4N0_4TH
```
Result (DNS part): `isfcr{ST3G4N0_4TH`

Step 2 — ICMP Echo payloads (ASCII in hex with padding)
Inspect ICMP payloads:
```bash
tshark -r suspicious_traffic_server_4.pcap -Y "icmp && data" -T fields -e data | sed -n '1,30p'
```
Key hex lines (repeated with padding):
- `5f4e33545f54523446...` → `xxd -r -p` → `_N3T_TR4F` (trailing `X`/`A` padding removed)
- `4631435f48314433...` → `xxd -r -p` → `F1C_H1D3S`
- `5f314e5f50523054307d...` → `xxd -r -p` → `_1N_PR0T0}`

Quick decode for just the meaningful lines:
```bash
tshark -r suspicious_traffic_server_4.pcap -Y "icmp && data" -T fields -e data \
| grep -E "^(5f4e33545f54523446|4631435f48314433|5f314e5f50523054307d)" \
| while read -r h; do echo "$h" | xxd -r -p | tr -d 'XA'; echo; done
# _N3T_TR4F
# F1C_H1D3S
# _1N_PR0T0}
```
Note: The first two fragments join across packet boundaries to form `TR4FF1C` (TR4F + F1C).

Step 3 — Combine
- DNS: `isfcr{ST3G4N0_4TH`
- ICMP: `_N3T_TR4F` + `F1C_H1D3S` + `_1N_PR0T0}` → `_N3T_TR4FF1C_H1D3S_1N_PR0T0}`
- Final: `isfcr{ST3G4N0_4TH_N3T_TR4FF1C_H1D3S_1N_PR0T0}`

One-liner recap
```bash
# DNS start
tshark -r suspicious_traffic_server_4.pcap -Y "dns.txt" -T fields -e dns.txt | tr -d '\r\n' | base64 -d; echo

# ICMP fragments (decode 3 interesting lines)
tshark -r suspicious_traffic_server_4.pcap -Y "icmp && data" -T fields -e data \
| grep -E "^(5f4e33545f54523446|4631435f48314433|5f314e5f50523054307d)" \
| while read -r h; do echo "$h" | xxd -r -p | tr -d 'XA'; echo; done
```

Final flag
```
isfcr{ST3G4N0_4TH_N3T_TR4FF1C_H1D3S_1N_PR0T0}
```

Artifacts
- Extracted text summary: `extracted_text.txt` (already generated)
- This writeup: `WRITEUP.md`
