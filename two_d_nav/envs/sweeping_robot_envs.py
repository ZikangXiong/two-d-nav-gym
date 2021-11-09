from typing import Tuple

import gym
import numpy as np

from two_d_nav import config
from two_d_nav.elements import Cat, VelRobot, create_maze, create_open_space
from two_d_nav.engine import MazeNavigationEngine


class Navigation(gym.Env):

    def __init__(self, engine: MazeNavigationEngine):
        self.engine = engine
        self.observation_space = gym.spaces.Box(low=np.array([-1, -1], dtype=np.float32),
                                                high=np.array([1, 1], dtype=np.float32))
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
            done = True

        if hit_obstacle:
            reward += config.hit_obstacle_reward
            done = True

        # compute reward advantage
        if self.prev_reward is None:
            self.prev_reward = reward
        reward_adv = reward - self.prev_reward
        self.prev_reward = reward

        reward_adv += config.step_penalty

        return reward_adv, done

    def step(self, action: np.ndarray, **kwargs):
        assert(
            action <= 1.0).all() and (
            action >= -1.0).all(), "action should in the range of [-1, 1]"

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

    def get_maze_info(self):
        obs_list = self.engine.obstacle_list
        obs_pos_list = [np.array(obs.center(), dtype=int) for obs in obs_list]
        walls = self.engine.maze.lines
        goal = np.array(self.engine.maze.goal.center())[::-1]
        initial_state = np.array(self.engine.robot.center())[::-1]
        board_size = config.map_size
        robot_radius = (self.engine.robot.shape / 2 + 0.5).astype(int)
        obs_size = obs_list[0].shape if len(obs_list) != 0 else (0, 0)

        return obs_pos_list, walls, initial_state, goal, board_size, robot_radius, obs_size

    def render(self, mode="human"):
        self.engine.render()


class OpenSpaceNavigation(Navigation):
    def __init__(self):
        robot = VelRobot(100, 700)
        obs_list = []
        maze = create_open_space()
        engine = MazeNavigationEngine(robot=robot, obstacle_list=obs_list, maze=maze)
        super(OpenSpaceNavigation, self).__init__(engine)


class StaticMazeNavigation(Navigation):
    def __init__(self):
        robot = VelRobot(700, 100)

        obs1 = Cat(200.0, 300.0)
        obs2 = Cat(250.0, 350.0)
        obs3 = Cat(100.0, 180.0)
        obs4 = Cat(400.0, 400.0)
        obs5 = Cat(300.0, 480.0)
        obs6 = Cat(200.0, 700.0)
        obs7 = Cat(300.0, 680.0)
        obs8 = Cat(500.0, 690.0)
        obs_list = [obs1, obs2, obs3, obs4, obs5, obs6, obs7, obs8]

        maze = create_maze(indx=1)

        engine = MazeNavigationEngine(robot=robot, obstacle_list=obs_list, maze=maze)

        super(StaticMazeNavigation, self).__init__(engine)
        self._init_robot_pos()

    def _init_robot_pos(self):
        initial_region_list = [[[80, 680], [150, 750]],
                               [[650, 100], [750, 150]],
                               [[100, 520], [200, 600]]]
        initial_region = initial_region_list[np.random.randint(0, len(initial_region_list))]
        initial_state = np.random.uniform(*initial_region)
        self.engine.robot.x, self.engine.robot.y = initial_state

    def reset(self, state: np.ndarray = None):
        if state is None:
            self._init_robot_pos()
        else:
            self.engine.robot.x = state[0]
            self.engine.robot.y = state[1]

        return self.obs()


class CatParade(Navigation):
    def __init__(self):
        robot = VelRobot(100, 400)

        obs_list = []
        for i in range(20):
            obs_list.append(Cat(100.0 + i * 30, 300.0))
            obs_list.append(Cat(100.0 + i * 30, 500.0))

        maze = create_maze(indx=2)
        engine = MazeNavigationEngine(robot=robot, obstacle_list=obs_list, maze=maze)

        super(CatParade, self).__init__(engine)
