

def resolve_movement(x_coordinate: int, y_coordinate: int, direction: str) -> tuple:
    assert direction in {'up', 'right', 'down', 'left'}
    if direction == "up":
        return x_coordinate, y_coordinate - 1
    elif direction == "right":
        return x_coordinate + 1, y_coordinate
    elif direction == "down":
        return x_coordinate, y_coordinate + 1
    elif direction == "left":
        return x_coordinate - 1, y_coordinate
