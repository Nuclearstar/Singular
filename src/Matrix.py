from .my_algorithms import my_range


class Matrix:
    """Matrix object"""

    def __init__(self, rows, n, m):
        """Construct a matrix.

        Keyword arguments:
        rows -- the list of rows in the matrix
        n    -- the number of rows in the matrix
        m    -- the number of column in the matrix
        """
        self.rowAmount = n
        self.colAmount = m
        self.rowArray = rows
        self.colArray = [[] for i in my_range(n)]
        self.scalar = 1

    def __str__(self):
        """Print the matrix in a readable format"""
        output = ""

        for row in self.rowArray:
            output += "["

            for i in my_range(len(row)):
                cell = row[i]
                elem = self.scalar * 1.0 * cell[0] / cell[1]

                if elem % 1 == 0:
                    elem = int(elem)

                if i == len(row) - 1:
                    output += str(elem)
                else:
                    output += str(elem) + " "

            output += "]\n"
        return output[:-1]

    def multiplyScalar(self, n):
        """Multiply the current scalar value.

        self.scalar handles the scalar multiplication of the matrix. Each time
        a value(s) is returned via a getter, the returned values have to be
        multiplied by the scalar.
        """
        self.scalar *= n

    def getRowAmount(self):
        """Return the amount of rows.

        This is needed mainly for testing purposes."""
        return self.rowAmount

    def getRowArray(self):
        """Return the row array.

        This is needed mainly for testing purposes."""
        if self.scalar == 1:
            return self.rowArray
        returnArray = [[self.scalar * elem for elem in row]
                       for row in self.rowArray]
        return returnArray

    def getColAmount(self):
        """Return the amount of columns.

        This is needed mainly for testing purposes."""
        return self.colAmount

    def getColArray(self):
        """Return the current column array.

        This is needed mainly for testing purposes"""
        return self.colArray

    def getScalar(self):
        """Return the current scalar value.

        This is needed mainly for testing purposes"""
        return self.scalar

    def getCell(self, row, col):
        """Return the content of the requested cell"""
        return (self.scalar * self.rowArray[row][col][0],
                self.rowArray[row][col][1])

    def getRow(self, row):
        """Return the requested row."""
        if self.scalar == 1:
            return self.rowArray[row]

        returnRow = [(self.scalar * elem[0], elem[1])
                     for elem in self.rowArray[row]]
        return returnRow

    def genColArray(self, col):
        """Generate only the requested column and store it in self.colArray.

        Generating only the needed column at a time keeps the worst case
        scenario at a reasonable O(m). As the same column vector is requested
        again, then getCol becomes O(1).
        """
        for i in my_range(self.rowAmount):
            self.colArray[col].append(self.rowArray[i][col])
        return self.colArray[col]

    def getCol(self, col):
        """Return the requested column of the matrix.

        If this is the first time requesting a column, the column must be first
        generated. Otherwise, we may just look the column up from self.colArray.
        """
        if len(self.colArray[col]) == 0:
            self.genColArray(col)

        if self.scalar == 1:
            return self.colArray[col]

        returnCol = [(self.scalar * elem[0], elem[1])
                     for elem in self.colArray[col]]
        return returnCol
