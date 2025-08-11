#!/opt/anaconda3/bin/python3

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


def convert_bytes_to_int(xbytes):
    return int.from_bytes(xbytes, "big")


def square_multiply(base, exponent, modulus):
    result = 1
    base = base % modulus

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent // 2
    return result


def encryption(message):
    key = open("mykey.pem.pub", "r").read()
    rsaPublicKey = RSA.importKey(key)
    e = rsaPublicKey.e
    n = rsaPublicKey.n

    return square_multiply(message, e, n)


def decryption(message):
    key = open("mykey.pem.priv", "r").read()
    rsaPrivateKey = RSA.importKey(key)
    d = rsaPrivateKey.d
    n = rsaPrivateKey.n

    if not isinstance(message, int):
        messageInt = convert_bytes_to_int(message)

    else:
        messageInt = message

    return square_multiply(messageInt, d, n)


def protocolAttack():
    target = 100
    # encrypt target using public key
    encryptedTarget = encryption(target)
    print(f"Result:\n{encryptedTarget}")

    # calculate s^e mod n
    bogusTarget = encryption(2)
    print(f"Modified:\n{bogusTarget}")

    key = open("mykey.pem.pub", "r").read()
    rsaPublicKey = RSA.importKey(key)
    n = rsaPublicKey.n
    # multiply encryptedTarget & bogusTarget mod n
    m = encryptedTarget * (bogusTarget % n)

    # decrypt m using private key
    decryptedM = decryption(m)
    print(f"Decrypted: {decryptedM}")


if __name__ == "__main__":
    print("Part II -------------")
    print(f"Encrypting: 100")
    protocolAttack()
