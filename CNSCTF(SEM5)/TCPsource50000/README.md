# TCP Source 50000 - CTF Challenge Solution

## Challenge Description
A TCP capture contains a single client that repeatedly sends ACKs to the same server. Inspect the repeated ACKs, convert the numeric values in the TCP header to characters in order, and reveal the flag.

## Analysis Steps

1. **Identify Relevant Packets**: The client uses source port 50000 and sends ACK packets to destination port 80.

2. **Extract TCP Header Values**: Focus on the TCP window size field in the ACK packets. The window sizes are:
   - 73, 83, 70, 67, 82, 123, 117, 110, 104, 51, 52, 114, 100, 95, 119, 104, 49, 115, 112, 51, 114, 122, 125

3. **Convert to Characters**: Interpret each window size as an ASCII character code:
   - 73 → 'I'
   - 83 → 'S'
   - 70 → 'F'
   - 67 → 'C'
   - 82 → 'R'
   - 123 → '{'
   - 117 → 'u'
   - 110 → 'n'
   - 104 → 'h'
   - 51 → '3'
   - 52 → '4'
   - 114 → 'r'
   - 100 → 'd'
   - 95 → '_'
   - 119 → 'w'
   - 104 → 'h'
   - 49 → '1'
   - 115 → 's'
   - 112 → 'p'
   - 51 → '3'
   - 114 → 'r'
   - 122 → 'z'
   - 125 → '}'

4. **Reveal the Flag**: Concatenating the characters gives: **ISFCR{unh34rd_wh1sp3rz}**

## Tools Used
- tshark (Wireshark command-line tool) for packet analysis
- Terminal commands to filter and extract TCP fields

## Notes
- The flag appears to be "unheard whispers" with some obfuscation.
- This technique uses TCP window sizes to hide data in plain sight within the TCP header.