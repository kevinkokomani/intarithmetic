#! /usr/bin/python

# Professor Dimitri Lisin
import unittest
import math


####################################################################
# Functions for converting between python integers and integers
# stored in bytearrays.
def int2bytearray(val, nbytes=-1):
    if val < 0:
        val = -val
        sign = -1
    else:
        sign = 1

    if nbytes == -1:
        nbytes = int(math.ceil(math.log(val, 2)) / 8) + 1

    array = bytearray(nbytes)
    for i in range(nbytes - 1, -1, -1):
        remainder = val % 256
        val = val / 256
        array[i] = remainder

    if sign == -1:
        negate_in_place(array)

    return array


def bytearray2int(input_array):
    temp_array = bytearray(len(input_array))
    temp_array[:] = input_array
    sign = 1
    if is_negative(temp_array):
        negate_in_place(temp_array)
        sign = -1

    val = 0
    factor = 1
    for i in range(len(temp_array) - 1, -1, -1):
        val += temp_array[i] * factor
        factor *= 256
    return sign * val


###############################################################
# Arithmetic functions for integers represented as bytearrays.

def is_negative(array):
    return get_highest_bit(array[0]) != 0


def negate(array):
    output = bytearray(len(array))
    output[:] = array
    negate_in_place(output)
    return output


def sign_extend(array, nbytes=1):
    # Extend the number by nbytes bytes.
    pad = bytearray(nbytes)
    if is_negative(array):
        for i in range(len(pad)):
            pad[i] = 0xff

    output = pad + array
    return output


def make_same_size(a, b):
    if len(a) < len(b):
        a_pad = sign_extend(a, len(b) - len(a))
    else:
        a_pad = bytearray(len(a))
        a_pad[:] = a

    if len(b) < len(a):
        b_pad = sign_extend(b, len(a) - len(b))
    else:
        b_pad = bytearray(len(b))
        b_pad[:] = b

    return [a_pad, b_pad]


def add(a, b):
    [a_pad, b_pad] = make_same_size(a, b)
    c = add_aux(a_pad, b_pad)
    if (not is_negative(a) and not is_negative(b) and is_negative(c)) or \
            (is_negative(a) and is_negative(b) and not is_negative(c)):
        a_pad = sign_extend(a_pad)
        b_pad = sign_extend(b_pad)
        c = add_aux(a_pad, b_pad)

    return c


def equal(a, b):
    [a_pad, b_pad] = make_same_size(a, b)
    for i in range(len(a_pad)):
        if a_pad[i] != b_pad[i]:
            return False
    return True


def greater_than(a, b):
    [a_pad, b_pad] = make_same_size(a, b)
    if is_negative(a_pad) and is_negative(b_pad):
        return greater_negative(a_pad, b_pad)
    elif not is_negative(a_pad) and not is_negative(b_pad):
        return greater_positive(a_pad, b_pad)
    elif is_negative(b_pad):
        return True
    else:
        return False


def less_than(a, b):
    return not equal(a, b) and not greater_than(a, b)


def is_even(array):
    return get_lowest_bit(array[-1]) == 0


def half(array):
    if is_negative(array):
        output = negate(array)
        if is_even(output):
            return negate(half_positive(output))
        else:
            return add(negate(half_positive(output)), int2bytearray(-1, len(output)))
    else:
        return half_positive(array)


def twice(array):
    if is_negative(array):
        return negate(twice_positive(negate(array)))
    else:
        return twice_positive(array)


def multiply(a, b):
    if len(a) < len(b):
        a_pad = sign_extend(a, len(b) - len(a))
    else:
        a_pad = a

    if len(b) < len(a):
        b_pad = sign_extend(b, len(a) - len(b))
    else:
        b_pad = b

    if is_negative(a_pad) and is_negative(b_pad):
        return multiply_positive(negate(a_pad), negate(b_pad))
    elif is_negative(a_pad):
        return negate(multiply_positive(negate(a_pad), b_pad))
    elif is_negative(b_pad):
        return negate(multiply_positive(a_pad, negate(b_pad)))
    else:
        return multiply_positive(a_pad, b_pad)


#############################################################
# Helper functions

def add_aux(a, b):
    c = bytearray(len(a))
    carry = 0
    for i in range(len(a) - 1, -1, -1):
        val = a[i] + b[i] + carry
        c[i] = val & 0xff
        carry = val >> 8

    return c


def greater_positive(a, b):
    for i in range(len(a)):
        if a[i] > b[i]:
            return True
        elif a[i] < b[i]:
            return False


