import time

import numpy as np

from two_d_nav.envs.autonomous_car_envs import OpenSpace


def test_reset():
    env = OpenSpace()

    for _ in range(10):
        env.reset()
        env.render()
        time.sleep(1)


def test_step():
    env = OpenSpace()
    env.reset()

    for _ in range(100):
        env.step(np.array([-5, np.pi]), )
        env.render()


def test_pid():
    env = OpenSpace()
    obs = env.reset()

    for _ in range(1000):
        speed = obs[1] / 20
        if obs[0] > 1:
            theta = -2 * np.random.random_sample(1)
        elif obs[0] < 1:
            theta = 2 * np.random.random_sample(1)
        else:
            theta = 0
        obs, _, done, _ = env.step(np.array([speed, theta]))
        env.render()

        if done:
            obs = env.reset()


if __name__ == '__main__':
    test_pid()
