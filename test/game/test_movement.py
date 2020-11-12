import random

from pygme.game import movement


def test_resolve_movement():
    """ Tests game.movement.resolve_movement function """
    for i in range(100):
        # Pick random starting coordinates and direction the movement is happening in
        x_coordinate = random.randint(-100, 100)
        y_coordinate = random.randint(-100, 100)
        random_direction = ["up", "down", "left", "right"][random.randint(0, 3)]
        new_x_coordinate, new_y_coordinate = movement.resolve_movement(x_coordinate, y_coordinate, random_direction)
        if random_direction == "up":
            assert new_x_coordinate == x_coordinate and new_y_coordinate == y_coordinate - 1
        elif random_direction == "down":
            assert new_x_coordinate == x_coordinate and new_y_coordinate == y_coordinate + 1
        elif random_direction == "right":
            assert new_x_coordinate == x_coordinate + 1 and new_y_coordinate == y_coordinate
        elif random_direction == "left":
            assert new_x_coordinate == x_coordinate - 1 and new_y_coordinate == y_coordinate
