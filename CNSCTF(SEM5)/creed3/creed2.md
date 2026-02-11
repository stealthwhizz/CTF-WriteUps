# Assassin's Creed – The Leap of Faith (Web + Forensics)

- Challenge URL: https://pes-u-ac-lof.chals.io/
- Goal: Login to the Assassin portal, get your codename and Vulture's last seen location.
- Flag format: `isfcr{Assassin name:Location}`

## Summary
- Access key from the previous challenge: `5il3nc3` (leet for "silence").
- After login, the API reveals a session-specific codename.
- Triggering a transmission yields a tiny PCAP containing two plaintext chunks.
- The chunks are an encrypted string intended for a Rail Fence cipher with depth 3 (hinted in the UI: "Pattern flows thrice like rails crossing fate.").
- Decoding gives the location: `Taj Mahal`.
- Final flag (for this session): `isfcr{Deimos:Taj Mahal}`

## Recon
- `index.html` links to `login.html` and `tasks.html`.
- `login.html` loads `js/app.js`. Key client logic from `app.js`:
  - POST `/api/login` with `{ password }`.
  - GET `/api/get_assassin` for the codename after auth.
  - POST `/api/send_coords` returns `{ download_url: "/api/download_pcap" }`.

## Steps

1) Login
```bash
# Use cookies to persist the session
curl -sS -c cookies.txt -b cookies.txt \
  -H 'Content-Type: application/json' \
  -d '{"password":"5il3nc3"}' \
  https://pes-u-ac-lof.chals.io/api/login
```
Expected: `{ "ok": true }`

2) Get codename
```bash
curl -sS -b cookies.txt https://pes-u-ac-lof.chals.io/api/get_assassin
```
Example output:
```json
{"location":null,"name":"Deimos","ok":true}
```
Codename here: `Deimos` (codename can vary per session).

3) Request coordinates and download PCAP
```bash
curl -sS -b cookies.txt -X POST \
  https://pes-u-ac-lof.chals.io/api/send_coords
# => {"ok":true,"download_url":"/api/download_pcap"}

curl -sS -b cookies.txt -o transmission.pcap \
  https://pes-u-ac-lof.chals.io/api/download_pcap
```

4) Inspect PCAP for payload
```bash
strings transmission.pcap
```
Observed lines:
```
#Chunk 1/2: TMla_aaj
"JChunk 2/2: h
```
Hex dump confirms the two UDP payloads contain the chunk labels and data.

5) Decrypt Rail Fence (depth = 3)
- Concatenate chunk data in order: `TMla_aaj` + `h` = `TMla_aajh`.
- Rail Fence decryption (rails=3) yields `Taj_Mahal` -> location: `Taj Mahal`.

Python snippet used:
```python
ct = "TMla_aajh"
rails = 3
pattern = list(range(rails)) + list(range(rails-2,0,-1))
idxs = []
r = 0
for _ in range(len(ct)):
    idxs.append(pattern[r])
    r = (r + 1) % len(pattern)
counts = [idxs.count(i) for i in range(rails)]
pos = 0
rails_slices = []
for c in counts:
    rails_slices.append(list(ct[pos:pos+c]))
    pos += c
res = []
for i in range(len(ct)):
    rail = idxs[i]
    res.append(rails_slices[rail].pop(0))
print(''.join(res))  # Taj_Mahal
```

## Final Flag
- Codename (this session): `Deimos`
- Location: `Taj Mahal`
- Flag: `isfcr{Deimos:Taj Mahal}`

## Notes / Gotchas
- The codename is personalized; verify it from your session via `/api/get_assassin`.
- Flag checker may be strict about spaces vs underscores. The decoded string contained an underscore (`Taj_Mahal`) but the canonical location uses a space: `Taj Mahal`.
- If your codename differs, substitute accordingly: `isfcr{<YourName>:Taj Mahal}`.
