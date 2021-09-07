import gym
import numpy as np

from two_d_nav.engine import NavigationEngine
from two_d_nav import config
from two_d_nav.utils import normalize_pos


class Navigation(gym.Env):

    def __init__(self, engine: NavigationEngine):
        self.engine = engine

    def step(self, action: np.ndarray, **kwargs):
        assert (action <= 1.0).all() and (action >= -1.0).all(), "action should in the range of [-1, 1]"

        scaled_action = action * config.robot_vel_scale
        state = self.engine.robot.move(*scaled_action)
        normalized_state = normalize_pos(state)

        dist_to_goal = self.engine.dist_goal()
        reward = np.exp(-config.reward_sensitive * dist_to_goal)
        done = False

        reach_goal, hit_obstacle, hit_wall = self.engine.get_robot_status()

        if hit_wall:
            reward += config.hit_wall_reward
            self.engine.robot.stay()

        if reach_goal:
            reward += config.reach_goal_reward
            self.engine.robot.reset()
            done = True

        if hit_obstacle:
            reward += config.hit_obstacle_reward
            self.engine.robot.reset()
            done = True

        return normalized_state, reward, done, {}

    def reset(self, state: np.ndarray):
        self.engine.robot.x = state[0]
        self.engine.robot.y = state[1]

    def render(self, mode="human"):
        self.engine.render()
