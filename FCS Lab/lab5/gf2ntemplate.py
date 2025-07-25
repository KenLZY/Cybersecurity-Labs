#!/opt/anaconda3/bin/python3

# 50.042 FCS Lab 5 Modular Arithmetic
# Year 2025
import copy


# Part 1: Algebraic Structures
class Polynomial2:
    def __init__(self, coeffs: list[int]):
        self.polynomial = coeffs

    def add(self, p2):
        result = []
        if len(self.polynomial) > len(p2.polynomial):
            maxLen = len(self.polynomial)
            while len(p2.polynomial) < maxLen:
                p2.polynomial.append(0)
        else:
            maxLen = len(p2.polynomial)
            while len(self.polynomial) < maxLen:
                self.polynomial.append(0)

        for bit1, bit2 in zip(self.polynomial, p2.polynomial):
            result.append(bit1 ^ bit2)
        return Polynomial2(result)

    def sub(self, p2):
        result = []
        if len(self.polynomial) > len(p2.polynomial):
            maxLen = len(self.polynomial)
            while len(p2.polynomial) < maxLen:
                p2.polynomial.append(0)
        else:
            maxLen = len(p2.polynomial)
            while len(self.polynomial) < maxLen:
                self.polynomial.append(0)

        for bit1, bit2 in zip(self.polynomial, p2.polynomial):
            result.append(bit1 ^ bit2)
        return Polynomial2(result)

    def mul(self, p2, modp=None):
        result_len = len(self.polynomial) + len(p2.polynomial) - 1
        result = [0] * result_len

        for i in range(len(self.polynomial)):
            for j in range(len(p2.polynomial)):
                result[i + j] ^= self.polynomial[i] & p2.polynomial[j]

        if modp is not None:
            result_copy = result[:]
            while len(result_copy) >= len(modp.polynomial):
                shift = len(result_copy) - len(modp.polynomial)
                for i in range(len(modp.polynomial)):
                    result_copy[i + shift] ^= modp.polynomial[i]
                while len(result_copy) > 0 and result_copy[-1] == 0:
                    result_copy.pop()
            return Polynomial2(result_copy)

        return Polynomial2(result)

    def degree(self) -> int:
        for i in reversed(range(len(self.polynomial))):
            if self.polynomial[i] == 1:
                return i
        return -1

    def div(self, p2):
        # Initial quotient and remainder
        quotient = Polynomial2(
            [0] * (len(self.polynomial) - len(p2.polynomial) + 1)
            if len(self.polynomial) >= len(p2.polynomial)
            else [0]
        )
        remainder = Polynomial2(self.polynomial.copy())

        while remainder.degree() >= p2.degree():
            shift = remainder.degree() - p2.degree()

            # s = x^shift
            s = Polynomial2([0] * shift + [1])

            # q = q + s
            quotient = quotient.add(s)

            # sb = shifted version of p2
            sb = Polynomial2([0] * shift + p2.polynomial)
            remainder = remainder.add(sb)  # r = r - sb (XOR)

        return quotient, remainder

    def __str__(self):
        terms = []
        for i in reversed(range(len(self.polynomial))):  # this is a list
            if self.polynomial[i] == 1:
                if i == 0:
                    terms.append("1")
                elif i == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{i}")
        return " + ".join(terms) if terms else "0"

    def __len__(self):
        return len(self.polynomial)

    @staticmethod
    def getInt(p):
        result = 0
        for bit in range(len(p.polynomial)):
            if p.polynomial[bit] == 1:
                result += 2**bit
        return result


