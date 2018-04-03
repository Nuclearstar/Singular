from .my_algorithms import my_split, my_strip, my_lower
from .calculator import frac_reduc
from .Matrix import Matrix
import sys

# Make everything work with python2.
if sys.version_info[0] == 2:
    input = raw_input


def __ask_input(string):
    """Ask input from user with 'string'."""
    try:
        input_data = input(string)
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
        sys.exit(0)
    return input_data


def __is_number(n):
    """Find out if a given argument is a number or not."""
    try:
        # Strings for example, can be converted to floats if the string is of
        # the correct form.
        float(n)
        return True
    except:
        return False


def __parse_float(string):
    """Try parsing a float from string."""
    elem = my_split(string, ".")

    # String is not of the form of 4389.109903.
    if len(elem) == 1:
        elem = my_split(string, ",")

    # String is of the form 1234.5678 or 1234,5678.
    if len(elem) == 2:
        # The whole part or the decimal part is not a number.
        if not (__is_number(elem[0])) or not (__is_number(elem[1])):
            return None

        numerator = int(elem[0]) * 10 ** len(elem[1])
        if numerator >= 0:
            numerator += int(elem[1])
        else:
            numerator -= int(elem[1])

        denominator = 10 ** len(elem[1])
        frac = (numerator, denominator)

        return frac_reduc(frac)

    return None


def __parse_fraction(string):
    """Parse a fraction from a string. Return none if input's not a fraction."""
    elem = my_split(string, "/")

    if len(elem) == 2:
        # Do things this weirdly just to handle the case where user gives a
        # value in the form 1.3/3,7.
        frac_1 = __parse_float(elem[0])
        frac_2 = __parse_float(elem[1])

        if not frac_1:
            if not __is_number(elem[0]):
                return None
            frac_1 = (int(elem[0]), 1)

        if not frac_2:
            if not __is_number(elem[1]):
                return None
            frac_2 = (int(elem[1]), 1)

        numerator = frac_1[0] * frac_2[1]
        denominator = frac_1[1] * frac_2[0]
        frac = (numerator, denominator)
        return frac_reduc(frac)

    return None


def __parse_values(row):
    """Parse numbers from a string into a list."""
    values = []
    args = my_split(row, " ")

    for i in range(len(args)):
        elem = __parse_fraction(args[i])

        if not elem:                      # elem is not a fraction
            elem = __parse_float(args[i])

        if not elem:                      # elem is not a float nor a fraction
            if not __is_number(args[i]):  # elem is not even a whole number
                return None
            elem = (int(args[i]), 1)

        values.append(elem)

    return values


def parseMatrix():
    """Ask user to input a matrix and return a new Matrix object."""

    rows = []

    print("")
    print("Input a matrix row by row. Plain enter stops.")

    row = my_strip(__ask_input("row: "))

    # Loop until an empty row is encountered.
    while row:
        newRow = __parse_values(row)

        # User inputs an invalid argument.
        if not newRow:
            print("")
            print("You inputted an invalid argument. Don't do that.")
            print("Please, input the row correctly.")
            print("Only integers, fractions and floats (decimals) "
                  "are accepted. No parenthesis please.")

        # User gives more values than there is in the first row.
        elif len(rows) > 0 and len(newRow) != len(rows[0]):
            print("")
            print("You inputted an invalid amount of numbers.")
            print("Please, input the row correctly.")

        else:
            rows.append(newRow)

        row = my_strip(__ask_input("row: "))

    # No rows given.
    if len(rows) == 0:
        return None

    ret = Matrix(rows, len(rows), len(rows[0]))
    return ret


def parseOperator():
    """Ask user, which operation they would like to perform next."""

    print("")

    print("Which operation you'd like to perform next?")
    
    print("")

    print("det:       Calculate the determinant of the current matrix.")
    print("inverse:   Invert the given matrix if possible.")
    
    print("print:     Print the current matrix.")

    print("")

    operator = my_lower(my_strip(__ask_input("Operator: ")))
    while operator not in ["det",
                           "inverse",
                           "invert",  # Alternative inputs for inversion.
                           "-1",      #
                           "print",
                           ]:
        print("Please choose a valid operator.")
        operator = my_lower(my_strip(__ask_input("Operator: ")))

    return operator


def askToContinue():
    """Ask the user to continue performing operations on the current matrix."""

    print("")
    print("Do you want to apply more options to the current matrix?")

    a = my_lower(__ask_input("Y/N: "))
    print("")

    while(a != "y" and a != "n"):
        a = my_lower(__ask_input("Y/N: "))

    if a == "y":
        return True
    return False
