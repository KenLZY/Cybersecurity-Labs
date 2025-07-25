#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS

import argparse


def getInfo(headerfile):
    with open(headerfile, mode="rb") as headerin:
        headerInfo = headerin.read()
        header = headerInfo.splitlines()
        magicNum = header[0].decode()

        for line in header:
            line = line.decode()
            if line.startswith("#"):
                continue
            elif line.startswith("P1") or line.startswith("P4"):
                continue
            else:
                width, height = map(int, line.strip().split())
        return magicNum, width, height


def extract(infile, outfile, headerfile):
    header, width, height = getInfo(headerfile)
    print(f"Magic Number: {header}\nWidth: {width}\nHeight: {height}")
    pixel_data = b"\n".join(header[2:]).decode().replace("\n", " ").split()
    pixels = [int(p) for p in pixel_data]

    # read the ECB encrypted file
    with open(infile, mode="rb") as fin:
        cipheredData = fin.read()

    # split the binary data into blocks
    blockSize = 16
    blocks = [
        cipheredData[i : i + blockSize] for i in range(0, len(cipheredData), blockSize)
    ]
    seen = {}  # dictionary to store first-time-seen blocks
    symbol_map = []  # stores the final pattern using 0/1
    current_symbol = 0  # toggles between 0 and 1
    for block in blocks:
        if block not in seen:
            seen[block] = str(current_symbol)
            current_symbol = (current_symbol + 1) % 2  # alternate 0/1
        symbol_map.append(seen[block])

    # reshape flat list of symbols into rows using image width
    lines = [
        "".join(symbol_map[i : i + width]) for i in range(0, len(symbol_map), width)
    ]

    # save the pattern into a .txt file
    with open(outfile, "w") as f:
        for row in lines:
            f.write(row + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract PBM pattern.")
    parser.add_argument("-i", dest="infile", help="input file, PBM encrypted format")
    parser.add_argument("-o", dest="outfile", help="output PBM file")
    parser.add_argument("-hh", dest="headerfile", help="known header file")

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    headerfile = args.headerfile

    print("Reading from: %s" % infile)
    print("Reading header file from: %s" % headerfile)
    print("Writing to: %s" % outfile)

    success = extract(infile, outfile, headerfile)
