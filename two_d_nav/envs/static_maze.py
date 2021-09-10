import numpy as np

from two_d_nav.elements import create_maze, VelRobot, Obstacle
from two_d_nav.envs.env_base import Navigation
from two_d_nav.engine import NavigationEngine


class StaticMazeNavigation(Navigation):
    def __init__(self):
        robot = VelRobot(100, 700)

        obs1 = Obstacle(400.0, 600.0)
        obs2 = Obstacle(700.0, 100.0)
        obs3 = Obstacle(300.0, 500.0)
        obs4 = Obstacle(150.0, 200.0)
        obs5 = Obstacle(350.0, 250.0)
        obs_list = [obs1, obs2, obs3, obs4, obs5]

        maze = create_maze(indx=1)

        engine = NavigationEngine(robot=robot, obstacle_list=obs_list, maze=maze)

        super(StaticMazeNavigation, self).__init__(engine)

    def reset(self, state: np.ndarray = None):
        if state is None:
            state = np.array([100, 700])

        self.engine.robot.x = state[0]
        self.engine.robot.y = state[1]

        return self.obs()

