from .parser import parseMatrix, parseOperator, askToContinue
from .calculator import *
import sys

# Make this module python2 compatible.
if sys.version_info[0] == 2:
    input = raw_input


def __handle_operator(operator, matrix):
    """Perform user given operation on user given matrix."""

    # User wants to calculate the determinant.
    if operator == "det":
        ans = matrixDeterminant(matrix)
        if ans != 0 and not ans:
            print("Determinant not defined for the given matrix.")
        else:
            print("The determinant is: " + str(ans))

    # User wants to calculate the inverse.
    if operator == "inverse" or operator == "-1":
        matrix2 = matrixInverse(matrix)
        if not matrix2:
            print("Matrix not invertible.")
        else:
            matrix = matrix2
            print("Inversion successful.")

    # Print the result matrix to user.
    print(matrix)
    return matrix


def main():
    """Wrap all things together."""

    # Ask 1st matrix.
    matrix = parseMatrix()

    # Perform matrix operations. Stop when no matrix is None
    while matrix:
        # Ask which operation the user wants to perform 
        operator = parseOperator()

        # Perform the operation on matrix.
        matrix = __handle_operator(operator, matrix)

        userWantsToContinueWithCurrentMatrix = askToContinue()
        if not userWantsToContinueWithCurrentMatrix:
            # Ask for a new matrix. If user inputs no rows, matrix is None and
            # the program will halt.
            matrix = parseMatrix()

    print("")
    print("Bye!")
