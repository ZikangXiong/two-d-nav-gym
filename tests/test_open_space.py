import numpy as np

from two_d_nav.envs.open_space import OpenSpaceNavigation


def test_open_space_navigation():
    env = OpenSpaceNavigation()

    for i in range(1000):
        obs, reward, done, _ = env.step(np.array([0.1, -0.1]))
        if done:
            print("reach goal at ", obs)
        env.render()


if __name__ == '__main__':
    test_open_space_navigation()
