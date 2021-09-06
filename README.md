# 2D Navigation Environment for Safe Hierarchical Reinforcement Learning

Pure-python based, light-weight reinforcement learning environments. 

## Task Description

![example](https://user-images.githubusercontent.com/73256697/132261693-ba12b340-94a2-484e-beb5-6c6514bb53c7.png)

The sweeping robot should

1. Go back to the charger
2. Avoid hitting any cats

## Project Structure

```shell
└── two_d_nav/
    ├── assets/             # Images
    ├── config.py           # configuration of environment
    ├── elements.py         # elements in the task, e.g, robot, maze
    ├── engine.py           # simulator engine
    └── envs/               # gym wrappers for the environment
        ├── env_base.py     # base class
        ├── open_space.py   # only has robot and charger in the environment
        └── static_maze.py  # environment with maze and static cats

```
## Robots

We support following robots for now.

### VelRobot

This robot is simply modeled with 2 states - the x-position and y-position. We suppose that the velocity of the robot
can be control in certain range. For simplicity, we use the velocity as control signal directly, which means that if we
tell the robot to go to certain velocity, it can achieve in the next moment.
