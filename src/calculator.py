from .Matrix import Matrix
from .my_algorithms import my_gcd, my_abs, my_range, my_reversed


def frac_add(frac_a, frac_b):
    """Return the sum of fractions frac_a and frac_b."""
    if frac_a[1] == frac_b[1]:
        return (frac_a[0] + frac_b[0], frac_a[1])

    numerator = frac_a[0] * frac_b[1] + frac_b[0] * frac_a[1]
    denominator = frac_a[1] * frac_b[1]
    return (numerator, denominator)


def frac_sub(frac_a, frac_b):
    """Return the difference of fractions frac_a and frac_b."""
    if frac_a[1] == frac_b[1]:
        return (frac_a[0] - frac_b[0], frac_a[1])

    numerator = frac_a[0] * frac_b[1] - frac_b[0] * frac_a[1]
    denominator = frac_a[1] * frac_b[1]
    return (numerator, denominator)


def frac_mult(frac_a, frac_b):
    """Return the product of fractions frac_a and frac_b."""
    numerator = frac_a[0] * frac_b[0]
    denominator = frac_a[1] * frac_b[1]
    return (numerator, denominator)


def frac_div(frac_a, frac_b):
    """Return frac_a divided by frac_b."""
    numerator = frac_a[0] * frac_b[1]
    denominator = frac_a[1] * frac_b[0]
    return (numerator, denominator)


def frac_abs(frac):
    """Return the absolute value of fraction frac."""
    return (my_abs(frac[0]), my_abs(frac[1]))


def frac_ge(frac_a, frac_b):
    """Return true, if frac_a is greater than frac_b"""
    return frac_a[0] * frac_b[1] > frac_b[0] * frac_a[1]


