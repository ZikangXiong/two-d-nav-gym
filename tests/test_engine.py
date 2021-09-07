from two_d_nav.elements import VelRobot, Obstacle, create_maze
from two_d_nav.engine import NavigationEngine


def test_engine():
    # See the environment in the envs folder.
    _robot = VelRobot(100, 700)
    obs1 = Obstacle(400.0, 600.0)
    obs2 = Obstacle(700.0, 100.0)
    obs3 = Obstacle(300.0, 500.0)
    obs4 = Obstacle(150.0, 200.0)
    obs5 = Obstacle(350.0, 250.0)
    obs_list = [obs1, obs2, obs3, obs4, obs5]
    _maze = create_maze(1)

    eng = NavigationEngine(_robot, obs_list, _maze)
    eng.run()


if __name__ == '__main__':
    test_engine()
