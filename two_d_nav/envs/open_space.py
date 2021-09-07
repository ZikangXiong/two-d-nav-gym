import numpy as np

from two_d_nav.elements import create_open_space, VelRobot
from two_d_nav.envs.env_base import Navigation
from two_d_nav.engine import NavigationEngine


class OpenSpaceNavigation(Navigation):
    def __init__(self):
        robot = VelRobot(100, 700)
        obs_list = []
        maze = create_open_space()
        engine = NavigationEngine(robot=robot, obstacle_list=obs_list, maze=maze)
        super(OpenSpaceNavigation, self).__init__(engine)
