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


def test_open_space_navigation():
    env = OpenSpaceNavigation()

    for i in range(1000):
        obs, reward, done, _ = env.step(np.array([0.1, -0.1]))
        if done:
            print(obs)
        env.render()


if __name__ == '__main__':
    test_open_space_navigation()
