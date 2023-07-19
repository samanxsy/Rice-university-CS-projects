#  Rice University - Computer Science
#
#  Loyd's Fifteen puzzle (solver and visualizer)
#  note that solved configuration has the blank (zero) tile in upper left;
#  use the arrows key to swap this tile with its neighbors
#
# Written for Python 2
#
# Student: Saman Saybani


import poc_fifteen_gui


class Puzzle:
    ''' class representation for The Fifteen Puzzle '''
    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        ''' Initializer '''
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row for col in range(self._width)] for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        ''' generate string representation for puzzle; returns a string '''
        ans = ''

        for row in range(self._height):
            ans += str(self._grid[row])
            ans += '\n'

        return ans

    def get_height(self):
        ''' getter for puzzle height '''
        return self._height

    def get_width(self):
        ''' getter for puzzle width; returns an integer '''
        return self._width

    def get_number(self, row, col):
        ''' getter for the number at tile position pos '''
        return self._grid[row][col]

    def set_number(self, row, col, value):
        ''' setter for the number at tile position pos '''
        self._grid[row][col] = value

    def clone(self):
        ''' make a copy of the puzzle to update during solving '''
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    def current_position(self, solved_row, solved_col):
        """
        locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved;
        returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:

                    return (row, col)

    def update_puzzle(self, move_string):
        ''' updates the puzzle state based on the provided move string '''
        first_row, first_column = self.current_position(0, 0)

        for path in move_string:
            if path == 'l':
                assert first_column > 0, 'move off grid: ' + path
                self._grid[first_row][first_column] = self._grid[first_row][first_column - 1]
                self._grid[first_row][first_column - 1] = 0

                first_column -= 1

            elif path == 'r':
                assert first_column < self._width - 1, 'move off grid: ' + path
                self._grid[first_row][first_column] = self._grid[first_row][first_column + 1]
                self._grid[first_row][first_column + 1] = 0

                first_column += 1

            elif path == 'u':
                assert first_row > 0, 'move off grid: ' + path
                self._grid[first_row][first_column] = self._grid[first_row - 1][first_column]
                self._grid[first_row - 1][first_column] = 0

                first_row -= 1

            elif path == 'd':
                assert first_row < self._height - 1, 'move off grid: ' + path
                self._grid[first_row][first_column] = self._grid[first_row + 1][first_column]
                self._grid[first_row + 1][first_column] = 0

                first_row += 1

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) == 0:
            for columns in range(target_col + 1, self.get_width()):
                if not (target_row, columns) == self.current_position(target_row, columns):

                    return False
    
            if not target_row + 1 == self.get_height():
                for lower_column in range(0, self.get_width()):
                    if not (target_row + 1, lower_column) == self.current_position(target_row + 1, lower_column):

                        return False

            return True
        return False

    def move(self, target_row, target_col, row, column):
        column_action = ''
        action = 'druld'

        column_diff = target_col - column
        row_diff = target_row - row

        column_action += row_diff * 'u'
        if column_diff == 0:
            column_action += 'ld' + (row_diff - 1) * action

        else:
            if column_diff > 0:
                column_action += column_diff * 'l'
                if row == 0:
                    column_action += (abs(column_diff) - 1) * 'drrul'
                else:
                    column_action += (abs(column_diff) - 1) * 'urrdl'

            elif column_diff < 0:
                column_action += (abs(column_diff) - 1)  * 'r'
                if row == 0:
                    column_action += abs(column_diff) * 'rdllu'
                else:
                    column_action += abs(column_diff) * 'rulld'

            column_action += row_diff * action

        return column_action

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)

        row, column = self.current_position(target_row, target_col)
        column_action = self.move(target_row, target_col, row, column)

        self.update_puzzle(column_action)
        assert self.lower_row_invariant(target_row, target_col - 1)

        return column_action

    def solve_col0_tile(self, target_row):
        '''
        solve tile in column zero on specified row (> 1);
        updates puzzle and returns a move string
        '''
        assert self.lower_row_invariant(target_row, 0)
        column_action = 'ur'       
        self.update_puzzle(column_action)

        row, column = self.current_position(target_row, 0)
        if row == target_row and column == 0:
            move = (self.get_width() - 2) * 'r'

            self.update_puzzle(move)
            column_action += move

        else:
            move = self.move(target_row - 1, 1, row, column)
            move += 'ruldrdlurdluurddlu' + (self.get_width() - 1) * 'r'

            self.update_puzzle(move)
            column_action += move

        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)

        return column_action

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self.get_number(0, target_col) == 0:
            return False

        for column in range(self.get_width()):
            for row in range(self.get_height()):

                if (row == 0 and column > target_col) or (row == 1 and column >= target_col) or row > 1:
                    if not (row, column) == self.current_position(row, column):

                        return False

        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """

        if not self.lower_row_invariant(1, target_col):
            return False

        # check if all tiles in rows bellow row 1 are positioned at their solved location
        for column in range(0, self.get_width()):
            for row in range(2, self.get_height()):
    
                if not (row, column) == self.current_position(row, column):
                    return False

        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)

        column_action = 'ld'       
        self.update_puzzle(column_action)

        row, column = self.current_position(0, target_col)
        if row == 0 and column == target_col:
            return column_action

        else:
            move = self.move(1, target_col - 1, row, column)
            move += 'urdlurrdluldrruld'

            self.update_puzzle(move)
            column_action += move

        return column_action

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        row, column = self.current_position(1, target_col)

        column_action = self.move(1, target_col, row, column)
        column_action += 'ur'
        
        self.update_puzzle(column_action)

        return column_action
    
    def solve_2x2(self):
        '''
        solves the upper left 2x2 part of the puzzle;
        doesn't check for insolvable configuration!,
        updates the puzzle and returns a move string
        '''
        column_action = ''
        first_move = ''
              
        if self.get_number(1, 1) == 0:
            first_move += 'ul'
            self.update_puzzle(first_move)

            if (0, 1) == self.current_position(0, 1) and (1, 1) == self.current_position(1, 1):
                return first_move

            if self.get_number(0, 1) < self.get_number(1, 0):
                column_action += 'rdlu'

            else:
                column_action += 'drul'       
 
            self.update_puzzle(column_action)
            
        return first_move + column_action

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        column_action = ''

        row = self.get_height() - 1
        column = self.get_width() - 1

        row_current, column_current = self.current_position(0, 0)

        column_diff = column_current - column
        row_diff = row_current - row
        move = abs(column_diff) * 'r' + abs(row_diff) * 'd'

        self.update_puzzle(move)
        column_action += move

        for x in range(row, 1, -1):
            for y in range(column, 0, -1):
                column_action += self.solve_interior_tile(x, y)

            column_action += self.solve_col0_tile(x)

        for y in range(column, 1, -1):
            column_action += self.solve_row1_tile(y)
            column_action += self.solve_row0_tile(y)

        column_action += self.solve_2x2()

        return column_action


# RUN GUI
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
