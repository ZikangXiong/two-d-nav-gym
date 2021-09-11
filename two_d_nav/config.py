import os

root = os.path.dirname(os.path.abspath(__file__))

wall_collision_threshold = 15
obj_collision_threshold = 30

map_size = (800, 800)

robot_vel_scale = 10.0

reach_goal_reward = 20
hit_obstacle_reward = -20
hit_wall_reward = -5
step_penalty = -0.1

reward_sensitive = 1.0
