import two_d_nav.search.constants as c
from two_d_nav.search.location import Location


class State:
    def __init__(self, cost, state, board_rows, board_cols):

        self.board = [[Location(x, y) for x in range(board_cols)] for y in range(board_rows)]
        self.state = state
        self.board_rows = board_rows
        self.board_cols = board_cols

        # TODO: DEFINE A COST FUNCTION FROM STATE TO STATE
        #     For now, the cost function is just 0 for all the states, will update as requirements become clear
        self.cost = [[0 for x in range(board_cols)] for y in range(board_rows)]
        i = 0
        for r in range(board_rows):
            for c in range(board_cols):
                self.cost[r][c] = cost[i]
                i = i + 1

    def next_position(self, action, state):
        """
        action: up, down, left, right
        --  --  --  --  --  -- -
        0 | 1 | 2| 3|
        1 |
        2 |
        return next position
        """
        if action == "up":
            next_state = Location(state.row - c.STEP, state.col)
        elif action == "down":
            next_state = Location(state.row + c.STEP, state.col)
        elif action == "left":
            next_state = Location(state.row, state.col - c.STEP)
        else:
            next_state = Location(state.row, state.col + c.STEP)

        # if next state legal
        if next_state.row < 0:
            next_state.row = 0
        if next_state.row > self.board_rows - 1:
            next_state.row = self.board_rows - 1
        if next_state.col < 0:
            next_state.col = 0
        if next_state.col > self.board_cols - 1:
            next_state.col = self.board_cols - 1

        return next_state

    @staticmethod
    def heuristic(state_one, state_two):
        return abs(state_one.row - state_two.row) + abs(state_one.col - state_two.col)

    def get_cost(self, state):
        return self.cost[state.row][state.col]
