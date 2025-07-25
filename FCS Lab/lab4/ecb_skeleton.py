#!/opt/anaconda3/bin/python3
#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS

from present_skeleton import *
import argparse
import os

if not os.path.exists("keyfile"):
    # Generate a secure 80-bit key (10 bytes)
    key = os.urandom(10)

    # Save to a file
    with open("keyfile", "wb") as f:
        f.write(key)

    print("Key saved to 'keyfile':", key.hex())
else:
    print("Using current key...")


nokeybits = 80
blocksize = 64


def extract_ppm_header(data_bytes):
    newline_count = 0
    header_end = 0
    for i in range(len(data_bytes)):
        if data_bytes[i] == ord("\n"):
            newline_count += 1
            if newline_count == 5:
                header_end = i + 1
                break
    return data_bytes[:header_end], data_bytes[header_end:]


def ecb(infile, outfile, keyfile, mode):
    # Read key and convert to int
    with open(keyfile, "rb") as f:
        key_bytes = f.read()
    if len(key_bytes) != 10:
        raise ValueError("Key must be 80 bits (10 bytes) long")
    key_int = int.from_bytes(key_bytes, byteorder="big")

    # Read input file
    with open(infile, "rb") as f:
        content = f.read()

    # Extract PBM header (first non-comment line after dimensions)
    header, data = extract_ppm_header(content)
    print(f"Header:\n{header.decode(errors='ignore')}")
    print(f"Data preview (first 16 bytes): {data[:16].hex()}")

    # Pad data if encrypting
    if mode == "e":
        original_len = len(data)
        pad_len = blocksize - (original_len % blocksize)
        if pad_len != 0:
            data += bytes([0] * pad_len)
        len_bytes = original_len.to_bytes(8, byteorder="big")
        data = data + len_bytes

    # ECB encryption/decryption
    result = b""
    for i in range(0, len(data), blocksize):
        block = data[i : i + blocksize]
        block_int = int.from_bytes(block, byteorder="big")

        if mode == "e":
            encrypted = present(block_int, key_int)
            result += encrypted.to_bytes(blocksize, byteorder="big")
        elif mode == "d":
            print("Decryption mode...")
            decrypted = present_inv(block_int, key_int)
            result += decrypted.to_bytes(blocksize, byteorder="big")
        else:
            raise ValueError("Mode must be e or d")

    # Write output
    with open(outfile, "wb") as f:
        f.write(header + result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Block cipher using ECB mode.")
    parser.add_argument("-i", dest="infile", help="input file")
    parser.add_argument("-o", dest="outfile", help="output file")
    parser.add_argument("-k", dest="keyfile", help="key file")
    parser.add_argument("-m", dest="mode", help="mode", choices=["e", "d"])

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    keyfile = args.keyfile
    mode = args.mode

    ecb(infile, outfile, keyfile, mode)
