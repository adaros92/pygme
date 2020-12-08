import random


def get_coordinates_between_limits(grid_width: int, grid_length: int) -> tuple:
    random_x_coordinate = random.randint(0, grid_length - 1)
    random_y_coordinate = random.randint(0, grid_width - 1)
    return random_x_coordinate, random_y_coordinate


def are_contiguous_coordinates(coordinates: list) -> bool:
    y_coordinates = set()
    x_coordinates = set()
    coordinate_length = len(coordinates)
    for coordinate_tuple in coordinates:
        y_coordinates.add(coordinate_tuple[1])
        x_coordinates.add(coordinate_tuple[0])
    # To be contiguous in either x or y direction, at least one axis needs to be constant (1 unique value only)
    if len(y_coordinates) > 1 and len(x_coordinates) > 1:
        return False
    # Otherwise the difference between the max coordinate value and the minimum must have max increment of 1
    return (max(y_coordinates) - min(y_coordinates) + 1 == coordinate_length or
            max(x_coordinates) - min(x_coordinates) + 1 == coordinate_length)


def get_contiguous_coordinates(starting_coordinate: tuple, direction: str, size: int) -> list:
    assert direction in {"right", "down", "left", "up"}
    coordinate_list = [starting_coordinate]
    for idx in range(size - 1):
        if direction == "right":
            new_coordinate = (coordinate_list[idx][0] + 1, coordinate_list[idx][1])
        elif direction == "down":
            new_coordinate = (coordinate_list[idx][0], coordinate_list[idx][1] + 1)
        elif direction == "left":
            new_coordinate = (coordinate_list[idx][0] - 1, coordinate_list[idx][1])
        else:
            new_coordinate = (coordinate_list[idx][0], coordinate_list[idx][1] - 1)
        coordinate_list.append(new_coordinate)
    return coordinate_list
