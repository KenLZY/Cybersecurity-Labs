#!/opt/anaconda3/bin/python3

from Crypto.PublicKey import RSA


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


def rsaDigitalSignatureAttack():

    print("Let's start with Alice's part!\n")
    # Alice's part: choose any 1024-bit integer, s
    s = 17278428755466050461922416417456305911206992736355996744667988325383638453527287840229977116579519190350875998516779971720169560831899610583367448276948078728182600166896165251409169999908875528848631188462942214825966179684162812512274199976543984116159230198524269299599982349337245533972208601227522300185
    print(f"Selected 1024-bit integer, s:\n{s}\n")
    # Alice's part: compute new message, x, using public key
    x = encryption(s)
    print(f"Computed new message, x:\n{x}\n")
    print("Sending Bob signature, s and message, x...\n")
    print("Now's Bob's turn!\n")

    # Bob's part: use public key to get new digest xPrime
    xPrime = encryption(s)
    print(
        "After Bob computes a new digest, x prime using public key...\nHe checks if x prime == x"
    )
    if xPrime == x:
        print(f"Do these two messages match, Bob?\n{xPrime == x}\n")
        print("Since they both match, message and signature pair (x, s) is accepted!")


if __name__ == "__main__":
    print("Part III -------------")
    rsaDigitalSignatureAttack()