def greater_negative(a, b):
    a_mag = negate(a)
    b_mag = negate(b)
    return greater_positive(b_mag, a_mag)


def get_lowest_bit(byte):
    return byte & 0x01


def get_highest_bit(byte):
    return byte & 0x80


def half_positive(array):
    output = bytearray(len(array))
    carry = 0

    for i in range(0, len(array)):
        val = array[i]
        output[i] = (val >> 1) + carry
        carry = (get_lowest_bit(val) << 7) & 0xff

    return output


def twice_positive(array):
    # Check for overflow. The 0th bit is the sign bit,
    # which we assume to be 0 in this case. Thus twice()
    # will overflow, if the 1st bit 1.
    if array[0] & 0x40:
        return twice_positive_impl(sign_extend(array))
    else:
        return twice_positive_impl(array)


def twice_positive_impl(array):
    output = bytearray(len(array))
    carry = 0
    for i in range(len(array) - 1, -1, -1):
        val = ((array[i] << 1) + carry)
        carry = val >> 8
        output[i] = val & 0xff

    return output


def multiply_positive(x, y):
    zero = bytearray(len(x))
    if equal(y, zero):
        return zero

    z = multiply_positive(x, half(y))
    if is_even(y):
        return twice(z)
    else:
        return add(x, twice(z))


def negate_in_place(array):
    for i in range(len(array)):
        array[i] = ~array[i] & 0xff

    val = array[-1] + 1
    array[-1] = val & 0xff
    carry = val >> 8

    for i in range(len(array) - 2, -1, -1):
        val = array[i] + carry
        array[i] = val & 0xff
        carry = val >> 8


##############################################
# Tests

class TestIntToBytearray(unittest.TestCase):
    def test0(self):
        nbytes = 4
        b = int2bytearray(0, nbytes)
        for i in range(len(b)):
            self.assertEqual(b[i], 0)

    def test5(self):
        nbytes = 4
        b = int2bytearray(5, nbytes)
        self.assertEqual(b[nbytes - 1], 5)

    def test256(self):
        nbytes = 4
        b = int2bytearray(256, nbytes)
        self.assertEqual(b[nbytes - 1], 0)
        self.assertEqual(b[nbytes - 2], 1)

    def testAutosize5(self):
        b = int2bytearray(5)
        self.assertEqual(len(b), 1)
        self.assertEqual(bytearray2int(b), 5)

    def testAutosize729(self):
        b = int2bytearray(729)
        self.assertEqual(len(b), 2)
        self.assertEqual(bytearray2int(b), 729)


##############################################
class TestBytearrayToInt(unittest.TestCase):
    def test0(self):
        nbytes = 4
        array = bytearray(nbytes)
        val = bytearray2int(array)
        self.assertEqual(val, 0)

    def test5(self):
        nbytes = 4
        array = bytearray(nbytes)
        array[nbytes - 1] = 5;
        val = bytearray2int(array)
        self.assertEqual(val, 5)

    def test256(self):
        nbytes = 4
        array = bytearray(nbytes)
        array[nbytes - 2] = 1;
        val = bytearray2int(array)
        self.assertEqual(val, 256)


##############################################
class TestNegation(unittest.TestCase):
    def test0(self):
        array = bytearray(4)
        negate_in_place(array)
        self.assertEqual(bytearray2int(array), 0)

    def testNeg5(self):
        nbytes = 4
        array = int2bytearray(5, nbytes)
        negate_in_place(array)
        self.assertEqual(bytearray2int(array), -5)

    def testNeg50000(self):
        nbytes = 4
        array = int2bytearray(50000, nbytes)
        negate_in_place(array)
        self.assertEqual(bytearray2int(array), -50000)

    def testCreateNegativeArray(self):
        nbytes = 4
        array = int2bytearray(-50000, nbytes)
        self.assertTrue(is_negative(array))
        self.assertEqual(bytearray2int(array), -50000)


