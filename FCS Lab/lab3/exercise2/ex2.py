#! /opt/anaconda3/bin/python3
import argparse
import string
import hashlib
from itertools import product
import time

# Task 1: creating a hash
# plaintext = "Example"
# result = hashlib.md5(plaintext.encode())
# print(result) # this prints the address
# print(result.hexdigest()) # this prints the hash


def mainFunction(filein, fileout):
    fin = open(filein, mode="r", encoding="utf-8", newline="\n")  # read mode
    fout = open(fileout, mode="w", encoding="utf-8", newline="\n")  # write mode

    with open(filein, mode="r") as fin:
        hashes = fin.read()
        print(f"\nThese are the hashes we need to 'reverse':\n{hashes}")
        print("First, we split them into individual strings in a list...\n")
        hashList = hashes.strip().split("\n")
        print(hashList)
        print(
            "\nThe criteria for the input strings are:\n"
            "1. Each character can be a lowercase alphabet or numeric\n"
            "2. Input strings are 5 characters long\n"
            "So, I imported the string module and used 'string.printable', but I only take the first 36 items:\n"
        )

        possibleChar = string.printable[:36]
        possibleDigits = possibleChar[:10]
        possibleAlphabets = possibleChar[10:]
        possibleChar = possibleAlphabets + possibleDigits
        print(possibleChar)

        # now that we have all possible characters, we need to make every single possible combination to brute force
        # reversing the hash
        correctGuesses = []
        # first we need to add 5 characters for our input guess
        startTime = time.perf_counter()
        for candidate in product(possibleChar, repeat=5):
            guess = "".join(candidate)
            encodedGuess = HashEncode(guess)
            # print(guess)
            # then, we check if the hashed input guess is the same as any of the hashes in the list
            if encodedGuess not in hashList:
                continue
            else:
                correctGuesses.append(guess)
                if len(correctGuesses) == len(hashList):
                    break

        endTime = time.perf_counter()
        elapsedTime = endTime - startTime
        print(f"\nThe program ran for {elapsedTime}\n")
        print(correctGuesses)

        number = 1
        for guess in correctGuesses:
            fout.write(f"{number}: {guess}\n")
            number += 1


def HashEncode(text: str) -> str:
    result = hashlib.md5(text.encode())
    return result.hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="hash codes")
    parser.add_argument("-o", dest="fileout", help="output file")

    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout

    mainFunction(filein, fileout)
