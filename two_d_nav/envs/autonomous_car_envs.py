from abc import ABC

import gym
import numpy as np

from two_d_nav.elements import Car, Goal
from two_d_nav.engine import CarEngine


class CarEnvBase(gym.Env):
    def __init__(self, engine: CarEngine):
        self.engine = engine

        self.previous_theta = 0

        # config
        self.max_speed = 5

    def step(self, action: np.ndarray, **kwargs):
        speed, theta = action
        speed = speed.clip(-self.max_speed, self.max_speed)
        theta = theta.clip(self.previous_theta - 0.05, self.previous_theta + 0.05)
        self.previous_theta = theta

        dx = np.sin(theta) * speed
        dy = np.cos(theta) * speed

        self.engine.ego_car.move(dx, dy)

    def render(self, mode="human"):
        self.engine.render()


class OpenSpace(CarEnvBase):
    def __init__(self):
        self.ego_car = Car(400, 100)
        self.goal = Goal(400, 100)

        engine = CarEngine(self.ego_car, [], [self.goal])
        super().__init__(engine)

    def reset(self, **kwargs):
        pos = np.random.uniform(np.array([300, 500]), np.array([500, 700]))

        self.engine.ego_car.x = pos[0]
        self.engine.ego_car.y = pos[1]
        self.engine.ego_car.prev_x = pos[0]
        self.engine.ego_car.prev_y = pos[1]

        return self._obs()

    def _obs(self):
        return np.array([self.goal.x - self.ego_car.x, self.goal.y - self.ego_car.y])

    def step(self, action, **kwargs):
        super().step(action, **kwargs)

        done = (np.abs(self._obs()) < 20).all()
        return self._obs(), 0, done, {}


class ChangeLane(CarEnvBase):
    def __init__(self, engine: CarEngine):
        super().__init__(engine)
