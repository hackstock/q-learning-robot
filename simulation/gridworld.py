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

    def __eq__(self, other):
        return (self.row == other.row) and (self.col == other.col)

    def __repr__(self):
        return f"({self.row},{self.col})"

CAR_STATUS_NORMAL = 'normal'
CAR_STATUS_IN_FENCE = 'in_fence'
CAR_STATUS_IN_WALL = 'in_wall'
CAR_STATUS_AT_GOAL = 'at_goal'
class GridWorld(object):
    def __init__(self, size=(5,5), start_pos=(0,0)):
        self.rows = size[0]
        self.cols = size[1]
        self.start_pos = Cell(start_pos[0], start_pos[1])
        self.car_pos = self.start_pos
        self.car_status = CAR_STATUS_NORMAL
        self.goal_pos = Cell(self.rows - 1, self.cols - 1)
        self._walls = []
        self.world = None
        self.max_steps = self.rows * self.cols
        self.steps_taken = 0
        self.done = False
        self.rewards = {
            CAR_STATUS_IN_FENCE: -5,
            CAR_STATUS_IN_WALL: -5,
            CAR_STATUS_AT_GOAL: 100,
            CAR_STATUS_NORMAL: -1
        }

    def reset(self):
        self.steps_taken = 0
        self.done = False 
        self.car_status = CAR_STATUS_NORMAL
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
        if next_state.col == self.cols:
            self.car_status = CAR_STATUS_IN_FENCE
            next_state = self.car_pos
        elif next_state in self._walls:
            self.car_status = CAR_STATUS_IN_WALL
            next_state = self.car_pos
        else:
            self.car_status = CAR_STATUS_NORMAL

        return next_state

    def _move_left(self):
        next_state = Cell(self.car_pos.row, self.car_pos.col - 1)
        if next_state.col < 0:
            self.car_status = CAR_STATUS_IN_FENCE
            next_state = self.car_pos
        elif next_state in self._walls:
            self.car_status = CAR_STATUS_IN_WALL
            next_state = self.car_pos
        else:
            self.car_status = CAR_STATUS_NORMAL

        return next_state

    def _move_down(self):
        next_state = Cell(self.car_pos.row + 1, self.car_pos.col)
        if next_state.row == self.rows:
            self.car_status = CAR_STATUS_IN_FENCE
            next_state = self.car_pos
        elif next_state in self._walls:
            self.car_status = CAR_STATUS_IN_WALL
            next_state = self.car_pos
        else:
            self.car_status = CAR_STATUS_NORMAL

        return next_state

    def _move_up(self):
        next_state = Cell(self.car_pos.row - 1, self.car_pos.col)
        if next_state.row < 0:
            self.car_status = CAR_STATUS_IN_FENCE
            next_state = self.car_pos
        elif next_state in self._walls:
            self.car_status = CAR_STATUS_IN_WALL
            next_state = self.car_pos
        else:
            self.car_status = CAR_STATUS_NORMAL

        return next_state

    def _in_wall(self, cell):
        return cell in self._walls

    

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

        self.steps_taken += 1
        if self.steps_taken == self.max_steps:
            self.done = True

        self.car_pos = next_state
        if self.car_pos == self.goal_pos:
            self.car_status = CAR_STATUS_AT_GOAL
            self.done = True

        reward = self.rewards[self.car_status]
        return next_state, reward, self.done

    def render(self):
        self.world = self._update_world()
        print(tabulate(self.world, tablefmt="fancy_grid"))

