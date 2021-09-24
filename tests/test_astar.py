import numpy as np

from two_d_nav.elements import VelRobot, Obstacle, create_maze
from two_d_nav.engine import MazeNavigationEngine
from two_d_nav.search import constants as c
from two_d_nav.search.a_star import Agent
from two_d_nav.search.location import Location
from two_d_nav.search.state import State


def define_walls(board, lines):
    for l in lines:
        x1 = l[1][0]
        y1 = l[1][1]
        x2 = l[2][0]
        y2 = l[2][1]
        thickness = l[3]
        is_horizontal = y1 == y2
        if is_horizontal:
            for i in range(thickness):
                xval = min(x1, x2)
                for x in range(abs(x1 - x2)):
                    board[y1 + i - 1][xval + x - 1] = c.INFINITY
        else:
            for i in range(thickness):
                yval = min(y1, y2)
                for y in range(abs(y1 - y2)):
                    board[yval + y - 1][x1 + i - 1] = c.INFINITY

    return board


def define_obstacles(board, obs_list):
    size = c.OBSTACLE_SIZE
    for o in obs_list:
        x = int(o.init_x)
        y = int(o.init_y)
        for i in range(x, x + size):
            for j in range(y, y + size):
                board[j - 1][i - 1] = c.INFINITY
    return board


def create_board(lines, obs_list):
    board_size = c.BOARD_SIZE
    board = np.zeros(shape=(board_size, board_size))
    board = define_walls(board, lines)
    board = define_obstacles(board, obs_list)
    return board, board_size, board_size


def deconstruct_path(path):
    actions = []
    current = path[0]

    for i in range(len(path) - 1):
        _next = path[i]
        if current.col - c.STEP == _next.col:
            actions.append("up")
        elif current.col + c.STEP == _next.col:
            actions.append("down")
        elif current.row - c.STEP == _next.row:
            actions.append("left")
        elif current.row + c.STEP == _next.row:
            actions.append("right")
        current = _next
    return actions


def run_search(board, board_rows, board_cols):
    start = Location(c.START_POS_X, c.START_POS_Y)
    goal = Location(c.GOAL_POS_X, c.GOAL_POS_Y)

    state = State(board.flatten(), start, board_rows, board_cols)
    ag = Agent(state)
    path, pathCost = ag.a_star_search(start, goal)

    actions = deconstruct_path(path)
    return actions


def print_actions(actions):
    current = actions[0]
    counter = 0
    for i in range(len(actions)):
        _next = actions[i]
        if current == _next:
            counter += 1

        if current != _next or i == len(actions) - 1:
            print("", counter, " ", current)
            counter = 1
            current = _next


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
    board, board_rows, board_cols = create_board(_maze.lines, obs_list)
    actions = run_search(board, board_rows, board_cols)

    print("\n\nFollowing are the actions to take:\n")
    print_actions(actions)
    print("\n\n")

    eng = MazeNavigationEngine(_robot, obs_list, _maze)
    eng.run()


if __name__ == '__main__':
    test_engine()
