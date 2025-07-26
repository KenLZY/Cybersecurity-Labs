#!/opt/anaconda3/bin/python3
# 50.042 FCS Lab 6 template
# Year 2025

from primes import *
import presents
import random
import argparse


def isPrimitive(g, p):
    from math import gcd
    from sympy import factorint

    phi = p - 1
    factors = factorint(phi)

    for q in factors:
        if pow(g, phi // q, p) == 1:
            return False

    return True


def dhke_setup(nb):
    # TODO: choose a large prime number closest to 2^nb
    # this is used as the modulus
    p = gen_prime_nbits(nb)

    # TODO: choose an integer, a that belongs to [2, 3, ..., p-2] which is a primitive element
    # this is used as the base
    for g in range(2, p):
        if isPrimitive(g, p):
            a = g
            break

    return p, a


def gen_priv_key(p):
    """
    takes in the modulus and chooses a number between 2 and p - 2
    as the private key
    """
    return random.randint(2, p - 2)


def get_pub_key(alpha, a, p):
    """
    Computes the public key by the following formula:
    publicKey = alpha^a mod p
    where alpha = a
    a = random number we picked as private key
    p = modulus
    """
    return pow(alpha, a, p)


def get_shared_key(keypub, keypriv, p):
    """
    Computed by the following formula:
    sharedKey = public_key_other_party ^ your_own_privateKey mod p
    """
    return pow(keypub, keypriv, p)


def ecb(infile, outfile, mode):
    blockSize = 8  # PRESENT block size = 64-bits = 8 bytes

    if mode == "e":
        key = sharedKeyA
    elif mode == "d":
        key = sharedKeyB
    else:
        raise ValueError("Mode must be e or d")

    key &= (1 << 80) - 1  # Truncate to 80-bit key
    assert sharedKeyA == sharedKeyB, "Shared keys do not match!"

    # Read input file
    with open(infile, "rb") as f:
        data = f.read()
        original_len = len(data)

    # Pad data if encrypting
    if mode == "e":
        original_len = len(data)
        pad_len = blockSize - (original_len % blockSize)
        if pad_len != 0:
            data += bytes([0] * pad_len)
        len_bytes = original_len.to_bytes(8, byteorder="big")
        data = data + len_bytes

    # ECB encryption/decryption loop
    result = b""
    for i in range(0, len(data), blockSize):
        block = data[i : i + blockSize]
        block_int = int.from_bytes(block, byteorder="big")

        if mode == "e":
            encrypted = presents.present(block_int, key)
            result += encrypted.to_bytes(blockSize, byteorder="big")
        elif mode == "d":
            decrypted = presents.present_inv(block_int, key)
            result += decrypted.to_bytes(blockSize, byteorder="big")

    # Unpad result after decryption
    if mode == "d":
        original_len = int.from_bytes(result[-8:], byteorder="big")
        result = result[:original_len]

    # Write output
    with open(outfile, "wb") as f:
        f.write(result)


if __name__ == "__main__":
    p, alpha = dhke_setup(80)
    print("Generate P and alpha:")
    print("P:", p)
    print("alpha:", alpha)
    print()
    a = gen_priv_key(p)
    b = gen_priv_key(p)
    print("My private key is: ", a)
    print("Test other private key is: ", b)
    print()
    A = get_pub_key(alpha, a, p)
    B = get_pub_key(alpha, b, p)
    print("My public key is: ", A)
    print("Test other public key is: ", B)
    sharedKeyA = get_shared_key(B, a, p)
    sharedKeyB = get_shared_key(A, b, p)
    print("My shared key is: ", sharedKeyA)
    print("Test other shared key is: ", sharedKeyB)
    print("Length of key is %d bits." % sharedKeyA.bit_length())

    ecb("textA.txt", "ciphertext.txt", "e")
    ecb("ciphertext.txt", "deciphertext.txt", "d")

    ecb("textB.txt", "ciphertextB.txt", "e")
    ecb("ciphertextB.txt", "deciphertextB.txt", "d")
