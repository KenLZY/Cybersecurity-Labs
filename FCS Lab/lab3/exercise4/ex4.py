#! /opt/anaconda3/bin/python3
import hashlib
import string
import csv


def splitDifficulty(hashes: str) -> list:
    weakHash = []
    moderateHash = []
    strongHash = []

    hashes = hashes.strip().split("\n")

    for hash in hashes:
        if "=== Weak ===" == hash:
            targetList = weakHash
        if "=== Moderate ===" == hash:
            targetList = moderateHash
        if "=== Strong ===" == hash:
            targetList = strongHash

        targetList.append(hash)

    weakHash.pop(0)
    moderateHash.pop(0)
    strongHash.pop(0)

    return weakHash, moderateHash, strongHash


with open("hashes.txt", mode="r") as fin:
    hashes = fin.read()

print("First, we segment these hashes into their categories...\n")
print(
    "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
)

weakHash, moderateHash, strongHash = splitDifficulty(hashes)

############################ Writing all hashes to its corresponding text files ############################
with open("weakHashes.txt", mode="w") as fout1:
    for hash in weakHash:
        fout1.write(f"{hash}\n")

with open("moderateHashes.txt", mode="w") as fout2:
    for hash in moderateHash:
        fout2.write(f"{hash}\n")

with open("strongHashes.txt", mode="w") as fout3:
    for hash in strongHash:
        fout3.write(f"{hash}\n")

############################ Opening all cracked hashes lists ############################
with open("weakCracked.txt", mode="r") as weakin:
    crackedWeak = weakin.read()

with open("moderateCracked.txt", mode="r") as moderatein:
    crackedModerate = moderatein.read()

with open("strongCracked.txt", mode="r") as strongin:
    crackedStrong = strongin.read()

############################ Printing all cracked hashes lists ############################
crackedWeak = crackedWeak.strip().split("\n")
crackedWeak = [cracked[33::] for cracked in crackedWeak]
print(f"This is the list of cracked weak hashes:\n\n{crackedWeak}\n")
print(
    "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
)

crackedModerate = crackedModerate.replace(" ", "").strip().split("\n")
crackedModerate = [cracked[33::] for cracked in crackedModerate]
print(f"This is the list of cracked moderate hashes:\n\n{crackedModerate}\n")
print(
    "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
)

crackedStrong = crackedStrong.replace(" ", "").strip().split("\n")
crackedStrong = [cracked[33::] for cracked in crackedStrong]
print(f"This is the list of cracked strong hashes:\n\n{crackedStrong}\n")
print(
    "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
)

############################ Reading all hashes list ############################
with open("weakHashes.txt", mode="r") as fout4:
    weakHashes = fout4.read()

with open("moderateHashes.txt", mode="r") as fout5:
    moderateHashes = fout5.read()

with open("strongHashes.txt", mode="r") as fout6:
    strongHashes = fout6.read()

############################ Printing out the statistics for each difficulty ############################
weakHashList = [hash for hash in weakHashes.strip().split("\n")]
print(f"\nWe have a total of {len(weakHashList)} weak hashes\n")
print(f"We have solved a total of {len(crackedWeak)}/{len(weakHashList)}\n")
print(
    "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
)

moderateHashList = [hash for hash in moderateHashes.strip().split("\n")]
print(f"\nWe have a total of {len(moderateHashList)} moderate hashes\n")
print(f"We have solved a total of {len(crackedModerate)}/{len(moderateHashList)}\n")
print(
    "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
)

strongHashList = [hash for hash in strongHashes.strip().split("\n")]
print(f"\nWe have a total of {len(strongHashList)} strong hashes\n")
print(f"We have solved a total of {len(crackedStrong)}/{len(strongHashList)}\n")
print(
    "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
)

print(
    f"We have a total of {len(weakHashList) + len(moderateHashList) + len(strongHashList)} hashes in total"
)
print(
    f"We have solved, in total, {len(crackedWeak) + len(crackedModerate) + len(crackedStrong)} hashes"
)

print(f"All these are done using a website tool called: https://md5decrypt.net/")

headers = ["Hash", "Plaintext"]

######################### Weak hashes to CSV #########################
with open("weakCracked.txt", mode="r") as inCSV, open(
    "weakHashCSV.csv", mode="w", newline=""
) as outCSV:
    # create a csv object
    writer = csv.writer(outCSV)
    # set the headers first
    writer.writerow(headers)
    # now we iterate through each line of the weakHashes.txt file and separate them by ":"
    # then write the data as a row (delimiter sets it to different columns i.e. <hash> <plaintext>)
    for line in inCSV:
        data = line.strip().split(":")
        writer.writerow(data)

######################### Moderate hashes to CSV #########################
with open("moderateCracked.txt", mode="r") as inCSV, open(
    "moderateHashCSV.csv", mode="w", newline=""
) as outCSV:
    # create a csv object
    writer = csv.writer(outCSV)
    # set the headers first
    writer.writerow(headers)
    # now we iterate through each line of the weakHashes.txt file and separate them by ":"
    # then write the data as a row (delimiter sets it to different columns i.e. <hash> <plaintext>)
    for line in inCSV:
        data = line.strip().split(":")
        writer.writerow(data)

######################### Strong hashes to CSV #########################
with open("strongCracked.txt", mode="r") as inCSV, open(
    "strongHashCSV.csv", mode="w", newline=""
) as outCSV:
    # create a csv object
    writer = csv.writer(outCSV)
    # set the headers first
    writer.writerow(headers)
    # now we iterate through each line of the weakHashes.txt file and separate them by ":"
    # then write the data as a row (delimiter sets it to different columns i.e. <hash> <plaintext>)
    for line in inCSV:
        data = line.strip().split(":")
        writer.writerow(data)

######################### Combine all CSVs into one CSV #########################
with open("weakCracked.txt", mode="r") as csv0, open(
    "moderateCracked.txt", mode="r"
) as csv1, open("strongCracked.txt", mode="r") as csv2, open(
    "ex4.csv", mode="w", newline=""
) as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(headers)

    for line in csv0:
        data = line.strip().split(":")
        writer.writerow(data)

    for line in csv1:
        data = line.strip().split(":")
        writer.writerow(data)

    for line in csv2:
        data = line.strip().split(":")
        writer.writerow(data)

with open("ex4.csv", newline="") as f:
    reader = csv.reader(f)
    rowCount = sum(1 for row in reader) - 1
print(f"Total number of rows is {rowCount}")
