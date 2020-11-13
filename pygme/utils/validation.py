
def validate_user_input(input_variable: str, value_received: any, expected_type: type):
    expected_type_name = expected_type.__name__
    try:
        return expected_type(value_received)
    except ValueError:
        raise ValueError("Your input for {0} cannot be represented as {1}".format(input_variable, expected_type_name))


def validate_grid_index(grid_length: int, grid_width: int, x_coordinate: int, y_coordinate: int) -> bool:
    if x_coordinate < 0 or x_coordinate >= grid_length or y_coordinate < 0 or y_coordinate >= grid_width:
        return False
    return True
