# Kevin Kokomani

# Python 2.7

# Using the arithmetic functions in big.py, this program performs integer division for two positive integers represented
# as bytearrays of the same size. The division function works correctly with negative numbers, bytearrays of different sizes,
# and the program also supports the modulo operation and modular exponentiation. All code in big.py supplied by the instructor,
# all code in intarithmetic.py written by Kevin Kokomani

import unittest
import big

#Main divide function
def divide(a, b):
    if len(a) < len(b):
        a = big.sign_extend(a, len(b)-len(a))
    if len(b) < len(a):
        b = big.sign_extend(b, len(a) - len(b))

    if big.is_negative(a) and big.is_negative(b):
        quotient, remainder = dividePositive(big.negate(a), big.negate(b))
        return quotient
    elif big.is_negative(a):
        quotient, remainder = dividePositive(big.negate(a), b)
        return divideDifferentSigns(quotient, remainder)
    elif big.is_negative(b):
        quotient, remainder = dividePositive(a, big.negate(b))
        return divideDifferentSigns(quotient, remainder)
    else:
        quotient, remainder = dividePositive(a, b)
        return quotient

#Main modulo function
def modulo(a, b):
    if len(a) < len(b):
        a = big.sign_extend(a, len(b) - len(a))
    if len(b) < len(a):
        b = big.sign_extend(b, len(a) - len(b))

    if big.is_negative(a) and big.is_negative(b):
        quotient, remainder = dividePositive(big.negate(a), big.negate(b))
        return big.negate(remainder)
    elif big.is_negative(a):
        quotient, remainder = dividePositive(b, big.negate(a))
        return remainder
    elif big.is_negative(b):
        quotient, remainder = dividePositive(big.negate(b), a)
        return big.negate(remainder)
    else:
        quotient, remainder = dividePositive(a, b)
        return remainder

#Main Modulo Exp Function
def moduloExp(a, b, n):
    zero = bytearray(len(b))
    if (big.equal(b, zero)):
        return big.int2bytearray(1, len(b))

    z = moduloExp(a, big.half(b), n)
    if (big.is_even(b)):
        return modulo(big.multiply(z, z), n)
    else:
        return modulo(big.multiply(a, big.multiply(z, z)), n)

#Helper functions
def dividePositive(a, b):
    zero = bytearray(len(a))
    if big.equal(a, zero):
        return (zero,zero)
    quotient, remainder = dividePositive(big.half(a),b)
    quotient = big.twice(quotient)
    remainder = big.twice(remainder)
    if (not big.is_even(a)):
        remainder = incrementByOne(remainder)
    if big.greater_than(remainder, b) or big.equal(remainder, b):
        remainder = big.add(remainder, big.negate(b))
        quotient = incrementByOne(quotient)
    return (quotient, remainder)

def divideDifferentSigns(a, b):
    if not big.equal(b, bytearray(len(b))):
        return big.negate(incrementByOne(a))
    else:
        return big.negate(a)

def incrementByOne(number):
    return big.add(number, big.int2bytearray(1, len(number)))



