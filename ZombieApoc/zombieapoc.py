# Rice University Computer Science

# Zombie Apocalypse mini-project

# Written in Python 2

# Saman Saybani

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)

        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])

        if zombie_list != None:
            self._zombie = list(zombie_list)
        else:
            self._zombie = []

        if human_list != None:
            self._human = list(human_list)  
        else:
            self._human = []
        
    def clear(self):
        """
        Sets cells in obstacle grid to be empty
        Resets zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)

        self._zombie = []
        self._human = []
        
    def add_zombie(self, row, col):
        """
        Adds zombie to the zombie list
        """
        self._zombie.append((row,col))

    def num_zombies(self):
        """
        Returns number of zombies
        """
        return len(self._zombie)       

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie:
            yield zombie

    def add_human(self, row, col):
        """
        Adds human to the human list
        """
        self._human.append((row,col))

    def num_humans(self):
        """
        Returns number of humans
        """
        return len(self._human)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = [[EMPTY for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        distance_field = [[self._grid_width * self._grid_height for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]

        boundary = poc_queue.Queue()

        obstacles = [(row, col) for row in range(self.get_grid_height()) for col in range(self.get_grid_width()) if not self.is_empty(row, col)]

        if entity_type == ZOMBIE:
            for item in self.zombies():
                boundary.enqueue(item)

        if entity_type == HUMAN:
            for item in self.humans():
                boundary.enqueue(item)

        for cell in boundary:
            visited[cell[0]][cell[1]] = FULL
            distance_field[cell[0]][cell[1]] = 0

        while len(boundary) != 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors (current_cell[0], current_cell[1])

            for neighbor in neighbors:
                if (visited[neighbor[0]][neighbor[1]] == EMPTY)and (neighbor not in obstacles):
                    visited[neighbor[0]][neighbor[1]] = FULL

                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1

        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        copy = list(self._human)

        for num in range(len(copy)):
            human = copy[num]
            neighbors = self.eight_neighbors(human[0], human[1])
            human_dist = zombie_distance_field[human[0]][human[1]]
            top_cell = [human]
            distance = human_dist

            for neighbor in neighbors:
                if self.is_empty(neighbor[0],neighbor[1]):
                    neigh_dist = zombie_distance_field[neighbor[0]][neighbor[1]]
                    if neigh_dist > distance:
                        distance = neigh_dist
                        top_cell = [neighbor]
                    if neigh_dist == distance:
                        top_cell.append(neighbor)

            self._human[num] = random.choice(top_cell)

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        copy = list(self._zombie)

        for num in range(len(copy)):
            zombie = copy[num]
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            zombie_dist = human_distance_field[zombie[0]][zombie[1]]
            top_cell = [zombie]
            distance = zombie_dist

            for neighbor in neighbors:
                if self.is_empty(neighbor[0],neighbor[1]):
                    neigh_dist = human_distance_field[neighbor[0]] [neighbor[1]]

                    if neigh_dist < distance:
                        distance = neigh_dist
                        top_cell = [neighbor]

                    if neigh_dist == distance:
                        top_cell.append(neighbor)

            self._zombie[num] = random.choice(top_cell)

# Start up gui for simulation
poc_zombie_gui.run_gui(Apocalypse(30, 40))
