# Read the binary data
with open('binary_data.txt', 'r') as f:
    binary = f.read()

# Remove spaces and newlines
binary = binary.replace(' ', '').replace('\n', '')

# Convert binary to ASCII
result = ''
for i in range(0, len(binary), 8):
    byte = binary[i:i+8]
    if len(byte) == 8:
        result += chr(int(byte, 2))

print("Decoded text:")
print(result)

# Look for flag patterns
if '{' in result and '}' in result:
    start = result.find('{')
    end = result.find('}', start)
    if start != -1 and end != -1:
        print("\n\nFound flag fragment:")
        print(result[start:end+1])
