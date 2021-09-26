from typing import List, Union, Callable, Optional

import numpy as np
import pygame

from two_d_nav import config
from two_d_nav.elements import VelRobot, Cat, Maze, Charger, Flight, Car, ObjectBase
from two_d_nav.utils import normalize_pos, denormalize_pos, draw_dashed_line


class MazeNavigationEngine:
    def __init__(self, robot: VelRobot, obstacle_list: List[Cat], maze: Maze):
        self.screen = None

        pygame.display.set_caption("2D robot navigation")
        icon = pygame.image.load(f"{config.root}/assets/robot.png")

        try:
            pygame.display.set_icon(icon)
        except Exception:
            import os
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.robot = robot
        self.obstacle_list = obstacle_list
        self.maze = maze

        self.plan_lines = []

    def set_plan(self, plan: np.ndarray, denormalize: bool = False):
        assert plan.shape[1:] == (2,), f"shape {plan.shape[1:]} == (2, )"
        if denormalize:
            plan = denormalize_pos(plan)
        self.plan_lines = np.stack([plan[:-1], plan[1:]], axis=1)

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

        # plot plan
        for plan_line in self.plan_lines:
            pygame.draw.line(self.screen, "green", plan_line[0], plan_line[1], 1)

        # plot goal
        self.screen.blit(*goal)

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
        dist = goal_pos - robot_pos

        return dist

    def hit_wall(self) -> bool:
        robot_pos = np.array(self.robot.center())
        robot_shape = np.array(self.robot.shape)

        for line in self.maze.lines:
            point_1 = np.array(line[1])
            point_2 = np.array(line[2])

            line_high = np.max([point_1 + (robot_shape / 2 - 10),
                                point_2 + (robot_shape / 2 - 10)], axis=0)
            line_low = np.min([point_1 - (robot_shape / 2 - 10),
                               point_2 - (robot_shape / 2 - 10)], axis=0)

            if (robot_pos < line_high).all() and (robot_pos > line_low).all():
                return True
        return False

    def hit_object(self, obj: Union[Charger, Cat]) -> bool:
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


class FlightsEngine:
    def __init__(self, flights: List[Flight]):
        self.flights = flights
        self.screen = None

        pygame.display.set_caption("Flights")
        icon = pygame.image.load(f"{config.root}/assets/flight.png")

        try:
            pygame.display.set_icon(icon)
        except Exception:
            import os
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.plan_groups = [[]]

    def set_plan_groups(self, plan_groups):
        self.plan_groups = plan_groups

    def render(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 800))

        # white background
        self.screen.fill((255, 255, 255))

        # plot plan
        for plan_group in self.plan_groups:
            for plan_line in plan_group:
                for segment in plan_line:
                    pygame.draw.line(self.screen, "green", segment[0], segment[1], 1)

        # plot flights
        for flight in self.flights:
            robot_image, robot_pos = flight.render_info()
            robot_image = pygame.transform.rotate(robot_image, flight.heading())
            self.screen.blit(robot_image, robot_pos)

        pygame.display.update()


class CarEngine:
    def __init__(self,
                 ego_car: Car,
                 other_cars: List[Car],
                 static_objects: Optional[List[ObjectBase]] = None):
        self.ego_car = ego_car
        self.other_cars = other_cars

        self.screen = None
        self.static_objects = static_objects

        pygame.display.set_caption("Car")
        icon = pygame.image.load(f"{config.root}/assets/car.png")

        try:
            pygame.display.set_icon(icon)
        except Exception:
            import os
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.plan_lines = []
        self.road_lines = [{"line": [], "type": "solid"}]

    def set_plan(self, plan: np.ndarray, denormalize: bool = False):
        assert plan.shape[1:] == (2,), f"shape {plan.shape[1:]} == (2, )"
        if denormalize:
            plan = denormalize_pos(plan)
        self.plan_lines = np.stack([plan[:-1], plan[1:]], axis=1)

    def plot_plan(self):
        for segment in self.plan_lines:
            pygame.draw.line(self.screen, "green", segment[0], segment[1], 1)

    def plot_road(self):
        for road_line in self.road_lines:
            _type = road_line["type"]
            segments = np.stack([road_line["line"][:-1], road_line["line"][1:]], axis=1)

            for segment in segments:
                if _type == "dashed":
                    draw_dashed_line(self.screen, "black", segment[0], segment[1], 1)
                else:
                    pygame.draw.line(self.screen, "black", segment[0], segment[1], 1)

    def plot_cars(self):
        # plot ego car
        robot_image, robot_pos = self.ego_car.render_info()
        robot_image = pygame.transform.rotate(robot_image, self.ego_car.heading())
        self.screen.blit(robot_image, robot_pos)

        # plot other cars
        for car in self.other_cars:
            robot_image, robot_pos = car.render_info()
            robot_image = pygame.transform.rotate(robot_image, car.heading())
            self.screen.blit(robot_image, robot_pos)

    def plot_static_objects(self):
        if self.static_objects:
            for obj in self.static_objects:
                self.screen.blit(*obj.render_info())

    def render(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 800))

        # white background
        self.screen.fill((255, 255, 255))

        # plot plan
        self.plot_plan()

        # plot road
        self.plot_road()

        # plot cars
        self.plot_cars()

        # plot other objects
        self.plot_static_objects()

        pygame.display.update()