##############################################
class TestAddition(unittest.TestCase):
    def test0and0(self):
        a = bytearray(4)
        b = bytearray(4)
        c = add(a, b)
        self.assertEqual(bytearray2int(c), 0)

    def test10and5(self):
        nbytes = 4
        a = int2bytearray(10, nbytes)
        b = int2bytearray(5, nbytes)
        c = add(a, b)
        self.assertEqual(bytearray2int(c), 15)

    def testBigNumbers(self):
        nbytes = 4
        x = 50000
        y = 60729
        a = int2bytearray(x, nbytes)
        b = int2bytearray(y, nbytes)
        c = add(a, b)
        self.assertEqual(bytearray2int(c), x + y)

    def testAddNegative(self):
        nbytes = 4
        x = 50000
        y = -60729
        a = int2bytearray(x, nbytes)
        b = int2bytearray(y, nbytes)
        c = add(a, b)
        self.assertEqual(bytearray2int(c), x + y)

    def testPositiveOverflow(self):
        nbytes = 4
        a = bytearray(nbytes)
        b = bytearray(nbytes)
        a[0] = 0x7f
        b[0] = 0x7f
        for i in range(1, len(a)):
            a[i] = 0xff
            b[i] = 0xff
        c = add(a, b)
        self.assertFalse(is_negative(c))
        self.assertEqual(len(c), len(a) + 1)

    def testSignExtension(self):
        nbytes = 4
        a = int2bytearray(-5, nbytes)
        b = sign_extend(a)
        self.assertEqual(bytearray2int(a), bytearray2int(b))
        self.assertEqual(len(b), len(a) + 1)

    def testNegativeOverflow(self):
        nbytes = 2
        val = -32768
        a = int2bytearray(val, nbytes)
        b = int2bytearray(val, nbytes)

        self.assertTrue(is_negative(a))
        self.assertTrue(is_negative(b))

        c = add(a, b)
        self.assertTrue(is_negative(c))
        self.assertEqual(len(c), len(a) + 1)

    def testAddDifferentSizes(self):
        val = 32767
        a = int2bytearray(val, 2)
        b = int2bytearray(2 * val, 4)
        c = add(a, b)
        self.assertEqual(len(c), len(b))
        self.assertEqual(bytearray2int(c), 3 * val)

        c = add(b, a)
        self.assertEqual(bytearray2int(c), 3 * val)


##############################################
class TestEqual(unittest.TestCase):
    def test10and5(self):
        nbytes = 4
        a = int2bytearray(10, nbytes)
        b = int2bytearray(5, nbytes)
        self.assertFalse(equal(a, b))
        self.assertTrue(equal(a, a))

    def testDifferenceSizes(self):
        a = int2bytearray(5, 2)
        b = int2bytearray(5, 8)
        self.assertTrue(equal(a, b))


##############################################
class TestGreaterPositive(unittest.TestCase):
    def test10and5(self):
        nbytes = 4
        a = int2bytearray(10, nbytes)
        b = int2bytearray(5, nbytes)
        self.assertTrue(greater_positive(a, b))
        self.assertFalse(greater_positive(b, a))
        self.assertFalse(greater_positive(a, a))


##############################################
class TestGreaterNegative(unittest.TestCase):
    def testNeg10and5(self):
        nbytes = 4
        a = int2bytearray(-10, nbytes)
        b = int2bytearray(-5, nbytes)
        self.assertTrue(greater_negative(b, a))
        self.assertFalse(greater_negative(a, b))
        self.assertFalse(greater_negative(b, b))


##############################################
class TestGreaterThan(unittest.TestCase):
    def testPositives(self):
        nbytes = 4
        a = int2bytearray(10, nbytes)
        b = int2bytearray(5, nbytes)
        self.assertTrue(greater_than(a, b))
        self.assertFalse(greater_than(b, a))
        self.assertFalse(greater_than(a, a))

    def testNegatives(self):
        nbytes = 4
        a = int2bytearray(-10, nbytes)
        b = int2bytearray(-5, nbytes)
        self.assertTrue(greater_than(b, a))
        self.assertFalse(greater_than(a, b))
        self.assertFalse(greater_than(b, b))

    def testMixedSigns(self):
        nbytes = 4
        a = int2bytearray(-10, nbytes)
        b = int2bytearray(5, nbytes)
        self.assertTrue(greater_than(b, a))
        self.assertFalse(greater_than(a, b))
        self.assertFalse(greater_than(b, b))

    def testDifferentSizes(self):
        a = int2bytearray(100)
        b = int2bytearray(48957655)
        self.assertFalse(greater_than(a, b))


