import numpy as np

from two_d_nav.envs.static_maze import StaticMazeNavigation


def test_goal():
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
            print(f"Reach goal: {obs}")
            print(f"Reward: {reward}")


def test_obstacle():
    env = StaticMazeNavigation()

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
            print(f"Hit obstacle: {obs}")
            print(f"Reward: {reward}")


def test_wall():
    env = StaticMazeNavigation()
    reward = 0.0

    for i in range(20):
        obs, reward, done, _ = env.step(np.array([-1.0, 0.0]))
        env.render()

    print(f"Hit wall reward {reward}")


if __name__ == '__main__':
    test_goal()
    test_obstacle()
    test_wall()
