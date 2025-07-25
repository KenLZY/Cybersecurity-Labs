#!/opt/anaconda3/bin/python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out


# Import libraries
import sys
import argparse
import string


def doStuff(filein, fileout, key, mode):
    # open file handles to both files
    fin = open(filein, mode="r", encoding="utf-8", newline="\n")  # read mode
    fin_b = open(filein, mode="rb")  # binary read mode
    fout = open(fileout, mode="w", encoding="utf-8", newline="\n")  # write mode
    fout_b = open(fileout, mode="wb")  # binary write mode
    c = fin.read()  # read in file into c as a str
    # and write to fileout

    # close all file streams
    # fin.close()
    # fin_b.close()
    # fout.close()
    # fout_b.close()

    result = ""
    ALPHABET = string.printable
    N = len(ALPHABET)

    # PROTIP: pythonic way
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        text = fin.read()
        # do stuff

        if mode == "e":
            for char in text:
                if char in ALPHABET:
                    getCharIdx = ALPHABET.index(char)
                    newIdx = (getCharIdx + key) % N
                    encryptedChar = ALPHABET[newIdx]
                    result += encryptedChar

        else:
            for char in text:
                if char in ALPHABET:
                    getCharIdx = ALPHABET.index(char)
                    newIdx = (getCharIdx - key) % N
                    encryptedChar = ALPHABET[newIdx]
                    result += encryptedChar

        fout.write(result)

        # file will be closed automatically when interpreter reaches end of the block


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file")
    parser.add_argument(
        "-k",
        dest="keyIn",
        help="key",
        type=int,
        choices=range(1, len(string.printable) - 1),
    )
    parser.add_argument("-m", dest="mode", choices=["d", "e"], help="mode")

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.keyIn
    mode = args.mode

    doStuff(filein, fileout, key, mode)

    # all done
