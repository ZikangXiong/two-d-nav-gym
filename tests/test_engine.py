from two_d_nav.elements import VelRobot, Cat, create_maze
from two_d_nav.engine import MazeNavigationEngine


def test_engine():
    # See the environment in the envs folder.
    _robot = VelRobot(100, 700)
    obs1 = Cat(400.0, 600.0)
    obs2 = Cat(700.0, 100.0)
    obs3 = Cat(300.0, 500.0)
    obs4 = Cat(150.0, 200.0)
    obs5 = Cat(350.0, 250.0)
    obs_list = [obs1, obs2, obs3, obs4, obs5]
    _maze = create_maze(1)

    eng = MazeNavigationEngine(_robot, obs_list, _maze)
    eng.run()


if __name__ == '__main__':
    test_engine()
