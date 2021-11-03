import copy
from typing import List, Tuple

import numpy as np
import pygame

from two_d_nav import config


class ObjectBase:
    def __init__(self, image_path: str, shape: np.ndarray, init_x: float, init_y: float):
        self.image = pygame.image.load(image_path)
        self.shape = shape
        self.image = pygame.transform.scale(self.image, tuple(self.shape))

        self.x = init_x
        self.y = init_y
        self.init_x = init_x
        self.init_y = init_y
        self.prev_x = init_x
        self.prev_y = init_y

        self.kept_heading = None

    def center(self):
        return int(self.x + self.shape[0] / 2), \
            int(self.y + self.shape[1] / 2)

    def heading(self):
        if self.kept_heading is not None:
            return self.kept_heading

        if self.prev_x == self.x and self.prev_y == self.y:
            return 0

        dx = self.x - self.prev_x
        dy = self.y - self.prev_y
        r = np.linalg.norm([dx, dy], ord=2)
        angle = -np.arcsin(dx / r) / np.pi * 180

        if dy > 0:
            angle = 180 - angle

        return angle

    def render_info(self):
        return self.image, (int(self.x), int(self.y))

    def move(self, dx, dy) -> np.ndarray:
        self.prev_x = self.x
        self.prev_y = self.y
        self.x += dx
        self.y += dy

        if self.kept_heading is not None:
            self.kept_heading = None

        return np.array([self.x, self.y])

    def reset(self):
        self.x = self.init_x
        self.y = self.init_y

    def stay(self):
        self.kept_heading = self.heading()
        self.x = self.prev_x
        self.y = self.prev_y


class VelRobot(ObjectBase):
    def __init__(self, init_x: float, init_y: float):
        super(VelRobot, self).__init__(f"{config.root}/assets/robot.png",
                                       np.array((30, 30)),
                                       init_x, init_y)


class Cat(ObjectBase):
    def __init__(self, init_x: float, init_y: float):
        super(Cat, self).__init__(f"{config.root}/assets/cat.png",
                                  np.array((30, 30)),
                                  init_x, init_y)


class Charger(ObjectBase):
    def __init__(self, x: float, y: float):
        super(Charger, self).__init__(f"{config.root}/assets/charger.png",
                                      np.array((30, 30)),
                                      x, y)


class Flight(ObjectBase):
    def __init__(self, x: float, y: float):
        super(Flight, self).__init__(f"{config.root}/assets/flight.png",
                                     np.array((30, 30)),
                                     x, y)


class Car(ObjectBase):
    def __init__(self, x: float, y: float):
        super(Car, self).__init__(f"{config.root}/assets/Car.png",
                                  np.array((30, 30)),
                                  x, y)


class Goal(ObjectBase):
    def __init__(self, x: float, y: float):
        super(Goal, self).__init__(f"{config.root}/assets/goal.png",
                                   np.array((30, 30)),
                                   x, y)


class Maze:
    def __init__(self, lines: List[Tuple], goal_pos: Tuple[float, float]):
        self.lines = lines
        self.goal = Charger(*goal_pos)

    def render_info(self):
        return self.lines, self.goal.render_info()


def create_open_space() -> Maze:
    return Maze([], goal_pos=(400, 400))


def create_maze(indx=0) -> Maze:
    line0 = (0, [10, 10], [10, 790], 5)
    line1 = (0, [10, 790], [790, 790], 5)
    line2 = (0, [790, 790], [790, 10], 5)
    line3 = (0, [790, 10], [10, 10], 5)
    goal_pos = (50.0, 50.0)

    frame = [line0, line1, line2, line3]
    if indx == 0:
        return Maze(frame, goal_pos)
    elif indx == 1:
        maze_lines = copy.deepcopy(frame)
        wall0 = (0, [10, 200], [200, 200], 5)
        wall1 = (0, [10, 650], [650, 650], 5)
        wall2 = (0, [10, 500], [400, 500], 5)
        wall3 = (0, [300, 10], [300, 400], 5)
        wall4 = (0, [500, 10], [500, 500], 5)
        wall5 = (0, [500, 400], [650, 400], 5)
        wall6 = (0, [650, 200], [790, 200], 5)
        maze_lines.extend([wall0, wall1, wall2, wall3, wall4, wall5, wall6])

        return Maze(maze_lines, goal_pos)
    else:
        raise NotImplementedError()
