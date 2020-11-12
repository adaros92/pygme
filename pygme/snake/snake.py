from pygme.game import movement


class Node(object):

    def __init__(self, x_coordinate: int, y_coordinate: int, direction: str,
                 representation: str = '*', next_node=None, prev_node=None) -> None:
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.direction = direction
        self.representation = representation
        self.next_node = next_node
        self.prev_node = prev_node


class Body(object):

    def __init__(self, x_coordinate: int, y_coordinate: int, length: int = 1, direction: str = "left") -> None:
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.head = Node(x_coordinate, y_coordinate, direction)
        self.tail = self.head
        self.length = length
        self.direction = direction

    @staticmethod
    def _assign_node_coordinate(prev_node: Node, new_node: Node):
        new_node.x_coordinate, new_node.y_coordinate = movement.resolve_movement(
            prev_node.x_coordinate, prev_node.y_coordinate, prev_node.direction)

    def _create_new_node(self, x_coordinate: int, y_coordinate: int, direction: str, prev_node: Node):
        new_node = Node(x_coordinate, y_coordinate, direction, prev_node=prev_node)
        self._assign_node_coordinate(prev_node=prev_node, new_node=new_node)
        return new_node

    def grow(self, by: int = 1) -> None:
        """ Grows the current body by the specified amount of nodes

        :param by - the number of nodes to grow the body by
        """
        assert by > 0
        new_node_chain = None
        last_node = None
        # Create a new chain of nodes to append to the end of the body
        for new_node_num in range(by):
            # Create the first node in the chain
            if new_node_num == 0:
                new_node_chain = self._create_new_node(
                    x_coordinate=self.x_coordinate, y_coordinate=self.y_coordinate,
                    direction=self.tail.direction, prev_node=self.tail)
                last_node = new_node_chain
            # Create all the other nodes after the first one and add them to the chain
            else:
                tmp_node = self._create_new_node(
                    x_coordinate=self.x_coordinate, y_coordinate=self.y_coordinate,
                    direction=last_node.direction, prev_node=last_node
                )
                last_node.next_node = tmp_node
                last_node = tmp_node
        # Integrate the new chain as part of the current body
        self.tail.next_node = new_node_chain
        self.tail = last_node
        self.length += by

    def slither(self, speed: float = 1.0) -> None:
        # Each node will assign its direction and coordinate to the next node
        tmp_node = self.head.next_node
        while tmp_node:
            self._assign_node_coordinate(tmp_node.prev_node, tmp_node)
        # Once all other nodes have moved, the head moves to new location
        self.head.x_coordinate, self.head.y_coordinate = movement.resolve_movement(
            self.head.x_coordinate, self.head.y_coordinate, self.direction)


class Snake(object):

    def __init__(self, x_coordinate: int, y_coordinate: int) -> None:
        self.body = Body(x_coordinate, y_coordinate)

    def eat(self, food) -> None:
        pass

    def move(self, direction: str) -> None:
        # Change direction
        self.body.direction = direction
        # Move
        self.body.slither()
