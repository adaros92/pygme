import random


def get_coordinates_between_limits(grid_width: int, grid_length: int) -> tuple:
    random_x_coordinate = random.randint(0, grid_length - 1)
    random_y_coordinate = random.randint(0, grid_width - 1)
    return random_x_coordinate, random_y_coordinate
