from typing import List

import pygame

from two_d_nav import config
from two_d_nav.elements import Robot, Obstacle, Maze, create_maze


class NavigationEngine:
    def __init__(self, robot: Robot, obstacle_list: List[Obstacle], maze: Maze):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))

        pygame.display.set_caption("2D robot navigation")
        icon = pygame.image.load(f"{config.root}/assets/robot.png")
        pygame.display.set_icon(icon)

        self.robot = robot
        self.obstacle_list = obstacle_list
        self.maze = maze

    def run(self):
        # game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))
            self.screen.blit(*self.robot.render_info())

            for obs in self.obstacle_list:
                self.screen.blit(*obs.render_info())

            walls, goal = self.maze.render_info()
            for line in walls:
                pygame.draw.line(self.screen, *line)

            self.screen.blit(*goal)

            pygame.display.update()


if __name__ == '__main__':
    _robot = Robot(100.0, 750.0)
    obs1 = Obstacle(200.0, 600.0)
    obs2 = Obstacle(700.0, 100.0)
    obs_list = [obs1, obs2]
    _maze = create_maze(1)

    eng = NavigationEngine(_robot, obs_list, _maze)
    eng.run()
