# The Whisper Protocol - CTF Writeup

## Challenge Description
Our SOC team detected unusual network activity from a compromised workstation. The attacker used DNS tunneling to exfiltrate sensitive data, blending it among legitimate DNS requests. The data was fragmented and hidden in DNS queries to a "malicious" destination.

Flag format: `isfcr{...}`

## Analysis
The packet capture file `dns_exfil_instance_4.pcap` contains DNS traffic. To identify the exfiltration, I filtered DNS queries containing "malicious" using tshark:

```bash
tshark -r dns_exfil_instance_4.pcap -T fields -e dns.qry.name -Y "dns and dns.qry.name contains malicious"
```

This revealed two suspicious queries:
- `00aXNmY3J7c3ViZDBtNDFu.data.malicious-exfil.com`
- `01X2Q0dDRfbDM0azRnM30=.data.malicious-exfil.com`

The domain is `malicious-exfil.com`, and the data is base64-encoded in the subdomain before `.data.`.

## Decoding the Data
The subdomains start with a sequence number (00, 01) followed by the encoded data.

- Sequence 00: `aXNmY3J7c3ViZDBtNDFu` → Base64 decode → `isfcr{subd0m41n`
- Sequence 01: `X2Q0dDRfbDM0azRnM30=` → Replace `_` with `/` for standard base64 → `X2Q0dDR/bDM0azRnM30=` → Decode → `_d4t4_l34k4g3}`

## Flag
Concatenating the decoded fragments: `isfcr{subd0m41n_d4t4_l34k4g3}`

The flag represents "subdomain data leakage" in leetspeak.

## Reproduction Steps

Use tshark to locate the exfiltration queries and extract the data fragments embedded in the subdomain.

1) List the suspicious queries targeting the malicious domain:

```bash
tshark -r dns_exfil_instance_4.pcap -T fields -e dns.qry.name -Y "dns and dns.qry.name contains malicious-exfil"
```

Output shows two fragments with sequence prefixes:
- `00aXNmY3J7c3ViZDBtNDFu.data.malicious-exfil.com`
- `01X2Q0dDRfbDM0azRnM30=.data.malicious-exfil.com`

2) Extract just the fragment labels (everything before the first dot), and sort to ensure order:

```bash
tshark -r dns_exfil_instance_4.pcap -T fields -e dns.qry.name -Y "dns and dns.qry.name contains malicious-exfil" \
dns_exfil_instance_4.pcap | awk -F'.' '{print $1}' | sort
```

3) Decode each fragment. Note: DNS-safe base64 often uses base64url. Replace `_` with `/` and `-` with `+` before decoding.

```bash
# 00 -> aXNmY3J7c3ViZDBtNDFu
echo "aXNmY3J7c3ViZDBtNDFu" | base64 -d

# 01 -> X2Q0dDRfbDM0azRnM30=
echo "X2Q0dDRfbDM0azRnM30=" | tr '_-' '/+' | base64 -d
```

Concatenate results to form the flag: `isfcr{subd0m41n_d4t4_l34k4g3}`

## One-Liner Reconstruction

```bash
parts=$(tshark -r dns_exfil_instance_4.pcap -T fields -e dns.qry.name -Y "dns and dns.qry.name contains malicious-exfil" | awk -F'.' '{print $1}' | sort)
for p in $parts; do
dns_exfil_instance_4.pcap data=${p:2}
dns_exfil_instance_4.pcap echo -n "$data" | tr '_-' '/+' | base64 -d
done; echo
```

Expected output:

```
isfcr{subd0m41n_d4t4_l34k4g3}
```

## Notes and Indicators
- Exfil domain: `malicious-exfil.com` with a `.data.` label carrying payloads.
- Fragment prefix: two-digit sequence numbers (`00`, `01`) ensure ordering.
- Payload encoding: base64url inside DNS labels; normalize before decoding.

## Detection & Mitigations
- Monitor DNS queries for unusually long subdomains and high-entropy labels.
- Alert on patterns like sequential numeric prefixes plus long base64-like labels.
- Restrict or inspect outbound DNS to untrusted domains; prefer internal resolvers with logging.
- Use DNS tunneling detections (entropy, label length, label count) in IDS/EDR.
