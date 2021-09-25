import time

import gym
import numpy as np

from two_d_nav.engine import FlightsEngine
from two_d_nav.elements import Flight


class ThreeFlights(gym.Env):
    def __init__(self):
        self.f1 = Flight(200, 700)
        self.f2 = Flight(300, 700)
        self.f3 = Flight(400, 700)

        self.engine = FlightsEngine([self.f1, self.f2, self.f3])
        self.t = 0
        self.res = []

    @staticmethod
    def pid_controller(vec_to_goal: np.ndarray) -> np.ndarray:
        return vec_to_goal

    @staticmethod
    def vec_to_goal_func(dx_0: float):
        dx_1 = (dx_0 + 1)
        y_0 = np.tanh((dx_0 - 100) / 100) * 400 + 500
        y_1 = np.tanh((dx_1 - 100) / 100) * 400 + 500

        return np.array([1, y_0 - y_1])

    def step(self, action, **kwargs):
        self.t += 1

        a1 = self.pid_controller(self.vec_to_goal_func(self.t))
        a2 = self.pid_controller(self.vec_to_goal_func(self.t))
        a3 = self.pid_controller(self.vec_to_goal_func(self.t))

        if action == "safe":
            if self.t < 100:
                a2[0] += self.t * 0.01
            elif self.t < 150:
                a2[0] -= self.t * 0.01
        else:
            a2[0] += self.t * 0.01

        self.f1.move(*a1)
        self.f2.move(*a2)
        self.f3.move(*a3)
        time.sleep(0.01)
        self.res.append([self.f1.x, self.f1.y])

    def reset(self, **kwargs):
        self.engine.flights[0].x = 200
        self.engine.flights[0].y = 700
        self.engine.flights[1].x = 300
        self.engine.flights[1].y = 700
        self.engine.flights[2].x = 400
        self.engine.flights[2].y = 700
        self.t = 0

    def render(self, mode="human"):
        self.engine.render()
