#!/usr/bin/env python3
"""
Analyze the silent_clearance.pcap file to extract the flag
"""

try:
    from scapy.all import rdpcap, TCP, Raw
    from scapy.layers.http import HTTPResponse, HTTPRequest
except ImportError:
    print("Installing scapy...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'scapy'])
    from scapy.all import rdpcap, TCP, Raw
    from scapy.layers.http import HTTPResponse, HTTPRequest

def analyze_pcap(filename):
    print(f"Reading {filename}...")
    packets = rdpcap(filename)
    
    print(f"\nTotal packets: {len(packets)}\n")
    
    flag_fragments = []
    
    for i, pkt in enumerate(packets):
        if pkt.haslayer(Raw):
            payload = pkt[Raw].load
            try:
                payload_str = payload.decode('utf-8', errors='ignore')
                
                # Look for HTTP responses
                if 'HTTP/' in payload_str and '200 OK' in payload_str:
                    print(f"\n--- Packet {i} ---")
                    print(payload_str[:500])
                    
                    # Extract any flag fragments
                    lines = payload_str.split('\n')
                    for line in lines:
                        if 'flag{' in line or '_' in line or '}' in line:
                            flag_fragments.append(line.strip())
                            
            except:
                pass
    
    print("\n\n=== FLAG FRAGMENTS ===")
    for frag in flag_fragments:
        print(frag)
    
    return flag_fragments

if __name__ == "__main__":
    analyze_pcap("10/silent_clearance.pcap")
