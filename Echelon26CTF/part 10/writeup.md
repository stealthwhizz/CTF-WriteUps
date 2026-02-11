# Echelon26 CTF - Part 10: Silent Clearance

## Challenge Description

**Title:** Silent Clearance  
**Category:** Network Forensics  
**Difficulty:** Hard

### The Clue
```
Captured network traffic shows what appears to be meaningless communication.
Payloads are visible. Nothing seems hidden.
Yet meaning was exchanged in plain view.
```

### Challenge Files
- `silent_clearance.pcap` - Network capture file
- `question.txt` - Challenge context

## Initial Analysis

The question.txt file provides crucial context:

> Network captures show a series of approvals attributed to Arjun Rampal.
> Every approval appears as a valid HTTP 200 OK response from the server at 10.0.0.10:80 to a client at 10.0.0.5.
> However, inspection reveals that no HTTP requests containing authorization data exist at all.
> The only meaningful identifier is found in the response header X-Approved-For, which always contains the same name.
> If approvals exist without requests, the question is not what was approved, but who actually acted.

This immediately raises a red flag: **HTTP responses without requests**.

## Investigation

### Examining the PCAP File

Using `strings` command on the pcap file reveals the network traffic:

```bash
strings silent_clearance.pcap
```

### Key Findings

The pcap contains multiple HTTP 200 OK responses, all structured similarly:

```
HTTP/1.1 200 OK
Server: clearance-gateway
X-Approved-For: Arjun Rampal
Content-Length: 6
flag{a
```

```
HTTP/1.1 200 OK
Server: clearance-gateway
X-Approved-For: Arjun Rampal
Content-Length: 6
rjun_i
```

```
HTTP/1.1 200 OK
Server: clearance-gateway
X-Approved-For: Arjun Rampal
Content-Length: 6
s_inno
```

```
HTTP/1.1 200 OK
Server: clearance-gateway
X-Approved-For: Arjun Rampal
Content-Length: 5
cent}
```

## The Breakthrough

### What Makes This Suspicious?

1. **No HTTP Requests**: Normal HTTP communication follows a request-response pattern. Here we only see responses.
2. **All Attributed to Arjun**: Every response has `X-Approved-For: Arjun Rampal` header.
3. **Fragmented Message**: The response bodies contain fragments of text.

### The Hidden Message

The clue states: *"Payloads are visible. Nothing seems hidden. Yet meaning was exchanged in plain view."*

The payloads (response bodies) are indeed visible and nothing is encoded or encrypted. The flag is literally in plain view, split across multiple response bodies:

- Response 1: `flag{a`
- Response 2: `rjun_i`
- Response 3: `s_inno`
- Response 4: `cent}`

Concatenating these fragments: **`flag{arjun_is_innocent}`**

## The Answer: Who is Arjun Rampal?

Arjun Rampal is the character being **framed** in this scenario. The key insight is:

- The server generated approval responses autonomously
- Each response was attributed to "Arjun Rampal" via the `X-Approved-For` header
- **No requests from Arjun exist in the capture**
- Therefore, Arjun never actually initiated or approved anything

The system was acting on its own and falsely attributing the actions to Arjun. He's innocent because there's no evidence of him actually making any requests - only responses claiming he approved things.

## Solution

**Flag:** `flag{arjun_is_innocent}`

## Key Takeaways

1. **Protocol Anomalies**: HTTP responses without corresponding requests are abnormal and worth investigating
2. **Hidden in Plain Sight**: Sometimes steganography isn't about hiding data, but about what's missing (the absent requests)
3. **Fragmentation**: Important data can be split across multiple packets
4. **Attribution vs. Action**: Just because something is attributed to someone doesn't mean they did it

## Tools Used

- `strings` - Extract readable strings from binary files
- Basic understanding of HTTP protocol
- Critical thinking about network traffic patterns
