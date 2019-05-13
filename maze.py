# Implements the Maze ADT using a 2-D array.
from arrays import Array2D
from lliststack import Stack


class Maze:
    '''Class for Maze representation.Defines constants to represent contents of the maze cells.'''
    MAZE_WALL = "  *"
    PATH_TOKEN = "  x"
    TRIED_TOKEN = "  o"

    def __init__(self, n_rows, n_cols):
        '''Creates a maze object with all cells marked as open.'''
        self._mazeCells = Array2D(n_rows, n_cols)
        self._startCell = None
        self._exitCell = None

    def num_rows(self):
        '''
        Returns the number of rows in the maze.
        :return: int
        '''
        return self._mazeCells.num_rows()

    def num_cols(self):
        '''
        Returns the number of columns in the maze.
        :return: int
        '''
        return self._mazeCells.num_cols()

    def setWall(self, row, col):
        '''
        Fills the indicated cell with a "wall" marker.
        :param row: int
        :param col: int
        :return: None
        '''
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._mazeCells[row, col] = self.MAZE_WALL

    def setStart(self, row, col):
        '''Sets the starting cell position.'''
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._startCell = _CellPosition(row, col)

    def setExit(self, row, col):
        '''Sets the exit cell position.'''
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._exitCell = _CellPosition(row, col)

    def inside_the_field(self, tup):
        '''
        Defines whether cell with tup coordinates is inseide the field.
        :param tup: tuple
        :return: bool
        '''
        return 0 <= tup[0] < self.num_rows() and 0 <= tup[1] < self.num_cols()

    def neighbours(self, tup):
        '''
        Returns all the horizontal and vertical neighbours for cell with coordinates tuple.
        :param tup: tuple
        :return: list
        '''
        # lst = [(tup[0], tup[1] + 1), (tup[0] + 1, tup[1]), (tup[0], tup[1] - 1), (tup[0] - 1, tup[1]),
        #        (tup[0] + 1, tup[1] - 1), (tup[0] - 1, tup[1] + 1), (tup[0] + 1, tup[1] + 1), (tup[0] - 1, tup[1] - 1)]
        lst = [(tup[0], tup[1] + 1), (tup[0] + 1, tup[1]), (tup[0], tup[1] - 1), (tup[0] - 1, tup[1])]
        neighbors = [el for el in lst if self.inside_the_field(el)]
        return neighbors

    def findPath(self):
        '''
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        :return: bool
        '''
        label = ""
        stack = Stack()
        stack1 = Stack()
        stack.push((self._startCell.row, self._startCell.col))
        while not stack.isEmpty():
            count = 0
            tup = stack.pop()
            if self._exitFound(tup[0], tup[1]):
                self._markPath(tup[0], tup[1])
                return True
            elif self._validMove(tup[0], tup[1]):
                self._markPath(tup[0], tup[1])
                stack1.push(tup)
                if label == "second_time":
                    self.neighbours(tup).pop()
                for el in self.neighbours(tup):
                    if self._validMove(el[0], el[1]):
                        stack.push(el)
                        count += 1
                if not count:
                    last = stack1.pop()
                    self._markTried(last[0], last[1])
                    stack.push(stack1.peek())
                    label = "second_time"
        return False

    def reset(self):
        '''Resets the maze by removing all "path" and "tried" tokens.'''
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                if self._mazeCells[i, j] == self.PATH_TOKEN or self._mazeCells[i, j] == self.TRIED_TOKEN:
                    self._mazeCells[i, j] = None

    def draw(self):
        '''Prints a text-based representation of the maze.'''
        text = ""
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                if self._mazeCells[i, j]:
                    text += self._mazeCells[i, j]
                else:
                    text += "   "
            text += "\n"
        print(text)

    def _validMove(self, row, col):
        '''
        Returns True if the given cell position is a valid move.
        :param row: int
        :param col: int
        :return: True
        '''
        return row >= 0 and row < self.num_rows() \
               and col >= 0 and col < self.num_cols() \
               and self._mazeCells[row, col] is None

    def _exitFound(self, row, col):
        '''
        Helper method to determine if the exit was found.
        :param row: int
        :param col: int
        :return: bool
        '''
        return row == self._exitCell.row and col == self._exitCell.col

    def _markTried(self, row, col):
        '''
        Drops a "tried" token at the given cell.
        :param row: int
        :param col: int
        '''
        self._mazeCells[row, col] = self.TRIED_TOKEN

    def _markPath(self, row, col):
        '''
        Drops a "path" token at the given cell.
        :param row: int
        :param col: int
        '''
        self._mazeCells[row, col] = self.PATH_TOKEN


class _CellPosition(object):
    '''Private storage class for holding a cell position'''

    def __init__(self, row, col):
        '''
        Initialises a cell.
        :param row: int
        :param col: int
        '''
        self.row = row
        self.col = col
