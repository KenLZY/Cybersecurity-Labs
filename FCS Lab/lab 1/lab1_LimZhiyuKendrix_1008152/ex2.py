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
        binaryInput = fin_b.read()
        # create a bytearray with the binary input
        ba = bytearray(binaryInput)
        # take the first 8 bytes of the array to check for png file
        byteHeader = ba[:8]

        if mode != None:

            for char in ba:
                # each char is now an int
                if mode == "e":
                    shiftedChar = (char + key) % 256
                    fout_b.write(bytes([shiftedChar]))
                elif mode == "d":
                    shiftedChar = (char - key) % 256
                    fout_b.write(bytes([shiftedChar]))
        else:
            # iterate through every single possible key i.e. 0 - 255
            for possibleKey in range(256):
                # create an empty list to store every possible first 8 decrypted bytes
                decryptedBytes = []
                # use this key to decrypt the first 8 bytes
                for byte in byteHeader:
                    decryptedBytes.append((byte - possibleKey) % 256)
                    # then, we check if the current combination of the decrypted 8 bytes fits
                    # the PNG file special 8 byte combination
                if decryptedBytes == PNG:
                    print(f"The correct key has been found... {possibleKey}")
                    break

            # if indeed the correct key, we will use it to decrypt the whole file
            for byte in ba:
                shiftedChar = (byte - possibleKey) % 256
                fout_b.write(bytes([shiftedChar]))


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
