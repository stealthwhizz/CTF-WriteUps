import base64
import re
import subprocess
from pathlib import Path
from binascii import Error as BinasciiError

PCAP_PATH = Path(__file__).with_name("dns_exfil_lcr_delta.pcap")
OUT_DIR = Path(__file__).parent


def rot13_base32_decode(s: str) -> bytes:
    rot = s.translate(str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
    ))
    # Base32 requires correct padding; add if missing
    padding = (-len(rot)) % 8
    if padding:
        rot = rot + ("=" * padding)
    return base64.b32decode(rot, casefold=True)


def get_dns_queries() -> list[str]:
    cmd = [
        "tshark",
        "-r",
        str(PCAP_PATH),
        "-Y",
        "dns.flags.response==0 && dns.qry.name",
        "-T",
        "fields",
        "-e",
        "dns.qry.name",
    ]
    try:
        out = subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise SystemExit("tshark not found. Please install Wireshark/tshark.")
    return [line.strip() for line in out.splitlines() if line.strip()]


def main():
    queries = get_dns_queries()
    # Filter to *.exfil.example domain
    exfil = [q for q in queries if q.endswith(".exfil.example")]

    # Keep only payload chunks of the form NNNN-CHUNK.something.exfil.example
    pat = re.compile(r"^(?P<idx>\d{4})-(?P<chunk>[A-Z2-7]+)\.[^.]+\.exfil\.example$")
    in_order = []  # preserve capture order for parity logic
    for q in exfil:
        m = pat.match(q)
        if m:
            idx = int(m.group("idx"))
            chunk = m.group("chunk")
            in_order.append((idx, chunk))

    if not in_order:
        raise SystemExit("No exfil chunks matched expected pattern.")

    # Parity rule from ZIP comment: positions with odd word length are reversed
    words = [
        "Lumina",  # 6 even
        "Cinder",  # 6 even
        "Rook",    # 4 even
        "Bramble", # 7 odd -> reverse
        "Hearth",  # 6 even
        "Glint",   # 5 odd -> reverse
        "Fable",   # 5 odd -> reverse
        "Iris",    # 4 even
        "Vale",    # 4 even
    ]
    def b32(s: str) -> bytes:
        pad = (-len(s)) % 8
        if pad:
            s = s + ("=" * pad)
        return base64.b32decode(s, casefold=True)

    def try_decodes(label: str, text: str):
        results = {}
        try:
            # ROT13 -> B32
            rb = rot13_base32_decode(text)
            results["rot13->b32"] = rb
        except Exception:
            pass
        try:
            # B32 only
            results["b32"] = b32(text)
        except Exception:
            pass
        try:
            # B32 then ROT13 (treat as ASCII)
            b = b32(text)
            try:
                s = b.decode('utf-8', errors='ignore')
                s2 = s.translate(str.maketrans(
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                    "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
                ))
                results["b32->rot13_ascii"] = s2.encode()
            except Exception:
                pass
        except Exception:
            pass
        for k, v in results.items():
            print(f"[{label}] {k}: {len(v)} bytes")
        return results

    # Strategy A: capture order
    selected = in_order[:len(words)]
    adjusted_chunks = []
    for i, (_idx, ch) in enumerate(selected, start=1):
        odd_len = (len(words[i-1]) % 2 == 1)
        adjusted_chunks.append(ch[::-1] if odd_len else ch)
    b32_stream_parity = "".join(adjusted_chunks)
    results_a = try_decodes("capture+parity", b32_stream_parity)
    for name, data in results_a.items():
        (OUT_DIR / f"exfil_{name}_capture_parity.bin").write_bytes(data)

    # Strategy B: sort by 4-digit index then apply parity
    by_idx = sorted(in_order, key=lambda t: t[0])[:len(words)]
    adjusted_chunks_b = []
    for i, (_idx, ch) in enumerate(by_idx, start=1):
        odd_len = (len(words[i-1]) % 2 == 1)
        adjusted_chunks_b.append(ch[::-1] if odd_len else ch)
    b32_stream_sorted = "".join(adjusted_chunks_b)
    results_b = try_decodes("sorted+parity", b32_stream_sorted)
    for name, data in results_b.items():
        (OUT_DIR / f"exfil_{name}_sorted_parity.bin").write_bytes(data)

    # Strategy C: sorted, no parity
    b32_stream_sorted_nop = "".join(ch for _idx, ch in by_idx)
    results_c = try_decodes("sorted+noparity", b32_stream_sorted_nop)
    for name, data in results_c.items():
        (OUT_DIR / f"exfil_{name}_sorted_noparity.bin").write_bytes(data)

    # Try to interpret any ASCII-hex and print a preview
    def show_hex_as_ascii(label: str, data: bytes):
        hs = bytes([c for c in data if chr(c) in '0123456789abcdefABCDEF']).decode()
        try:
            s = bytes.fromhex(hs)
            print(f"{label} -> ASCII: {s!r}")
        except BinasciiError:
            pass
    for name, data in {**results_a, **results_b, **results_c}.items():
        show_hex_as_ascii(name, data)


if __name__ == "__main__":
    main()
