import random

from pygme.snake import snake


def test_change_direction():
    """ Tests snake.Body.change_direction method """
    for _ in range(100):
        # Choose a random starting direction
        directions = ["up", "down", "left", "right"]
        random_direction = directions[random.randint(0, 3)]
        opposite_direction = {"left": "right", "right": "left", "down": "up", "up": "down"}[random_direction]
        # Create a body moving in the random direction
        a_snake_body = snake.Body(x_coordinate=1, y_coordinate=2, direction=random_direction)
        previous_direction = a_snake_body.direction
        # Get a new random direction to change movement to and change it
        new_random_direction = directions[random.randint(0, 3)]
        a_snake_body.change_direction(new_random_direction)
        # Direction of movement should only change if the new direction is not opposite to the previous direction
        if new_random_direction == opposite_direction:
            assert a_snake_body.direction == previous_direction
        else:
            assert a_snake_body.direction == new_random_direction


def test_assign_node_coordinate():
    """ Tests snake.Body._assign_node_coordinate method """
    for _ in range(100):
        directions = ["up", "down", "left", "right"]
        random_prev_direction = directions[random.randint(0, 3)]
        # Create two random nodes going in random directions
        prev_node = snake.Node(
            x_coordinate=random.randint(-100, 100), y_coordinate=random.randint(-100, 100),
            direction=random_prev_direction)
        directions = ["up", "down", "left", "right"]
        random_direction = directions[random.randint(0, 3)]
        new_node = snake.Node(
            x_coordinate=random.randint(-100, 100), y_coordinate=random.randint(-100, 100), direction=random_direction)
        snake.Body._assign_node_coordinate(prev_node, new_node)
        # Test that the assignment of coordinates to the new node based on the previous node works as expected
        if random_prev_direction == "up":
            assert new_node.x_coordinate == prev_node.x_coordinate and \
                   new_node.y_coordinate == prev_node.y_coordinate - 1
        elif random_prev_direction == "down":
            assert new_node.x_coordinate == prev_node.x_coordinate and \
                   new_node.y_coordinate == prev_node.y_coordinate + 1
        elif random_prev_direction == "right":
            assert new_node.x_coordinate == prev_node.x_coordinate + 1 and \
                   new_node.y_coordinate == prev_node.y_coordinate
        elif random_prev_direction == "left":
            assert new_node.x_coordinate == prev_node.x_coordinate - 1 and \
                   new_node.y_coordinate == prev_node.y_coordinate


def test_grow_body():
    """ Tests snake.Body.grow method """
    # Check that the growth results in the right ending length
    a_snake_body = snake.Body(x_coordinate=1, y_coordinate=2)
    for growth_amount in range(1, 100):
        prev_length = a_snake_body.length
        a_snake_body.grow(growth_amount)
        assert a_snake_body.length == prev_length + growth_amount
    # Check that all of the nodes that were supposed to be added are presently in the body
    expected_node_representation = "*" * a_snake_body.length
    tmp_node = a_snake_body.head
    node_representation = ''
    while tmp_node:
        node_representation += tmp_node.representation
        tmp_node = tmp_node.next_node
    assert expected_node_representation == node_representation


def test_body_slither():
    """ Tests snake.Body.slither method """
    for _ in range(100):
        directions = ["up", "down", "left", "right"]
        random_direction = directions[random.randint(0, 3)]
        x_coordinate = random.randint(-100, 100)
        y_coordinate = random.randint(-100, 100)
        # Create a random snake body
        a_snake_body = snake.Body(
            x_coordinate=x_coordinate, y_coordinate=y_coordinate, direction=random_direction)
        # Grow the body by a random amount
        a_snake_body.grow(by=random.randint(1, 100))
        coordinates = []
        tmp_node = a_snake_body.head
        # Get previous coordinates by node
        while tmp_node:
            coordinates.append((tmp_node.x_coordinate, tmp_node.y_coordinate))
            tmp_node = tmp_node.next_node
        # Move the body
        a_snake_body.slither()
        # Get coordinates after the movement
        tmp_node = a_snake_body.head.next_node
        node_count = 0
        while tmp_node:
            # Each node should have the same coordinates now as their previous node before the movement
            assert tmp_node.x_coordinate == coordinates[0][0]
            assert tmp_node.y_coordinate == coordinates[0][1]
            tmp_node = tmp_node.next_node
            node_count += 1
