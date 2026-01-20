# Localghost (ghost4) — Write-up

- Challenge: “Something strange lurks in the network traffic. Connect, capture, and uncover what the ghost left behind in the wire.”
- Goal: Capture and analyze local traffic produced by `ghost4` to recover the flag.
- Flag: `isfcr{c0vert_fr4m3_r3tr1ev4l}`

## Files Provided
- `ghost4` (ELF 64-bit, stripped, statically linked)
- `ghost4.exe` (Windows PE, 64-bit)

## Tools Used (WSL)
- `ss` (or `netstat`) — discover listening ports
- `tcpdump` — capture loopback traffic to pcap
- `nc` (netcat) — trigger the service to emit data
- `tshark` — follow TCP stream and extract ASCII
- `base64` — decode Base64 tokens

## Steps

1) Run the Linux binary and identify ports
```bash
cd /mnt/c/Users/whizy/CTF/CNSCTF/localghost
./ghost4 &
ss -plnt | grep ghost4   # shows a localhost listening port (e.g., 49348)
```

2) Capture loopback traffic while interacting with the service
```bash
# Start capture (Ctrl+C later or kill the PID when done)
sudo tcpdump -i lo -w ghost4-wsl.pcap -U &
TCPD_PID=$!

# Trigger the service to speak
printf "hello\n" | nc -v 127.0.0.1 <PORT_FROM_SS>

# Stop capture
kill "$TCPD_PID"
```

3) Extract Base64 from the TCP stream and decode
```bash
# View stream and extract base64
tshark -r ghost4-wsl.pcap -q -z follow,tcp,ascii,0 \
  | grep -Eo '[A-Za-z0-9+/]{12,}={0,2}' \
  | sort -u \
  | while read s; do echo "$s" | base64 -d 2>/dev/null || true; echo; done
```

4) Result
- Among the decoded tokens you get: `isfcr{c0vert_fr4m3_r3tr1ev4l}`

## Notes
- The service emits chunks that include Base64; following the TCP stream as ASCII reveals them cleanly.
- If `tshark` isn’t available, you can fallback to a rough scan:
```bash
# Less precise fallback
tcpdump -A -r ghost4-wsl.pcap 2>/dev/null \
  | grep -Eo '[A-Za-z0-9+/]{12,}={0,2}' \
  | sort -u \
  | while read s; do echo "$s" | base64 -d 2>/dev/null || true; echo; done
```

## One-liner (from final extraction)
```bash
cd /mnt/c/Users/whizy/CTF/CNSCTF/localghost
# View stream and extract base64
tshark -r ghost4-wsl.pcap -q -z follow,tcp,ascii,0 | grep -Eo '[A-Za-z0-9+/]{12,}={0,2}' | sort -u | while read s; do echo "$s" | base64 -d 2>/dev/null || true; echo; done
```