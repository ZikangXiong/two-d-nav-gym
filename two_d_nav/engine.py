from typing import List, Union

import pygame
import numpy as np

from two_d_nav import config
from two_d_nav.elements import VelRobot, Obstacle, Maze, create_maze, Goal


class NavigationEngine:
    def __init__(self, robot: VelRobot, obstacle_list: List[Obstacle], maze: Maze):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))

        pygame.display.set_caption("2D robot navigation")
        icon = pygame.image.load(f"{config.root}/assets/robot.png")
        pygame.display.set_icon(icon)

        self.robot = robot
        self.obstacle_list = obstacle_list
        self.maze = maze

    def hit_wall(self) -> bool:
        for line in self.maze.lines:
            point_1 = np.array(line[1])
            point_2 = np.array(line[2])
            upper = np.max([point_1 + config.wall_collision_threshold,
                            point_2 + config.wall_collision_threshold], axis=0)
            lower = np.min([point_1 - config.wall_collision_threshold,
                            point_2 - config.wall_collision_threshold], axis=0)

            robot_pos = np.array(self.robot.center())

            if (robot_pos < upper).all() and (robot_pos > lower).all():
                return True
        return False

    def hit_object(self, obj: Union[Goal, Obstacle]) -> bool:
        dx = self.robot.x - obj.x
        dy = self.robot.y - obj.y

        if abs(dx) < config.obj_collision_threshold \
                and abs(dy) < config.obj_collision_threshold:
            return True

        return False

    def run(self):
        # game loop, only for test purpose, see the environment in the envs folder.
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.robot.move(-config.robot_vel, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.robot.move(config.robot_vel, 0)
                    elif event.key == pygame.K_UP:
                        self.robot.move(0, -config.robot_vel)
                    elif event.key == pygame.K_DOWN:
                        self.robot.move(0, config.robot_vel)

            # white background
            self.screen.fill((255, 255, 255))

            # plot all obstacles
            for obs in self.obstacle_list:
                self.screen.blit(*obs.render_info())

            walls, goal = self.maze.render_info()
            # plot walls
            for line in walls:
                pygame.draw.line(self.screen, *line)

            # plot goal
            self.screen.blit(*goal)

            # wall collision detection
            if self.hit_wall():
                self.screen.fill((0, 0, 255))
                self.robot.stay()

            # plot robot
            robot_image, robot_pos = self.robot.render_info()
            robot_image = pygame.transform.rotate(robot_image, self.robot.heading())
            self.screen.blit(robot_image, robot_pos)

            # obstacle collision detection
            for obs in self.obstacle_list:
                if self.hit_object(obs):
                    self.screen.fill((255, 0, 0))
                    self.robot.reset()

            # achieve goal
            if self.hit_object(self.maze.goal):
                self.screen.fill((0, 255, 0))
                self.robot.reset()

            pygame.display.update()


def test_engine():
    # See the environment in the envs folder.
    _robot = VelRobot(100, 700)
    obs1 = Obstacle(400.0, 600.0)
    obs2 = Obstacle(700.0, 100.0)
    obs3 = Obstacle(300.0, 500.0)
    obs4 = Obstacle(150.0, 200.0)
    obs5 = Obstacle(350.0, 250.0)
    obs_list = [obs1, obs2, obs3, obs4, obs5]
    _maze = create_maze(1)

    eng = NavigationEngine(_robot, obs_list, _maze)
    eng.run()


if __name__ == '__main__':
    test_engine()