##############################################
class TestLessThan(unittest.TestCase):
    def testPositives(self):
        nbytes = 4
        a = int2bytearray(10, nbytes)
        b = int2bytearray(5, nbytes)
        self.assertFalse(less_than(a, b))
        self.assertTrue(less_than(b, a))
        self.assertFalse(less_than(a, a))

    def testNegatives(self):
        nbytes = 4
        a = int2bytearray(-10, nbytes)
        b = int2bytearray(-5, nbytes)
        self.assertFalse(less_than(b, a))
        self.assertTrue(less_than(a, b))
        self.assertFalse(less_than(b, b))

    def testMixedSigns(self):
        nbytes = 4
        a = int2bytearray(-10, nbytes)
        b = int2bytearray(5, nbytes)
        self.assertFalse(less_than(b, a))
        self.assertTrue(less_than(a, b))
        self.assertFalse(less_than(b, b))


##############################################
class TestIsEven(unittest.TestCase):
    def test4(self):
        nbytes = 8
        a = int2bytearray(4, nbytes)
        self.assertTrue(is_even(a))

    def test3(self):
        nbytes = 8
        a = int2bytearray(3, nbytes)
        self.assertFalse(is_even(a))


##############################################
class TestHalf(unittest.TestCase):
    def test4(self):
        nbytes = 1
        a = int2bytearray(4, nbytes)
        self.assertFalse(is_negative(a))
        b = half(a)
        self.assertEqual(bytearray2int(b), 2)

    def test500(self):
        nbytes = 16
        a = int2bytearray(500, nbytes)
        b = half(a)
        self.assertEqual(bytearray2int(b), 250)

    def test501(self):
        nbytes = 16
        a = int2bytearray(501, nbytes)
        b = half(a)
        self.assertEqual(bytearray2int(b), 250)

    def testNeg4(self):
        nbytes = 16
        a = int2bytearray(-4, nbytes)
        b = half(a)
        self.assertEqual(bytearray2int(b), -2)

    def testNeg5(self):
        nbytes = 16
        a = int2bytearray(-5, nbytes)
        b = half(a)
        self.assertEqual(bytearray2int(b), -3)


##############################################
class TestTwice(unittest.TestCase):
    def test4(self):
        nbytes = 1
        a = int2bytearray(4, nbytes)
        b = twice(a)
        self.assertEqual(bytearray2int(b), 8)

    def test250(self):
        nbytes = 16
        a = int2bytearray(250, nbytes)
        b = twice(a)
        self.assertEqual(bytearray2int(b), 500)

    def testNeg250(self):
        nbytes = 16
        a = int2bytearray(-250, nbytes)
        b = twice(a)
        self.assertEqual(bytearray2int(b), -500)

    def testOverflow(self):
        nbytes = 2
        val = 32767
        a = int2bytearray(val, nbytes)
        b = twice(a)
        self.assertEqual(len(b), 3)
        self.assertEqual(bytearray2int(b), 2 * val)


##############################################
class TestMultiply(unittest.TestCase):
    def testZero(self):
        nbytes = 4
        x = int2bytearray(729, nbytes)
        y = int2bytearray(0, nbytes)
        z = multiply(x, y)
        self.assertEqual(bytearray2int(z), 0)

    def testBigNumbers(self):
        nbytes = 4
        x = int2bytearray(729, nbytes)
        y = int2bytearray(927, nbytes)
        z = multiply(x, y)
        self.assertEqual(bytearray2int(z), 729 * 927)

    def testBigNegativeNumbers(self):
        nbytes = 4
        x = int2bytearray(-729, nbytes)
        y = int2bytearray(-927, nbytes)
        z = multiply(x, y)
        self.assertEqual(bytearray2int(z), -729 * -927)

    def testBigMixedNumbers1(self):
        nbytes = 4
        x = int2bytearray(-729, nbytes)
        y = int2bytearray(927, nbytes)
        z = multiply(x, y)
        self.assertEqual(bytearray2int(z), -729 * 927)

    def testBigMixedNumbers2(self):
        nbytes = 4
        x = int2bytearray(729, nbytes)
        y = int2bytearray(-927, nbytes)
        z = multiply(x, y)
        self.assertEqual(bytearray2int(z), -729 * 927)

    def testInfinitePrecision(self):
        nbytes = 2
        val = 32767
        x = int2bytearray(val, nbytes)
        y = int2bytearray(val, nbytes)
        z = multiply(x, y)
        self.assertEqual(bytearray2int(z), val * val)
        self.assertEqual(len(z), 4)

    def testDifferentSizes(self):
        a = 729
        b = 123456789
        x = int2bytearray(a)
        y = int2bytearray(b)
        c = multiply(x, y)
        self.assertEqual(bytearray2int(c), a * b)

        c = multiply(y, x)
        self.assertEqual(bytearray2int(c), b * a)


##############################################
if __name__ == '__main__':
    # run the unit tests
    unittest.main()
