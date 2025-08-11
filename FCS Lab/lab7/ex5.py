#!/opt/anaconda3/bin/python3

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS


def generate_RSA(bits):
    key = RSA.generate(bits)
    privateKey = key.export_key()
    with open("private.pem", "wb") as f:
        f.write(privateKey)

    publicKey = key.publickey().export_key()
    with open("public.pem", "wb") as f:
        f.write(publicKey)


def encrypt_RSA(publicKeyFile, message):
    """
    Input(s): public key file, message to encrypt (string)
    Description: encrypts a string message using public key from publicKeyFile
    Output(s): ciphertext in base64
    """
    # read public key from file
    key = open(publicKeyFile, "r").read()
    publicKey = RSA.importKey(key)

    # create a new PKCS1_OAEP object
    object = PKCS1_OAEP.new(publicKey)

    # encrpyt using the object's encryption method
    if isinstance(message, bytes):
        encryptedMessage = object.encrypt(message)

    else:
        encryptedMessage = object.encrypt(bytes(message, "utf-8"))

    print("Encryption Successful!")

    return encryptedMessage


def decrypt_RSA(privateKeyFile, data):
    key = open(privateKeyFile, "r").read()
    privateKey = RSA.importKey(key)

    object = PKCS1_OAEP.new(privateKey)

    # decrypt
    decryptedMessage = object.decrypt(data)

    print("Decryption Successful!")

    return decryptedMessage


def sign_data(privateKeyFile, data):
    key = open(privateKeyFile, "r").read()
    privateKey = RSA.importKey(key)

    # we need to use SHA256 to create a new message digest first
    hashObject = SHA256.new()
    hashObject.update(bytes(data, "utf-8"))

    hashedMessage = hashObject

    # now we sign
    sigObj = PKCS1_PSS.new(privateKey)
    encryptedHash = sigObj.sign(hashedMessage)

    print("Signing Successful!")

    return encryptedHash


def verify_sign(publicKeyFile, sign, data):
    key = open(publicKeyFile, "r").read()
    publicKey = RSA.importKey(key)

    sigObj = PKCS1_PSS.new(publicKey)

    hashObject = SHA256.new()
    hashObject.update(data)

    hashedMessage = hashObject

    return sigObj.verify(hashedMessage, sign)


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

    pub_path = "public.pem"
    pub = RSA.import_key(open(pub_path, "rb").read())
    n, e = pub.n, pub.e

    print("Let's start with Alice's part!\n")
    # Alice's part: choose any 1024-bit integer s
    s = 17278428755466050461922416417456305911206992736355996744667988325383638453527287840229977116579519190350875998516779971720169560831899610583367448276948078728182600166896165251409169999908875528848631188462942214825966179684162812512274199976543984116159230198524269299599982349337245533972208601227522300185
    print(f"Selected 1024-bit integer, s:\n{s}\n")

    # Alice's part: compute new "message" x = s^e mod n
    x = pow(s, e, n)
    print(f"Computed new message, x = s^e mod n:\n{x}\n")
    print("Sending Bob the signature s and the message x...\n")
    print("Now it's Bob's turn!\n")

    h = SHA256.new()

    verifier = PKCS1_PSS.new(pub)
    ok_pss = verifier.verify(h, s)

    print(f"Result: {ok_pss}")


if __name__ == "__main__":
    print("Task IV -------------")
    print("\n1: Encrypt mydata.txt with public key")
    generate_RSA(1024)
    message = open("mydata.txt", "r").read()
    print(f"Message to encrypt: {message}")
    encryptedMessage = encrypt_RSA("public.pem", message)
    print("\n2: Decrypt mydata.txt with private key")
    decryptedMessage = decrypt_RSA("private.pem", encryptedMessage)
    print("\n3: Sign mydata.txt using private key")
    signedMessage = sign_data("private.pem", message)
    print("\n4: Verify signature")
    verification = verify_sign("public.pem", signedMessage, decryptedMessage)
    print(f"\nVerified: {verification}")

    print("\nNow, we are going to redo the protocol attack again to see if it works!")
    rsaDigitalSignatureAttack()
    print("\nThe attack did not work on this new RSA")
