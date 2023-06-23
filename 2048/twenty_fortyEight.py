"""
Clone of 2048 game.
"""
import random
import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # Creating a new list of zeros with the same length as the line[]
    merged_line = [0] * len(line)
    merge_index = 0

    for value in line:

        if value != 0:
            if merged_line[merge_index] == 0:
                merged_line[merge_index] = value
            elif merged_line[merge_index] == value:
                merged_line[merge_index] *= 2
                merge_index += 1

            else:
                # Moving to the next position for the next tile
                merge_index += 1
                # Moving the current tile to the next available position
                merged_line[merge_index] = value

    return merged_line


class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        direction = {}

        up_ind = []
        down_ind = []
        for col in range(grid_width):
            up_ind.append((0, col))
            down_ind.append((grid_height-1, col))

        left_ind = []
        right_ind = []
        for row in range(grid_height):
            left_ind.append((row, 0))
            right_ind.append((row, grid_width-1))

        direction[UP] = up_ind
        direction[DOWN] = down_ind
        direction[LEFT] = left_ind
        direction[RIGHT] = right_ind
        self._direction = direction

        self.reset()

    def reset(self):
        """
        Resets the game so the grid is empty except for two
        initial tiles.
        """
        self._cells = [[0 for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Returns a string representation of the grid for debugging.
        """
        return "Welcome to 2048"

    def get_grid_height(self):
        """
        Gets the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Gets the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Moves all tiles in the given direction and adds
        a new tile if any tiles moved.
        """
        if direction == UP or direction == DOWN:
            steps = self._grid_height
        else:
            steps = self._grid_width

        changes = 0
        for tile in self._direction[direction]:
            pointer = []
            for step in range(steps):
                row = tile[0] + step * OFFSETS[direction][0]
                col = tile[1] + step * OFFSETS[direction][1]
                cell = (row, col)
                pointer.append(cell)

            current_pos = []
            for j in range(len(pointer)):
                value = self.get_tile(pointer[j][0], pointer[j][1])
                current_pos.append(value)

            new_pos = merge(current_pos)
            for i in range(len(new_pos)):
                if current_pos[i] != new_pos[i]:
                    self.set_tile(pointer[i][0], pointer[i][1], new_pos[i])
                    changes += 1

        if changes > 0:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        null_cell = []
        for row in range(self._grid_height):
            for cell in range(self._grid_width):
                if self._cells[row][cell] == 0:
                    null_cell.append((row, cell))

        tile = random.choice(null_cell)
        val = random.randint(1, 10)

        if val <= 9:
            self._cells[tile[0]][tile[1]] = 2

        else:
            self._cells[tile[0]][tile[1]] = 4

    def set_tile(self, row, col, value):
        """
        Sets the tile at position row, col to have the given value.
        """
        self._cells[row][col] = value

    def get_tile(self, row, col):
        """
        Returns the value of the tile at position row, col.
        """
        return self._cells[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