class IntArithmetic(unittest.TestCase):

    # START Unit Tests for Problem 1
    def testDividePositive1(self):
        print("Positive Division Test 1:")
        a = big.int2bytearray(120, 8)
        b = big.int2bytearray(4, 8)
        c = divide(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "/" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "/", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, 120/4)

    def testDividePositive2(self):
        print("Positive Division Test 2:")
        a = big.int2bytearray(47, 8)
        b = big.int2bytearray(5, 8)
        c = divide(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "/" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "/", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, 47/5)
    # END Unit Tests for Problem 1

    # START Unit Tests for Problem 2
    def testDivideNegative1(self):
        print("Negative Division Test 1:")
        a = big.int2bytearray(-5, 8)
        b = big.int2bytearray(4, 8)
        c = divide(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "/" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "/", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, -5/4)

    def testDivideNegative2(self):
        print("Negative Division Test 2:")
        a = big.int2bytearray(8, 8)
        b = big.int2bytearray(-4, 8)
        c = divide(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "/" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "/", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, 8/-4)

    def testDivideNegative3(self):
        print("Negative Division Test 3:")
        a = big.int2bytearray(-6, 8)
        b = big.int2bytearray(3, 8)
        c = divide(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "/" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "/", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, -6/3)

    def testDivideNegative4(self):
        print("Negative Division Test 4:")
        a = big.int2bytearray(-15, 8)
        b = big.int2bytearray(-5, 8)
        c = divide(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "/" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "/", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, -15/-5)
    # END Unit Tests for Problem 2

    # START Unit Tests for Problem 3
    def testDivideSignExt1(self):
        print("Sign Extension Division Test 1:")
        a = big.int2bytearray(1234567890)
        b = big.int2bytearray(2)
        c = divide(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "/" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "/", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, 1234567890/2)
    # END Unit Tests for Problem 3

    # START Unit Tests for Problem 4
    def testModulo1(self):
        print("Modulo Test 1:")
        a = big.int2bytearray(7, 8)
        b = big.int2bytearray(3, 8)
        c = modulo(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "%" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "%", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, 7 % 3)

    def testModulo2(self):
        print("Modulo Test 2:")
        a = big.int2bytearray(-98, 8)
        b = big.int2bytearray(-17, 8)
        c = modulo(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "%" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "%", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, -98 % -17)
    # END Unit Tests for Problem 4

    # START Unit Tests for Problem 5
    def testModulo3(self):
        print("Modulo Test 3:")
        a = big.int2bytearray(-3, 8)
        b = big.int2bytearray(4, 8)
        c = modulo(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "%" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "%", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, -3%4)

    def testModulo4(self):
        print("Modulo Test 4:")
        a = big.int2bytearray(3, 8)
        b = big.int2bytearray(-4, 8)
        c = modulo(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "%" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "%", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, 3%-4)

    def testModulo5(self):
        print("Modulo Test 5:")
        a = big.int2bytearray(1234567890)
        b = big.int2bytearray(2)
        c = modulo(a, b)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(big.bytearray2int(a)) + "%" + str(big.bytearray2int(b)) + "=" + str(ans)
        print(printstatement)
        # print("\n", big.bytearray2int(a), "%", big.bytearray2int(b), "=", ans)
        self.assertEqual(ans, 1234567890%2)
    # END Unit Tests for Problem 5

    # START Unit Tests for Problem 6
    def testExpMod1(self):
        print("Exponential Modulo Test 1:")
        a = 5
        aArray = big.int2bytearray(5, 8)

        b = 756
        bArray = big.int2bytearray(756, 8)

        n = 25
        nArray = big.int2bytearray(25, 8)

        c = moduloExp(aArray, bArray, nArray)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(a) + "^" + str(b) + "%" + str(n) + "=" + str(ans)
        print(printstatement)
        # print("\n", a, "^", b, "%", n, "=", ans)
        self.assertEqual(ans, pow(a, b, n))

    def testExpMod2(self):
        print("Exponential Modulo Test 2:")
        a = 9
        aArray = big.int2bytearray(9, 8)

        b = 3
        bArray = big.int2bytearray(3, 8)

        n = 4
        nArray = big.int2bytearray(4, 8)

        c = moduloExp(aArray, bArray, nArray)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(a) + "^" + str(b) + "%" + str(n) + "=" + str(ans)
        print(printstatement)
        # print("\n", a, "^", b, "%", n, "=", ans)
        self.assertEqual(ans, pow(a, b, n))

    def testExpMod3(self):
        print("Exponential Modulo Test 3:")
        a = 12
        aArray = big.int2bytearray(12, 8)

        b = 17
        bArray = big.int2bytearray(17, 8)

        n = 7
        nArray = big.int2bytearray(7, 8)

        c = moduloExp(aArray, bArray, nArray)
        ans = big.bytearray2int(c)
        printstatement = "\n" + str(a) + "^" + str(b) + "%" + str(n) + "=" + str(ans)
        print(printstatement)
        # print("\n", a, "^", b, "%", n, "=", ans)
        self.assertEqual(ans, pow(a, b, n))
    # END Unit Tests for Problem 6

if __name__ == '__main__':
    unittest.main()