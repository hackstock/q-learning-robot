import subprocess

import numpy as np 
from tabulate import tabulate

class Cell(object):
    def __init__(self, row, col):
        self._row = row 
        self._col = col 

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, value):
        self._col = value

class GridWorld(object):
    def __init__(self, size=(5,5), start_state=(0,0)):
        self.rows = size[0]
        self.cols = size[1]
        self.position = Cell(start_state[0], start_state[1])
        self._walls = []
        self.world = self._update_world()

    @property
    def walls(self):
        return self._walls

    @walls.setter
    def walls(self, value):
        self._walls = [Cell(row, col) for row, col in value]

    def _update_world(self):
        world = np.array([[' '] * self.cols for _ in range(self.rows)])
        wall_rows = [cell.row for cell in self._walls]
        wall_cols = [cell.col for cell in self._walls]
        world[wall_rows, wall_cols] = '#'
        world[self.position.row][self.position.col] = 'C'

        return world

    def move(self, direction):
        if direction == 'r':
            self.position.col += 1
        self.world = self._update_world()


    def render(self):
        print(tabulate(self.world, tablefmt="fancy_grid"))

