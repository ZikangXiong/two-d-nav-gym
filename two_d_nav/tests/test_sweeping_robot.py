import time

from two_d_nav.envs.sweeping_robot_envs import StaticMazeNavigation


def test_reset():
    env = StaticMazeNavigation()

    for _ in range(100):
        env.reset()
        env.render()
        time.sleep(0.5)


if __name__ == '__main__':
    test_reset()
