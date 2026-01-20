import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the whitespace between the specific div tags
match = re.search(r'<div>\n([\t \n]+)</div>', content, re.DOTALL)
if match:
    whitespace = match.group(1)
    
    # Split by newlines and filter out empty lines
    lines = whitespace.split('\n')
    
    # Build binary string: tab=1, space=0
    binary = ''
    for line in lines:
        if line and line.strip():  # Skip completely empty lines
            for char in line:
                if char == '\t':
                    binary += '1'
                elif char == ' ':
                    binary += '0'
    
    print(f"Binary length: {len(binary)}")
    print(f"Binary: {binary}")
    
    # Convert binary to ASCII
    flag = ''
    for i in range(0, len(binary), 8):
        if i + 8 <= len(binary):
            byte = binary[i:i+8]
            flag += chr(int(byte, 2))
    
    print(f"\nDecoded flag: {flag}")
else:
    print("Pattern not found")
