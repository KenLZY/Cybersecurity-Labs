#! /opt/anaconda3/bin/python3
import hashlib
import random

# Task 1: creating a hash
plaintext = "123"
result = hashlib.md5(plaintext.encode())
# print(result)  # this prints the address
print(result.hexdigest())  # this prints the hash
print(
    f"The length of this plaintext is {len(plaintext)}\nThe length of the hashcode is {len(result.hexdigest())}"
)
