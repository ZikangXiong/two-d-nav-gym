# 2D Navigation Environment

Pure-python based, light-weight reinforcement learning environments.

## Task Description

<img src="https://user-images.githubusercontent.com/73256697/132261693-ba12b340-94a2-484e-beb5-6c6514bb53c7.png" alt="drawing" width="400"/>

The sweeping robot should

1. Go back to the charger
2. Avoid hitting any cats

## Project Structure

```shell
├── tests                   # test cases
│   ├── test_engine.py
│   ├── test_open_space.py
│   └── test_static_maze.py
└── two_d_nav/
    ├── assets/             # images
    ├── config.py           # configuration of environment
    ├── elements.py         # elements in the task, e.g, robot, maze
    ├── engine.py           # simulator engine
    ├── engine.py           # utils
    └── envs/               # gym wrappers for the environment
        ├── env_base.py     # base class
        ├── open_space.py   # only has robot and charger in the environment
        └── static_maze.py  # environment with maze and static cats

```

## Robots

We only support one simple robot for now.

### VelRobot

This robot is simply modeled with 2 states - the x-position and y-position. We suppose that the velocity of the robot
can be controlled as we wish. For simplicity, we use the velocity as control signal directly, which means that if we tell
the robot to go to a certain velocity, it can achieve in the next moment. This is an unrealistically simple setting.
However, this robot is modeled with continuous state and action, thus it can be very challenge for algorithms like DQN.
The complex maze setting is also a great challenge for non-hierarchical reinforcement learning algorithms like SAC, TD3,
DDPG or PPO, etc.

## Example

### Create gym Environment

The code below created a static maze navigation task and moved, rendering the environment.

```python
import numpy as np

from two_d_nav.envs import static_maze

env = static_maze.StaticMazeNavigation()
obs = env.reset()

for i in range(60):
    obs, reward, done, _ = env.step(np.array([1.0, -0.1]))
    env.render()
```

### Play

Unlike the gym environments, playing with a keyboard only supports 4 directions control (up, down, left, and right).

One can start the keyboard control with following code

```shell
python tests/test_engine.py
```
