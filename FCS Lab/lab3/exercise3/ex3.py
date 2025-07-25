#! /opt/anaconda3/bin/python3
import random
import hashlib
import string
from itertools import product
import time

# TODO: load the hashes from ex2_hash.txt and append one random lower case character
# as a salt value to all the elements of the list of passwords we recovered from previous
# exercise


def mainFunction():

    # first, we read the hash values from previous exercise
    with open("ex2_hash.txt", mode="r") as fin:
        passwords = fin.read()
        # print(passwords)

    # next, we need to clean up the data
    passwordList = cleanData(passwords)
    print(f"\nThis is the password list:\n{passwordList}\n")

    # from here, we pick a random word
    randomWord = random.choice(passwordList)

    # then, we pick a random lowercase character from the word
    notAlphabet = True
    while notAlphabet:
        randomChar = random.choice(randomWord)
        if randomChar.isalpha():
            notAlphabet = False

    print(f"\nThe selected salt character is '{randomChar}'!\n")

    # this is done so that the next time we run this program,
    # I don't just append it to the previously saved plaintext and hashes
    open("plain6.txt", mode="w").close()
    open("salted6.txt", mode="w").close()

    for password in passwordList:
        # (1) append the random character to the passwords
        newPassword = password + randomChar
        # (2) add the new appended passwords to plain6.txt
        with open("plain6.txt", mode="a") as fout:
            fout.write(f"{newPassword}\n")
        # (3) re hash the new passwords and add it to salted6.txt
        hashedPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with open("salted6.txt", mode="a") as fout:
            fout.write(f"{hashedPassword}\n")

    # we store the salted hash into a list
    with open("salted6.txt", mode="r") as fin:
        hashList = fin.read()

    with open("plain6.txt", mode="r") as fout:
        newPasswords = fout.read()

    print(f"These are the new passwords:\n{newPasswords}\n")

    # now, we brute force it again
    # print(hashList)
    possibleChar = string.printable[:36]
    possibleDigits = possibleChar[:10]
    possibleAlphabets = possibleChar[10:]
    possibleChar = possibleAlphabets + possibleDigits
    # print(possibleChar)

    # now that we have all possible characters, we need to make every single possible combination to brute force
    # reversing the hash
    correctGuesses = []
    salt = ""
    # since we have to pretend that we don't know the original cracked passwords, we have to brute force all
    # possible combination
    startTime = time.perf_counter()
    print("Program is running...")
    for candidate in product(possibleChar, repeat=6):
        guess = "".join(candidate)
        encodedGuess = HashEncode(guess)
        if encodedGuess not in hashList:
            continue
        else:
            salt = guess[-1]
            correctGuesses.append(guess)
            break
    for candidate in product(possibleChar, repeat=5):
        guess = "".join(candidate) + salt
        encodedGuess = HashEncode(guess)
        if encodedGuess not in hashList and guess not in correctGuesses:
            continue
        else:
            correctGuesses.append(guess)
            if len(correctGuesses) == len(hashList):
                break
    endTime = time.perf_counter()
    elapsedTime = endTime - startTime
    print(f"\nThe program ran for {elapsedTime}s\n")
    print(correctGuesses)


def cleanData(data: str) -> list:
    # strip all white spaces & split into a list
    dataList = data.strip().split("\n")
    dataList = [data[3:].strip() for data in dataList]
    return dataList


def HashEncode(text: str) -> str:
    result = hashlib.md5(text.encode())
    return result.hexdigest()


mainFunction()
