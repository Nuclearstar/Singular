# coding: utf-8
import sys

# Ensure Python 3 compatibility.
if sys.version_info[0] == 3:
    # unicode is not defined in Python 3. However, unicode is needed when
    # dealing with non-ascii characters in Python 2.
    unicode = str


def __is_number(n):
    """Find out if a given argument is a number or not."""
    return isinstance(n, float) or isinstance(n, int)


def __is_string(s):
    """Find out if a given argument is a string or not."""
    return isinstance(s, str) or isinstance(s, unicode)


def my_abs(n):
    """Calculate the absolute value of a given number."""
    if n < 0:
        return -n
    return n


def my_gcd(n, m):
    """Calculate the gcd of n and m using Stein's algorithm.

    For a description of Stein's algorithm, see for example
    https://en.wikipedia.org/wiki/Binary_GCD_algorithm
    """

    # Unit is needed to mimic the default Python implementation of gcd. Python
    # thinks that if m < 0, then the gcd shall be negative.
    unit = 1
    if m < 0:
        unit = -1
    n = my_abs(n)
    m = my_abs(m)

    # Base cases.
    if n == m == 0:
        return 0
    if n == 0:
        return unit * m
    if m == 0:
        return n
    if n == m:
        return unit * n

    # For convenience, make sure n is the bigger one of the two.
    if n < m:
        n, m = m, n

    # Exp is the largest power of two that divides both n and m.
    exp = 0
    # While n and m are both even, divide both by 2, and increment exp.
    while (n | m) & 1 == 0:
        n >>= 1
        m >>= 1
        exp += 1

    # Remove possible leftover factors of 2 from n. Hence n will be odd.
    while n & 1 == 0:
        n >>= 1

    while n != 0:
        # Here we ensure that n is always the bigger of the two. Thus n will be
        # positive until n == m.
        if n < m:
            n, m = m, n

        n -= m
        # N is even if m was odd, so remove any leftover factors of 2 from n.
        while n != 0 and n & 1 == 0:
            n >>= 1

    # At this point, n == 0 and hence gcd(n, m) == m. Multiply the resulting m
    # by 2^exp, which is also a common factor of the original n and m.
    return unit * (m << exp)


def my_max(x, *args):
    """Return the maximum of the given numbers or a given list."""

    # If x is a non-empty list, find the maximum value in it.
    if isinstance(x, list) and len(x) > 0:
        greatest = x[0]
        i = 0
        while i < len(x):
            # The list x must contain only numbers (floats and/or integeres.)
            if not (__is_number(x[i])):
                raise TypeError('Expected an integer or a float.')
            if x[i] > x[0]:
                greatest = x[i]
            i += 1
        return greatest

    # If x is a number, find the maximum of the given n-arguments.
    if __is_number(x):
        greatest = x
        i = 0
        # Iterate through the rest of the arguments given by the user.
        while i < len(args):
            # All arguments must be numbers.
            if not __is_number(args[i]):
                raise TypeError('Expected an integer or a float.')
            if args[i] > x:
                greatest = args[i]
            i += 1
        return greatest

    raise TypeError(
        'Expected a list of ints/floats, or a sequence of ints/floats')


def my_range(x, *args):
    """Return a list of integers, mimicing the default my_range() call."""
    # By default, the lower bound is zero.
    lower = 0
    # By default, the upper bound is x.
    upper = x

    # User gave two arguments i.e. user gave also a lower bound. Then x is the
    # lower-bound and the second argument (args[0]) is the upper bound.
    if len(args) == 1:
        lower = x
        upper = args[0]

    # Here we generate the my_range.
    ret = []
    i = lower
    while i < upper:
        ret.append(i)
        i += 1

    return ret


def my_reversed(x):
    """Reverse a list."""

    # Copy the elements of x to ret, starting from the end of x.
    ret = []
    i = len(x) - 1
    while i >= 0:
        ret.append(x[i])
        i -= 1
    return ret


def my_split(s, char):
    """Split string into a list by treating char as a separator."""
    if not __is_string(s):
        raise TypeError('Expected a string.')

    result = []
    current_string = ""
    for i in my_range(len(s)):
        # i:s character of s
        c = s[i]
        # If c is the separator character char, append current_string to the
        # result list.
        if c == char:
            result.append(current_string)
            current_string = ""
            continue
        # c is not the separator char, so we append c to current_string
        current_string += c
    # Done iterating through s. Add the last string to result.
    result.append(current_string)
    return result


def my_strip(s):
    """Remove spaces from the beginning and ending of a string."""
    if not __is_string(s):
        raise TypeError('Expected a string.')

    # Find the first non-space character and let i be its index.
    i = 0
    while i < len(s) and s[i] == ' ':
        i += 1

    # Find the last non-space character and let j be its index.
    j = len(s) - 1
    while j >= 0 and s[j] == ' ':
        j -= 1

    # The result will be the substring s[i] + ... + s[j].
    result = ""
    for char in my_range(i, j+1):
        result += s[char]

    return result


def my_lower(s):
    """Convert uppercase letters of the Finnish alphabet into lowercase.

    This is done lazily so that I can avoid creating my own hash-map."""
    if not __is_string(s):
        raise TypeError('Expected a string.')

    uppers = u"ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    lowers = u"abcdefghijklmnopqrstuvwxyzåäö"

    result = ""
    # Iterate through the characters of s.
    for i in my_range(len(s)):
        char = s[i]
        # Compare char to uppercase letters.
        for j in my_range(len(uppers)):
            # Char is an uppercase letter, convert it to a lowercase one.
            if char == uppers[j]:
                char = lowers[j]
        result += char

    return result
