#!/opt/anaconda3/bin/python3

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


def convert_bytes_to_int(xbytes):
    return int.from_bytes(xbytes, "big")


def convert_int_to_bytes(x):
    return x.to_bytes(8, "big")


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

    messageInt = convert_bytes_to_int(message)

    return square_multiply(messageInt, d, n)


def verification(signature, originalBytes):
    verifiedMessageInt = encryption(signature)

    # convert it from int to bytes
    bytesVerifiedMessage = verifiedMessageInt.to_bytes(32, byteorder="big")
    if bytesVerifiedMessage == originalBytes:
        return "Match!"

    return "No Match!"


def createSignature():

    with open("message.txt", "r") as f:
        textToSign = f.read()

    # first, we need to hash the text

    hashObject = SHA256.new()
    hashObject.update(bytes(textToSign, "utf-8"))
    print(f"Original Message:\n{textToSign}\n")
    print(
        f"After hashing using SHA256:\nstring: {hashObject.hexdigest()}\nbytes: {hashObject.digest()}\n"
    )

    # then, we need to exponentiate the hash using s = x^d mod n
    digestBytes = hashObject.digest()  # <-- this is in bytes
    signature = decryption(  # <-- i pass it into my decryption function which will convert bytes into int for me
        digestBytes
    )
    print(f"Signature created!\n{signature}\n")
    print(f"Verifying signature... {verification(signature, digestBytes)}")


if __name__ == "__main__":
    createSignature()
