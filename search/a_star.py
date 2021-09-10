import numpy as np
from queue import PriorityQueue
from search.location import Location
from search.state import State
import constants as c
# Agent of player

class Agent:
    def __init__(self, State):
        self.states = []
        self.actions = ["up", "down", "left", "right"]
        self.State = State

        # initial state reward
        self.state_values = {}
        for i in range(State.board_rows):
            for j in range(State.board_cols):
                self.state_values[(i, j)] = 0  # set initial value to 0

    def reconstruct_path(self, path, start, goal):
      new_path = []
      new_path.insert(0, goal)
      curr = path[goal]
      while path[curr] is not None:
        new_path.insert(0, curr)
        curr = path[curr]
      new_path.insert(0, start)
      return new_path

    def getAverageCost(self, x, y):
      cost = 0
      for i in range(c.ROBOT_SIZE):
        for j in range(c.ROBOT_SIZE):
          cost = cost + self.State.cost[y+j-1][x+i-1]
          if cost > 0:
            hi = 9
      cost = cost / (c.ROBOT_SIZE*c.ROBOT_SIZE)
      return cost

    def a_star_search(self, start_state, goal_state):
      q = PriorityQueue()
      q.put(start_state, 0)
      path = {}
      path[start_state] = None
      path_cost = {}
      path_cost[start_state] = 0.0

      while not q.empty():
        current = q.get()

        if current == goal_state:
          break
        else:
          for dir in self.actions:
            next_state = self.State.next_position(dir, current)
            next_state_cost = self.getAverageCost(next_state.row, next_state.col)
            new_cost = path_cost[current] + next_state_cost
            if next_state_cost > 0:
              hi = 9
            if (next_state not in path_cost and next_state_cost == 0) or (next_state in path_cost and new_cost < path_cost[next_state]):
              path_cost[next_state] = new_cost
              newPriority = new_cost + (self.State.heuristic(next_state, goal_state))
              q.put(next_state, newPriority)
              path[next_state] = current

      return self.reconstruct_path(path, start_state, goal_state), path_cost