class GF2N:
    affinemat = [
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1],
    ]

    def __init__(self, x, n=8, ip=None):

        def int_to_bin_list(x: int, n: int) -> list[int]:
            """Convert int x to little-endian binary list of max length n."""
            bits = []
            while x:
                bits.append(x & 1)
                x >>= 1
            return bits[:n]

        self.n = n
        if ip is None:
            ip = Polynomial2([1, 0, 0, 1, 1])  # x^4 + x + 1

        if isinstance(ip, Polynomial2):
            self.ip = ip
        else:
            self.ip = Polynomial2(ip)

        # Convert x to binary polynomial if it’s an int
        if isinstance(x, int):
            bin_list = int_to_bin_list(x, n)
        elif isinstance(x, list):
            bin_list = x[:n]
        elif isinstance(x, Polynomial2):
            bin_list = x.polynomial[:n]
        else:
            raise TypeError("x must be int, list, or Polynomial2")

        # Now reduce x mod ip
        px = Polynomial2(bin_list)
        _, reduced = px.div(self.ip)

        self.poly = reduced

    def add(self, g2):
        if self.n != g2.n or self.ip.polynomial != g2.ip.polynomial:
            raise ValueError("Mismatched fields")

        # XOR the two polynomials
        result_poly = self.poly.add(g2.poly)

        # Reduce mod irreducible polynomial (if needed)
        _, reduced = result_poly.div(self.ip)

        return GF2N(reduced.polynomial, self.n, self.ip)

    def sub(self, g2):
        if self.n != g2.n or self.ip.polynomial != g2.ip.polynomial:
            raise ValueError("Mismatched fields")

        # XOR the two polynomials
        result_poly = self.poly.add(g2.poly)

        # Reduce mod irreducible polynomial (if needed)
        _, reduced = result_poly.div(self.ip)

        return GF2N(reduced.polynomial, self.n, self.ip)

    def mul(self, other):
        if self.n != other.n or self.ip.polynomial != other.ip.polynomial:
            raise ValueError("Mismatched fields")

        product = self.poly.mul(other.poly, self.ip)
        _, reduced = product.div(self.ip)

        return GF2N(reduced.polynomial, self.n, self.ip)

    def inverse(self):
        a = self.ip  # Polynomial2
        b = self.poly  # Polynomial2

        if b.polynomial == [0]:
            raise ZeroDivisionError("Cannot invert zero in GF(2^n)")

        r0, r1 = a, b
        t0, t1 = Polynomial2([0]), Polynomial2([1])

        while r1.polynomial != [0]:
            q, _ = r0.div(r1)  # q = r0 // r1

            # r0 = r1
            # r1 = r0 - q*r1
            new_r = r0.add(q.mul(r1))  # r = r0 - q*r1
            new_t = t0.add(q.mul(t1))  # t = t0 - q*t1

            r0, r1 = r1, new_r
            t0, t1 = t1, new_t

        # At this point, r0 = gcd, should be 1
        if r0.polynomial != [1]:
            raise ValueError(
                "Polynomial has no inverse (not relatively prime to modulus)"
            )

        return GF2N(t0.polynomial, self.n, self.ip)

    def div(self, g2):
        if self.n != g2.n or self.ip.polynomial != g2.ip.polynomial:
            raise ValueError("Field mismatch")

        inv = g2.inverse()  # Step 1: get inverse
        result = self.mul(inv, self.ip)  # Step 2: multiply

        return result

    def getPolynomial2(self):
        return self.poly

    def __str__(self):
        return str(self.poly)

    def getInt(self):
        pass

    def mulInv(self):
        pass

    def affineMap(self):
        pass


print("\nTest 1")
print("======")
print("p1=x^5+x^2+x")
print("p2=x^3+x^2+1")
p1 = Polynomial2([0, 1, 1, 0, 0, 1])
p2 = Polynomial2([1, 0, 1, 1])
p3 = p1.add(p2)
print("p3= p1+p2 = ", p3)
print(f"{Polynomial2.getInt(p1)} + {Polynomial2.getInt(p2)} = {Polynomial2.getInt(p3)}")

print("\nTest 2")
print("======")
print("p4=x^7+x^4+x^3+x^2+x")
print("modp=x^8+x^7+x^5+x^4+1")
p4 = Polynomial2([0, 1, 1, 1, 1, 0, 0, 1])
# modp=Polynomial2([1,1,0,1,1,0,0,0,1])
modp = Polynomial2([1, 0, 0, 0, 1, 1, 0, 1, 1])
p5 = p1.mul(p4, modp)
print("p5=p1*p4 mod (modp)=", p5)
print(
    f"{Polynomial2.getInt(p5)} mod {Polynomial2.getInt(modp)} = {Polynomial2.getInt(p5)}"
)

print("\nTest 3")
print("======")
print("p6=x^12+x^7+x^2")
print("p7=x^8+x^4+x^3+x+1")
p6 = Polynomial2([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
p7 = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
p8q, p8r = p6.div(p7)
print(f"{Polynomial2.getInt(p6)} / {Polynomial2.getInt(p7)} =")
print("q for p6/p7=", p8q)
print(f"{Polynomial2.getInt(p8q)}")
print("r for p6/p7=", p8r)
print(f"{Polynomial2.getInt(p8r)}")

####
print("\nTest 4")
print("======")
g1 = GF2N(100)
g2 = GF2N(5)
print("g1 = ", g1.getPolynomial2())
print("g2 = ", g2.getPolynomial2())
g3 = g1.add(g2)
print("g1+g2 = ", g3)

print("\nTest 5")
print("======")
ip = Polynomial2([1, 1, 0, 0, 1])
print("irreducible polynomial", ip)
g4 = GF2N(0b1101, 4, ip)
g5 = GF2N(0b110, 4, ip)
print("g4 = ", g4.getPolynomial2())
print("g5 = ", g5.getPolynomial2())
g6 = g4.mul(g5)
print("g4 x g5 = ", g6.poly)

print("\nTest 6")
print("======")
g7 = GF2N(0b1000010000100, 13, None)
g8 = GF2N(0b100011011, 13, None)
print("g7 = ", g7.getPolynomial2())
print("g8 = ", g8.getPolynomial2())
q, r = g7.div(g8)
print("g7/g8 =")
print("q = ", q.getPolynomial2())
print("r = ", r.getPolynomial2())

print("\nTest 7")
print("======")
ip = Polynomial2([1, 1, 0, 0, 1])
print("irreducible polynomial", ip)
g9 = GF2N(0b101, 4, ip)
print("g9 = ", g9.getPolynomial2())
print("inverse of g9 =", g9.mulInv().getPolynomial2())

print("\nTest 8")
print("======")
ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
print("irreducible polynomial", ip)
g10 = GF2N(0xC2, 8, ip)
print("g10 = 0xc2")
g11 = g10.mulInv()
print("inverse of g10 = g11 =", hex(g11.getInt()))
g12 = g11.affineMap()
print("affine map of g11 =", hex(g12.getInt()))
