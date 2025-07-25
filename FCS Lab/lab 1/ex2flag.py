#!/opt/anaconda3/bin/python3

import sys
import argparse
import string


def doStuff(filein, fileout, key, mode):
    # open file handles to both files
    fin = open(filein, mode="r", encoding="utf-8", newline="\n")  # read mode
    fin_b = open(filein, mode="rb")  # binary read mode
    fout = open(fileout, mode="w", encoding="utf-8", newline="\n")  # write mode
    fout_b = open(fileout, mode="wb")  # binary write mode

    PNG = [137, 80, 78, 71, 13, 10, 26, 10]

    with open(filein, mode="rb") as fin_b:
        byteObj = bytearray(fin_b.read())
        byteHeader = byteObj[:8]
        decrypted = []
        for possibleKey in range(256):
            for byte in byteHeader:
                decrypted.append((byte - possibleKey) % 256)
            if decrypted == PNG:
                print(f"Correct key has been found... {possibleKey}")
                break
            else:
                decrypted = []

        # once found the correct key, use it to decrypt the whole file
        for byte in byteObj:
            decryptByte = (byte - possibleKey) % 256
            fout_b.write(bytes([decryptByte]))


if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file")
    parser.add_argument("-k", dest="keyIn", help="key", type=int, choices=range(256))
    parser.add_argument("-m", dest="mode", choices=["d", "e"], help="mode")

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.keyIn
    mode = args.mode

    doStuff(filein, fileout, key, mode)
