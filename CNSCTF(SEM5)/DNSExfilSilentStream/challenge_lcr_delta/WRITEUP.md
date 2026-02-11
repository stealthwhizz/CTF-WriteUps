# DNS Exfil — Silent Stream (challenge_lcr_delta)

This writeup documents how the real exfiltration was identified from mixed DNS queries, how the chunks were ordered and transformed, and how the final flag was obtained.

## Clues
- PCAP: `dns_exfil_lcr_delta.pcap`
- README hint: `13 -> 32` (apply ROT13, then Base32)
- ZIP artifact in traffic: `challenge_lcr_delta.zip` (visible as `challenge_lcr_delta.zip.7288.assets.exfil.example`)
- `exiftool` on the ZIP reveals a comment with the rule and words:
  - Rule: Word-length parity — if a word's length is odd, reverse that sequence's chunk; if even, keep it.
  - Words (sequence order): Lumina Cinder Rook Bramble Hearth Glint Fable Iris Vale

Odd-length words: Bramble (7), Glint (5), Fable (5) → positions 4, 6, 7 are reversed.

## Extracting the exfil queries
Filter queries to the exfil domain and list the chunk-pattern queries:
```bash
# WSL path shown; adjust if needed
tshark -r \
  "/mnt/c/Users/whizy/CTF/CNSCTF/DNSExfilSilentStream/challenge_lcr_delta/dns_exfil_lcr_delta.pcap" \
  -Y "dns.flags.response==0 && dns.qry.name contains \"exfil.example\"" \
  -T fields -e frame.number -e dns.qry.name | \
  grep -E "^[0-9]+\s+[0-9]{4}-[A-Z2-7]+\.[0-9]+\\.exfil\\.example$"
```
Observed 9 payload queries (frame → name):
- 11 → `0009-EIT42QBMN.2054.exfil.example`
- 15 → `0005-ZH2JZAMFTL.8422.exfil.example`
- 36 → `0002-3QTAMFT5EQ.5795.exfil.example`
- 75 → `0006-G3HTJEABG4.4051.exfil.example`
- 118 → `0003-ZLMJTR3TXA.4629.exfil.example`
- 151 → `0004-JEZBG2LTHM.8918.exfil.example`
- 158 → `0007-ZGM4TTYAR.1702.exfil.example`
- 182 → `0001-TL4GBZMJTL.8562.exfil.example`
- 235 → `0008-AWJTZ3GRA.3804.exfil.example`

Noise/decoys like `vfqccy4khop3.9621.exfil.example` and the `assets.exfil.example` host are ignored for payload reconstruction.

## Ordering and parity rule
- Ordering: use the explicit 4-digit indices (`0001` … `0009`), not capture order.
- Extract chunks (sorted by index):
  1. `TL4GBZMJTL`
  2. `3QTAMFT5EQ`
  3. `ZLMJTR3TXA`
  4. `JEZBG2LTHM`  ← reverse
  5. `ZH2JZAMFTL`
  6. `G3HTJEABG4`  ← reverse
  7. `ZGM4TTYAR`   ← reverse
  8. `AWJTZ3GRA`
  9. `EIT42QBMN`

Apply parity: reverse chunks 4, 6, 7; keep others as-is. Concatenate the adjusted 9 chunks to form a single string.

## Decoding pipeline (13 → 32)
- Per hint, apply ROT13 to the concatenated string, then Base32-decode the result.
- The resulting bytes are ASCII-hex; convert hex → bytes to reveal plaintext.

Using the provided solver (`solve_silent_stream.py`), the “sorted + parity” + ROT13→Base32 path yields:
```text
69736663727b6c616e7465726e5f72697665725f7365637265747d
```
Hex → ASCII:
```text
isfcr{lantern_river_secret}
```

## Final flag
Depending on the event’s flag format, the recovered secret phrase is:
- `lantern_river_secret`

The exfil message embeds a non-standard prefix `isfcr{...}`. For CNSCTF-style flags, submit:
- `CNSCTF{lantern_river_secret}` (or, if lowercase enforced) `cnsctf{lantern_river_secret}`

## Reproduce quickly
```bash
python3 /mnt/c/Users/whizy/CTF/CNSCTF/DNSExfilSilentStream/challenge_lcr_delta/solve_silent_stream.py
# Inspect the decoded ASCII-hex
xxd -g 1 -c 64 \
  /mnt/c/Users/whizy/CTF/CNSCTF/DNSExfilSilentStream/challenge_lcr_delta/exfil_rot13->b32_sorted_parity.bin
# Convert ASCII-hex to text
python3 - << 'PY'
import binascii
h = open('/mnt/c/Users/whizy/CTF/CNSCTF/DNSExfilSilentStream/challenge_lcr_delta/exfil_rot13->b32_sorted_parity.bin','rb').read().decode()
print(binascii.unhexlify(h))
PY
```

## Notes
- Capture-order + parity decoding produces corrupted bytes; the index labels are authoritative.
- Some `.exfil.example` names are decoys; constrain to `^\d{4}-[A-Z2-7]+\.[0-9]+\.exfil\.example$`.
- The ZIP-in-traffic is a breadcrumb: its comment encodes the reconstruction logic only; it is not the exfil payload.
