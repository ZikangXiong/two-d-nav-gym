import numpy as np

from two_d_nav import config


def normalize_pos(pos: np.ndarray) -> np.ndarray:
    map_size = np.array(config.map_size)
    center = map_size / 2
    radius = map_size - center

    return (pos - center) / radius


def denormalize_pos(pos: np.ndarray) -> np.ndarray:
    map_size = np.array(config.map_size)
    center = map_size / 2
    radius = map_size - center

    return center + pos * radius
