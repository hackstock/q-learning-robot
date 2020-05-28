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

    def __repr__(self):
        return f"({self.row},{self.col})"

class GridWorld(object):
    def __init__(self, size=(5,5), start_pos=(0,0)):
        self.rows = size[0]
        self.cols = size[1]
        self.start_pos = start_pos
        self.car_pos = Cell(start_pos[0], start_pos[1])
        self.goal_pos = Cell(self.rows - 1, self.cols - 1)
        self._walls = []
        self.world = None
        self.max_steps = self.rows * self.cols
        self.steps_taken = 0
        self.done = False
        self.rewards = {
            'into_fence': -5,
            'into_wall': -5,
            'at_goal': 100,
            'good_move': -1
        }

    def reset(self):
        self.steps_taken = 0
        self.done = False 
        return self.start_pos

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
        world[self.car_pos.row][self.car_pos.col] = 'C'
        world[self.goal_pos.row][self.goal_pos.col] = 'G'

        return world

    def _move_right(self):
        next_state = Cell(self.car_pos.row, self.car_pos.col + 1)
        if next_state.col == self.cols or next_state in self._walls:
            next_state = self.car_pos
        
        return next_state

    def _move_left(self):
        next_state = Cell(self.car_pos.row, self.car_pos.col - 1)
        if next_state.col < 0 or next_state in self._walls:
            next_state = self.car_pos
           
        return next_state

    def _move_down(self):
        next_state = Cell(self.car_pos.row + 1, self.car_pos.col)
        if next_state.row == self.rows or next_state in self._walls:
            next_state = self.car_pos
        
        return next_state

    def _move_up(self):
        next_state = Cell(self.car_pos.row - 1, self.car_pos.col)
        if next_state.row < 0 or next_state in self._walls:
            next_state = self.car_pos
        
        return next_state
         

    def move(self, direction):
        next_state = None
        if direction == 'r':
            next_state = self._move_right()
        elif direction == 'l':
            next_state = self._move_left()
        elif direction == 'd':
            next_state = self._move_down()
        elif direction == 'u':
            next_state = self._move_up()

        self.car_pos = next_state
        return next_state

    def render(self):
        self.world = self._update_world()
        print(tabulate(self.world, tablefmt="fancy_grid"))

