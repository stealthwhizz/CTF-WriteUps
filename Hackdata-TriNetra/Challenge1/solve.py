#!/usr/bin/env python3
from Crypto.Cipher import AES
from hashlib import blake2b
import string

# Encrypted data from the binary
encrypted_hex = "ce2f380761f7894d6cd89f98a0a40b5b1a0242b0e49a720c41ab5976ebf63b26"
encrypted_data = bytes.fromhex(encrypted_hex)

printable = set(string.printable)

# Brute force all possible single byte values
for byte_val in range(256):
    try:
        # Hash the single byte with BLAKE2b-512
        h = blake2b(bytes([byte_val]), digest_size=64)
        hash_result = h.digest()
        
        # Extract key (first 32 bytes) and IV (next 16 bytes) from hash
        key = hash_result[:32]
        iv = hash_result[32:48]
        
        # Try to decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data)
        
        # Check if decryption produced valid data
        try:
            # Try to decode and check for printable characters
            decrypted_str = decrypted.decode('ascii', errors='ignore')
            
            # Check if most characters are printable
            printable_count = sum(1 for c in decrypted_str if c in printable and c != '\x00')
            
            if printable_count > len(decrypted_str) * 0.5:  # At least 50% printable
                char_rep = chr(byte_val) if 32 <= byte_val < 127 else f'\\x{byte_val:02x}'
                print(f"\nByte: {byte_val} ('{char_rep}')")
                print(f"Hex: {decrypted.hex()}")
                print(f"ASCII: {repr(decrypted_str)}")
                
                # Check for flag format
                if "TriNetra" in decrypted_str or "flag" in decrypted_str.lower():
                    print(f"*** POSSIBLE FLAG ***")
        except:
            pass
            
    except Exception as e:
        pass

print("\nDone!")