def frac_reduc(frac):
    """Reduce the given fraction."""
    syt = my_gcd(frac[0], frac[1])

    # This condition here ensures we don't end up dividing by 0. Namely, in
    # Python gcd(0, 0) == 0.
    if syt == 0:
        syt = 1

    return (int(frac[0] / syt), int(frac[1] // syt))


def matrixAddition(A, B):
    """Add matrix B to matrix A if the sum matrix is defined."""

    if not A or not B:
        return None
    # Addition undefined.
    if A.getColAmount() != B.getColAmount():
        return None
    # Addition undefined.
    if A.getRowAmount() != B.getRowAmount():
        return None

    # Resulting matrix.
    C = []
    for rowIndex in my_range(A.getRowAmount()):
        resultRow = []
        for colIndex in my_range(A.getColAmount()):
            cellOfA = A.getCell(rowIndex, colIndex)
            cellOfB = B.getCell(rowIndex, colIndex)
            result = frac_add(cellOfA, cellOfB)
            resultRow.append(frac_reduc(result))
        C.append(resultRow)

    return Matrix(C, A.getRowAmount(), A.getColAmount())


def matrixSubstraction(A, B):
    """Substract matrix B from A if the difference is defined."""

    if not A or not B:
        return None

    # A very special case that should never happen (except in my tests).
    if A == B:
        # Return a zero matrix of the same size as A (and B).
        return Matrix(
            [[(0, 1) for i in my_range(A.getColAmount())]
             for j in my_range(A.getRowAmount())],
            A.getRowAmount(),
            A.getColAmount())

    # Multiply B by a scalar of -1. This is because A-B == A+(-1*B).
    B.multiplyScalar(-1)
    resultMatrix = matrixAddition(A, B)

    # Set B's scalar back to original.
    B.multiplyScalar(-1)

    return resultMatrix


def matrixScalarMultiplication(A, scalar):
    """Multiply a matrix by a scalar."""
    A.multiplyScalar(scalar)
    return A


def matrixMultiplication(A, B):
    """Multiply two matrices if the product is defined."""

    if not A or not B:
        return None
    # Multiplication is undefined if this condition holds.
    if A.getColAmount() != B.getRowAmount():
        return None

    n = A.getRowAmount()
    m = A.getColAmount()
    p = B.getColAmount()

    # This will be the result matrix.
    C = [[(0, 1) for i in my_range(p)] for j in my_range(n)]

    for i in my_range(n):
        for j in my_range(p):
            cellValue = (0, 1)

            for k in my_range(m):
                toAdd = frac_mult(A.getCell(i, k), B.getCell(k, j))
                cellValue = frac_add(cellValue, toAdd)

            cellValue = frac_reduc(cellValue)
            C[i][j] = cellValue

    return Matrix(C, n, p)


def matrixTranspose(A):
    """Calculate the transpose of matrix A."""
    n = A.getRowAmount()
    m = A.getColAmount()
    result = [[A.getCell(j, i) for j in my_range(n)] for i in my_range(m)]
    return Matrix(result, m, n)


def __pivot(A):
    """Pivot A so that largest element of each column is on the diagonal.

    More specifically, A is modified so that every diagonal element has a value
    that is has at least as large absolute value as every cell below it."""
    n = A.getRowAmount()

    # At first, P is the identity matrix.
    P = [[(int(i == j), 1) for i in my_range(n)] for j in my_range(n)]

    # Needed for calculating the determinant of P.
    totalPivots = 0

    # Iterate through columns.
    for j in my_range(n):
        greatest = (0, 1)
        swapWith = j

        # We don't have to care about column values above the diagonal.
        for row in my_range(j+1, n):
            if frac_ge(frac_abs(A.getCell(row, j)), greatest):
                greatest = frac_abs(A.getCell(row, j))
                swapWith = row

        # True if we need to swap rows.
        if swapWith != j:
            # Swap rows so that the greatest element is now on the diagonal.
            P[j], P[swapWith] = P[swapWith], P[j]
            totalPivots += 1

    return (Matrix(P, n, n), totalPivots)


def __LUP_decomposition(A):
    """Calculate the LUP decomposition of A."""
    n = A.getRowAmount()

    # Format L and U as the zero matrix. Note that we are dealing with fractions
    # here for 100% accuracy.
    L = [[(0, 1) for i in my_range(n)] for j in my_range(n)]
    U = [[(0, 1) for i in my_range(n)] for j in my_range(n)]

    pivot_info = __pivot(A)
    P = pivot_info[0]

    # Set mult equal to the determinant of P.
    mult = (-1) ** pivot_info[1]

    Prod = matrixMultiplication(P, A)

    # We use the general algorithm described here:
    # https://rosettacode.org/wiki/LU_decomposition to calculate cell values for
    # U and L. There is a summation formula given for U_ij and L_ij, which is
    # implemented here.
    for j in my_range(n):
        # Calculate U[i][j].
        for i in my_range(j+1):
            the_sum = (0, 1)

            for k in my_range(i):
                toAdd = frac_mult(U[k][j], L[i][k])
                the_sum = frac_add(the_sum, toAdd)

            the_sum = frac_reduc(the_sum)
            # U_ij == Prod_ij - the_sum
            U[i][j] = frac_sub(Prod.getCell(i, j), the_sum)

        # Calculate L[i][j].
        for i in my_range(j, n):
            the_sum = (0, 1)

            for k in my_range(j):
                toAdd = frac_mult(L[i][k], U[k][j])
                the_sum = frac_add(the_sum, toAdd)

            the_sum = frac_reduc(the_sum)
            L[i][j] = frac_sub(Prod.getCell(i, j), the_sum)
            L[i][j] = frac_div(L[i][j], U[j][j])

    L = Matrix(L, n, n)
    U = Matrix(U, n, n)

    return (L, U, P, mult)


def matrixDeterminant(A):
    """Calculate the determinant of matrix A."""

    # Determinant is undefined for non-square matrices.
    if A.getRowAmount() != A.getColAmount():
        return None

    # Decompose the matrix. Return value is (L, U, P, mult).
    decomposition = __LUP_decomposition(A)

    U = decomposition[1]

    # The determinant is the product of U's diagonal values.
    ans = (1, 1)
    for i in my_range(U.getRowAmount()):
        ans = frac_mult(ans, U.getCell(i, i))
        ans = frac_reduc(ans)

    # If the determinant is zero, ans[1] might also be zero so we treat this
    # case separately.
    if ans[1] == 0:
        return 0

    det_of_P = decomposition[3]
    det = ans[0] * det_of_P * 1.0 / ans[1]
    if det // 1 == det:
        return int(det)
    return det


def __forward_substitution(L):
    """Invert L using forward substitution.

    For more information, see for example
    http://en.wikipedia.org/wiki/Triangular_matrix#Forward_and_back_substitution
    """
    m = L.getRowAmount()
    inverse = [[(0, 1) for i in my_range(m)] for j in my_range(m)]

    # bVector is the a:th column of the identity matrix. Solve the a:th column
    # of the inverse of L.
    for a in my_range(m):
        bVector = [(0, 1) for i in my_range(m)]
        bVector[a] = (1, 1)

        # This will be the a:th column of the inverse matrix of L.
        xVector = []
        for x in my_range(m):
            # Calculate the summation of x_index using the formula given for x_m
            # in the article above.
            the_sum = (0, 1)

            for i in my_range(x):
                toAdd = frac_mult(L.getCell(x, i), xVector[i])
                the_sum = frac_add(the_sum, toAdd)

            the_sum = frac_reduc(the_sum)
            value = frac_sub(bVector[x], the_sum)
            value = frac_mult(value, L.getCell(x, x))
            value = frac_reduc(value)
            xVector.append(value)

        # xVector is now the a:th column of L's inverse.
        for i in my_range(m):
            inverse[i][a] = xVector[i]

    return Matrix(inverse, m, m)


def __backward_substitution(U):
    """Invert U using backward substitution.

    This is basically the same as forward substitution, but done working
    backwards."""
    m = U.getRowAmount()
    inverse = [[(0, 1) for i in my_range(m)]
               for j in my_range(m)]

    for a in my_range(m):
        bVector = [(0, 1) for i in my_range(m)]
        bVector[a] = (1, 1)

        xVector = []
        for x in my_reversed(my_range(m)):
            the_sum = (0, 1)

            for i in my_reversed(my_range(x+1, m)):
                toAdd = frac_mult(U.getCell(x, i), xVector[m-1 - i])
                the_sum = frac_add(the_sum, toAdd)

            the_sum = frac_reduc(the_sum)
            value = frac_sub(bVector[x], the_sum)
            value = frac_div(value, U.getCell(x, x))
            value = frac_reduc(value)
            xVector.append(value)

        for i in my_range(m):
            inverse[m-1-i][a] = xVector[i]

    return Matrix(inverse, m, m)


def matrixInverse(A):
    """Invert matrix A."""
    # Inverse not defined iff the determinant is zero.
    if matrixDeterminant(A) == 0:
        return None

    # Calculate the LUP decomposition of A. PA = LU
    decomposition = __LUP_decomposition(A)

    # Invert L using forward substitution.
    L_inv = __forward_substitution(decomposition[0])
    # Invert U using forward substitution.
    U_inv = __backward_substitution(decomposition[1])

    P = decomposition[2]

    # PA = LU
    # -> (PA)^-1 = (LU)^-1
    # -> A^-1 * P^-1 = U^-1 * L^-1
    # -> A^-1 = U^-1 * L^-1 * P
    C = matrixMultiplication(U_inv, L_inv)
    return matrixMultiplication(C, P)
