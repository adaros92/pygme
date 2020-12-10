import random


def get_coordinates_between_limits(grid_width: int, grid_length: int) -> tuple:
    """ Provides random coordinates between the specified limits on a 2D grid

    :param grid_width - the width of the grid in number of squares
    :param grid_length - the length of the grid in number of squares
    :returns a tuple with (x-coordinate, y-coordinate)
    """
    random_x_coordinate = random.randint(0, grid_length - 1)
    random_y_coordinate = random.randint(0, grid_width - 1)
    return random_x_coordinate, random_y_coordinate


def are_coordinates_between_limits(coordinates: tuple, grid_width: int, grid_length: int) -> bool:
    """ Checks whether the given (x-coordinate, y-coordinate) square is within the given grid dimensions

    :param coordinates - (x-coordinate, y-coordinate) coordinates representing a square on a grid
    :param grid_width - the width of the grid in number of squares
    :param grid_length - the length of the grid in number of squares
    :returns True if the coordinates are within the grid dimensions, False otherwise
    """
    x_coordinate, y_coordinate = coordinates[0], coordinates[1]
    if (0 <= y_coordinate < grid_width) and (0 <= x_coordinate < grid_length):
        return True
    return False


def get_random_directions(possible_directions: list, number_of_directions: int) -> list:
    """ Generates random directions from the possible directions given

    :param possible_directions - a list of possible directions to choose from
    :param number_of_directions - the number of random directions to generate
    :returns a list of [number_of_directions] random directions
    """
    directions = []
    # Make sure possible directions are unique
    possible_directions = list(set(possible_directions))
    possible_directions_count = len(possible_directions)
    for _ in range(number_of_directions):
        random_direction = possible_directions[random.randint(0, possible_directions_count - 1)]
        directions.append(random_direction)
    return directions



def are_contiguous_coordinates(coordinates: list) -> bool:
    """ Checks if the given list of coordinate tuples are in a contiguous sequence of each other in either the X or
    Y direction (diagonals not considered contiguous)

    Example: (1,0), (2,0), (3,0) are contiguous
    (1,0), (2,1), (4,0) are not

    :param coordinates - a list of coordinate tuples (x-coordinate, y-coordinate)
    :returns True if the coordinates are contiguous, false otherwise
    """
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
    """ Provides a list of contiguous coordinate tuples from the starting coordinate in the given direction
    Contiguous coordinates are those in a sequence without skipping in either the X or Y direction

    Example: (1,0), (2,0), (3,0) are contiguous
    (1,0), (2,1), (4,0) are not

    :param starting_coordinate - an (x-coordinate, y-coordinate) tuple of the starting square
    :param direction - one of four directions (right, down, left, up) to generate the sequence in
    :param size - the size of the sequence in number of squares
    :returns a list of coordinate tuples in a contiguous sequence
    """
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
