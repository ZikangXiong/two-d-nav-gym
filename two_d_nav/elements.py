import copy
from typing import List, Tuple

import pygame

from two_d_nav import config


class Robot:
    def __init__(self, init_x: float, init_y: float):
        self.init_x = init_x
        self.init_y = init_y
        self.x = init_x
        self.y = init_y
        self.prev_x = init_x
        self.prev_y = init_y

        self.image = pygame.image.load(f"{config.root}/assets/robot.png")
        self.shape = (45, 45)
        self.image = pygame.transform.scale(self.image, self.shape)

    def center(self):
        return int(self.x + self.shape[0] / 2), \
               int(self.y + self.shape[1] / 2)

    def render_info(self):
        return self.image, (int(self.x), int(self.y))

    def move(self, dx, dy):
        self.prev_x = self.x
        self.prev_y = self.y
        self.x += dx
        self.y += dy

    def reset(self):
        self.x = self.init_x
        self.y = self.init_y

    def stay(self):
        self.x = self.prev_x
        self.y = self.prev_y


class Obstacle:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.image = pygame.image.load(f"{config.root}/assets/obstacle.png")
        self.shape = (45, 45)
        self.image = pygame.transform.scale(self.image, self.shape)

    def render_info(self):
        return self.image, (int(self.x), int(self.y))

    def center(self):
        return int(self.x + self.shape[0] / 2), \
               int(self.y + self.shape[1] / 2)


class Goal:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.image = pygame.image.load(f"{config.root}/assets/goal.png")
        self.shape = (45, 45)
        self.image = pygame.transform.scale(self.image, self.shape)

    def render_info(self):
        return self.image, (int(self.x), int(self.y))

    def center(self):
        return int(self.x + self.shape[0] / 2), \
               int(self.y + self.shape[1] / 2)


class Maze:
    def __init__(self, lines: List[Tuple], goal_pos: Tuple[float, float]):
        self.lines = lines
        self.goal = Goal(*goal_pos)

    def render_info(self):
        return self.lines, self.goal.render_info()


def create_open_space() -> Maze:
    return Maze([], goal_pos=(50, 50))


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
