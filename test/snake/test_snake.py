from pygme.snake import snake


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
