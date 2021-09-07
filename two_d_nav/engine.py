from typing import List, Union

import pygame
import numpy as np

from two_d_nav import config
from two_d_nav.elements import VelRobot, Obstacle, Maze, create_maze, Goal
from two_d_nav.utils import normalize_pos


class NavigationEngine:
    def __init__(self, robot: VelRobot, obstacle_list: List[Obstacle], maze: Maze):
        self.screen = None

        pygame.display.set_caption("2D robot navigation")
        icon = pygame.image.load(f"{config.root}/assets/robot.png")
        pygame.display.set_icon(icon)

        self.robot = robot
        self.obstacle_list = obstacle_list
        self.maze = maze

    def render(self):
        # call other functions before calling it
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode(config.map_size)

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

        reach_goal, hit_obstacle, hit_wall = self.get_robot_status()

        # plot robot
        robot_image, robot_pos = self.robot.render_info()
        robot_image = pygame.transform.rotate(robot_image, self.robot.heading())
        self.screen.blit(robot_image, robot_pos)

        pygame.display.update()

    def get_robot_status(self):
        hit_wall = self.hit_wall()
        reach_goal = self.hit_object(self.maze.goal)
        hit_obstacle = False
        for obs in self.obstacle_list:
            if self.hit_object(obs):
                hit_obstacle = True
                break

        return reach_goal, hit_obstacle, hit_wall

    def dist_goal(self) -> np.ndarray:
        # distance to goal in the normalize coordinator
        robot_pos = normalize_pos(np.array([self.robot.x, self.robot.y]))
        goal_pos = normalize_pos(np.array([self.maze.goal.x, self.maze.goal.y]))
        dist = robot_pos - goal_pos

        return dist

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
                        self.robot.move(-config.robot_vel_scale, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.robot.move(config.robot_vel_scale, 0)
                    elif event.key == pygame.K_UP:
                        self.robot.move(0, -config.robot_vel_scale)
                    elif event.key == pygame.K_DOWN:
                        self.robot.move(0, config.robot_vel_scale)

            reach_goal, hit_obstacle, hit_wall = self.get_robot_status()

            if hit_wall:
                self.robot.stay()

            if reach_goal or hit_obstacle:
                self.robot.reset()

            self.render()
