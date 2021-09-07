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


def test_static_maze_navigation():
    env = StaticMazeNavigation()

    for i in range(60):
        obs, reward, done, _ = env.step(np.array([1.0, -0.1]))
        env.render()

    for i in range(30):
        obs, reward, done, _ = env.step(np.array([-1.0, -0.5]))
        env.render()

    for i in range(5):
        obs, reward, done, _ = env.step(np.array([0.0, -1.0]))
        env.render()

    for i in range(15):
        obs, reward, done, _ = env.step(np.array([-1.0, 0.0]))
        env.render()

    for i in range(30):
        obs, reward, done, _ = env.step(np.array([0.0, -1.0]))
        env.render()

    for i in range(18):
        obs, reward, done, _ = env.step(np.array([-1.0, -0.6]))
        env.render()

        if done:
            print(reward), print(obs)

    for i in range(60):
        obs, reward, done, _ = env.step(np.array([1.0, -0.1]))
        env.render()

    for i in range(5):
        obs, reward, done, _ = env.step(np.array([0.0, -1.0]))
        env.render()

    for i in range(30):
        obs, reward, done, _ = env.step(np.array([-1.0, 0.0]))
        env.render()

        if done:
            print(reward), print(obs)

    for i in range(20):
        obs, reward, done, _ = env.step(np.array([-1.0, 0.0]))
        env.render()

    print(reward)


if __name__ == '__main__':
    test_static_maze_navigation()
