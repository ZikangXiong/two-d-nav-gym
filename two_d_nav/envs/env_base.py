from typing import Tuple

import gym
import numpy as np

from two_d_nav.engine import NavigationEngine
from two_d_nav import config


class Navigation(gym.Env):

    def __init__(self, engine: NavigationEngine):
        self.engine = engine
        self.observation_space = gym.spaces.Box(low=np.array([-2, -2], dtype=np.float32),
                                                high=np.array([2, 2], dtype=np.float32))
        self.action_space = gym.spaces.Box(low=np.array([-1, -1], dtype=np.float32),
                                           high=np.array([1, 1], dtype=np.float32))
        # For computing the advantage (first order derivative) of reward
        self.prev_reward = None

    def obs(self):
        return self.engine.dist_goal()

    def reward_and_done(self) -> Tuple[np.ndarray, bool]:
        reward = np.exp(-config.reward_sensitive * np.sum(np.abs(self.obs())))
        done = False

        reach_goal, hit_obstacle, hit_wall = self.engine.get_robot_status()

        if hit_wall:
            reward += config.hit_wall_reward
            self.engine.robot.stay()

        if reach_goal:
            reward += config.reach_goal_reward
            self.reset()
            done = True

        if hit_obstacle:
            reward += config.hit_obstacle_reward
            self.reset()
            done = True

        # compute reward advantage
        if self.prev_reward is None:
            self.prev_reward = reward
        reward_adv = reward - self.prev_reward
        self.prev_reward = reward

        reward_adv += config.step_penalty

        return reward_adv, done

    def step(self, action: np.ndarray, **kwargs):
        assert (action <= 1.0).all() and (action >= -1.0).all(), "action should in the range of [-1, 1]"

        scaled_action = action * config.robot_vel_scale
        self.engine.robot.move(*scaled_action)
        _obs = self.obs()

        reward, done = self.reward_and_done()

        return _obs, reward, done, {}

    def reset(self, state: np.ndarray = None):
        if state is None:
            state = np.random.uniform(low=np.array([0, 0]), high=np.array([800, 800]))

        self.engine.robot.x = state[0]
        self.engine.robot.y = state[1]

        self.prev_reward = None

        return self.obs()

    def render(self, mode="human"):
        self.engine.render()
