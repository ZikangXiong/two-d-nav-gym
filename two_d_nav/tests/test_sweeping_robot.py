import time

from two_d_nav.envs.sweeping_robot_envs import CatParade, StaticMazeNavigation


def test_reset():
    env = StaticMazeNavigation()

    for _ in range(100):
        env.reset()
        env.render()
        time.sleep(0.5)


def test_cat_parade_render():
    env = CatParade()
    env.render()
    time.sleep(10)


if __name__ == '__main__':
    # test_reset()
    test_cat_parade_render()
