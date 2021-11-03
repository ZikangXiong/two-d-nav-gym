import numpy as np

from two_d_nav.envs.sweeping_robot_envs import (OpenSpaceNavigation,
                                                StaticMazeNavigation)


def test_open_space_navigation():
    env = OpenSpaceNavigation()

    for i in range(1000):
        obs, reward, done, _ = env.step(np.array([0.1, -0.1]))
        if done:
            print("reach goal at ", obs)
            break
        env.render()


def test_goal():
    env = StaticMazeNavigation()

    for i in range(60):
        obs, reward, done, _ = env.step(np.array([1.0, -0.05]))
        env.render()

    for i in range(30):
        obs, reward, done, _ = env.step(np.array([-0.9, -0.5]))
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

    for i in range(40):
        obs, reward, done, _ = env.step(np.array([-1.0, -0.4]))
        env.render()

        if done:
            print(f"reach goal: {obs}")
            print(f"reward: {reward}")
            break


def test_obstacle():
    env = StaticMazeNavigation()

    for i in range(60):
        obs, reward, done, _ = env.step(np.array([1.0, -0.05]))
        env.render()

    for i in range(5):
        obs, reward, done, _ = env.step(np.array([0.0, -1.0]))
        env.render()

    for i in range(30):
        obs, reward, done, _ = env.step(np.array([-1.0, 0.0]))
        env.render()

        if done:
            print(f"hit obstacle: {obs}")
            print(f"reward: {reward}")


def test_wall():
    env = StaticMazeNavigation()
    reward = 0.0

    for i in range(200):
        obs, reward, done, _ = env.step(np.array([-1.0, 0.0]))
        if reward < -4:
            break
        env.render()

    print(f"hit wall reward {reward}")


if __name__ == '__main__':
    test_open_space_navigation()
    test_goal()
    test_obstacle()
    test_wall()
