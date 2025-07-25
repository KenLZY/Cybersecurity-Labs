#!/opt/anaconda3/bin/python3
# 50.042 FCS Lab 6 template
# Year 2025

import random


def square_multiply(a, x, n):
    y = 1
    originalX = x
    # n_b is the number of bits in x
    xBinary = ""

    while x > 0:
        remainder = x % 2
        xBinary += f"{remainder}"
        quotient = x // 2
        x = quotient

    xBinary = xBinary[::-1]

    # print(f"The representation in binary for {originalX} is {xBinary}")
    # print(f"Number of bits in x is {len(xBinary)}\n")

    for bit in xBinary:
        y = (y**2) % n
        if bit == "1":
            y = (a * y) % n
    return y


def miller_rabin(n, a):
    # n - 1 = 2^r * d
    # TODO determine r and d
    oddYet = False
    target = n - 1
    count = 0
    while not oddYet:
        target //= 2
        count += 1
        if target % 2 != 0:
            oddYet = True
    r = count
    d = target

    # TODO: compute x = a^d mod n
    x = square_multiply(a, d, n)

    if x == 1 or x == n - 1:
        # print("Probably prime")
        return True
    else:
        for i in range(r - 1):
            x = square_multiply(x, 2, n)
            if x == n - 1:
                # print("Probably prime")
                return True
            if x == 1:
                return True
    # print("Probably composite")
    return False


def gen_prime_nbits(n):
    """
    Generates a random prime number with exactly n bits
    """
    while True:
        candidate = random.randint(2 ** (n - 1), (2**n) - 1)
        if candidate % 2 == 0:
            candidate += 1
        if miller_rabin(candidate, 2):
            return candidate


if __name__ == "__main__":

    print(square_multiply(2, 3, 5))
    print(square_multiply(3, 4, 7))
    print(square_multiply(3, 13, 7))

    print("Is 561 a prime?")
    print(miller_rabin(561, 2))
    print("Is 27 a prime?")
    print(miller_rabin(27, 2))
    print("Is 61 a prime?")
    print(miller_rabin(61, 2))

    print("Random number (100 bits):")
    print(gen_prime_nbits(100))
    print("Random number (80 bits):")
    print(gen_prime_nbits(80))
    print("Random number (8 bits):")
    print(gen_prime_nbits(8))
