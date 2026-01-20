# The Leaky Wall

## Challenge Description

You are a security analyst at a major corporation. A sensor alerted you to suspicious activity, and you've been tasked with reviewing a snippet of the company's firewall logs. An attacker was seen probing your network and finally managed to connect to a high, non-standard port on an internal server. Your mission is to identify the attacker's IP address and the specific port they connected to.

**Flag Format:** isfcr{AttackerIP:PortNo.}

## Log Analysis

The firewall logs are in the following format:
```
ACTION=DENY SRC=<source_ip> DST=<destination_ip> PROTO=<protocol> DPT=<destination_port>
```

Key observations:
- Multiple DENY actions from IP `203.0.113.5` attempting to connect to `192.168.1.100` on common ports (22, 23, 80, 443, 3389).
- One ALLOW action from the same IP `203.0.113.5` to `192.168.1.100` on port `4444`.
- Port 4444 is a high, non-standard port, indicating successful exploitation.

## Solution

The attacker is `203.0.113.5`, and they connected to port `4444`.

**Flag:** isfcr{203.0.113.5:4444}