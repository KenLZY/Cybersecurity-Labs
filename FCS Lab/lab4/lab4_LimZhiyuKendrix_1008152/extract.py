#!/opt/anaconda3/bin/python3
#!/usr/bin/env python3
# ECB plaintext extraction for PBM (P1) format — 50.042 FCS

import argparse


def getInfo(headerfile):
    with open(headerfile, mode="rb") as headerin:
        headerInfo = headerin.read()
        header = headerInfo.splitlines()

        for line in header:
            line = line.decode()
            if line.startswith("#") or line.startswith("P1") or line.startswith("P4"):
                continue
            else:
                width, height = map(int, line.strip().split())
                return width, height


def extract(infile, outfile, headerfile):
    width, height = getInfo(headerfile)
    total_pixels = width * height

    print(f"Image width: {width}, height: {height}, total pixels: {total_pixels}")

    # Read the ECB encrypted pixel data
    with open(infile, mode="rb") as fin:
        cipheredData = fin.read()
        cipheredData = cipheredData.strip()
        cipheredData = cipheredData.replace(b" ", b"")

    blockSize = 16
    blocks = [
        cipheredData[i : i + blockSize] for i in range(0, len(cipheredData), blockSize)
    ]

    seen = {}
    symbol_map = []
    current_symbol = 0

    for block in blocks:
        if block not in seen:
            seen[block] = str(current_symbol)
            current_symbol = (current_symbol + 1) % 2  # alternate 0 and 1
        symbol_map.extend([seen[block]] * blockSize)  # each block = 16 pixels

    actual_pixels = len(symbol_map)
    print(f"Total blocks: {len(blocks)}, total reconstructed pixels: {actual_pixels}")

    with open(outfile, mode="w") as f:
        f.write("P1\n")
        f.write(f"{width} {height}\n")
        for i in range(height):
            row = symbol_map[i * width : (i + 1) * width]
            f.write(" ".join(row) + "\n")

    print(f"Output written to: {outfile}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract visual pattern from ECB-encrypted PBM pixel data."
    )
    parser.add_argument("-i", dest="infile", help="Input file: encrypted PBM data")
    parser.add_argument("-o", dest="outfile", help="Output file: extracted PBM image")
    parser.add_argument(
        "-hh", dest="headerfile", help="Header file: original PBM header"
    )

    args = parser.parse_args()

    print(f"Reading from: {args.infile}")
    print(f"Reading header from: {args.headerfile}")
    print(f"Writing output to: {args.outfile}")

    extract(args.infile, args.outfile, args.headerfile)
